import tkinter as tk
from tkinter import messagebox
from db_connector import create_connection # Digunakan untuk login
from atm_gui import LoginFrame, RegisterFrame, NasabahFrame, AdminFrame, StrukFrame #mengimpor 5 kelas tersebut
import mysql.connector
from mysql.connector import Error

# Pusat Kontrol App untuk mengatur pergantian halaman, mengatur jendela, dan mengatur seluruh app
class ATMApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Manajemen ATM Sederhana")
        master.geometry("700x500")
        
        # Konfigurasi grid untuk frame agar menumpuk 
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        self.current_user = {} # Menyimpan data user yang sedang login (username, role, saldo)
        
        self.frames = {}
        # Inisialisasi semua frame dari gui_frames.py
        for F in (LoginFrame, RegisterFrame, NasabahFrame, AdminFrame, StrukFrame):
            page_name = F.__name__
            frame = F(master, self) 
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        # Menampilkan frame tertentu berdasarkan nama kelasnya.
        frame = self.frames[page_name]
        frame.tkraise()
        # memuat data saat ditampilkan untuk adminframe
        if page_name == "AdminFrame":
            frame.load_data_on_show()
        
    def login(self, username, pin):
        # verifikasi sudah terhubung ke database
        conn = create_connection()
        if conn is None:
            messagebox.showerror("Error", "Koneksi Database Gagal!")
            return

        cursor = conn.cursor(dictionary=True)
        # verifikasi data di database
        query = "SELECT id, username, role, saldo, pin FROM users WHERE username = %s AND pin = %s" #proses verifikasi
        cursor.execute(query, (username, pin))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Menyimpan data user ke cache aplikasi (tanpa PIN)
            self.current_user = {'id': user_data['id'], 'username': user_data['username'], 'role': user_data['role'], 'saldo': user_data['saldo']}
            
            if user_data['role'] == 'nasabah':
                # Memanggil metode pada frame nasabah untuk update UI
                self.frames['NasabahFrame'].update_saldo(user_data['saldo'])
                self.show_frame("NasabahFrame")
            elif user_data['role'] == 'admin':
                # Memanggil metode pada frame admin untuk memuat data
                self.show_frame("AdminFrame")
        else:
            messagebox.showerror("Login Gagal", "Username atau PIN salah.")

    def logout(self):
        # meriset data untuk kembali ke halaman login
        self.current_user = {}
        self.show_frame("LoginFrame")
        # Bersihkan input login di Frame Login
        self.frames['LoginFrame'].user_entry.delete(0, tk.END)
        self.frames['LoginFrame'].pin_entry.delete(0, tk.END)

# bertugas menjalankan dan mengontrol seluruh kode
if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()