import nbtlib
import anvil
import os

world_input = input("Enter the path of your minecraft world: ")

item_id = input("Enter the Item ID you want to find, (e.g. minecraft:diamond): ")



print("\nSearching player Inventories")
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
                    print(f"Found {count}x {item_id} in {filename}'s Ender Chest at {pos_tuple}")

            if not found:
                print(f"No {item_id} found in {filename}")

        except Exception as e:
            print(f"Error reading {filename}: {e}")


print("\nSearching World Containers (chest, barrels, etc.)")
region_path = os.path.join(world_input, "region")

for filename in os.listdir(region_path):
    if filename.endswith(".mca"):
        filepath = os.path.join(region_path, filename)
        try:
            region = anvil.Region.from_file(filepath)

            for x in range(32):
                for z in range(32):
                    try:
                        chunk = region.get_chunk(x, z)

                        for tile in chunk.tile_entities:
                            if "Items" in tile:
                                for item in tile["Items"]:
                                    if item["id"] == item_id:
                                        coords = (tile["x"].value, tile["y"].value, tile["z"].value)
                                        count = int(item["Count"].value)
                                        print(f"Found {count}x {item_id} in container at {coords}")
                    except Exception:
                        pass
        except Exception:
            print(f"Error reading region {filename}: {e}")
    