# LinkedIn Scraper

A LinkedIn Scraper that can extract data about jobs and companies. 

## Installation

Python 3.11 is required.

Then install the required libraries:
```
pip install -r requirements.txt
```

## Set Up

Create a .env file with the email and password for linkedin, and optionally if you are going to save the data directly into a database, db_api_key:
```
eMAIL = "" 
PASSWORD = ""
DB_API_KEY= "" 
```

## API

Here I show all the options arguments option on terminal, the options below offer you specify parameters for search, only
--search is mandatory, which is the title/name of the job looking for. Another important point to consider is skills section, the program 
will also extract the skills keywords for each job, but for this a keyword list must be provided, be it at --keywords,    
or --keywords_path; Filter by skills will let you only find jobs with the skills you are looking for.

Running example: 
```
python main.py --search Software_Engineer --location Spain  --experience Entry-level --posted Past_24_hours --skills_keywords_path predlist.txt --skills_keywords_path_category predlist_categorized.json  --filter_by_skills --save_in_database
```

### `headless`            
Run the scraper in headless mode (default).
### `find_companies`
Make the scraper to also find basic information about jobs' companies. Storying it in a csv and part of the scraped data json.
### `not_use_cookies`     
Disables the use of cookies.
### `search SEARCH`
Name for the title of the job to search.
### `disable_json`
Used to disable the exportion of data as json
### `disable_csv`
Used to disable the exportion of data as csv
### `csv_file_location CSV_FILE_LOCATION`
Directory location to store csv scraped data, default will be a created /data dir in the current dir.
### `json_file_location JSON_FILE_LOCATION`
Directory location to store json scraped data, default will be a created /data dir in the current dir.
### `save_in_database`
Flags on for storing data in database. IMPORTANT!. In order to access the database, make an .env with the database api, variable named as "DB_API_KEY", then modify db.py to configure the data import
### `filter_by_skills`
 Set the scraper so only saves data that contain one of the selected jobs
### `skills_keywords [SKILLS_KEYWORDS ...]`
The name of the skills you want to find.
### `skills_keywords_path SKILLS_KEYWORDS_PATH`
File location of list of skills you want for the job, it needs to be a .txt filetype, with content like follows:    
Skill_1, Skill_2, Skil_3... Skilln.
### `skills_keywords_path_category SKILLS_KEYWORDS_PATH_CATEGORY`
File location of list of skills you want for the job, it must be a .json file, the category can be like follows:    
{"category_1": ["skill_1","skill_2"...], ... "category_n":[...] ...}
### `location LOCATION`
Location for the job to search around.
### `experience [EXPERIENCE ...]`
How much experienced required for the job; Options: Internship, Entry_level, Associate, Mid-Senior_level, Director, Executive.
### `job_type [JOB_TYPE ...]`
Type of employment, its duration and work hours; Options: Full-time, Part-time, Internship, Contract.
### `workplace [WORKPLACE ...]`
Place where work; Options: On-site, Remote, Hybrid.
### `company [COMPANY ...]`
As the name sugggests, you can look for specific jobs in companies here.
### `posted POSTED`      
 Time range in which the job was posted; Options: Any_time, Past_month, Past_week, Past_24_hours.
### `benefits [BENEFITS ...]`
Try to find benefits for job such as pensions plans,etc. 

