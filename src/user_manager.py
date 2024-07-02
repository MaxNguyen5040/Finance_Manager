import json

class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.user_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.users, f)

    def add_user(self, username, password):
        if username in self.users:
            raise ValueError('User already exists')
        self.users[username] = {'password': password, 'settings': {}}
        self.save_users()

    def authenticate_user(self, username, password):
        return self.users.get(username, {}).get('password') == password

    def get_user_settings(self, username):
        return self.users.get(username, {}).get('settings', {})

    def update_user_settings(self, username, settings):
        self.users[username]['settings'] = settings
        self.save_users()
