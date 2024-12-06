from enum import StrEnum

class job_place(StrEnum):
    ON_SITE = 'On-site'
    HYBRID  = 'Hybrid'
    REMOTE  = 'Remote'

class job_type(StrEnum):
    FULL_TIME = 'Full-time'
    PART_TIME = 'Part-time'
    INTERNSHIP = 'Internship'
    CONTRACT   = 'Contract'

class posted_data(StrEnum):
    ANY_TIME = 'Any time'
    PAST_WEEK = 'Past week'
    PAST_MONTH = 'Past month'
    PAST_DAY   = 'Past 24 hours'

class level(StrEnum):
    INTERNSHIP = 'Internship'
    ENTRY_LEVEL = 'Entry level'
    ASSOCIATE = 'Associate'
    MID_SENIOR_LEVEL   = 'Mid-Senior level'
    DIRECTOR = 'Director'
    EXECUTIVE =  'Executive'