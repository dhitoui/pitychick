# Fungsi login sebagai costumer
def custLogin():
    print("Login as Costumer")
    username = input("Input Username: ")
    pess = getpass("Input Password")

# Fungsi costumer
def custMenu():
    print("What We Can Help You?")
    print("1. View Orders History")
    print("2. Want to Buy")
    print("3. Logout")

    pilih = int(input("Choose Main Menu (1/2/3): "))
    if pilih == 1:
        viewOrders()
    elif pilih == 2:
        wtb()
    elif pilih == 3:
        logout()
    else:
        print("Please input a number between 1 to 3!")
    custLogin()

def viewOrders():
    print("")

def wtb():
    print("What Do You Want To?")
    print("1. See The Menu")
    print("2. Place to Orders")


    
    def orders():
        print("What we can get for you?")
        print("1. Food")
        print("2. Drink")
        print("3. Snack")

        pilih = int(input("Choose the number (1/2/3): "))
        # if pilih == 1:
        #     chicken = input("Which part of the chicken would you like: ")
        #     lots = int(input("How much you want to orders: "))
        #     sauce = input("Would you like to add sauce? (yes/no): ")
        #     if sauce == 'yes':
        #         print("1. Blackpaper")
        #         print("2. Spicy Cheese")
        #         print("3. Spicy Mayo")
        #         print("4. Brown Creamy")
        #         sauce2 = int(input("Choose your sauce: "))
        #         print(f"Your orders is {lots} {chicken} with {sauce}")
        #     else:
        #         print(f"Your orders is {lots} {chicken} without sauce.")
                
            
    
    try:
        choose = int(input("Choose the number (1/2): "))
        if choose == 1:
            displayMenu()
        elif choose == 2:
            orders()
        else:
            print("Sorry, we don't have option for that command.")
    except ValueError:
        print("You can only input numbers.")

def custLogout():