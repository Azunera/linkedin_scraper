from job_scraper import inJobScraper
from dataclasses_list import job_config
from dotenv import dotenv_values
from data_filters import filter_underscore
import json
import argparse

parser = argparse.ArgumentParser(
                    prog="Azu's LinkedIn Scraper",
                    description='''Scraper for LinkedIn jobs which can include its companies as well.\n
                    
                    The options below offer you specify parameters for search, only --search is mandatory,
                    which is the title/name of the job looking for.\n
                    
                    Another important point to consider is skills section, the program also will extract the skills keywords
                    for each job, but for this the program has to be provided with some keywords, be it at --keywords, or --keywords_path;
                    Filter by skills will let you only find jobs with the skills you are looking for.
                    ''',
                    
                    epilog='Thanks for using the scraper! For any questions or suggestions visit https://github.com/Azunera/LinkedIn_scrapper')

# <---- Essential requirements ---->
parser.add_argument('--headless', dest='headless', action='store_true',  help="Run the scraper in headless mode (default).")
parser.add_argument('--find_companies', dest='find_companies', action='store_true',  help="Make the scraper to also find basic information about jobs' companies. Storying it in a csv and part of the scraped data json.")
parser.add_argument('--not_use_cookies', dest='use_cookies', action='store_false', help="WARNING! Disables the use of cookies.\n")

# parser.add_argument('--no-headless', dest='headless', action='store_false', help="Run the scraper with browser visible.")
parser.set_defaults(use_cookies= True)  

parser.add_argument('--search',    type=str,  help='Name for the title of the job to search.', required=True)

parser.add_argument('--disable_json', dest='no_json', action='store_true', help='Used to disable the exportion of data as json')
parser.add_argument('--disable_csv', dest='no_csv', action='store_true', help='Used to disable the exportion of data as csv')

parser.add_argument('--csv_file_location',   type=str,  help='Directory location to store csv scraped data, default will be a created /data dir in the current dir.')
parser.add_argument('--json_file_location',  type=str,  help='Directory location to store json scraped data, default will be a created /data dir in the current dir.')

parser.add_argument('--save_in_database', dest='save_in_database', action='store_true', help='Flags on for storing data in database. IMPORTANT!. In order to access the database, make an .env with the database api, variable named as "DB_API_KEY", then modify db.py to configure the data import')


# <---- Skill parameters section ---->
parser.add_argument('--filter_by_skills', dest='filter_by_skills', action='store_true', help='Set the scraper so only saves data that contain one of the selected jobs')
parser.add_argument('--skills_keywords',  type=str,  help='The name of the skills you want to find.', nargs="*")
parser.add_argument('--skills_keywords_path', type=str, help="File location of list of skills you want for the job, it needs to be a .txt filetype, with content like follows: Skill_1, Skill_2, Skil_3... Skilln.")
parser.add_argument('--skills_keywords_path_category', type=str, help='File location of list of skills you want for the job, it must be a .json file, the category can be like follows: {"category_1": ["skill_1","skill_2"...], ... "category_n":[...] ...}')

# <---- Search parameters section ---->
parser.add_argument('--location',  type=str,  help='Location for the job to search around.')
parser.add_argument('--experience',type=str,  help='How much experienced required for the job; Options: Internship, Entry_level, Associate, Mid-Senior_level, Director, Executive.', nargs="*")
parser.add_argument('--job_type',  type=str,  help='Type of employment, its duration and work hours; Options: Full-time, Part-time, Internship, Contract.', nargs="*")
parser.add_argument('--workplace', type=str,  help='Place where work; Options: On-site, Remote, Hybrid.', nargs="*")
parser.add_argument('--company',   type=str,  help='As the name sugggests, you can look for specific jobs in companies here.', nargs="*")
parser.add_argument('--posted',    type=str,  help='Time range in which the job was posted; Options: Any_time, Past_month, Past_week, Past_24_hours.')
parser.add_argument('--benefits',  type=str,  help='Benefits for the particular job, such as insurances, etc.', nargs="*")

args = parser.parse_args()

job_configuration = job_config(
    search     = args.search.replace('_', ' '),
    location   = args.location.replace('_', ' '),
    level      = filter_underscore(args.experience),
    job_type   = filter_underscore(args.job_type),
    workplace  = filter_underscore(args.workplace),
    posted =  filter_underscore([args.posted]), # used to have  []
    company = filter_underscore(args.company),
    benefits = filter_underscore(args.benefits),
)

if not args.skills_keywords:
    args.skills_keywords = []
    
if args.skills_keywords_path_category:
    with open(args.skills_keywords_path_category, 'r') as f:
        skills_categorized = json.load(f)
        skills_categorized = {item: key for key, value in skills_categorized.items() for item in value}
else:
    skills_categorized = None

if args.skills_keywords_path:
    with open(args.skills_keywords_path, 'r', encoding='UTF-8') as f:
        file_skills = f.read().replace(', ',',').replace('\n','').replace('.','').split(',')
else:
    file_skills = []
        
skills = args.skills_keywords + file_skills
skills_dict = {skill: 0 for skill in skills}

skills = [skills, skills_categorized]

myScraper = inJobScraper(job_configuration, skills, args.use_cookies, args.find_companies, args.filter_by_skills, args.save_in_database)
config = dotenv_values()
myScraper.set_credentials(config['EMAIL'], config['PASSWORD'])
myScraper.run(slow_mo = 0, headless = args.headless)



    