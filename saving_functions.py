from dataclasses import fields
import json
import csv 

def append_to_json(job, json_file):
    '''Appends jobs into a json file, if it isn't found, it is created. The standard name is "data/jobs.json", it can be changed'''
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        jobs = []

    jobs.append(job)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)

    print('Appended job to JSON file')
    
def append_to_csv(data, csv_file):
    '''Appends data into a csv file, if it isn't found, it is created. The standard name is "data/jobs.csv", it can be changed'''
    # field_names = data.keys()
    field_names = [key for key in data.keys() if key != "description"]
    
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        if f.tell() == 0:  
            writer.writeheader()
        filt_data = {k: v for k, v in data.items() if k != "description"}
        writer.writerow(filt_data)
    
def export_to_json(json_file, scrap_data):
    try:
        with open(json_file, 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(scrap_data)

    # Write back to JSON file
    with open(json_file, 'w') as file:
        json.dump(existing_data, file, indent=2)
