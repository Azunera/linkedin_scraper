from db import upload_jobs, upload_skills, upload_companies, get_skills_for_linking, check_tables_existance, initialize_database
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from saving_functions import append_to_csv, export_to_json
from scraping_functions import parse_job_page, parse_company_page
from datetime import datetime
from dataclasses_list import JobScrapeResult
from dataclasses import asdict

import json
import time
import os
import pyautogui

class inJobScraper:
    
    def __init__(self, config, skills:list, use_cookies:bool, find_companies:bool, filter_by_skills:bool, save_in_database:bool):
        '''Crawler and scraper for jobs, initilizations parameters:
        Args:
            config: Instance of `job_config` class. Contains job search configurations (title, location, job type, etc.).
            use_cookies: Boolean to determine if cookies are used to avoid login and captchas.
            find_companies: Boolean, if True, scrapes company information as well.
        '''
        
        self.search_config = config
        self.use_cookies = use_cookies
        self.find_companies = find_companies
        self.skills = skills[0]
        self.skills_dict = {skill: 0 for skill in self.skills}
        self.skills_categories = skills[1]
        self.save_in_database = save_in_database
        self.filter_by_skills = filter_by_skills

    def set_config(self, config):
        '''Updates the scraper's configuration.'''
        self.search_config = config
    
    def set_credentials(self, mail, password):
        '''Enter credentials if needed login without cookies or cookies not found. 
            args:
                mail: str
                password: str
        '''
        self.mail = mail
        self.password = password
        

    def login(self, page, context, cookies_location='cookies.json'):
        
        '''Tries to log in, if use_cookies is False, it's going to only log in and wait for the feed page to load.
        If use_cookies is True, it's going to check for cookies_location for a cookie.
        If it is not found, it's going to proceed login with credentials, and then save cookies for next time. '''
        
        def save_cookies(context, cookies_location='cookies.json'):
            """Saves cookies to the specified location."""
            cookies = context.cookies()
            with open(cookies_location, "w") as f:
                json.dump(cookies, f, indent=2)
                
        def manual_login(page, save_cookie= False):
            try:
                page.fill('input#username', self.mail)
                page.fill('input#password', self.password)
            except AttributeError:
                print('Credentials not found, set them using the method entering_credentials')
                
            page.click('button.btn__primary--large.from__button--floating')
            print('WARNING! At this point you may need to complete recaptcha')
            page.set_default_timeout(0)
            # page.wait_for_url('https://www.linkedin.com/feed/')
            page.set_default_timeout(1000000)
            page.locator('input.search-global-typeahead__input').wait_for(state='visible')

            if save_cookie:
                save_cookies(context)
                
        if self.use_cookies:

            if os.path.exists(cookies_location) and os.path.getsize(cookies_location) > 0:
                with open(cookies_location, 'r') as f:
                    cookies = json.load(f)  
                    for cookie in cookies: # for better visualization
                        cookie['domain'] = cookie['domain'].lstrip('.')

                    context.add_cookies(cookies)
                    try:
                        page.set_default_timeout(65000)
                        time.sleep(10)
                        page.waitforurl('https://www.linkedin.com/feed/')
                        
                    except:
                        print('Cookies expired, proceeding to manual logging and new upload')
                        context.clear_cookies()
                        page.goto('https://www.linkedin.com/feed/')
                        manual_login(page, save_cookie= True) 
            else:
                manual_login(page, save_cookie= True)
        else:
            manual_login(page)
            
            
    def setting_configs_and_search(self, page):
        '''Goes from the main page to the job search page. Then it uses the given search config to add as a parameters of search'''
        # Getting into search
        page.locator('input.search-global-typeahead__input').wait_for(state='visible')
        page.set_default_timeout(60000)
        page.click('input.search-global-typeahead__input')
    
        # Setting basics  of search
        page.fill('input.search-global-typeahead__input', self.search_config.search)
        page.keyboard.press('Enter')
        page.click('button:has-text("Jobs")')
        
        # Location
        page.click('input[aria-label="City, state, or zip code"]')
        page.fill('input[aria-label="City, state, or zip code"]', self.search_config.location)
        page.keyboard.press('Enter')

        # Settings filters
        page.click('button.search-reusables__all-filters-pill-button')
        filters = page.locator('div.artdeco-modal__content span')
        
        page.set_default_timeout(0)

        time.sleep(2)
        is_first_internship_complete =  False
        for config_list in self.search_config.optional_config:
            if config_list is not None: # used to be  if config_list[0] is not None
                page.set_default_timeout(20000)
                for config in config_list:
                    # There are two Internships on linkedin, that's why I use a system to select the second one after the first one was selected
                    
                    filters_element = filters.get_by_text(str(config), exact= True).nth(0)
                    if is_first_internship_complete and config == 'Internship':
                        filters_element = filters.get_by_text(str(config), exact= True).nth(1)
                    if config == 'Internship':
                        is_first_internship_complete = True
                    if filters_element is None:
                        print(f'Parameter {config} not found, the program will continue its normal process')
                    try:
                        filters_element.click()
                    except:
                        print(f'Parameter {config} not found, the program will continue its normal process')
                        
        
        page.click('button.reusable-search-filters-buttons.search-reusables__secondary-filters-show-results-button')
        page.set_default_timeout(32000)

    
    def run(self, headless = False,  slow_mo = 50):
        '''Runs the job scraper/crawler.
            args:
            - Headless: If False, will show the browser, making it useful for see what's going, debugging and solving captchas if needed, otherwise True doesn't show it, making it more efficient.
            - slow_mo: How slow you want the crawler to run.
        '''
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
            
            screen_width, screen_height = pyautogui.size()
            # Check if a saved session exists and load it
            if os.path.exists('./storage.json') and os.path.getsize('./storage.json') > 0:
                print(f"Loading session from {'./storage.json'}")
                context = browser.new_context(
                    viewport={"width": screen_width, "height": screen_height},
                    storage_state='./storage.json',
                )
            else:
                print("No saved session found, starting fresh.")
                context = browser.new_context(
                    viewport={"width": screen_width, "height": screen_height},
                )

            # screen_width, screen_height = pyautogui.size()
            # context = browser.new_context(
            #     viewport={'width': screen_width, 'height': screen_height, },
            # )
            page = context.new_page()
            page.set_default_timeout(65000)
            page.goto('https://www.linkedin.com/feed/')
            page.set_default_timeout(0)

            # If no session, login and save the session state
            if not os.path.exists('./storage.json') or os.path.getsize('./storage.json') == 0:
                page.goto("https://www.linkedin.com/login")
                self.login(page, context)
                # Save session state after login
                context.storage_state(path='./storage.json')

            # # Proceed with the rest of the workflow
            # self.setting_configs_and_search(page)

            # page.set_default_timeout(0)
            
            # page.goto('https://www.linkedin.com/login')
            # self.login(page, context)
            
            self.setting_configs_and_search(page)

            page_num = 0
            companies_name_list = []
            companies_list = []
            jobs_list = []

            while True:
                page_num += 1
                page_button = page.locator(f'button[aria-label="Page {page_num}"]')

                try:
                    page_button.scroll_into_view_if_needed()
                    page_button.click()
                except:
                    if page_num > 1:
                        print(f"Page number {page_num} not found. Scraping completed")
                        break
                    
                date = datetime.today().strftime("%m_%d_%Y")
                
                #<---- SCRAPPING LINKEDIN JOB CARD NUMS ---->
                for job_card_num in range(0,25): #25 is LinkedIn's max job cards per page
                    job_card = page.locator(f'li.relative.scaffold-layout__list-item:nth-child({job_card_num + 1})')
                    try: job_card.scroll_into_view_if_needed()
                    except: break

                    page.click(f'div.jobs-search-two-pane__job-card-container--viewport-tracking-{job_card_num}')
                    html_content = page.content()
                    html = HTMLParser(html_content)

                    # Call scrapping function
                    new_job = parse_job_page(page, html, job_card_num, self.skills, self.skills_dict)
                    
                    
                    if not new_job:
                        continue
                    
                    if len(new_job.skills) == 0 and self.filter_by_skills:
                        continue
                    
                    jobs_list.append(new_job)
                
                    append_to_csv(asdict(new_job), f'data/jobs_{date}.csv')
        
                    if self.find_companies:
                        new_company_data = parse_company_page(context, html, companies_name_list)
                        
                        if new_company_data:
                            companies_list.append(new_company_data)
                            append_to_csv(asdict(new_company_data[0]), f'data/company_{date}.csv')
               
            # <!--- Scraping over, proceeding with---->             
            date = datetime.today().strftime("%m_%d_%Y")
        
            if not check_tables_existance():
                initialize_database() 
                
            if self.save_in_database:
                if self.find_companies:
                    upload_companies(companies_list)
            
                upload_skills(self.skills_dict, self.skills_categories, len(jobs_list))
                upload_jobs(jobs_list, self.skills_dict, date)
                    

            scrap_info = asdict(JobScrapeResult(
                scrape_time = datetime.now().isoformat(),
                keywords = self.search_config.search,
                location = self.search_config.location,
                company  = self.search_config.optional_config[0],
                posted   = self.search_config.optional_config[1],
                workplace  = self.search_config.optional_config[2],
                job_type  = self.search_config.optional_config[3],
                benefits =  self.search_config.optional_config[4],
                job_level =  self.search_config.optional_config[5],
                jobs_data = jobs_list,
                companies_data =  [sublist[0] for sublist in companies_list]
            ))
            
            export_to_json(f'data/scraped_data_{date}.json', scrap_info)
   

            
            
        
            
                                
                                        
