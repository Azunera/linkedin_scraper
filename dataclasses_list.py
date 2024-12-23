from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
import search_enums

@dataclass
class Job:
    title:       str
    company:     str | None 
    location:    str | None
    country:     str | None
    workplace:   str | None
    job_type:    str | None
    level:       str | None
    applicants:  int | None
    salary:      str | None
    posted:      str | None  # If LinkedIn offers skills, this needs to be set a STR, if its skills are extracted from text, needs to be SET
    description: str | None
    skills:      dict[str] | None
    link: str | None

@dataclass
class Company:
    name:        str  | None
    website:      str  | None
    industry:     str  | None
    company_size: str  | None
    headquarters: str  | None
    founded:      int  | None
    specialties:  str  | None 
    description:  str  | None


@dataclass
class JobScrapeResult:
    scrape_time: datetime
    keywords: str 
    location: str        | None
    company: list[str]   | None 
    posted: list[str]    | None
    workplace: list[str] | None
    job_type: list[str]  | None
    job_level: list[str] | None
    benefits: list[str]  | None
    jobs_data: list[Job] = field(default_factory=list)
    companies_data: list[Company] = field(default_factory=list)

class job_config():
    
    def __init__(
        self,
        search:str,
        location    :str|None = None,
        level       :list[search_enums.level]|None = None,
        company     :list[str]|None = None,
        posted      :list[search_enums.posted_data]|None = None,
        workplace   :list[search_enums.job_place]|None = None,
        job_type    :list[search_enums.job_type]|None = None,
        benefits    :list[str]|None = None,
    ):

        self.search = search
        self.location = location

        self.optional_config = [company, posted, workplace, job_type, benefits, level]
        
        
