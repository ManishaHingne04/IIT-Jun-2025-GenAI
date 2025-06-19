import json
import uuid

COLLECTION_USER = "users.json"
COLLECTION_QUOTES = "quotes.json"
COLLECTION_LIKED_QUOTES = "liked_quotes.json"

class Database:
    def __init__(self):
        pass

    def write_data(self, data, file_name):
        # read the existing users data
        file = open(file_name, "w")
        file.write(data)
        file.close()

    def read_data(self, file_name):
        # read the existing users data
        file = open(file_name, "r")
        info = file.read()
        file.close()
        return info

    def get_quotes(self, user_id=None):
        info = self.read_data(COLLECTION_QUOTES )
        quotes_array = json.loads(info)

        if user_id is None:
            # return all quotes
            return quotes_array

        return list(filter(lambda q: q['user_id'] == user_id, quotes_array))

    def get_quotes_by_ids(self, quote_ids):
        info = self.read_data(COLLECTION_QUOTES )
        quotes_array = json.loads(info)
        return list(filter(lambda q: q['id'] in quote_ids, quotes_array))

    def get_my_liked_quotes(self, user_id):
        # reading all liked quotes
        info = self.read_data(COLLECTION_LIKED_QUOTES)
        liked_quotes_array = json.loads(info)

        # filter the quotes liked by the user
        return list(filter(lambda q: q['user_id'] == user_id, liked_quotes_array))

    def create_a_quote(self, quote, user_id):
        info = self.read_data(COLLECTION_QUOTES)

        # read the contents and convert them into list of dictionary
        quotes_array = json.loads(info)

        # add a new quote
        quotes_array.append({
            "quote": quote,
            "user_id": user_id,
            "id": f"{uuid.uuid1()}"
        })

        self.write_data(json.dumps(quotes_array), COLLECTION_QUOTES)

    def store_user_data(self, data, file_name):
        # read the existing users data
        info = self.read_data(COLLECTION_USER)

        # read the contents and convert them into list of dictionary
        user_array = json.loads(info)

        for user in user_array:
            if user['email'] == data['email']:
                print("email exists, please pass a different email")
                return

        # add a user_id before we store the user data
        # data["user_id"] = len(user_array) + 1
        data["id"] = uuid.uuid1().__str__()

        # append the user
        user_array.append(data)
        self.write_data(json.dumps(user_array), COLLECTION_USER)

    def get_user_with_email(self, email, password):
        info = self.read_data(COLLECTION_USER)

        user_array = json.loads(info)
        for user in user_array:
            if (user['email'] == email) and (user['password'] == password):
                print("welcome to the application")
                return user
        else:
            print("user does not exist, please try with right email and password")
            return None

    def like_quote(self, quote_id, user_id):
        # find if the quote is owned by user
        all_quotes = self.read_data(COLLECTION_QUOTES)
        array_all_quotes = json.loads(all_quotes)
        filter_quotes = lambda q: (q['id'] == quote_id) and (q['user_id'] == user_id)
        rows = list(filter(filter_quotes, array_all_quotes))
        if len(rows) == 1:
            print("YOU CAN NOT LIKE YOUR OWN QUOTES")
            return

        # check if user has already liked this quote
        all_liked_quotes = self.read_data(COLLECTION_LIKED_QUOTES)
        array_all_liked_quotes = json.loads(all_liked_quotes)
        filter_quotes = lambda q: (q['quote_id'] == quote_id) and (q['user_id'] == user_id)
        rows = list(filter(filter_quotes, array_all_liked_quotes))
        if len(rows) == 1:
            print("ARE YOU DRUNK? YOU ALREADY HAVE LIKED THIS QUOTE")
            return

        # like the quote
        info = self.read_data(COLLECTION_LIKED_QUOTES)
        array_liked_quotes = json.loads(info)

        new_like_info = {
            "user_id": user_id,
            "quote_id": quote_id
        }
        array_liked_quotes.append(new_like_info)
        self.write_data(json.dumps(array_liked_quotes), COLLECTION_LIKED_QUOTES)

    def unlike_quote(self, quote_id, user_id):
        # get all the quotes
        info = self.read_data(COLLECTION_LIKED_QUOTES)
        array_liked_quotes = json.loads(info)

        # remove the record whose user_id and quote_id is matching
        index = 0
        for quote in array_liked_quotes:
            if (quote['user_id'] == user_id) and (quote['quote_id'] == quote_id):
                array_liked_quotes.pop(index)
                break
            index += 1

        self.write_data(json.dumps(array_liked_quotes), COLLECTION_LIKED_QUOTES)