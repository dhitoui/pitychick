import mysql.connector
from getpass import getpass
import pandas as pd


#Fungsi supaya terkoneksi dengan database MySQL
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
def start():
    while True:
        userType = int(input("Login as:\n1. Admin\n2. Kitchen\n3.Customer\nSelect (1-3): "))
        if userType == 1:
            adminLogin()
            break
        if userType == 2:
            kitchenLogin()
            break
        if userType == 3:
            custLogin()
            break
        else:
            print("Invalid input! Input either 1 or 2.")

#Fungsi login sebagai admin
def adminLogin():
    try:
        print("Login as Admin:")
        username = input("Input username: ")
        password = getpass("Input password: ")

        if not db.is_connected(): 
            db.reconnect(attempts=1, delay=0)

        login_query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        cursor.execute(login_query, (username, password))
        result = cursor.fetchone()

        if result:
            adminMainMenu()
        else:
            print("Access denied. Identity was not found.")
    except Exception as e:
        print(e)

#Fungsi admin datang
def adminMainMenu():
    bannerCard()
    print("Admin's Main Menu")
    print("1. Manage Product Categories")
    print("2. Manage Products")
    print("3. Manage Customer's Purchase")
    print("4. Logout")
    index = int(input("Choose menu (1-4): "))
    if index == 1:
        manageCategory()
    if index == 2:
        manageProduct()
    if index == 3:
        custOrder()
    if index == 4:
        adminLogout()
    else:
        print("Invalid input! Please input a number between 1 to 4.\n")
        adminMainMenu()


def manageCategory():
    bannerCard()
    print("Manage Categories")
    print("1. Show Categories")
    print("2. Add Categories")
    print("3. Edit Categories")
    print("4. Delete Categories")
    print("5. Back to Main Menu")
    categoryMenu = int(input("Select menu (1-5): "))
    if categoryMenu == 1:
        showCategory()
        divider()
        manageCategory()
    if categoryMenu == 2:
        addCategory()
        divider()
        manageCategory()
    if categoryMenu == 3:
        editCategory()
        divider()
        manageCategory()
    if categoryMenu == 4:
        deleteCategory()
        divider()
        manageCategory()
    if categoryMenu == 5:
        adminMainMenu()
    else:
        print("Invalid input! Please input a number between 1 to 5.\n")
        manageCategory()


def showCategory():
    try:
            query = "SELECT * FROM category"
            cursor.execute(query)
            data = cursor.fetchall()
            data_frame = pd.DataFrame(data)
            header = ["ID", "Kategori"]
            print("Daftar Kategori".center(30))
            print(tabulate(data_frame, headers = header, tablefmt = "fancy_grid", showindex = False, numalign = 'center', stralign = 'center'))

    except Exception as e:
            print("Error:", e)


def manageProduct():
    bannerCard()
    print("Manage Products")
    print("1. Show Products")


def custOrder():
    bannerCard()
    print("Customer's Purchase")
    print("1. Show Transaction")


def adminLogout():




    