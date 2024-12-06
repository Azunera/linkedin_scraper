
languages = {
    'Python', 'Java', 'C', 'C++', 'C#', 'R', 'Rust', 'Go', 'Golang','JavaScript',
    'VBA', 'T-SQL', 'PowerShell', 'HTML', 'Scala', 'SAS', 'CSS', 'TypeScript', 'Perl', 'Ruby', 'PHP', 'Julia', 
    'Rust', 'Crystal', 'Swift', 'Kotlin', 'Virtual Basic', 'Assembly', 'Groovy', 'VB.NET', 'COBOL', 
    'Solidity', 'Lua', 'APL', 'Sass', 'Clojure', 'Fortran', 'Dart', 'Elixir', 'Haskell', 'F#', 
    'Objective-C', 'Erlang', 'Lisp', 'Delphi', 'Pascal', 'OCaml', 'visualbasic'
}

frameworks = {'Angular', 'Node.js', 'Django', 'Flask', 'Vue.js', 'Express', 'FastAPI', 'jQuery', 'Ruby on Rails', 'ASP.NET', 'React.js', 'Next.js', 'Laravel', 'Gatsby', 'Symfony', 'Lavarel', 'Spring Boot'}

libraries = {'Spark', 'Apache Spark', 'Kafka', 'Apache Kafka', 'React', 'Hadoop', 'Spring', 'Airflow', 'Pandas', 'GraphQL', 'NumPy', 'TensorFlow', 'PyTorch', 'PySpark', 'Selenium', 'Playwright', 'GDPR', 'Scikit-learn', 'Jupyter', 'Matplotlib', 'Seaborn', 'Flutter', 'Keras', 'BeautifulSoup', 'PIL', 'Pillow', 'SciPy', 'Chai', 'OpenCV'}

clouds = {'AWS', 'Azure', 'Snowflake', 'DataBricks', 'RedShift', 'GCP', 'Oracle', 'BigQuery', 'IBM Cloud', 'Alibaba Cloud', 'DigitalOcean', 'Heroku'}

databases = {'MySQL', 'Cassandra', 'PostgreSQL', 'MongoDB', 'Elasticsearch', 'DynamoDB', 'Redis', 'DB2', 'Neo4j', 'MariaDB', 'Firebase', 'Couchbase', 'SQLite', 'Firestore', 'CouchDB', 'MariaDB',  'Amazon Aurora', 'GraphQL'}

devops = {'Jenkins', 'GitLab CI', 'CircleCI', 'Travis CI', 'Docker', 'Kubernetes', 'OpenShift'}
other_languages = {'SQL', 'NoSQL', 'MongoDB', 'HTML', 'CSS', 'Bash', 'Shell', 'VBA', 'SAS', 'T-SQL'}

 # Use above lists for order, you can fuse them with code below, copy from terminal and then make a single list to increase running time
    # all_sets = [languages, frameworks, libraries, clouds, databases, devops, other_languages]
    # predlist = set().union(*all_sets)  
    # print(predlist)
pred_list = {'Express', 'Angular', 'APL', 'Ruby', 'Seaborn', 'MySQL', 'GDPR', 'jQuery', 'Docker',
                 'Matplotlib', 'Vue.js', 'Kubernetes', 'Ruby on Rails', 'Rust', 'Couchbase', 'Pillow', 
                 'SQLite', 'Elasticsearch', 'Fortran', 'PyTorch', 'C', 'Crystal', 'BeautifulSoup',
                 'T-SQL', 'TensorFlow', 'ASP.NET', 'Swift', 'DataBricks', 'Java', 'Delphi', 'Scikit-learn', 
                 'CircleCI', 'Lisp', 'GCP', 'SQL', 'F#', 'AWS', 'Kotlin', 'IBM Cloud', 'Snowflake', 'Assembly', 
                 'Apache Kafka', 'Pandas', 'Symfony', 'Redis', 'Travis CI', 'Objective-C', 'PHP', 'Gatsby', 
                 'Spring Boot', 'Bash', 'PowerShell', 'Keras', 'Spring', 'Next.js', 'Django', 'PIL', 'Jenkins', 
                 'Virtual Basic', 'Chai','MariaDB', 'Groovy', 'Playwright', 'DynamoDB', 'Scala', 'COBOL', 
                 'React.js', 'Haskell', 'Apache Spark', 'Jupyter', 'visualbasic', 'C#', 'Alibaba Cloud', 'OpenShift', 
                 'R', 'Amazon Aurora', 'Erlang', 'BigQuery', 'HTML', 'MongoDB', 'C++', 'Sass', 'CSS', 'VBA', 'Hadoop', 
                 'Laravel', 'Airflow', 'Golang', 'Perl', 'Lavarel','Flask', 'Flutter', 'Oracle', 'Clojure', 'Lua', 'Dart', 
                 'Selenium', 'Heroku', 'DB2', 'JavaScript', 'RedShift',  'Neo4j', 'DigitalOcean', 'Elixir', 'OCaml', 
                 'Spark', 'PySpark', 'Cassandra', 'NumPy', 'GitLab CI', 'Pascal', 'Python', 'SciPy', 'VB.NET', 'TypeScript', 
                 'CouchDB', 'Firestore', 'NoSQL', 'Firebase', 'Go', 'React', 'FastAPI', 'Node.js', 'GraphQL', 'Azure', 
                 'PostgreSQL', 'Kafka', 'OpenCV', 'Solidity', 'SAS', 'Julia', 'Shell'}


# EC2, Lambda, SNS, and S3