import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk

def create_connection():
    db_config = {
        "host": "localhost",
        "user": "root", 
        "password": "",
        "database": "gemini"
    }
    
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    

# Asumsi file db_connector.py sudah dibuat dan dikonfigurasi

class ATMApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Manajemen ATM Sederhana")
        master.geometry("600x400")
        
        # Konfigurasi grid untuk frame agar menumpuk
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        self.current_user = {} # Menyimpan data user yang sedang login
        
        self.frames = {}
        for F in (LoginFrame, NasabahFrame, AdminFrame, RegisterFrame):
            page_name = F.__name__
            frame = F(master, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
    def login(self, username, pin):
        conn = create_connection()
        if conn is None:
            messagebox.showerror("Error", "Koneksi Database Gagal!")
            return

        cursor = conn.cursor(dictionary=True)
        query = "SELECT username, role, saldo FROM users WHERE username = %s AND pin = %s"
        cursor.execute(query, (username, pin))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            self.current_user = user_data
            if user_data['role'] == 'nasabah':
                self.frames['NasabahFrame'].update_saldo(user_data['saldo'])
                self.show_frame("NasabahFrame")
            elif user_data['role'] == 'admin':
                self.frames['AdminFrame'].load_nasabah_data()
                self.show_frame("AdminFrame")
        else:
            messagebox.showerror("Login Gagal", "Username atau PIN salah.")

    def logout(self):
        self.current_user = {}
        self.show_frame("LoginFrame")
        self.frames['LoginFrame'].user_entry.delete(0, tk.END)
        self.frames['LoginFrame'].pin_entry.delete(0, tk.END)

# --- Frame Login ---
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="LOGIN SISTEM ATM", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(self, text="Username/Rekening:").pack()
        self.user_entry = tk.Entry(self, width=30)
        self.user_entry.pack(pady=5)
        
        tk.Label(self, text="PIN:").pack()
        self.pin_entry = tk.Entry(self, show="*", width=30)
        self.pin_entry.pack(pady=5)
        
        tk.Button(self, text="Login", command=self.check_login, bg="green", fg="white", width=15).pack(pady=10)
        tk.Button(self, text="Register (Nasabah Baru)", command=lambda: controller.show_frame("RegisterFrame"), width=25).pack()

    def check_login(self):
        username = self.user_entry.get()
        pin = self.pin_entry.get()
        self.controller.login(username, pin)

# --- Frame Register ---
class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="REGISTRASI NASABAH BARU", font=("Arial", 14, "bold")).pack(pady=20)
        
        tk.Label(self, text="Nomor Rekening (Username):").pack()
        self.rek_entry = tk.Entry(self, width=30)
        self.rek_entry.pack(pady=3)
        
        tk.Label(self, text="PIN (4 Digit):").pack()
        self.pin_entry = tk.Entry(self, show="*", width=30)
        self.pin_entry.pack(pady=3)
        
        tk.Button(self, text="Daftar", command=self.register_new_user, bg="blue", fg="white", width=15).pack(pady=10)
        tk.Button(self, text="Kembali ke Login", command=lambda: controller.show_frame("LoginFrame"), width=25).pack()
        
    def register_new_user(self):
        rek = self.rek_entry.get()
        pin = self.pin_entry.get()
        
        if not rek or not pin or len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "Mohon isi Nomor Rekening dan PIN (harus 4 digit angka).")
            return

        conn = create_connection()
        if conn is None: return

        try:
            cursor = conn.cursor()
            query = "INSERT INTO users (username, pin, role, saldo) VALUES (%s, %s, 'nasabah', 0.00)"
            cursor.execute(query, (rek, pin))
            conn.commit()
            messagebox.showinfo("Sukses", f"Registrasi nasabah {rek} berhasil! Saldo awal Rp 0.00")
            self.rek_entry.delete(0, tk.END)
            self.pin_entry.delete(0, tk.END)
            self.controller.show_frame("LoginFrame")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Nomor Rekening sudah terdaftar.")
        except Error as e:
            messagebox.showerror("Error DB", f"Terjadi kesalahan database: {e}")
        finally:
            conn.close()

