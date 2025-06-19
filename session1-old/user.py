from database import Database


def sign_up(first_name, last_name, email, password, address, phone):
    user = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password,
        "address": address,
        "phone": phone
    }
    database = Database()
    database.store_user_data(user, "users.json")


def sign_in(email, password):
    database = Database()
    return database.get_user_with_email(email, password)