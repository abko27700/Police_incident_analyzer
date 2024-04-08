import sqlite3
import os
from collections import Counter
# from augmentFunctions
import logger

def destroy_db():

    db_file_path = "resources/normanpd.db"

    if os.path.exists(db_file_path):
        os.remove(db_file_path)
    else:
        logger.log_message("Database file not found.")


def createDb():
    resources_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)
        # logger.log_message(f"Created resources folder: {resources_folder}")

    db_path = os.path.abspath(os.path.join("resources", "normanpd.db"))
    if os.path.exists(db_path):
        os.remove(db_path)
        # logger.log_message(f"Existing database file removed: {db_path}")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    """)
    con.commit()  
    con.close() 
    
def insertIntoDb(parsed_data):
    db_path = os.path.abspath(os.path.join("resources", "normanpd.db"))

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for row in parsed_data:
        c.execute("INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)", row)

    conn.commit() 
    conn.close()  

def generate_report():
    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()

    query = """
        SELECT id, incident_time, incident_number, incident_location, nature, incident_ori
        FROM incidents
        ORDER BY id ASC
    """

    cursor.execute(query)
    results = cursor.fetchall()
    
    report = ""
    for row in results:
        report += "\t".join(map(str, row)) + "\n"
        
    connection.close()

    return report

def get_nature_frequencies():
    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT nature FROM incidents")
    natures = [row[0] for row in cursor.fetchall()]
    nature_counter = Counter(natures)
    sorted_natures = sorted(nature_counter.items(), key=lambda x: (-x[1], x[0]))  # Sort by frequency descending, then by nature
    connection.close()
    return sorted_natures

def assign_nature_rankings(sorted_natures):
    rankings = {}
    rank = 1
    prev_freq = None
    for i, (nature, freq) in enumerate(sorted_natures):
        if freq != prev_freq:
            rank = i + 1
        rankings[nature] = rank
        prev_freq = freq
    return rankings

def get_location_frequencies():
    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT incident_location FROM incidents")
    locations = [row[0] for row in cursor.fetchall()]
    location_counter = Counter(locations)
    sorted_locations = sorted(location_counter.items(), key=lambda x: (-x[1], x[0]))  # Sort by frequency descending, then by nature
    connection.close()
    return sorted_locations

def assign_location_rankings(sorted_locations):
    rankings = {}
    rank = 1
    prev_freq = None
    for i, (location, freq) in enumerate(sorted_locations):
        if freq != prev_freq:
            rank = i + 1
        rankings[location] = rank
        prev_freq = freq
    return rankings

def get_nature_rankings():
    sorted_natures = get_nature_frequencies()
    nature_rankings = assign_nature_rankings(sorted_natures)
    return nature_rankings


def get_location_rankings():
    sorted_locations = get_location_frequencies()
    location_rankings = assign_location_rankings(sorted_locations)
    return location_rankings


def get_incidents_from_database():
    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM incidents")
    incidents = cursor.fetchall()
    connection.close()
    return incidents

def create_coordinates_db():
    db_path = 'resources/coordinates.db'
    if not os.path.exists(db_path):
        # Connect to SQLite database (or create if it doesn't exist)
        conn = sqlite3.connect(db_path)
        # Create a cursor object to execute SQL queries
        c = conn.cursor()
        # Create a table to store location data
        c.execute('''CREATE TABLE IF NOT EXISTS coordinates (
                        name TEXT,
                        latitude REAL,
                        longitude REAL
                    )''')
        # Commit changes and close connection
        conn.commit()
        conn.close()
       

def check_coordinates_in_db(location_str):
    db_path = 'resources/coordinates.db'
    if not os.path.exists(db_path):
        create_coordinates_db()
        logger.log_message("db not found.")
        return None, None, -2  # Return None for latitude and longitude, and status code -2 for DB not found

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM coordinates WHERE name=?", (location_str,))
    location = c.fetchone()
    conn.close()
    if location:
        logger.log_message("returning from cache for location "+ location_str)
        # logger.log_message(location[1])
        # logger.log_message(location[2])
        return location[1], location[2], 0  # Return latitude, longitude, and status code 0 for found in DB
    else:
        return None, None, -1  # Return None for latitude and longitude, and status code -1 for not found in DB


def insert_coordinates_to_db(name, latitude, longitude):
    db_path = 'resources/coordinates.db'
    if not os.path.exists(db_path):
        create_coordinates_db()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT INTO coordinates (name, latitude, longitude)
                VALUES (?, ?, ?)''', (name, latitude, longitude))
    conn.commit()
    conn.close()

def fetch_incident_window(current_incident_id, window_size=3):
    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()

    # Calculate the ID range to query
    start_id = current_incident_id - window_size
    end_id = current_incident_id + window_size

    cursor.execute("""
        SELECT * FROM incidents
        WHERE id BETWEEN ? AND ?
        ORDER BY id ASC
    """, (start_id, end_id))

    incidents = cursor.fetchall()
    connection.close()

    return incidents
