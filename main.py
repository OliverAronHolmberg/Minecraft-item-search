import nbtlib
import os

world_input = input("Enter the path of your minecraft world: ")

item_id = input("Enter the Item ID you want to find, (e.g. minecraft:diamond): ")



player_data = os.path.join(world_input, "playerdata")

for filename in os.listdir(player_data):
    