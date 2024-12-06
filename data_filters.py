from html import unescape

def clean_applicant_data(data):
    '''Filters the words "applicants", "applicant", and "Over" from applicant data.'''
    ban_list = ['applicants', 'applicant', 'Over', 'people clicked apply']
    for word in ban_list: 
        if word in data:
            data = data.replace(word, "")
    return data.strip()

def clean_job_html_description(description_html):
    '''
    Filters the html from a job description.
    Args:
        description_html (str): Required to be a string html, usually got from .html property from a css_first selector

    Returns:
        str: The job description filtered, containing '\\n'. Check inside function for filters
    '''
    
    banned_elements = ['<p>', '</p>', '<div class=\"job-details-module__content\">\n    ', '<p dir=\"ltr\">', '<!---->', '<span>', '</span>', '<div class="mt4">', '</div>', '<ul>', '</ul>', '<strong>', '</strong>', '<em>', '</em>'  '      ']
    # Deleting undesired text
    for element in banned_elements:
        if element in description_html:
            description_html = description_html.replace(element, "")
    
    replacing_elements = [
        ['<br>', '\n'],
        ['<span class="white-space-pre">', " "],
        ['<li>', '-'],
        ['</li>', '\n'],
        ]
    

    for element in replacing_elements:
        description_html = description_html.replace(element[0], element[1])

    description_html = unescape(description_html.strip())
    
    return description_html

def filter_underscore(argument):
    if argument is None:
        return None
    for i in range(len(argument)):
        if argument[i] is not None:
            argument[i] = argument[i].replace('_', ' ')
        else:
            del argument[i]
    
    if not len(argument):
        argument = None
    
    return argument