# --- Frame Nasabah (CRUD: Cek Saldo, Tarik, Setor) ---
class NasabahFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="MENU NASABAH", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Display Saldo
        self.saldo_label = tk.Label(self, text="Saldo Anda: Rp 0.00", font=("Arial", 12))
        self.saldo_label.pack(pady=10)
        
        # Operasi
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Cek Saldo", command=self.check_saldo, width=15).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Setor Tunai", command=self.setor_dialog, width=15).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Tarik Tunai", command=self.tarik_dialog, width=15).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Ganti PIN", width=15).grid(row=1, column=1, padx=10, pady=5) # Belum diimplementasi
        
        tk.Button(self, text="Logout", command=controller.logout, bg="red", fg="white", width=15).pack(pady=20)

    def update_saldo(self, saldo):
        # Format saldo dengan koma sebagai pemisah ribuan
        formatted_saldo = f"Rp {saldo:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".") 
        self.saldo_label.config(text=f"Saldo Anda: {formatted_saldo}")

    def check_saldo(self):
        conn = create_connection()
        if conn is None: return
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT saldo FROM users WHERE username = %s"
            cursor.execute(query, (self.controller.current_user['username'],))
            result = cursor.fetchone()
            if result:
                self.controller.current_user['saldo'] = result['saldo']
                self.update_saldo(result['saldo'])
                messagebox.showinfo("Cek Saldo", f"Saldo Anda saat ini: {self.saldo_label.cget('text')}")
        except Error as e:
            messagebox.showerror("Error", f"Gagal mengambil saldo: {e}")
        finally:
            conn.close()
            
    # Fungsi Setor dan Tarik memerlukan jendela dialog terpisah untuk input jumlah
    def setor_dialog(self):
        self.dialog_transaksi("Setor Tunai", self.setor_tunai)

    def tarik_dialog(self):
        self.dialog_transaksi("Tarik Tunai", self.tarik_tunai)

    def dialog_transaksi(self, title, action_func):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        
        tk.Label(dialog, text=f"Masukkan Jumlah {title}:").pack(pady=10)
        amount_entry = tk.Entry(dialog, width=20)
        amount_entry.pack(pady=5)
        
        tk.Button(dialog, text="Proses", command=lambda: action_func(dialog, amount_entry.get())).pack(pady=10)

    def setor_tunai(self, dialog, amount_str):
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka.")
            return

        conn = create_connection()
        if conn is None: return

        try:
            cursor = conn.cursor()
            query = "UPDATE users SET saldo = saldo + %s WHERE username = %s"
            cursor.execute(query, (amount, self.controller.current_user['username']))
            conn.commit()
            
            # Update saldo di UI dan cache
            new_saldo = self.controller.current_user['saldo'] + amount
            self.controller.current_user['saldo'] = new_saldo
            self.update_saldo(new_saldo)
            
            messagebox.showinfo("Sukses", "Setor tunai berhasil.")
            dialog.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Setor gagal: {e}")
        finally:
            conn.close()

    def tarik_tunai(self, dialog, amount_str):
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka.")
            return

        current_saldo = self.controller.current_user.get('saldo', 0)

        if amount > current_saldo:
            messagebox.showerror("Error", "Saldo tidak mencukupi.")
            return

        conn = create_connection()
        if conn is None: return

        try:
            cursor = conn.cursor()
            query = "UPDATE users SET saldo = saldo - %s WHERE username = %s"
            cursor.execute(query, (amount, self.controller.current_user['username']))
            conn.commit()
            
            # Update saldo di UI dan cache
            new_saldo = current_saldo - amount
            self.controller.current_user['saldo'] = new_saldo
            self.update_saldo(new_saldo)
            
            messagebox.showinfo("Sukses", "Tarik tunai berhasil.")
            dialog.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Tarik gagal: {e}")
        finally:
            conn.close()

# --- Frame Admin (Hanya Melihat) ---
class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="MENU ADMIN - DATA NASABAH", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Membuat Treeview (Tabel)
        columns = ('id', 'username', 'saldo')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('username', text='Nomor Rekening')
        self.tree.heading('saldo', text='Saldo')
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('username', width=150, anchor='w')
        self.tree.column('saldo', width=150, anchor='e')
        
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Button(self, text="Refresh Data", command=self.load_nasabah_data, width=15).pack(pady=10)
        tk.Button(self, text="Logout", command=controller.logout, bg="red", fg="white", width=15).pack(pady=10)

    def load_nasabah_data(self):
        # Bersihkan data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = create_connection()
        if conn is None: return
        
        try:
            cursor = conn.cursor(dictionary=True)
            # Admin hanya bisa melihat data nasabah
            query = "SELECT id, username, saldo FROM users WHERE role = 'nasabah'"
            cursor.execute(query)
            data_nasabah = cursor.fetchall()
            
            for nasabah in data_nasabah:
                # Format saldo sebelum dimasukkan ke tabel
                formatted_saldo = f"Rp {nasabah['saldo']:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                self.tree.insert('', tk.END, values=(nasabah['id'], nasabah['username'], formatted_saldo))
                
        except Error as e:
            messagebox.showerror("Error", f"Gagal memuat data nasabah: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()