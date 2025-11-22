import tkinter as tk
from tkinter import messagebox, ttk
from db_connector import create_connection, format_rupiah
import mysql.connector
from mysql.connector import Error

# ====================================================================
# --- Frame Login ---
# ====================================================================
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
        # Memanggil metode login pada controller
        self.controller.login(username, pin)

# ====================================================================
# --- Frame Register ---
# ====================================================================
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

# ====================================================================
# --- Frame Nasabah (Transaksi) ---
# ====================================================================
class NasabahFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="MENU NASABAH", font=("Arial", 16, "bold")).pack(pady=20)
        
        # menampilkan saldo nasabah
        self.saldo_label = tk.Label(self, text="Saldo Anda: Rp 0,00", font=("Arial", 12))
        self.saldo_label.pack(pady=10)
        
        # Operasi
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cek Saldo", command=self.check_saldo, width=15).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Setor Tunai", command=self.setor_dialog, width=15).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Tarik Tunai", command=self.tarik_dialog, width=15).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Ganti PIN", command=self.change_pin_dialog, width=15).grid(row=1, column=1, padx=10, pady=5) 
        tk.Button(self, text="Logout", command=controller.logout, bg="red", fg="white", width=15).pack(pady=20)

    def update_saldo(self, saldo):
        """Memformat dan memperbarui label saldo di GUI."""
        formatted_saldo = format_rupiah(saldo) 
        self.saldo_label.config(text=f"Saldo Anda: {formatted_saldo}")
        self.controller.current_user['saldo'] = saldo # Pastikan cache di controller juga terupdate

    def check_saldo(self):
        """Mengambil saldo terbaru dari database dan memperbarui UI/cache."""
        username = self.controller.current_user['username']
        conn = create_connection()
        if conn is None: return
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT saldo FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                self.update_saldo(result['saldo'])
                messagebox.showinfo("Cek Saldo", f"Saldo Anda saat ini: {self.saldo_label.cget('text')}")
        except Error as e:
            messagebox.showerror("Error", f"Gagal mengambil saldo: {e}")
        finally:
            conn.close()
            
    # Dialog input untuk Setor/Tarik
    def setor_dialog(self):
        self.dialog_transaksi("Setor Tunai", self.setor_tunai)

    def tarik_dialog(self):
        self.dialog_transaksi("Tarik Tunai", self.tarik_tunai)

    def dialog_transaksi(self, title, action_func):
        """Membuat jendela dialog generik untuk input jumlah transaksi."""
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        
        tk.Label(dialog, text=f"Masukkan Jumlah {title}:").pack(pady=10)
        amount_entry = tk.Entry(dialog, width=20)
        amount_entry.pack(pady=5)
        
        tk.Button(dialog, text="Proses", command=lambda: action_func(dialog, amount_entry.get())).pack(pady=10)

    def setor_tunai(self, dialog, amount_str):
        """Logika untuk Setor Tunai."""
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka.")
            return

        username = self.controller.current_user['username']
        conn = create_connection()
        if conn is None: return

        try:
            cursor = conn.cursor()
            query = "UPDATE users SET saldo = saldo + %s WHERE username = %s"
            cursor.execute(query, (amount, username))
            conn.commit()
            
            # Update saldo di UI dan cache
            new_saldo = self.controller.current_user['saldo'] + amount
            self.update_saldo(new_saldo)
            
            messagebox.showinfo("Sukses", "Setor tunai berhasil.")
            dialog.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Setor gagal: {e}")
        finally:
            conn.close()

    def tarik_tunai(self, dialog, amount_str):
        """Logika untuk Tarik Tunai."""
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka.")
            return

        current_saldo = self.controller.current_user.get('saldo', 0)

        # Cek saldo tidak mencukupi
        if amount > current_saldo:
            messagebox.showerror("Error", "Saldo tidak mencukupi.")
            return

        username = self.controller.current_user['username']
        conn = create_connection()
        if conn is None: return

        try:
            cursor = conn.cursor()
            query = "UPDATE users SET saldo = saldo - %s WHERE username = %s"
            cursor.execute(query, (amount, username))
            conn.commit()
            
            # Update saldo di UI dan cache
            new_saldo = current_saldo - amount
            self.update_saldo(new_saldo)
            
            messagebox.showinfo("Sukses", "Tarik tunai berhasil.")
            dialog.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Tarik gagal: {e}")
        finally:
            conn.close()
            
    # Dialog Ganti PIN
    def change_pin_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Ganti PIN")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="GANTI PIN NASABAH", font=("Arial", 12, "bold")).pack(pady=10)

        # PIN Lama
        tk.Label(dialog, text="PIN Lama (4 Digit):").pack()
        old_pin_entry = tk.Entry(dialog, show="*", width=20)
        old_pin_entry.pack(pady=3)

        # PIN Baru
        tk.Label(dialog, text="PIN Baru (4 Digit):").pack()
        new_pin_entry = tk.Entry(dialog, show="*", width=20)
        new_pin_entry.pack(pady=3)
        
        tk.Button(dialog, text="Ubah PIN", command=lambda: self.change_pin(dialog, old_pin_entry.get(), new_pin_entry.get()), bg="blue", fg="white", width=15).pack(pady=10)

    def change_pin(self, dialog, old_pin, new_pin):
        """Logika untuk mengganti PIN user."""
        username = self.controller.current_user['username']

        # Validasi PIN Baru
        if not new_pin or len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror("Error", "PIN Baru harus 4 digit angka.")
            return

        conn = create_connection()
        if conn is None: return
        
        cursor = conn.cursor(dictionary=True)
        
        # 1. Verifikasi PIN Lama
        query_check = "SELECT pin FROM users WHERE username = %s"
        cursor.execute(query_check, (username,))
        result = cursor.fetchone()
        
        if not result or result['pin'] != old_pin:
            messagebox.showerror("Error", "PIN Lama salah atau user tidak ditemukan.")
            conn.close()
            return
            
        # 2. Update PIN Baru
        try:
            query_update = "UPDATE users SET pin = %s WHERE username = %s"
            cursor.execute(query_update, (new_pin, username))
            conn.commit()
            
            messagebox.showinfo("Sukses", "PIN berhasil diganti. Anda harus **Login Ulang**.")
            dialog.destroy()
            self.controller.logout() # Wajibkan login ulang
            
        except Error as e:
            messagebox.showerror("Error", f"Gagal mengubah PIN: {e}")
        finally:
            conn.close()

# ====================================================================
# --- Frame Admin (Melihat Data Nasabah) ---
# ====================================================================
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
        """Mengambil data semua nasabah (role='nasabah') dari database dan menampilkannya di Treeview."""
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
                formatted_saldo = format_rupiah(nasabah['saldo'])
                self.tree.insert('', tk.END, values=(nasabah['id'], nasabah['username'], formatted_saldo))
                
        except Error as e:
            messagebox.showerror("Error", f"Gagal memuat data nasabah: {e}")
        finally:
            conn.close()