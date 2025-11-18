import mysql.connector
from getpass import getpass
from tabulate import tabulate
import pandas as pd
from admin import *
from kitchen import *
from customer import *

#Fungsi supaya terkoneksi dengan database MySQL
def connect():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "pitychick_db"
    )
    cursor = db.cursor()

def bannerCard():
    print("Pity Chick Headquarter!\n", ">"*50)
def divider():
    print(">"*50)

#Fungsi login sebagai admin, kitchen, atau customer
def login_regist():
    def login():
        try:
            print("Login to Pity Chick Headquarter")
            username = input("Masukkan Username :")
            password = input("Masukkan Password :")

            if not db.is_connected():
                db.reconnect(attempts=1, delay=0)

            login_query_admin = "SELECT * FROM admint WHERE username = %s AND password = %s"
            cursor.execute(login_query_admin, (username, password))
            result_admin = cursor.fetchone()

            login_query_kitchen = "SELECT * FROM kitchen WHERE username = %s AND password = %s"
            cursor.execute(login_query_kitchen, (username, password))
            result_kitchen = cursor.fetchone()

            login_query_customer = "SELECT * FROM customer WHERE username = %s AND password = %s"
            cursor.execute(login_query_customer, (username, password))
            result_customer = cursor.fetchone()

            if result_admin:
                adminStart()
            elif result_kitchen:
                kitchenStart()
            elif result_customer:
                custStart()
            else:
                print("Identitas tidak ditemukan. Akses ditolak.")
                while True:
                    choice = input("Apakah anda ingin mencoba login kembali? (ya / tidak):").lower()
                    if choice == 'ya':
                        break
                    elif choice == 'tidak':
                        print("Keluar dari Login.")
                        break  
                    else:
                        print("Harap masukkan 'ya' atau 'tidak'.")

        except Exception as e:
            print("Error:", e)

    def regist():
        while True:
            try:
                print("Register")
                username = input("Masukkan username :")

                check_username_query = f"SELECT * FROM customer WHERE username = '{username}'"
                cursor.execute(check_username_query)
                result = cursor.fetchone()

                if result:
                    print("Nama pengguna sudah ada. Silakan masukkan nama pengguna lain.")
                    continue  

                password = input("Masukkan password :")
                email = input("Masukkan email :")
                phone = input("Masukkan nomor ponsel :")

                insert_query = f"INSERT INTO customer (username, password, email, phone) VALUES " \
                                f"('{username}', '{password}', '{email}', '{phone}')"
                cursor.execute(insert_query)
                db.commit()
                print("Pendaftaran berhasil. Silahkan login.")
                login()
                break  
            except Exception as e:
                print("Error:", e)

    bannerCard()
    print("Login or Register")
    while True:
        i = int(input("1. Login\n2. Register\nSelect (1/2): "))
        if i == 1:
            login()
        elif i == 2:
            regist()

login_regist()



