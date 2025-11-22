import mysql.connector
from mysql.connector import Error

# Menghubungkan database lokal 
DB_CONFIG = {
    "host": "localhost",
    "user": "root", 
    "password": "", 
    "database": "atm_db"
}

def create_connection():
    conn = None
    try:
        # **DB_CONFIG mengubah dictionary menjadi argumen keyword
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        # Mencetak error ke konsol jika koneksi gagal
        print(f"Error connecting to MySQL: {e}")
        return None