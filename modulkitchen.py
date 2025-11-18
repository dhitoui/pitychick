# Fungsi login sebagai orang dapur
def kitchenLogin():
    print("Login as Kitchen Person.")
    username = input("Input Username: ")
    password = getpass("Input Password: ")

# Fungsi orang dapur
def KitchenMenu():
    print("Kitchen's Main Menu")
    print("1. View Orders")
    print("2. Remove Orders")
    print("3. Logout")

    pilih = int(input("Choose menu (1/2/3): "))
    if pilih == 1:
        viewOrders()
    elif pilih == 2:
        removeOrders()
    else:
        logout()

def viewOrders():
    print("Category Menu")
    print("1. Food")
    print("2. Drink")
    print("3. Snack")

    def foodOption():
        print("")

    def drinkOption():
        print("")

    def snackOption():
        print("")

    try:
        menu_option = int(input("Choose Category (1/2/3): "))
        if menu_option == 1:
            foodOption()
        elif menu_option == 2:
            drinkOption()
        elif menu_option == 3: 
            snackOption()
        else:
            print("Sorry there no option for that.")
    except ValueError:
        print("Invalid. Input Can Only be Numbers!")


def removeOrders():
    print("1. Remove All Orders")
    print("2. Choose Orders to Remove")

    def removeAll():
        print("")

    def chooseRemove():
        print("")

    try:
        remove = int(input("Choose Between (1/2): "))
        if remove == 1:
            removeAll()
        elif remove == 2:
            chooseRemove()
        else:
            print("There's No Option.")
    except ValueError:
        print("Input Can Only be Numbers!")


def logout():