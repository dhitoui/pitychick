import tkinter as tk
from tkinter import messagebox, ttk
from db_connector import create_connection, format_rupiah 
import mysql.connector
from mysql.connector import Error
import datetime # untuk mencatat waktu transaksi
from decimal import Decimal, InvalidOperation

# Frame Login
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="LOGIN SISTEM ATM", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(self, text="Username/Rekening:").pack()
        self.user_entry = tk.Entry(self, width=30)
        self.user_entry.pack(pady=5)
        
        tk.Label(self, text="PIN:").pack()
        self.pin_entry = tk.Entry(self, show="*", width=30) #membuat pin yang dimasukkan berubah menjadi *
        self.pin_entry.pack(pady=5)
        
        tk.Button(self, text="Login", command=self.check_login, bg="green", fg="white", width=15).pack(pady=10)
        tk.Button(self, text="Register (Nasabah Baru)", command=lambda: controller.show_frame("RegisterFrame"), width=25).pack()

    def check_login(self):
        username = self.user_entry.get()
        pin = self.pin_entry.get()
        # Memanggil login pada controller
        self.controller.login(username, pin)

# Frame Register
class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="REGISTRASI NASABAH BARU", font=("Arial", 14, "bold")).pack(pady=20)
        
        tk.Label(self, text="Nomor Rekening (Username):").pack()
        self.rek_entry = tk.Entry(self, width=30)
        self.rek_entry.pack(pady=3)
        
        tk.Label(self, text="PIN (4 Digit):").pack()
        self.pin_entry = tk.Entry(self, show="*", width=30) #membuat tampilan pin menjadi *
        self.pin_entry.pack(pady=3)
        
        tk.Button(self, text="Daftar", command=self.register_new_user, bg="blue", fg="white", width=15).pack(pady=10)
        tk.Button(self, text="Kembali ke Login", command=lambda: controller.show_frame("LoginFrame"), width=25).pack()
        
    def register_new_user(self):
        rek = self.rek_entry.get() #menampung inputan user di variabel rek
        pin = self.pin_entry.get() #menampung inputan user di variabel pin
        
        # no rek dan pin wajib diisi dengan format pin 4 digit dan tipe data harus angka
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

# Frame struk
class StrukFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="BUKTI TRANSAKSI ATM", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Label untuk menampilkan detail struk
        self.details_label = tk.Label(self, justify=tk.LEFT, font=("Courier", 10))
        self.details_label.pack(padx=30, pady=10, fill='x')

        # Tombol kembali ke menu nasabah
        tk.Button(self, text="Kembali ke Menu", command=lambda: controller.show_frame("NasabahFrame"), width=20).pack(pady=20)

    def show_struk(self, struk_data):
        # Format data struk untuk ditampilkan
        
        # Menggunakan data dari hasil pencatatan transaksi
        date_str = struk_data['date'].strftime("%Y-%m-%d")
        time_str = struk_data['date'].strftime("%H:%M:%S")
        
        amount_formatted = format_rupiah(struk_data['amount'])
        final_saldo_formatted = format_rupiah(struk_data['final_balance'])
        
        # Format untuk bukti transaksi
        struk_text = (
            f"==========================================\n"
            f"          STRUK {struk_data['type'].upper()}\n"
            f"==========================================\n"
            f"Tanggal       : {date_str}\n"
            f"Waktu         : {time_str}\n"
            f"ID Transaksi  : {struk_data['id']}\n"
            f"No. Rekening  : {struk_data['username']}\n"
            f"------------------------------------------\n"
            f"Jenis Transaksi: {struk_data['type'].title()}\n"
            f"Jumlah        : {amount_formatted}\n"
            f"------------------------------------------\n"
            f"SALDO AKHIR   : {final_saldo_formatted}\n"
            f"==========================================\n"
        )
        self.details_label.config(text=struk_text)
        self.controller.show_frame("StrukFrame")
        
