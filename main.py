import nbtlib
import anvil
import os

world_input = input("Enter the path of your minecraft world: ")

item_id = input("Enter the Item ID you want to find, (e.g. minecraft:diamond): ")



playerdata_path = os.path.join(world_input, "playerdata")

for filename in os.listdir(playerdata_path):
    if filename.endswith(".dat"):
        filepath = os.path.join(playerdata_path, filename)
        try:
            nbt = nbtlib.load(filepath)

            #Player Position
            pos = nbt["Pos"]
            pos_tuple = (float(pos[0]), float(pos[1]), float(pos[2]))

            found = False

            for item in nbt["Inventory"]:
                if item["id"] == item_id:
                    found = True
                    count = int(item["Count"])
                    print(f"Found {count}x {item_id} in {filename}'s Inventory at {pos_tuple}")

            for item in nbt.get("EnderItems", []):
                if item["id"] == item_id:
                    found = True
                    count = int(item["Count"])
                    print(f"Found {count}x {item_id} in {filename}'s Ender Cheast at {pos_tuple}")

            if not found:
                print(f"No {item_id} found in {filename}")

        except Exception as e:
            print("Errpr reading {filename}: {e}")