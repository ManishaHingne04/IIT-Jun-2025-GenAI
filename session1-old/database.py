import json
import uuid


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
        info = self.read_data("quotes.json")
        quotes_array = json.loads(info)

        if user_id is None:
            # return all quotes
            return quotes_array

        return list(filter(lambda q: q['user_id'] == user_id, quotes_array))

    def create_a_quote(self, quote, user_id):
        info = self.read_data("quotes.json")

        # read the contents and convert them into list of dictionary
        quotes_array = json.loads(info)

        # add a new quote
        quotes_array.append({
            "quote": quote,
            "user_id": user_id
        })

        self.write_data(json.dumps(quotes_array), "quotes.json")

    def store_user_data(self, data, file_name):
        # read the existing users data
        info = self.read_data("users.json")

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
        self.write_data(json.dumps(user_array), "users.json")

    def get_user_with_email(self, email, password):
        info = self.read_data("users.json")

        user_array = json.loads(info)
        for user in user_array:
            if (user['email'] == email) and (user['password'] == password):
                print("welcome to the application")
                return user
        else:
            print("user does not exist, please try with right email and password")
            return None

