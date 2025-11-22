import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Mencoba membuat koneksi ke database MySQL.
    Aplikasi Anda harus memastikan database 'atm_db' sudah tersedia.
    """
    db_config = {
        "host": "localhost",
        "user": "root", 
        "password": "",
        "database": "atm_db" # Pastikan database ini sudah ada
    }
    
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        # Menampilkan pesan error di console jika koneksi gagal
        print(f"Error connecting to MySQL: {e}")
        return None

# Fungsi utilitas untuk memformat saldo dalam format Rupiah
def format_rupiah(amount):
    """Memformat float menjadi string format Rupiah (ex: Rp 1.000.000,00)"""
    # Menggunakan f-string dengan pemisah ribuan koma, lalu mengganti koma desimal
    formatted = f"Rp {amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return formatted