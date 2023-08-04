import csv
import os

import psycopg2
import json

# Function to create tables if they don't exist
def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS constituency (
            id SERIAL PRIMARY KEY,
            name_assembly_c TEXT,
            part_no TEXT,
            name_parliamentary_c TEXT,
            year_revision TEXT,
            polling_station_name TEXT,
            polling_station_type TEXT,
            number_electors TEXT,
            starting_no TEXT,
            ending_no TEXT,
            male TEXT,
            female TEXT,
            third TEXT,
            state TEXT,
            police_station TEXT,
            revenue_division TEXT,
            main_town TEXT,
            district TEXT,
            mandal TEXT,
            pin_code TEXT,
            file_name TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS electorate (
            id SERIAL PRIMARY KEY,
            voter_id TEXT,
            name TEXT,
            name2 TEXT,
            type_name2 TEXT,
            house_no TEXT,
            age TEXT,
            sex TEXT,
            file_name TEXT,
            page TEXT
        )
    ''')

def create_conn():

    # Create a connection to the PostgreSQL database
    conn = psycopg2.connect(host='localhost', user='documentocr',
                                  password='Ocr@123#',
                                  dbname='documentocr', port=5432
    )
    return conn
def insert_json(json_file):
    conn = psycopg2.connect(host='localhost', user='documentocr',
                            password='Ocr@123#',
                            dbname='documentocr', port=5432
                            )
    cursor = conn.cursor()
    # Load data from the JSON file
    with open(os.path.join("fileupload", json_file), 'r') as f:
        json_data = json.load(f)
    # Insert the "constituence" data into the "constituency" table
    constituence_data = json_data['constituence']
    cursor.execute('''
        INSERT INTO constituency (
            name_assembly_c, part_no, name_parliamentary_c, year_revision, polling_station_name,
            polling_station_type, number_electors, starting_no, ending_no, male, female, third,
            state, police_station, revenue_division, main_town, district, mandal, pin_code, file_name
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    ''', (
        constituence_data['name_assembly_c'],
        constituence_data['part_no'],
        constituence_data['name_parliamentary_c'],
        constituence_data['year_revision'],
        constituence_data['polling_station_name'],
        constituence_data['polling_station_type'],
        constituence_data['number_electors'],
        constituence_data['starting_no'],
        constituence_data['ending_no'],
        constituence_data['male'],
        constituence_data['female'],
        constituence_data['third'],
        constituence_data['state'],
        constituence_data['police_station'],
        constituence_data['revenue_division'],
        constituence_data['main_town'],
        constituence_data['district'],
        constituence_data['mandal'],
        constituence_data['pin_code'],
        json_file.replace(".json", ".pdf")
    ))


    electorate_data = json_data['electorate']
    for electorate_entry in electorate_data:
        cursor.execute('''
            INSERT INTO electorate (
                voter_id, name, name2, type_name2, house_no, age, sex, file_name
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        ''', (
            electorate_entry['id'],
            electorate_entry['name'],
            electorate_entry['name2'],
            electorate_entry['type_name2'],
            electorate_entry['house_no'],
            electorate_entry['age'],
            electorate_entry['sex'],
            json_file.replace(".json", ".pdf")
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    f.close()

def insert_csv(csv_file):
    conn = psycopg2.connect(host='localhost', user='documentocr',
                            password='Ocr@123#',
                            dbname='documentocr', port=5432
                            )
    cursor = conn.cursor()


    # Read the data from the CSV file and insert into the table
    with open(os.path.join("fileupload", csv_file), 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT INTO electorate (page, voter_id, name, name2, type_name2, house_no, age, sex, file_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                row['page'], row['id'], row['name'], row['name2'], row['type_name2'],
                row['house_no'], row['age'], row['sex'], csv_file.replace(".csv", ".pdf")
            ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    f.close()

conn = create_conn()
cursor = conn.cursor()

# Create tables if they don't exist
create_tables(cursor)
conn.commit()
conn.close()