# Frame Transaksi untuk Nasabah
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
        # untuk mencetak dan memperbarui data tampilan gui
        formatted_saldo = format_rupiah(saldo) 
        self.saldo_label.config(text=f"Saldo Anda: {formatted_saldo}")
        self.controller.current_user['saldo'] = saldo

    def check_saldo(self):
        # mengambil data dari databse dan memperbarui ui
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
        # menampilkan jendela pop up yang menyuruh user megninputkan jumalh uang
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        
        tk.Label(dialog, text=f"Masukkan Jumlah {title}:").pack(pady=10)
        amount_entry = tk.Entry(dialog, width=20)
        amount_entry.pack(pady=5)
        
        tk.Button(dialog, text="Proses", command=lambda: action_func(dialog, amount_entry.get())).pack(pady=10)

    def setor_tunai(self, dialog, amount_str):
        # logika exception setor tunai
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
                return
        except InvalidOperation: # Exception khusus untuk konversi Decimal yang gagal
            messagebox.showerror("Error", "Input harus berupa angka.")
            return
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka.")
            return

        # mengidenetifikasi pengguna aktif dan ketersediaan data di database
        username = self.controller.current_user['username']
        user_id = self.controller.current_user['id']
        conn = create_connection()
        if conn is None: return

        try:
            cursor = conn.cursor()
            # mengambil data user_id dan saldo awal
            cursor.execute("SELECT id, saldo FROM users WHERE username = %s FOR UPDATE", (username,))
            user_data = cursor.fetchone()
            if not user_data:
                messagebox.showerror("Error", "User tidak ditemukan.")
                return
            
            initial_saldo = user_data[1]
            new_saldo = initial_saldo + amount
            current_datetime = datetime.datetime.now()

            # mengudate saldo
            query_update = "UPDATE users SET saldo = %s WHERE id = %s" # logika inti untuk proses transaksi setor tunai
            cursor.execute(query_update, (new_saldo, user_id))
            
            # mencatat transaksi
            query_trans = """
            INSERT INTO transactions (user_id, transaction_date, type, amount, initial_balance, final_balance)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_trans, (user_id, current_datetime, 'setor', amount, initial_saldo, new_saldo))
            
            # Ambil ID Transaksi yang diinsert
            transaction_id = cursor.lastrowid
            
            conn.commit()

            # Update saldo di UI dan cache
            self.update_saldo(new_saldo)
            
        # menyiapkan data untuk struk
            struk_data = {
                'id': transaction_id,
                'date': current_datetime,
                'type': 'setor',
                'amount': amount,
                'final_balance': new_saldo,
                'username': username
            }

            # pesan jika transaksi berhasil dan menampilkan struk
            messagebox.showinfo("Sukses", "Setor tunai berhasil.")
            dialog.destroy()
            self.controller.frames['StrukFrame'].show_struk(struk_data)
        except Error as e:
            # pesan jika transaksi gagal
            messagebox.showerror("Error", f"Setor gagal: {e}")
        finally:
            conn.close()

    def tarik_tunai(self, dialog, amount_str):
        # logika exception untuk tarik tunai
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
                return
        except InvalidOperation: 
            messagebox.showerror("Error", "Input harus berupa angka.")
            return
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka.")
            return

        # berfungsi mengambil data saldo user yang sedang login
        current_saldo = self.controller.current_user.get('saldo', Decimal (0))
        username = self.controller.current_user['username']
        user_id = self.controller.current_user['id']

        # pesan jika saldo tidak mencukupi
        if amount > current_saldo:
            messagebox.showerror("Error", "Saldo tidak mencukupi.")
            return

        conn = create_connection()
        if conn is None: return

        try:
            cursor = conn.cursor()
            new_saldo = current_saldo - amount
            current_datetime = datetime.datetime.now()

            query_update = "UPDATE users SET saldo = %s WHERE id = %s" # logika proses saat tarik tunai
            cursor.execute(query_update, (new_saldo, user_id))

            # mencatat transaksi
            query_trans = """
            INSERT INTO transactions (user_id, transaction_date, type, amount, initial_balance, final_balance)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_trans, (user_id, current_datetime, 'tarik', amount, current_saldo, new_saldo))
            
            transaction_id = cursor.lastrowid
            
            conn.commit()
            
            # menampilakan update saldo di UI dan cache
            self.update_saldo(new_saldo)
            
            # data untuk Struk
            struk_data = {
                'id': transaction_id,
                'date': current_datetime,
                'type': 'tarik',
                'amount': amount,
                'final_balance': new_saldo,
                'username': username
            }

            # pesan jika transaksi berhasil
            messagebox.showinfo("Sukses", "Tarik tunai berhasil.")
            dialog.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Tarik gagal: {e}")
        finally:
            conn.close()
            
    # Ganti PIN
    def change_pin_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Ganti PIN")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="GANTI PIN NASABAH", font=("Arial", 12, "bold")).pack(pady=10)

        # menginputkan pin lama nasabah
        tk.Label(dialog, text="PIN Lama (4 Digit):").pack()
        old_pin_entry = tk.Entry(dialog, show="*", width=20)
        old_pin_entry.pack(pady=3)

        # menginputkan pin baru
        tk.Label(dialog, text="PIN Baru (4 Digit):").pack()
        new_pin_entry = tk.Entry(dialog, show="*", width=20)
        new_pin_entry.pack(pady=3)
        
        # tombol untuk mengkonfirmasi mengubah pin
        tk.Button(dialog, text="Ubah PIN", command=lambda: self.change_pin(dialog, old_pin_entry.get(), new_pin_entry.get()), bg="blue", fg="white", width=15).pack(pady=10)

    def change_pin(self, dialog, old_pin, new_pin):
        username = self.controller.current_user['username']

        # Validasi PIN Baru
        if not new_pin or len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror("Error", "PIN Baru harus 4 digit angka.")
            return

        conn = create_connection()
        if conn is None: return
        
        cursor = conn.cursor(dictionary=True)
        
        # memverifikasi PIN Lama
        query_check = "SELECT pin FROM users WHERE username = %s"
        cursor.execute(query_check, (username,))
        result = cursor.fetchone()
        
        if not result or result['pin'] != old_pin:
            # apabila user salah menginputkan data
            messagebox.showerror("Error", "PIN Lama salah atau user tidak ditemukan.")
            conn.close()
            return
            
        # Update PIN Baru
        try:
            query_update = "UPDATE users SET pin = %s WHERE username = %s"
            cursor.execute(query_update, (new_pin, username))
            conn.commit()
            
            messagebox.showinfo("Sukses", "PIN berhasil diganti. Anda harus **Login Ulang**.")
            dialog.destroy()
            self.controller.logout() # mengembalikkan ke halaman login
            
        except Error as e:
            messagebox.showerror("Error", f"Gagal mengubah PIN: {e}")
        finally:
            conn.close()

