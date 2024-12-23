from selectolax.parser import HTMLParser
from data_filters import clean_applicant_data, clean_job_html_description
from dataclasses_list import Job, Company
from dataclasses import asdict
from html import unescape
from io import BytesIO
import requests


def extract_text(html, sel, filters= True):
    '''
    Retrieves the content of an html node/element which is searched.

    * Args:
        - html (selectolax.parser.HTMLParser): HTML to search for the element.
        - sel (str): Selector for the element
        - filter (bool): Standard true, will unescape and strip the tect

    * Returns:
        - str: If filters true,wit will unescape it, and strip it
        - None: If an error occurs, usually because the element has not been found, or the element lacks text.
    '''
    try:
        text = html.css_first(sel).text()
        
        return str(unescape(text.strip())) if filters else str(text)
    
    except AttributeError:
        return None

def download_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        image_blob = BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            image_blob.write(chunk)
        image_blob.seek(0)  
        
        return image_blob.getvalue()  
    except requests.RequestException as e:
        print(f'Failed to download image from {image_url}: {e}')
        return None
    
def extract_job_details(html):
    '''
    Retrieves some details of the job that requires comparison between htmls, these datas are: Salary, work_place, job_type, and level.

    * Args:
        - html (selectolax.parser.HTMLParser): HTML to search for the elements

    * Returns:
        - data (dict: Contains all the data ready to be used for a parser. Retrieve them as: data['data_name']
    '''
    
    job_details = html.css_first('div.mt2.mb2 li:first-child span')
    data = {
        'salary': None,
        'work_place': None,
        'job_type': None,
        'level': None
    }

    if not job_details:
        return data

    for info in job_details.iter():
        text = info.text().strip()
        if text in ['Remote', 'Hybrid', 'On-site']:
            data['work_place'] = unescape(text)
        elif text in ['Full-time', 'Part-time', 'Contract', 'Internship']:
            data['job_type'] = unescape(text)
        elif text in ['Internship', 'Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']:
            data['level'] = unescape(text)
        else:
            data['salary'] = unescape(text)
    
    return data

def extract_skills(page, find_skills=False):
    '''
    Retrieves the content of an html node/element which is searched.

    * Args:
        - page : Must be the first base page with the job information. Used as gonna retrieve a new html later.
        - find_skills: 
        - filter (bool): Standard true, will unescape and strip the tect

    * Returns:
        - str: If filters true,wit will unescape it, and strip it
        - None: If an error occurs, usually because the element has not been found, or the element lacks text.
    '''
    if not find_skills:
        return None
    
    skills_button = page.locator('button.mv5.t-16')
    # sleep(1)
    if not skills_button.is_visible():
        print('Skills not found. Either job uploader did not include them or LinkedIn is not offering the feature')
        return None

    page.click('button.mv5.t-16')
    # sleep(1)
    skills_popup_html = HTMLParser(page.content())
    skills_list = skills_popup_html.css('ul.job-details-skill-match-status-list div[aria-label]')

    if not skills_list:
        print("No skills found, LinkedIn may be inconsistent.")
        return None

    skills_data = [skill.text().strip() for skill in skills_list]
    page.click('button[aria-label="Dismiss"]')

    return skills_data

def extract_skills_fromdesc(description, predlist, skills_dict): 
    # Import your predlist, or make a variable and set it here

    found_words = [] 
    for word in description.split():
        clean_word = word.strip(".,:;?!")
        if clean_word in predlist and clean_word not in found_words:
            found_words.append(clean_word)
            skills_dict[clean_word] += 1
            
    return found_words  

def parse_job_page(page, html: HTMLParser, job_card_num, skills_list, skills_dict):
    '''
    Creates an object from the dataclass 'Job' with parameters found within the given html.
    A brief showcase of the dataclass definition (which is within this module) is the next one:
        title:       str | None
        company:     str | None 
        location:    str | None
        work_place:  str | None
        job_type:    str | None
        level:       str | None
        applicants:  int | None
        salary:      str | None
        skills: list[str]| None
        description: str | None
        posted:      str | None

    * Args:
        - html (selectolax.parser.HTMLParser): HTML to find the info from.
        - job_card_num (num): A num used to extract the info about the job company, it is the job card num in the html.

    * Returns:
        - dict: Dictionary from the dataclass job through asdict. Ideally used for importation.
    '''

    job_details = extract_job_details(html)
 
    applicant_node = extract_text(html, "div.job-details-jobs-unified-top-card__primary-description-container span.tvm__text:nth-child(5)")
    applicant_data = clean_applicant_data(applicant_node) if applicant_node else None
    description_data = clean_job_html_description(html.css_first('div#job-details div.mt4').html)



    new_job = Job(
        title      =  extract_text(html, "h1 a"),
        company    =  extract_text(html, "div.job-details-jobs-unified-top-card__company-name a"),
        salary     =  job_details['salary'],
        workplace  =  job_details['work_place'],
        job_type   =  job_details['job_type'],
        level      =  job_details['level'],
        skills     =  extract_skills_fromdesc(description_data, skills_list, skills_dict),
        location   =  extract_text(html, "div.job-details-jobs-unified-top-card__primary-description-container span.tvm__text:nth-child(1)"),
        country    =  extract_text(html, "span#results-list__title").split(" in ")[-1].strip(),
        posted     =  extract_text(html, "div.job-details-jobs-unified-top-card__primary-description-container span.tvm__text:nth-child(3)"),
        applicants =  applicant_data,
        description = description_data,
        link        = page.url.split('&')[0].replace('search/?currentJobId=', 'view/'),
    )
        
    return new_job
                                          
