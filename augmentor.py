import argparse
import csv
import os
import re
import shutil
# import requests
# from pypdf import PdfReader
import sqlite3
import requests
# from dbOperations import createDb, insertIntoDb,get_nature_rankings,get_location_rankings,destroy_db
import dbOperations
from augmentFunctions import augment_data
from pypdf import PdfReader
from datetime import datetime

def read_csv(file_path):
    urls = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.append(row[0])  # Assuming URLs are in the first column
    return urls

def extract_date_from_url(url):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', url)
    if match:
        return match.group(1)
    else:
        filename = os.path.splitext(os.path.basename(url))[0]
        return filename

def download_pdf(url,dest_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        return dest_path
        
    else:
        print(f"Error when trying to download PDF. Status code: {response.status_code}")

def parse_pdf(filePath):
    parsed_data = []
    global pdf_data
    pdf_data=""
    filePath = os.path.abspath(filePath)
    reader = PdfReader(filePath)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        temp_data=page.extract_text(extraction_mode="layout")
        pdf_data+=temp_data+"\n"

    lines = pdf_data.split('\n')
    parent_array = [] 
    for line in lines:
        data_array = [e.strip() for e in re.split(r"\s{4,}", line.strip())]
        if len(data_array)>1 and data_array[0] and data_array[0][0].isdigit() :
            if len(data_array)==3:
                data_array.insert(2,'')
                data_array.insert(3,'')
            elif len(data_array)==4:
                data_array.insert(3,'')
            parent_array.append(tuple(data_array))
    return parent_array

def processPdfs(file_path):

    pdf_urls = read_csv(file_path)
    destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tempFiles')
    os.makedirs(destination_folder, exist_ok=True)
    dbOperations.createDb()
    clear_log_file()
    for url in pdf_urls:
        date = extract_date_from_url(url)
        filename = f"{date}.pdf"
        dest_path = os.path.join(destination_folder, filename)
        download_pdf(url,dest_path)
        parsed_data = parse_pdf(dest_path)
        dbOperations.insertIntoDb(parsed_data)
    augment_data()
    dbOperations.destroy_db()
    shutil.rmtree(destination_folder)

def clear_log_file(log_file_path='logs.txt'):
    """Clears the contents of the log file."""
    with open(log_file_path, 'w') as file:
        pass  # Opening in 'w' mode clears the file


    
    
def get_day_of_week(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.weekday()

def get_time_of_day(time_str):
    hour = int(time_str.split(':')[0])
    if 6 <= hour < 12:
        return 1  # Morning
    elif 12 <= hour < 18:
        return 2  # Afternoon
    elif 18 <= hour < 24:
        return 3  # Evening
    else:
        return 4  # Night

def main():
    parser = argparse.ArgumentParser(description='Process a CSV file containing PDF URLs.')
    parser.add_argument('--urls', type=str, help='Path to the CSV file with PDF URLs')
    args = parser.parse_args()
    if args.urls:
        processPdfs(args.urls)
    else:
        print("Please provide the --urls option with a path to the CSV file.")

if __name__ == '__main__':
    main()
