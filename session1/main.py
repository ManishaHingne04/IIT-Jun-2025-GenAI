from user import sign_up, sign_in
from quote import add_quote, show_all_quotes, show_my_quotes, like_quote, show_liked_quotes, unlike_quote

# user login status
current_user = None


def show_menu():
    choice = 0

    print("")

    def show_menu_before_authentication():
        print("Welcome to the hackathon application")
        print("0. exit")
        print("1. sign up")
        print("2. sing in")

    def show_menu_after_authentication():
        print(f"Welcome {current_user['firstName']}, to the hackathon application")
        print("0. sign out")
        print("1. all quotes")
        print("2. my quotes")
        print("3. liked quotes")
        print("4. add quote")
        print("5. like quote")
        print("6. unlike quote")

    # user has not logged in yet
    if current_user is None:
        show_menu_before_authentication()
    else:
        show_menu_after_authentication()

    choice = int(input("enter your choice: "))
    return choice


while True:
    choice = show_menu()
    if current_user is None:
        if choice == 1:
            print("please sign up with following information")
            first_name = input("enter first name: ")
            last_name = input("enter last name: ")
            email = input("enter email: ")
            password = input("enter password: ")
            phone = input("enter phone: ")
            address = input("enter address: ")

            sign_up(first_name, last_name, email, password, address, phone)
        elif choice == 2:
            email = input("enter email: ")
            password = input("enter password: ")

            # if user found then let user logged in
            # if current_user is not None then we will assume that
            # the user is logged in
            current_user = sign_in(email, password)
        else:
            break
    else:
        if choice == 0:
            # log out user means just reset the current_user
            current_user = None
        elif choice == 1:
            show_all_quotes()
        elif choice == 2:
            show_my_quotes(current_user)
        elif choice == 3:
            show_liked_quotes(current_user)
        elif choice == 4:
            text = input("enter your quote: ")
            add_quote(text, current_user)
        elif choice == 5:
            quote_id = input("enter quote id: ")
            like_quote(quote_id, current_user)
        elif choice == 6:
            quote_id = input("enter quote id: ")
            unlike_quote(quote_id, current_user)
        else:
            break

