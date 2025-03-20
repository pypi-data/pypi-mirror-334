import json
import datetime
#I can't tell how to make unit tests for this stuff
class JsonHandle:
    def __init__(self, playername: str):
        try:
            with open('player_info.json', 'r') as openfile: self.player_info_object = json.load(openfile)
            self.add_player_if_unique(playername)
        except:
            newfile = {"players": []}
            with open("player_info.json", "w") as json_file:
                json.dump(newfile, json_file)

    def add_player_if_unique(self, playername: str):
        unique = True
        for i in range(len(self.player_info_object["players"])):
            if self.player_info_object["players"][i]["username"] == playername:
                unique = False
        if unique:
            self.player_info_object["players"].append({"username": playername, "gambling": "False"})
            json_object = json.dumps(self.player_info_object, indent=2) 
            with open("player_info.json", "w") as outfile: outfile.write(json_object)
        pass

    def add_roll(self, playername: str, die: str, roll: int, timestamp: datetime.datetime):
        index = self.calc_index(playername)
        try:
            self.player_info_object["players"][index]["rolls"].append({
            "die": die, 
            "roll": roll,
            "timestamp": timestamp
            })
        except:
            self.player_info_object["players"][index]["rolls"] = [{
            "die": die, 
            "roll": roll,
            "timestamp": timestamp
            }]
        json_object = json.dumps(self.player_info_object, indent=2) 
        with open("player_info.json", "w") as outfile: outfile.write(json_object)

    def calc_index(self, playername: str):
        for i in range(len(self.player_info_object["players"])):
            if self.player_info_object["players"][i]["username"] == playername: 
                return i
        else: return None

    def gambling(self, playername: str):
        index = self.calc_index(playername)
        return self.player_info_object["players"][index]["gambling"] == "True"

    def update_json(self, playername: str, gambling: bool):
        index = self.calc_index(playername)
        if (gambling != None):
            self.player_info_object["players"][index]["gambling"] = str(gambling)
        json_object = json.dumps(self.player_info_object, indent=2)
        with open("player_info.json", "w") as outfile: outfile.write(json_object)

    def get_rolls(self, playername: str):
        index = self.calc_index(playername)
        try:
            return self.player_info_object["players"][index]["rolls"]
        except:
            return None