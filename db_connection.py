import mysql.connector
from mysql.connector import Error
import sys

def colored(text,color_code):
    return f"\033[{color_code}m{text}\033[0m"
class Database:
    
    def connect(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",          
                user="root",               
                password="Raju0612@",  
                database="employee_management"  
            )
            cursor = connection.cursor()
            if connection.is_connected():
                print(colored("Connected to MySQL Database✅","1;32"))
            return connection,cursor
        except Error as e:
            print(f"Error: {e}")
    

    def commit(self,connection):
        try:
            connection.commit()
        except Exception as e:
            print(colored(f"Error: {e}","1;31"))
            sys.exit()

    def close(self,connection):
        try:
            connection.close()
        except Exception as e:
            print(colored(f"Error: {e}","1;31"))
            sys.exit()
Database()