#fungsi untuk login admin
def adminStart():
    def adminLogin():
        try:
            adminChoice()
            
        except Exception as e:
            print("Error:", e)

    adminLogin()

    #fungsi untuk menampilkan kategori
    def adminDisplayKategori():
        try:
            query = "SELECT * FROM categories"
            cursor.execute(query)
            data = cursor.fetchall()
            data_frame = pd.DataFrame(data)
            header = ["ID", "Kategori"]
            print("Daftar Kategori".center(30))
            print(tabulate(data_frame, headers = header, tablefmt = "fancy_grid", showindex = False, numalign = 'center', stralign = 'center'))

        except Exception as e:
            print("Error:", e)

    #fungsi untuk menambahkan kategori
    def addKategori():
        while True:
            try:
                new_id = int(input("Masukkan ID Kategori :"))
                new_category = input("Masukkan Nama Kategori :")

                add_query = f"INSERT INTO categories VALUES ({new_id}, '{new_category}')"
                cursor.execute(add_query)
                db.commit()
                print("Kategori berhasil ditambahkan.")

                choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk menambahkan kategori lain :")
                if choice.lower() == 'exit':
                    print("Keluar dari tambahkan kategori.")
                    break
            except ValueError:
                print("Harap masukkan ID yang valid (nilai numerik).")
            except Exception as e:
                print("Error:", e)

    #fungsi untuk mengedit kategori
    def editKategori():
        while True:
            try:
                category_id = int(input("Masukkan ID kategori yang akan diedit : "))
                new_category = input("Masukkan nama kategori baru : ")

                check_category_query = "SELECT * FROM categories WHERE category_id = %s"
                cursor.execute(check_category_query, (category_id,))
                result = cursor.fetchone()

                if result:
                    update_query = "UPDATE categories SET category = %s WHERE category_id = %s"
                    cursor.execute(update_query, (new_category, category_id))
                    db.commit()
                    print("Kategori berhasil diperbarui.")
                else:
                    print("ID kategori tidak ditemukan. Harap masukkan ID kategori yang valid.")

                choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk memperbarui kategori lain : ")
                if choice.lower() == 'exit':
                    print("Keluar dari edit kategori.")
                    break
            except ValueError:
                print("Harap masukkan nilai numerik yang valid untuk ID kategori.")
            except Exception as e:
                print("Error:", e)

    #fungsi untuk menghapus kategori
    def removeKategori():
        while True:
            try:
                category_id = int(input("Masukkan ID dari kategori yang ingin dihapus :"))

                check_category_query = f"SELECT * FROM categories WHERE category_id = {category_id}"
                cursor.execute(check_category_query)
                result = cursor.fetchone()

                if result:
                    delete_query = f"DELETE FROM categories WHERE category_id = {category_id}"
                    cursor.execute(delete_query)
                    db.commit()
                    print("Kategori berhasil dihapus.")
                else:
                    print("ID kategori tidak ditemukan. Harap masukkan ID kategori yang valid.")

                choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk menghapus kategori lain :")
                if choice.lower() == 'exit':
                    print("Keluar dari hapus kategori.")
                    break
            except Exception as e:
                print("Error:", e)

    #fungsi untuk menampilkan produk
    def adminDisplayProducts():
        try:
            query = "SELECT m.product_id, m.menu, m.price, c.category_id FROM products p JOIN categories c ON m.category_id = c.category_id"
            cursor.execute(query)
            data = cursor.fetchall()
            data_frame = pd.DataFrame(data)
            header = ["ID", "Nama Produk", "Harga", "Kategori"]
            print("Daftar Produk".center(50))
            print(tabulate(data_frame, headers = header, tablefmt = "fancy_grid", showindex = False, numalign = 'center', stralign = 'center'))

        except Exception as e:
            print("Error:", e)

    #fungsi untuk menambahkan produk
    def addProduct():
        while True:
            try:
                product_id = int(input("Product ID :"))
                menu = input("Menu :")
                price = float(input("Price :"))
                category_id = int(input("Category ID :"))
                category = input("Category: ")

                check_category_query = f"SELECT * FROM categories WHERE category_id = {category_id}"
                cursor.execute(check_category_query)
                result = cursor.fetchone()

                if result:
                    insert_query = f"INSERT INTO menus (product_id, category_id, menu, price, category) VALUES ({product_id}, {category_id}, '{menu}', {price}, {category})"
                    cursor.execute(insert_query)
                    db.commit()
                    print("Produk berhasil ditambahkan.")
                else:
                    print("ID kategori tidak ditemukan. Harap masukkan ID kategori yang valid.")

                choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk menambahkan poduk lain :")
                if choice.lower() == 'exit':
                    print("Keluar dari tambahkan kategori.")
                    break
            except ValueError:
                print("Silakan masukkan nilai numerik yang valid untuk ID, harga, dan ID kategori.")
            except Exception as e:
                print("Error:", e)

    #fungsi untuk mengedit produk   
    def editProduct():
        while True:
            try:
                product_id = int(input("Masukkan ID produk yang akan diedit : "))
                new_category_id = int(input("Masukkan ID kategori baru : "))
                new_product_name = input("Masukkan nama produk baru : ")
                new_price = float(input("Masukkan harga produk baru : "))
                new_category = int(input("Masukkan kategori baru : "))

                check_category_query = "SELECT * FROM categories WHERE category_id = %s"
                cursor.execute(check_category_query, (new_category_id,))
                category_result = cursor.fetchone()

                if category_result:
                    check_product_query = "SELECT * FROM menus WHERE product_id = %s"
                    cursor.execute(check_product_query, (product_id,))
                    product_result = cursor.fetchone()

                    if product_result:
                        update_query = "UPDATE menus SET category_id = %s, product_name = %s, price = %s, category = %s WHERE product_id = %s"
                        cursor.execute(update_query, (new_category_id, new_product_name, new_price, new_category, product_id))
                        db.commit()
                        print("Produk berhasil diperbarui.")
                    else:
                        print("ID produk tidak ditemukan. Harap masukkan ID produk yang valid.")
                else:
                    print("ID kategori tidak ditemukan. Harap masukkan ID kategori yang valid.")

                choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk memperbarui produk lain : ")
                if choice.lower() == 'exit':
                    print("Keluar dari edit produk.")
                    break
            except ValueError:
                print("Harap masukkan nilai numerik yang valid untuk ID, harga, dan ID kategori.")
            except Exception as e:
                print("Error:", e)

    #fungsi untuk menghapus produk
    def removeProduct():
        while True:
            try:
                product_id = int(input("Masukkan ID dari produk yang ingin dihapus :"))

                check_product_query = f"SELECT * FROM menus WHERE product_id = {product_id}"
                cursor.execute(check_product_query)
                result = cursor.fetchone()

                if result:
                    delete_query = f"DELETE FROM menus WHERE product_id = {product_id}"
                    cursor.execute(delete_query)
                    db.commit()
                    print("Produk berhasil dihapus.")
                else:
                    print("ID produk tidak ditemukan. Harap masukkan ID produk yang valid.")

                choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk menghapus produk lain :")
                if choice.lower() == 'exit':
                    print("Keluar dari Hapus Produk.")
                    break
            except ValueError:
                print("Harap masukkan nilai numerik yang valid untuk ID produk.")
            except Exception as e:
                print("Error:", e)

    #fungsi untuk menampilkan pembelian customer
    def displayorder():
        try:
            query = """
            SELECT ph.purchase_id, cc.username AS customer_name, pr.product_name, pm.total_amount, pm.payment_proof, pm.status, DATE_FORMAT(ph.purchase_date, '%Y-%m-%d %H:%i:%s') AS purchase_date
            FROM purchase_history ph
            JOIN payments pm ON ph.payment_id = pm.payment_id
            JOIN menus m ON ph.product_id = pr.product_id
            JOIN customer cc ON pm.customer_id = cc.id
            """

            cursor.execute(query)
            data = cursor.fetchall()

            if data:
                headers = ["ID", "Nama Customer", "Nama Produk", "Total", "Bukti Pembayaran", "Status", "Tanggal Pembelian"]

                print("Riwayat Pembelian Customer".center(120))
                print(tabulate(data, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

            else:
                print("Tidak ada riwayat pembelian.")

        except Exception as e:
            print("Error:", e)

    #fungsi untuk mengedit status pembelian customer
    def edit_purchase_status():
        while True:
            try:
                purchase_id = int(input("Masukkan ID pembelian untuk memperbarui status :"))
                new_status = input("Masukkan status baru :")

                check_purchase_query = f"SELECT * FROM purchase_history WHERE purchase_id = {purchase_id}"
                cursor.execute(check_purchase_query)
                result = cursor.fetchone()

                if result:
                    update_query = f"UPDATE payments pm \
                                    JOIN purchase_history ph ON pm.payment_id = ph.payment_id \
                                    SET pm.status = '{new_status}' \
                                    WHERE ph.purchase_id = {purchase_id}"

                    cursor.execute(update_query)
                    db.commit()
                    print("Status berhasil diperbarui.")
                else:
                    print("ID pembelian tidak ditemukan. Harap masukkan ID pembelian yang valid.")

                choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk memperbarui status lain :")
                if choice.lower() == 'exit':
                    print("Keluar dari perbarui status.")
                    break
            except ValueError:
                print("Harap masukkan nilai numerik yang valid untuk ID pembelian.")
            except Exception as e:
                print("Error:", e)

    #fungsi untuk logout admin
    def logout():
        db.close()
        print("Berhasil logout!")

    #fungsi untuk pilihan menu kategori
    def kategoriMenu():
        print("=" * 132)
        print("MENU KATEGORI".center(132))
        print("=" * 132)
        print("  Silahkan pilih dari opsi berikut :")
        print("1. Tampilkan Kategori               ")
        print("2. Tambah Kategori                  ")
        print("3. Edit  Kategori                   ")
        print("4. Hapus Kategori                   ")
        print("5. Kembali ke Main Menu             ")
        print("=" * 132)

        choice = int(input("Harap masukkan pilihan anda :"))
        if choice == 1:
            adminDisplayKategori()
            print("-" * 132)
            kategoriMenu()
        elif choice == 2:
            addKategori()
            print("-" * 132)
            kategoriMenu()
        elif choice == 3:
            adminDisplayKategori()
            print("-" * 132)
            editKategori()
            print("-" * 132)
            kategoriMenu()
        elif choice == 4:
            adminDisplayKategori()
            print("-" * 132)
            removeKategori()
            print("-" * 132)
            kategoriMenu()
        elif choice == 5:
            adminChoice()
        else:
            print("\nPilihan tidak valid. Harap masukkan pilihan yang valid!")
            kategoriMenu()

    #fungsi untuk pilihan menu produk
    def produkMenu():
        print("=" * 132)
        print("MENU PRODUK".center(132))
        print("=" * 132)
        print("  Silahkan pilih dari opsi berikut :")
        print("1. Tampilkan Produk                 ")
        print("2. Tambah Produk                    ")
        print("3. Edit Produk                      ")
        print("4. Hapus Produk                     ")
        print("5. Kembali ke Main Menu             ")
        print("=" * 132)

        choice = int(input("Harap masukkan pilihan anda :"))
        if choice == 1:
            adminDisplayProducts()
            print("-" * 132)
            produkMenu()
        elif choice == 2:
            addProduct()
            print("-" * 132)
            produkMenu()
        elif choice == 3:
            adminDisplayProducts()
            print("-" * 132)
            editProduct()
            print("-" * 132)
            produkMenu()
        elif choice == 4:
            adminDisplayProducts()
            print("-" * 132)
            removeProduct()
            print("-" * 132)
            produkMenu()
        elif choice == 5:
            adminChoice()
        else:
            print("\nPilihan tidak valid. Harap masukkan pilihan yang valid")
            print("-" * 132)
            produkMenu()

    #fungsi untuk pilihan menu customer
    def customerMenu():
        print("=" * 132)
        print("MENU CUSTOMER".center(132))
        print("=" * 132)
        print("  Silahkan pilih dari opsi berikut :")
        print("1. Tampilkan Pembelian Customer     ")
        print("2. Ubah Status Pembelian            ")
        print("3. Kembali ke Main Menu             ")
        print("=" * 132)

        choice = int(input("Harap masukkan pilihan anda :"))
        if choice == 1:
            displayorder()
            customerMenu()
        elif choice == 2:
            displayorder()
            edit_purchase_status()
            print("-" * 132)
            customerMenu()
        elif choice == 3:
            adminChoice()
        else:
            print("\nPilihan tidak valid. Harap masukkan pilihan yang valid!")
            print("-" * 132)
            customerMenu()

    #fungsi menu utama admin/panel admin
    def adminChoice():
        print("=" * 132)
        print("PANEL ADMIN".center(132))
        print("=" * 132)
        print("  Silahkan pilih dari opsi berikut :")
        print("1. Kelola Kategori Produk           ")
        print("2. Kelola Produk                    ")
        print("3. Akses Tindakan Pelanggan         ")
        print("4. Keluar Panel Admin               ")
        print("=" * 132)

        choice = int(input("Harap masukkan pilihan anda :"))
        if choice == 1:
            kategoriMenu()
        elif choice == 2:
            produkMenu()
        elif choice == 3:
            customerMenu()
        elif choice == 4:
            logout()
        else:
            print("\nPilihan tidak valid. Harap masukkan pilihan yang valid!")
            print("\n*\n")
            adminChoice()

    #fungsi untuk memulai siklus login admin
    def start():
        while True:  
            adminLogin()
            choice = input("Ketik 'exit' untuk keluar, atau tekan Enter untuk login kembali :")
            if choice.lower() == 'exit':
                print("Keluar program...")
                break  


    start()


#fungsi untuk login customer
def custStart():
    displayMenuForCustomer()

    #fungsi untuk menu utama customer
    def displayMenuForCustomer(customer_id):
        while True:
            try:
                print("=" * 132)
                print("  Silahkan pilih tindakan anda :")
                print("1. Lihat riwayat pembelian")
                print("2. Order                ")
                print("3. Logout                 ")
                print("=" * 132)

                action_choice = input("Masukkan pilihan anda (1 / 2 / 3):")

                if action_choice == '1':
                    viewOrderHistory(customer_id)
                    break 
                elif action_choice == '2':
                    displayCategories("categories", customer_id)
                    break  
                elif action_choice == '3': 
                    print("Logout...")
                    return  
                else:
                    print("Pilihan tidak valid. Harap masukkan 1, 2, atau 3.")

            except Exception as e:
                print("Error:", e)

    #fungsi untuk menampilkan kategori
    def displayCategories(categories, customer_id):
        while True:
            try:
                query = f"SELECT * FROM {categories}"
                cursor.execute(query)
                category = cursor.fetchall()
                
                if category:
                    headers = ["ID", "Nama Kategori"]
                
                    print("Kategori".center(30))
                    print(tabulate(category, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))
            
                    chosen_category_id = int(input("Masukkan ID kategori untuk melihat produk :"))
                
                    valid_category_ids = [categories[0] for categories in category]
                    if chosen_category_id in valid_category_ids:
                        displayProducts(chosen_category_id, customer_id)
                        break
                    else:
                        print("ID kategori tidak valid. Harap masukkan ID yang valid.")
                else:
                    print("Tidak ada kategori yang tersedia.")

            except ValueError:
                print("Input tidak valid. Harap masukkan ID kategori yang valid.")
            except Exception as e:
                print("Error:", e)

    #fungsi untuk menampilkan produk
    def displayProducts(category_id, customer_id):
        try:
            query = f"SELECT * FROM menus WHERE category_id = {category_id}"
            cursor.execute(query)
            products = cursor.fetchall()

            if products:
                headers = ["ID", "Nama Produk", "Harga Produk", "Kategori"]
            
                print("List Produk".center(60))
                print(tabulate(products, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

                while True:
                    order_choice = input("Ketik 'order' untuk membuat pesanan atau 'back' untuk kembali ke main menu : ")
                    if order_choice.lower() == 'order':
                        valid_product_ids = [product[0] for product in products]
                        try:
                            product_id = int(input("Masukkan ID produk : "))

                            if product_id in valid_product_ids:
                                quantity = int(input("Jumlah pembelian : "))
                                placeOrder(customer_id, product_id, quantity)
                                break
                            else:
                                print("ID produk tidak valid. Masukkan ID yang valid.")
                        except ValueError:
                            print("Input tidak valid. Harap masukkan ID produk dan jumlah yang benar.")
                    elif order_choice.lower() == 'back':
                        displayMenuForCustomer(customer_id)
                        break
                    else:
                        print("Pilihan tidak valid. Harap ketik 'order' atau 'back'.")
            else:
                print("Tidak ada produk dalam kategori ini.")

        except ValueError:
            print("Input tidak valid. Harap masukkan nilai yang valid.")
        except Exception as e:
            print("Error:", e)

    #fungsi untuk membuat pesanan
    def placeOrder(customer_id, product_id, quantity):
        try:
            cursor.execute(f"SELECT price FROM menus WHERE product_id = {product_id}")
            price = cursor.fetchone()[0]
            total_price = price * quantity
            checkout(customer_id, total_price, product_id, quantity) 
        except Exception as e:
            print("Error:", e)

    #fungsi untuk membuat pembayaran
    def checkout(customer_id, total_price, product_id, quantity):
        try:
            print("Total anda yaitu :", total_price)
            print("-" * 132)
            while True:
                payment_choice = input("Ketik 'pay' untuk membuat pembayaran atau 'cancel' untuk membatalkan :")
                if payment_choice.lower() == 'pay':
                    print("-" * 132)
                    bank_number = "1234-5678-9012"
                    print(f"Harap transfer total pembayaran ke akun bank berikut : {bank_number}")
                    print("Total anda yaitu :", total_price)
                    print("-" * 132)
                    input("Tekan Enter setelah transfer selesai...")
                    payment_confirmation(customer_id, total_price, product_id, quantity)
                    break
                elif payment_choice.lower() == 'cancel':
                    print("Pesanan dibatalkan")
                    displayMenuForCustomer(customer_id)
                    break
                else:
                    print("Pilihan tidak valid. Harap ketik 'pay' atau 'cancel'.")
        except Exception as e:
            print("Error:", e)

    #fungsi untuk konfirmasi pembayaran
    def payment_confirmation(customer_id, total_price, product_id, quantity):
        try:
            while True:
                payment_proof = input("Masukkan nomor bukti pembayaran(kosongkan untuk membatalkan) :")
                if payment_proof.strip() == "":
                    print("Bukti pembayaran diperlukan. Transaksi dibatalkan.")
                    displayMenuForCustomer(customer_id)
                    return

                confirmation_choice = input("Lanjutkan dengan konfirmasi pembayaran? (yes/no):").lower()
                if confirmation_choice == 'yes':
                    payment_query = f"INSERT INTO payments (customer_id, total_amount, payment_proof, status) " \
                                    f"VALUES ({customer_id}, {total_price}, '{payment_proof}', 'Menunggu Konfirmasi')"
                    cursor.execute(payment_query)
                    db.commit()

                    cursor.execute("SELECT LAST_INSERT_ID()")
                    payment_id = cursor.fetchone()[0]       
                    purchase_query = f"INSERT INTO purchase_history (payment_id, product_id, quantity) " \
                                    f"VALUES ({payment_id}, {product_id}, {quantity})"
                    cursor.execute(purchase_query)
                    db.commit()

                    print("Konfirmasi pembayaran diterima. Menunggu konfirmasi admin.")
                    viewOrderHistory(customer_id)
                    break
                elif confirmation_choice == 'no':
                    print("Konfirmasi pembayaran dibatalkan.")
                    displayMenuForCustomer(customer_id)
                    break
                else:
                    print("Pilihan tidak valid. Harap ketik 'yes' atau 'no'.")
        except Exception as e:
            print("Error:", e)

    #fungsi untuk melihat riwayat pembelian
    def viewOrderHistory(customer_id):
        try:
            query = f"SELECT m.menu, ph.quantity, p.total_amount, p.status, DATE_FORMAT(ph.purchase_date, '%Y-%m-%d %H:%i:%s') AS purchase_date " \
                    f"FROM purchase_history ph " \
                    f"INNER JOIN menus m ON ph.product_id = pr.product_id " \
                    f"INNER JOIN payments p ON ph.payment_id = p.payment_id " \
                    f"WHERE p.customer_id = {customer_id}"

            cursor.execute(query)
            purchase_history = cursor.fetchall()

            if purchase_history:
                headers = ["Nama Produk", "Jumlah", "Total Harga", "Status", "Tanggal Pembelian"]

                print("Riwayat Pembelian".center(80))
                print(tabulate(purchase_history, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))
            else:
                print("Riwayat pembelian tidak ditemukan.")

            while True:
                return_choice = input("Apakah anda ingin kembali ke Main Menu? (Yes/No): ")
                if return_choice.lower() == 'yes':
                    displayMenuForCustomer(customer_id)
                    break
                elif return_choice.lower() == 'no':
                    break
                else:
                    print("Pilihan tidak valid. Harap ketik 'Yes' atau 'No'.")

        except Exception as e:
            print("Error:", e)
                
    #fungsi untuk memulai siklus login customer
    def start():
        while True:
            login_regist()
            choice = input("Ketik 'exit' untuk keluar program, atau tekan Enter untuk login/mendaftar kembali :")
            if choice.lower() == 'exit':
                print("Keluar program...")
                break
    
    start()


def kitchenStart():
    def kitchenLogin():
        print("Customer Purchase")
        try:
            query = """
            SELECT ph.purchase_id, cc.username AS customer_name, m.menu, pm.total_amount, DATE_FORMAT(ph.purchase_date, '%Y-%m-%d %H:%i:%s') AS purchase_date
            FROM purchase_history ph
            JOIN payments pm ON ph.payment_id = pm.payment_id
            JOIN menus m ON ph.product_id = m.product_id
            JOIN customer cc ON pm.customer_id = cc.id
            """

            cursor.execute(query)
            data = cursor.fetchall()

            if data:
                headers = ["ID", "Nama Customer", "Menu", "Total", "Tanggal"]

                print("Riwayat Pembelian Customer".center(120))
                print(tabulate(data, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

            else:
                print("Tidak ada riwayat pembelian.")

        except Exception as e:
            print("Error:", e)


    def start():
        while True:
            kitchenLogin()
            choice = input("Ketik 'exit' untuk keluar program, atau tekan Enter untuk login/mendaftar kembali :")
            if choice.lower() == 'exit':
                print("Keluar program...")
                break
    start()