import mysql.connector
from mysql.connector import Error

def create_connection():
    db = {
        "host": "localhost", 
        "user": "root", 
        "password": "",
        "database": "atm_db" 
    }
    
    conn = None
    try:
        conn = mysql.connector.connect(**db)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}") 
        return None
    
def format_rupiah(amount):
    format_str = f"{amount:,.2f}"  # 1. Format dasar dengan pemisah ribuan default (koma) dan 2 desimal
    format_temp = format_str.replace(",", "_") # Ganti koma (pemisah ribuan default) menjadi underscore sementara
    format_dec = format_temp.replace(".", ",") # 3. Ganti titik (pemisah desimal default) menjadi koma
    final_format = format_dec.replace("_", ".") # 4. Ganti underscore menjadi titik (pemisah ribuan)
    return f"Rp {final_format}"