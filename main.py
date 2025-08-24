import os
import zlib
from io import BytesIO
import nbtlib
import json

world_input = input("Enter the path of your minecraft world: ")

item_id = input("Enter the Item ID you want to find, (e.g. minecraft:diamond): ")


def get_count(item):
    count_tag = item.get("Count", nbtlib.tag.Byte(1))
    if count_tag == None:
        return 1
    if hasattr(count_tag, "value"):
        return int(count_tag.value)
    return int(count_tag)

def get_slot(item):
    slot_tag = item.get("Slot")
    if slot_tag is None:
        return 0
    if hasattr(slot_tag, "value"):
        return int(slot_tag.value)
    return int(slot_tag)




with open(os.path.expanduser(r"C:\Users\Olive\AppData\Roaming\.minecraft\usercache.json"), "r") as f:
    usercache = json.load(f)
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
                    count_tag = item.get("Count", nbtlib.tag.Byte(1))
                    count = int(count_tag.value if hasattr(count_tag, "value") else count_tag)
                    player_uuid = filename[:-4]
                    uuid_to_name = {entry['uuid']: entry['name'] for entry in usercache}
                    player_name = uuid_to_name.get(player_uuid, player_uuid)
                    print(f"Found {count}x {item_id} in player {player_name}'s Inventory at {pos_tuple}")

            for item in nbt.get("EnderItems", []):
                if item["id"] == item_id:
                    count_tag = item.get("Count", nbtlib.tag.Byte(1))
                    count = int(count_tag.value if hasattr(count_tag, "value") else count_tag)
                    player_uuid = filename[:-4]
                    uuid_to_name = {entry['uuid']: entry['name'] for entry in usercache}
                    player_name = uuid_to_name.get(player_uuid, player_uuid)
                    print(f"Found {count}x stack of {item_id} in player {player_name}'s Ender Chest at {pos_tuple}")

            

        except Exception as e:
            pass


print("\nSearching World Containers (chest, barrels, etc.)")


region_folder = os.path.join(world_input, "region")

for region_file in os.listdir(region_folder):
    if not region_file.endswith(".mca"):
        continue
    region_path = os.path.join(region_folder, region_file)

    with open(region_path, "rb") as f:
        offsets = f.read(4096)
        for i in range(1024):
            offset = int.from_bytes(offsets[i*4:i*4+3], "big")
            sector_count = offsets[i*4+3]

            if offset == 0 or sector_count == 0:
                continue

            cx, cz = i % 32, i // 32
            f.seek(offset * 4096)
            length = int.from_bytes(f.read(4), "big")
            compression_type = f.read(1)[0]
            chunk_data = f.read(length - 1)

            try:
                if compression_type == 2:
                    chunk_data = zlib.decompress(chunk_data)
                elif compression_type == 1:
                    import gzip
                    chunk_data = gzip.decompress(chunk_data)
            except:
                continue

            try:
                nbt_file = nbtlib.File.parse(BytesIO(chunk_data))
            except:
                continue

            block_entities = nbt_file.get("block_entities", []) or nbt_file.get("tile_entities", [])
            for be in block_entities:
                x = int(be.get("x", 0).value if hasattr(be.get("x"), "value") else be.get("x", 0))
                y = int(be.get("y", 0).value if hasattr(be.get("y"), "value") else be.get("y", 0))
                z = int(be.get("z", 0).value if hasattr(be.get("z"), "value") else be.get("z", 0))
                coords = f"({x},{y},{z})"

                items = be.get("Items", [])
                for item in items:
                    item_name_tag = item.get("id")
                    item_name = item_name_tag.value if hasattr(item_name_tag, "value") else str(item_name_tag)
                    count_tag = item.get("Count", 1)
                    count = int(count_tag.value) if hasattr(count_tag, "value") else int(count_tag)


                    if item_name == item_id:
                        print(f"Found {count}x stack of{item_id} in container at {coords}")