import mysql.connector
from mysql.connector import Error

# fungsi untuk menyambungkan dengan database
def create_connection():
    db = {
        "host": "localhost", #alamat database
        "user": "root", #username database
        "password": "",
        "database": "atm_db" #nama database
    }
    
    conn = None
    # mencoba membuat koneksi ke database
    try:
        conn = mysql.connector.connect(db)
        return conn
    except Error as e:
        # jika terjadi error akan mecetak pesan berikut
        print(f"Error connecting to MySQL: {e}") 
        return None
    
# membuat tampilan rupiah menjadi Rp 0.000,00
def format_rupiah(amount):
    format = f"Rp {amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    # mengganti koma menjadi underscore sementara, mengganti titik menjadi koma, lalu mengubah underscore sementara menjadi titik
    return format #mengubah format sebagai
