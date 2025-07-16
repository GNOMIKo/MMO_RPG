import json

class JsonDatabase:
    def __init__(self, filename='base.json'):
        self.filename = filename
        self.data = {}
        self.current_id = None

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_current_player(self, player_id):
        self.current_id = str(player_id)

    def get_current_player(self):
        return self.data.get(self.current_id, None)

    def update_current_player(self, player_dict):
        self.data[self.current_id] = player_dict
        self.save()

    def create_player(self, player_id, player_dict):
        self.data[str(player_id)] = player_dict
        self.save()

    def list_players(self):
        return {pid: pdata['username'] for pid, pdata in self.data.items()}

def printd(string):
    print(f'\033[1;32m!!!DevInfo!!!\n{string}\n!!!DevInfo!!!\033[0m')