# Frame Admin
class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="MENU ADMIN", font=("Arial", 16, "bold")).pack(pady=10)
        
        # tab untuk memisahkan data nasabah dan data transaksi
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=20, pady=5)
        
        # Data Nasabah
        self.nasabah_tab = tk.Frame(self.notebook)
        self.notebook.add(self.nasabah_tab, text='Data Nasabah')
        
        tk.Label(self.nasabah_tab, text="DATA NASABAH", font=("Arial", 12, "bold")).pack(pady=5)

        # Membuat Tabel
        columns = ('id', 'username', 'saldo')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('username', text='Nomor Rekening')
        self.tree.heading('saldo', text='Saldo')
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('username', width=150, anchor='w')
        self.tree.column('saldo', width=150, anchor='e')
        self.tree.pack(fill='both', expand=True, padx=20, pady=5)

        tk.Button(self.nasabah_tab, text="Refresh Data Nasabah", command=self.load_nasabah_data, width=25).pack(pady=10)

        # Tab 2: Data Transaksi
        self.transaksi_tab = tk.Frame(self.notebook)
        self.notebook.add(self.transaksi_tab, text='Data Transaksi')
        
        tk.Label(self.transaksi_tab, text="DATA TRANSAKSI", font=("Arial", 12, "bold")).pack(pady=5)

        # Tabel Data Transaksi
        columns_transaksi = ('id_transaksi', 'tanggal', 'no_rek', 'tipe', 'jumlah', 'saldo_akhir')
        self.tree_transaksi = ttk.Treeview(self.transaksi_tab, columns=columns_transaksi, show='headings')
        self.tree_transaksi.heading('id_transaksi', text='ID Transaksi')
        self.tree_transaksi.heading('tanggal', text='Waktu')
        self.tree_transaksi.heading('no_rek', text='No. Rekening')
        self.tree_transaksi.heading('tipe', text='Tipe')
        self.tree_transaksi.heading('jumlah', text='Jumlah')
        self.tree_transaksi.heading('saldo_akhir', text='Saldo Akhir')

        self.tree_transaksi.column('id_transaksi', width=70, anchor='center')
        self.tree_transaksi.column('tanggal', width=120, anchor='center')
        self.tree_transaksi.column('no_rek', width=100, anchor='w')
        self.tree_transaksi.column('tipe', width=50, anchor='center')
        self.tree_transaksi.column('jumlah', width=100, anchor='e')
        self.tree_transaksi.column('saldo_akhir', width=100, anchor='e')
        
        self.tree_transaksi.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Button(self.transaksi_tab, text="Refresh Data Transaksi", command=self.load_transaksi_data, width=25).pack(pady=10)

        # Tombol logout di bawah notebook
        tk.Button(self, text="Logout", command=controller.logout, bg="red", fg="white", width=15).pack(pady=10)

        # binding untuk memuat data ketika tab berubah
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        # Muat data saat tab Transaksi dipilih
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == 'Data Transaksi':
            self.load_transaksi_data()
        elif selected_tab == 'Data Nasabah':
            self.load_nasabah_data()

    def load_nasabah_data(self):
        # mengambil data nasabah dari database untuk ditampilkan di tabel
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
        
    def load_transaksi_data(self):
        # mengambil data transaksi dari database
        for item in self.tree_transaksi.get_children():
            self.tree_transaksi.delete(item)
            
        conn = create_connection()
        if conn is None: return
        
        try:
            cursor = conn.cursor(dictionary=True)
            # Query untuk mengambil data transaksi beserta username (no_rek)
            query = """
            SELECT 
                t.id, t.transaction_date, t.type, t.amount, t.final_balance, u.username 
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            ORDER BY t.transaction_date DESC
            """
            cursor.execute(query)
            data_transaksi = cursor.fetchall()
            
            for trans in data_transaksi:
                # Format data
                waktu = trans['transaction_date'].strftime("%Y-%m-%d %H:%M:%S")
                jumlah_formatted = format_rupiah(trans['amount'])
                saldo_akhir_formatted = format_rupiah(trans['final_balance'])
                
                self.tree_transaksi.insert('', tk.END, 
                    values=(
                        trans['id'], 
                        waktu, 
                        trans['username'], 
                        trans['type'].title(), 
                        jumlah_formatted, 
                        saldo_akhir_formatted
                    )
                )
                
        except Error as e:
            messagebox.showerror("Error", f"Gagal memuat data transaksi: {e}")
        finally:
            conn.close()

    # Metode yang dipanggil saat frame admin ditampilkan
    def load_data_on_show(self):
        # Muat data nasabah saat pertama kali masuk ke frame Admin
        self.notebook.select(self.nasabah_tab)
        self.load_nasabah_data()