import os
import json

if os.path.isfile("db.json"):
    print("db.json exists\nCODE 0 OK")
else:
    print("db.json doesn't exist\nCODE 1 ERROR\nCreating db file..")
    try:
        open("db.json", "w").close()
    except:
        print("db.json can't be created\nCODE 1 ERROR")
    print("db.json created\nCODE 0 OK")

class DatabaseInteraction:
    def __init__(self, db_file='db.json'):
        self.db_file = db_file
    
    def add_user(self, user_id, points, user_type):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        
        if user_id not in db_data:
            db_data[user_id] = {}
            db_data[user_id]["points"] = points
            db_data[user_id]["user_type"] = user_type
            with open(self.db_file, "w") as db:
                json.dump(db_data, db, indent=4)
        else:
            print("User already exists")
    
    def remove_user(self, user_id):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        if user_id in db_data:
            del db_data[user_id]
            with open(self.db_file, "w") as db:
                json.dump(db_data, db, indent=4)
        else:
            print("User doesn't exist")
    
    def get_user(self, user_id):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
                print(db_data)
        if user_id in db_data:
            return db_data[user_id]
        else:
            print("User doesn't exist")
    
    def get_user_points(self, user_id):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        if user_id in db_data:
            return db_data[user_id]["points"]
        else:
            print("User doesn't exist")
    
    def get_user_type(self, user_id):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        if user_id in db_data:
            return db_data[user_id]["user_type"]
        else:
            print("User doesn't exist")
    
    def set_user_points(self, user_id, points):
        with open(self.db_file, "r") as db:
            db_data = json.load(db)
        if user_id in db_data:
            db_data[user_id]["points"] = points
            with open(self.db_file, "w") as db:
                json.dump(db_data, db, indent=4)
        else:
            print("User doesn't exist")
    
    def set_user_type(self, user_id, user_type):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        if user_id in db_data:
            db_data[user_id]["user_type"] = user_type
            with open(self.db_file, "w") as db:
                json.dump(db_data, db, indent=4)
        else:
            print("User doesn't exist")
    
    def add_points(self, user_id, points):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        if user_id in db_data:
            db_data[user_id]["points"] += points
            with open(self.db_file, "w") as db:
                json.dump(db_data, db, indent=4)
        else:
            print("User doesn't exist")
    
    def remove_points(self, user_id, points):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        if user_id in db_data:
            if db_data[user_id]["points"] - points < 0:
                db_data[user_id]["points"] = 100
            else:
                db_data[user_id]["points"] -= points
            with open(self.db_file, "w") as db:
                json.dump(db_data, db, indent=4)
        else:
            print("User doesn't exist")
    
    def get_user_profile(self, user_id):
        db_data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as db:
                db_data = json.load(db)
        if user_id in db_data:
            return db_data[user_id]
        else:
            print("User doesn't exist")
