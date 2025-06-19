from database import Database

database = Database()


def add_quote(text, user):
    database.create_a_quote(text, user['id'])


def show_quotes_table(quotes, type):
    print(f"{type + ' QUOTES':^80}")
    print(f"|{'id':^40}|{'quote':<50}|")
    for quote in quotes:
        print(f"|{quote['id']:^40}|{quote['quote']:<50}")


def show_all_quotes():
    quotes = database.get_quotes()
    show_quotes_table(quotes, "ALL")


def show_liked_quotes(user):
    # find the user's liked quote ids
    all_liked_quotes = database.get_my_liked_quotes(user['id'])

    # get all quotes ids
    ids = list(map(lambda q: q['quote_id'], all_liked_quotes))

    # find the quotes with quote id
    quotes = database.get_quotes_by_ids(ids)

    if len(quotes) == 0:
        print("you have not liked any quotes yet ....")
    else:
        show_quotes_table(quotes, "LIKED")


def show_my_quotes(user):
    quotes = database.get_quotes(user['id'])
    if len(quotes) == 0:
        print("you have not added any quotes yet ....")
    else:
        show_quotes_table(quotes, "MY")


def like_quote(quote_id, user):
    database.like_quote(quote_id, user['id'])


def unlike_quote(quote_id, user):
    database.unlike_quote(quote_id, user['id'])
