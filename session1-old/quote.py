from database import Database

database = Database()


def add_quote(text, user):
    database.create_a_quote(text, user['id'])


def show_all_quotes():
     quotes = database.get_quotes()
     for quote in quotes:
         print(quote['quote'])


def show_my_quotes(user):
    quotes = database.get_quotes(user['id'])
    if len(quotes) == 0:
        print("you have not added any quotes yet ....")
    else:
        for quote in quotes:
            print(quote['quote'])

