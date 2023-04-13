import mysql.connector as mysql
from mysql.connector import Error
from datetime import date, timedelta
import shutil
import os

# EERST DIT UITVOEREN IN MYSQL WORKBENCH! (enkel nodig voor de allereerste keer dat je het script draait)
# CREATE SCHEMA IF NOT EXISTS `flight_oltp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

conn = None
cursor = None

DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = 'flight_oltp'
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

try:
    # autocommit is zéér belangrijk.
    conn = mysql.connect(host=DB_HOST, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, autocommit=True)    
    print(type(conn))
    if conn.is_connected():
        # choose a specific start_date    
        start_date = date(2023, 4, 6)
        end_date = date.today()
        delta = timedelta(days=1) 
        while start_date <= end_date:

            date_format = start_date.strftime("%Y_%m_%d")

            # for each date check if the file exists and copy the file to C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\
            
            # hieronder is wat je moet aanpassen naar het csv mapje binnen het project zelf
            # old_path = "C:\\Users\\svre257\\OneDrive - Hogeschool Gent\\Documenten\\Lesgeven Voorjaar 2023\\Data Engineering Project I\\Scrape\\" + airline + "_" + date_format + ".csv" 
            # old_path = 
            # zorg er dan voor dat je csvToGithub.py script geen All.csv meer genereert, maar een csv file per datum
            new_path = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\" + "All" + ".csv"
            
            # Remove file if it already exists
            if os.path.exists(new_path):
                os.remove(new_path)
            if os.path.exists(old_path):    
                shutil.copy(old_path, new_path)

            # conn.reconnect is important, otherwise error
            conn.reconnect()
            cursor = conn.cursor()  

            # Execute commands in file LoadFiles.sql to import data into database airfares
            file_name = 'LoadFiles.sql'
            
            for root, dirs, files in os.walk('/'):
                if file_name in files:
                    path = os.path.join(root, file_name)
                    break
            
            with open(path, 'r') as file:
                cursor.execute(file.read(), multi=True)   
                                           
            cursor.close()

            start_date += delta
            
    conn.close()       

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (conn.is_connected()):
        cursor.close()
        conn.close()
        print("MySQL connection is closed")


