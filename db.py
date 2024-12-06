from sqlalchemy       import create_engine, Column, Integer, Numeric, String, Table, ForeignKey, UniqueConstraint, select, func, inspect
from sqlalchemy.orm   import Session, declarative_base, relationship, sessionmaker
from dataclasses_list import Job
from dotenv           import dotenv_values

# Here using sql-alchemy you can upload data directly to a relational database.

Base = declarative_base()
engine = create_engine(dotenv_values()['DB_API_KEY'])

class JobDb(Base):
    __tablename__ = "job"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    country  = Column(String)
    location = Column(String)
    workplace = Column(String)
    job_type = Column(String)
    experience = Column(String)
    salary = Column(String)
    date = Column(String)
    description = Column(String)
    skills = relationship("Skill", secondary="job_skills", back_populates="jobs")
    
class Skill(Base):
    __tablename__ = 'skill'
    
    id   = Column(Integer, primary_key=True)
    name = Column(String,  nullable=False)
    category = Column(String)
    skill_count = Column(Integer, nullable=False)
    skill_percent = Column(Numeric(5,2), nullable=False)

    jobs = relationship("JobDb", secondary="job_skills", back_populates="skills")
    
class JobSkills(Base):
    __tablename__  = 'job_skills'
    
    id             = Column(Integer, primary_key=True)
    job_id         = Column(Integer, ForeignKey('job.id'), nullable=False)
    skill_id       = Column(Integer, ForeignKey('skill.id'), nullable=False)
    __table_args__ = (UniqueConstraint('job_id', 'skill_id', name='uq_job_skill'),)

def check_tables_existance():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    for table_name in ['job', 'skill', 'job_skills']:
        if table_name not in table_names:
            return False
    return True


def initialize_database():
    """Ensures that all necessary tables exist in the database."""
    Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
# initialize_database()
    
def upload_jobs(jobs_list: list, skills_dict, date):
    '''Due to the need of skills in order to upload jobs linked with skills. When used along upload skills, this must be used as the last one, as we want the upload_skills data complete'''

    with Session(engine) as session:
        skill_objects_list = get_skills_for_linking(skills_dict) 
  
    for job in jobs_list:
        if len(job.skills) > 0: 
            skill_data = [skill_object for skill_object in skill_objects_list if skill_object.name in job.skills]
        else:
            skill_data = None

        new_job = JobDb(
            title=job.title,
            location=job.location,
            country= job.country,
            workplace=job.workplace,
            job_type=job.job_type,
            experience=job.level,
            salary=job.salary,
            date = date,
            description=job.description,
            skills = skill_data
        )
        
        session.add(new_job)
        session.commit()

def upload_skills(skills_dict, skills_categorized, jobs_len):
    '''Uploads skills data to database.'''
    if not skills_dict:
        print('No skills has been selected')
        return
    
    Session = sessionmaker(bind=engine)
    session = Session()

    # Preparing local and db skills data.
    local_skills_data  = {name: [skill_count, 0] for name, skill_count in skills_dict.items()}
    db_skills_data = session.query(Skill.name, Skill.skill_count, Skill.skill_percent).all()
    db_skills_data = {name: [skill_count, skill_percent] for name, skill_count, skill_percent in db_skills_data}
    job_count = session.execute(select(func.count(JobDb.id))).scalar_one() + jobs_len

    # Merging the lists
    skills_data = {}
    all_keys = set(local_skills_data.keys()).union(db_skills_data.keys())
    for key in all_keys:
        total_count = local_skills_data.get(key, [0, 0])[0] + db_skills_data.get(key, [0, 0])[0]
        total_percent = (total_count / job_count) * 100 if job_count > 0 else 0 # just in case for any reason 0 things reach here
        skills_data[key] = [total_count, total_percent]
    
    
    # Properly uploading the data
    for skill in skills_data.keys():
        skill_count = skills_data[skill][0]
        
        if skill_count == 0:
            continue
        
        if skill not in db_skills_data:

            if skill_count == 0: 
                continue 
            try:
                category = skills_categorized[skill]
            except:
                category = 'Uncategorized'
                
            new_skill = Skill(
                name = skill,
                category = category,
                skill_count = skill_count,
                skill_percent = skills_data[skill][1]
            )
            
            session.add(new_skill)
            
        else:            
            session.query(Skill).filter(Skill.name == skill).update({
                Skill.skill_count: skill_count,
                Skill.skill_percent: skills_data[skill][1]
            })

            
    session.commit()

def get_skills_for_linking(skills_dict):
    '''The purpose of this function could have been linked to upload_skills for efficiency and reduce database queries. 
    However to keep the upload_skills more focused on a single function'''
    with Session(engine) as session:
        skill_object_list = session.query(Skill).filter(Skill.name.in_(skills_dict.keys())).all()
    return skill_object_list 
    
    