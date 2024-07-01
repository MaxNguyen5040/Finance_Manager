import bcrypt
import csv

class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file

    def create_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with open(self.user_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password.decode('utf-8')])

    def authenticate_user(self, username, password):
        with open(self.user_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                stored_username, stored_password = row
                if stored_username == username and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return True
        return False