def parse_company_page(context, page1_html, companies_list):
    company_page_node = page1_html.css_first('div.job-details-jobs-unified-top-card__company-name a')
    if company_page_node is None:
        return None
    
    company_name = unescape(company_page_node.text()).strip()
    if company_name in companies_list:
        return None
    
    if company_page_node is not None:
        company_page_link = company_page_node.attributes.get('href', "").strip("life") + 'about/'
    else:
        print('Link for the company not found.')
        return None
    
    page2 = context.new_page()
    
    try:
        page2.goto(company_page_link)
        page2.wait_for_url(company_page_link)
    except Exception as e:
        print(f'Error going to company LinkedIn link {company_page_link}: {e}')
        page2.close()
        return None

    # new local html
    html = HTMLParser(page2.content())
    
    # Sometimes the company pages are not even verified and lack a lot information, so instead need to find it somehow else
    local_company_name = extract_text(html, 'h1.org-top-card-summary__title')  
    if local_company_name is None:
        print(f'Unclaimed page for company link: {company_page_link}, company name: {local_company_name}')
    
    website_data = None
    company_size_data = None
    headquarters_data = None
    industry_data = None
    specialties_data = None
    founded_data = None
    
    n = 0
    d = 0  

    base = 'dl.overflow-hidden'

    try:
        for i in range(7):
            n += 1
            data = [extract_text(html, f'{base} dt:nth-of-type({n})'), extract_text(html, f'{base} dd:nth-of-type({n+d})')]
            try:
                if (data[0] == "Company size") and (extract_text(html, f'{base} dd:nth-of-type({n+1}')[0].isdigit()):
                    d+= 1
            except:
                pass
            match data[0]:
                case 'Website':
                    website_data = data[1]
                case 'Company size':
                    company_size_data = data[1]
                
                case 'Industry':
                    industry_data = data[1]
                    
                case 'Headquarters':
                    headquarters_data = data[1]
                
                case 'Specialties':
                    specialties_data = data[1]
                    
                case 'Founded':
                    founded_data = data[1]
    except:
        pass
            
            
    
    # # Logic for irregularities in  retrieving data from description, since sometimes it won't have some data
    # specialties_data = extract_text(html, 'dl.overflow-hidden dd:nth-last-of-type(1)') if extract_text(html, 'dl.overflow-hidden dt:nth-last-of-type(1) h3') == 'Specialties' else None
    # founded_data = extract_text(html, 'dl.overflow-hidden dd:nth-last-of-type(1)') if specialties_data else extract_text(html, 'dl.overflow-hidden dd:nth-last-of-type(2)')

    # headquarters_data = extract_text(html, 'dd.mb4:nth-of-type(1)') if html.css('dl.overflow-hidden dt:nth-of-type(1) h3') == "Website" else None

    # # headquarters_data = extract_text(html, 'div.block.mt2 div.inline-block div.org-top-card-summary-info-list__info-item:nth-of-type(1)') if html.css('dl.overflow-hidden dt:nth-of-type(1) h3') == "Website" else None
    # website_data = html.css_first('dl.overflow-hidden a').attributes.get('href') if html.css_first('dl.overflow-hidden a') else None
    
    logo_image = download_image(page1_html.css_first('div.jobs-search-results-list__list-item--active div.job-card-list__entity-lockup img').attributes.get('src'))
    
    new_company = Company(
        name = company_name,       
        website = website_data,
        industry = industry_data,
        company_size = company_size_data,
        headquarters = headquarters_data,
        founded = founded_data,
        specialties = specialties_data,
        description = extract_text(html, 'p.break-words'),
    )
    
    page2.close()
    return [new_company, logo_image]
    
