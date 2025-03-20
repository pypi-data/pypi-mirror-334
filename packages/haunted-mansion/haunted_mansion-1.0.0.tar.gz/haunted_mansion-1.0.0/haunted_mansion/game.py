import random
from colorama import Fore, Back, Style, init
import emoji
import json
import os

# Initialize colorama
init(autoreset=True)

class Game:
    def __init__(self, title):
        self.title = title
        self.rooms = {}
        self.inventory = []
        self.current_room = None
        self.player_health = 100
        self.player_experience = 0
        self.player_level = 1
        self.quests = []
        self.status_effects = []
        self.quests_completed = {
            "Find the ring": False,
            "Defeat the ghost": False,
            "Find the spellbook": False
        }
        # Assuming the save file is located in the assets folder
        self.save_directory = "assets"
        self.save_file = os.path.join(self.save_directory, "save_game.json")

    def add_room(self, room_name, description):
        self.rooms[room_name] = {"description": description, "items": [], "interactions": [], "npc": None}

    def add_item(self, item_name, description, room_name):
        if room_name in self.rooms:
            self.rooms[room_name]["items"].append({"name": item_name, "description": description})

    def add_interaction(self, room_name, interaction):
        if room_name in self.rooms:
            self.rooms[room_name]["interactions"].append(interaction)

    def add_npc(self, room_name, npc_name, npc_dialogue, npc_quests=None):
        if room_name in self.rooms:
            self.rooms[room_name]["npc"] = {"name": npc_name, "dialogue": npc_dialogue, "quests": npc_quests or []}

    def show_room(self, room_name):
        room = self.rooms.get(room_name)
        if room:
            print(f"\n{Fore.CYAN}{'='*40}")
            print(f"{Fore.YELLOW}You are in the {room_name}: {Fore.WHITE}{room['description']}")
            if room["items"]:
                print(f"\n{Fore.GREEN}Items here:")
                for item in room["items"]:
                    print(f"  - {Fore.MAGENTA}{item['name']}: {Fore.WHITE}{item['description']}")
            if room["interactions"]:
                print(f"\n{Fore.BLUE}Interactions:")
                for interaction in room["interactions"]:
                    print(f"  - {interaction}")
            if room["npc"]:
                npc = room["npc"]
                print(f"\n{Fore.RED}{'-'*40}")
                print(f"There is an NPC here: {Fore.LIGHTYELLOW_EX}{npc['name']}")
                print(f"NPC Dialogue: {Fore.WHITE}{npc['dialogue']}")
                if npc["quests"]:
                    print(f"\n{Fore.CYAN}Quests available:")
                    for quest in npc["quests"]:
                        print(f"  - {Fore.GREEN}{quest}")
            print(f"{Fore.CYAN}{'='*40}")
        else:
            print("This room doesn't exist.")

    def pick_up_item(self, item_name):
        for room in self.rooms.values():
            for item in room["items"]:
                if item["name"].lower() == item_name.lower():
                    self.inventory.append(item)
                    room["items"].remove(item)
                    print(f"\n{Fore.GREEN}You have picked up: {Fore.MAGENTA}{item_name} {emoji.emojize(':key:')}")
                    # Check if the player picked up the ring
                    if item_name.lower() == "ring":
                        self.quests_completed["Find the ring"] = True
                        print(f"{Fore.CYAN}You have found the lost ring! Quest completed!")
                    elif item_name.lower() == "spellbook":
                        self.quests_completed["Find the spellbook"] = True
                        print(f"{Fore.CYAN}You have found the spellbook! Quest completed!")
                    return
        print(f"{Fore.RED}Item '{item_name}' not found.")

    def show_inventory(self):
        print(f"\n{Fore.GREEN}Inventory:")
        if not self.inventory:
            print(f"{Fore.YELLOW}Your inventory is empty.")
        for item in self.inventory:
            print(f"  - {Fore.MAGENTA}{item['name']}: {Fore.WHITE}{item['description']}")

    def interact(self):
        if self.current_room:
            room = self.rooms.get(self.current_room)
            if room["interactions"]:
                print(f"\n{Fore.BLUE}You interact with:")
                for interaction in room["interactions"]:
                    print(f"  - {interaction}")
                print(f"{Fore.CYAN}You feel something strange, perhaps something more will happen later.")
            else:
                print(f"{Fore.YELLOW}There's nothing to interact with here.")
        else:
            print(f"{Fore.RED}You need to be in a room to interact.")

    def examine_item(self, item_name):
        found = False
        for item in self.inventory:
            if item_name.lower() == item["name"].lower():
                print(f"\n{Fore.GREEN}Examine {item['name']}: {Fore.WHITE}{item['description']}")
                found = True
                break
        if not found:
            print(f"{Fore.RED}Item '{item_name}' not found in your inventory.")

    def use_item(self, item_name):
        found = False
        for item in self.inventory:
            if item_name.lower() == item["name"].lower():
                # Example usage: "Key" can be used to open a door (add more logic for other items)
                if item_name.lower() == "key":
                    print(f"{Fore.GREEN}You use the {item_name} to open a hidden door!{emoji.emojize(':door:')}")
                    self.inventory.remove(item)  # Use the key and remove it from inventory
                elif item_name.lower() == "potion":
                    self.player_health += 20
                    if self.player_health > 100:
                        self.player_health = 100
                    print(f"{Fore.GREEN}You drank the potion and restored 20 health!{emoji.emojize(':green_heart:')}")
                    self.inventory.remove(item)
                else:
                    print(f"{Fore.YELLOW}You can't use the {item_name} here.")
                found = True
                break
        if not found:
            print(f"{Fore.RED}Item '{item_name}' not found in your inventory.")

    def talk_to_npc(self):
        if self.current_room:
            room = self.rooms.get(self.current_room)
            if room["npc"]:
                npc = room["npc"]
                print(f"\n{Fore.RED}Talking to {npc['name']}: {npc['dialogue']}")
                if npc["quests"]:
                    print(f"{Fore.YELLOW}Available quests:")
                    for quest in npc["quests"]:
                        print(f"  - {Fore.GREEN}{quest}")
                    # Check if the player has completed the quest
                    if self.quests_completed["Find the ring"]:
                        print(f"{Fore.GREEN}Thank you for finding my ring! Here is your reward.")
                        npc['dialogue'] = "Thank you for finding my ring!"
            else:
                print(f"{Fore.RED}There's no NPC to talk to here.")
        else:
            print(f"{Fore.RED}You need to be in a room to talk to an NPC.")

    def combat(self):
        print(f"\n{Fore.RED}A wild enemy appears!{emoji.emojize(':dragon:')}\n")
        enemy_health = 50 + (self.player_level * 5)  # Scale enemy health with player level
        while enemy_health > 0 and self.player_health > 0:
            print(f"Your health: {self.player_health}, Enemy health: {enemy_health}")
            action = input(f"{Fore.YELLOW}Choose an action: (a) Attack, (r) Run: ").lower()
            if action == "a":
                damage = random.randint(5, 15)
                enemy_health -= damage
                print(f"{Fore.CYAN}You attacked the enemy for {damage} damage!")
            elif action == "r":
                print(f"{Fore.GREEN}You ran away from the battle.")
                break
            else:
                print(f"{Fore.RED}Invalid action. Try again.")
                continue

            if enemy_health > 0:
                enemy_damage = random.randint(5, 15)
                self.player_health -= enemy_damage
                print(f"{Fore.RED}The enemy attacks you for {enemy_damage} damage!")

        if self.player_health <= 0:
            print(f"\n{Fore.RED}You have been defeated!{emoji.emojize(':pensive_face:')}")
        elif enemy_health <= 0:
            print(f"\n{Fore.GREEN}You have defeated the enemy!{emoji.emojize(':trophy:')}")
            self.gain_experience(10)

    def gain_experience(self, points):
        self.player_experience += points
        print(f"\n{Fore.YELLOW}You gained {points} experience points.")
        if self.player_experience >= 100:
            self.level_up()

    def level_up(self):
        self.player_level += 1
        self.player_experience = 0
        self.player_health = 100  # Restore health on level-up
        print(f"\n{Fore.CYAN}Congratulations! You've leveled up to level {self.player_level}!{emoji.emojize(':partying_face:')}")
        print(f"{Fore.GREEN}Your health has been restored.")

    def show_status(self):
        print(f"\n{Fore.YELLOW}Player Status:")
        print(f"{Fore.GREEN}Health: {self.player_health}")
        print(f"{Fore.CYAN}Level: {self.player_level}")
        print(f"{Fore.YELLOW}Experience: {self.player_experience}/100")
        print(f"{Fore.RED}Status Effects: {', '.join(self.status_effects) if self.status_effects else 'None'}")

    def save_game(self):
        game_data = {
            "inventory": self.inventory,
            "current_room": self.current_room,
            "player_health": self.player_health,
            "player_experience": self.player_experience,
            "player_level": self.player_level,
            "quests_completed": self.quests_completed
        }
        # Save the game data to the file in the assets directory
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        with open(self.save_file, "w") as file:
            json.dump(game_data, file)
        print(f"\n{Fore.GREEN}Game saved successfully!{emoji.emojize(':floppy_disk:')}")

    def load_game(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as file:
                game_data = json.load(file)
            self.inventory = game_data["inventory"]
            self.current_room = game_data["current_room"]
            self.player_health = game_data["player_health"]
            self.player_experience = game_data["player_experience"]
            self.player_level = game_data["player_level"]
            self.quests_completed = game_data["quests_completed"]
            print(f"\n{Fore.GREEN}Game loaded successfully!{emoji.emojize(':open_file_folder:')}")
        else:
            print(f"\n{Fore.RED}No saved game found.")

    # (Previous code remains the same until the start method)

    def start(self):
        print(f"\n{Fore.CYAN}{'='*40}\n{Fore.MAGENTA}Welcome to {self.title}! 🏠\n{Fore.CYAN}{'='*40}")
        print(f"{Fore.YELLOW}Type 'help' for commands.\n")
        print(f"{Fore.GREEN}Hints: Start in the Living Room, pick up the Key 🔑, and talk to the Old Man 👴 to get your first quest!")

        while True:
            print(f"\n{Fore.GREEN}Current room: {self.current_room if self.current_room else 'None'}")
            command = input(f"{Fore.YELLOW}What do you want to do? ").lower()

            if command == "help":
                print(f"\n{Fore.CYAN}Commands: ")
                print(f"- 'look' 👀 to see the current room.")
                print(f"- 'go [room_name]' 🚶 to enter a room.")
                print(f"- 'pick up [item_name]' 🖐️ to pick up an item.")
                print(f"- 'inventory' 🎒 to check your inventory.")
                print(f"- 'combat' ⚔️ to start a combat.")
                print(f"- 'status' ❤️ to view your player status.")
                print(f"- 'interact' 🔍 to interact with objects in the room.")
                print(f"- 'examine [item_name]' 🔎 to examine an item in your inventory.")
                print(f"- 'use [item_name]' 🛠️ to use an item from your inventory.")
                print(f"- 'talk' 🗣️ to talk to NPCs.")
                print(f"- 'save' 💾 to save your progress.")
                print(f"- 'load' 📂 to load your progress.")
                print(f"- 'quit' 🚪 to exit the game.")
                print(f"\n{Fore.YELLOW}There are {len(self.rooms)} rooms in this game:")  # Shows list of rooms
                for room_name in self.rooms:
                    print(f"  - {Fore.GREEN}{room_name}")

            # (Rest of the code remains the same)
            
            elif command.startswith("go "):
                room_name = command[3:].strip()  # Strip any extra spaces
                # Use case-insensitive matching for room names
                room_name_lower = room_name.lower()
                found_room = None
                for room in self.rooms:
                    if room.lower() == room_name_lower:
                        found_room = room
                        break
                if found_room:
                    self.current_room = found_room
                    self.show_room(found_room)
                else:
                    print(f"{Fore.RED}Room not found.")

            elif command == "look":
                if self.current_room:
                    self.show_room(self.current_room)
                else:
                    print(f"{Fore.RED}You haven't entered any room yet.")

            elif command.startswith("pick up "):
                item_name = command[8:].strip()
                self.pick_up_item(item_name)

            elif command == "inventory":
                self.show_inventory()

            elif command == "interact":
                self.interact()

            elif command.startswith("examine "):
                item_name = command[8:].strip()
                self.examine_item(item_name)

            elif command.startswith("use "):
                item_name = command[4:].strip()
                self.use_item(item_name)

            elif command == "talk":
                self.talk_to_npc()

            elif command == "combat":
                self.combat()

            elif command == "status":
                self.show_status()

            elif command == "save":
                self.save_game()

            elif command == "load":
                self.load_game()

            elif command == "quit":
                print(f"\n{Fore.MAGENTA}Exiting the game...{emoji.emojize(':wave:')}\n")
                break

            else:
                print(f"{Fore.RED}Unknown command. Type 'help' for a list of commands.")

# Create a game world
def main():
    game = Game("The Haunted Mansion")

    # Add rooms
    game.add_room("Living Room", "A dark, dusty room with old furniture.")
    game.add_room("Kitchen", "You can smell something strange here.")
    game.add_room("Basement", "A cold, damp place with eerie noises.")
    game.add_room("Library", "Rows of ancient books line the walls.")
    game.add_room("Attic", "A dusty, cramped space filled with old belongings.")

    # Add items and interactions
    game.add_item("Key", "A rusty old key", "Living Room")
    game.add_item("Ring", "A shiny gold ring", "Kitchen")  # The ring is in the Kitchen
    game.add_item("Knife", "A sharp kitchen knife", "Kitchen")
    game.add_item("Flashlight", "A battery-powered flashlight", "Basement")
    game.add_item("Spellbook", "An ancient book of spells", "Library")
    game.add_item("Potion", "A healing potion", "Attic")
    game.add_interaction("Living Room", "You see a strange painting on the wall.")
    game.add_interaction("Kitchen", "There is a strange smell coming from the fridge.")
    game.add_interaction("Basement", "You hear whispers in the dark.")
    game.add_interaction("Library", "A book falls off the shelf by itself.")
    game.add_interaction("Attic", "You find an old diary.")

    # Add NPCs with quests
    game.add_npc("Living Room", "Old Man", "I need help finding my lost ring.", ["Find the ring"])
    game.add_npc("Library", "Ghost", "Defeat me if you dare!", ["Defeat the ghost"])
    game.add_npc("Attic", "Witch", "Find my spellbook, and I'll reward you.", ["Find the spellbook"])

    # Start the game
    game.start()

if __name__ == "__main__":
    main()
