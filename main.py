import requests
import json
import os

#VARIABLES
ID1 = ""
ID2 = ""
ICON1 = "https://fortnite-api.com/images/cosmetics/br/" + ID2 + "/icon.png"
ICON2 = "https://fortnite-api.com/images/cosmetics/br/" + ID1 + "/icon.png"
NAME1 = ""
NAME2 = ""

def getidnames():
    global NAME1
    global NAME2
    url = 'https://fortnite-api.com/v2/cosmetics/br/search?id=' + ID1
    url2 = 'https://fortnite-api.com/v2/cosmetics/br/search?id=' + ID2

    try:
        response = requests.get(url)
        response2 = requests.get(url2)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            NAME1 = data['data']['name']
        else:
            print(f"Failed with status code: {response.status_code}")

        if response2.status_code == 200:
            data2 = response2.json()
            NAME2 = data2['data']['name']
        else:
            print(f"Failed with status code: {response2.status_code}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

def export_uasset_file(file_path, type):
    url = 'https://fortnitecentral.genxgames.gg/api/v1/export'

    # Parameters
    params = {
        'path': file_path,
        'raw': 'true'  # Note: 'true' as a string, not a boolean value
    }

    headers = {
        'accept': 'application/json'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json().get('jsonOutput', [{}])[0]  # Check for existence of 'jsonOutput'

            if data:
                name = data.get('Name')
                # Removing underscores from the file name

                # Creating a directory if not exists
                export_folder = "Exports"
                if not os.path.exists(export_folder):
                    os.makedirs(export_folder)

                if type == "skin" and 'BaseCharacterParts' in data['Properties']:
                    with open(os.path.join(export_folder, name + '.json'), 'w') as file:
                        json.dump(data['Properties']['BaseCharacterParts'], file, indent=4)

                elif type == "backpack" and 'CharacterParts' in data['Properties']:
                    with open(os.path.join(export_folder, name + '.json'), 'w') as file:
                        json.dump(data['Properties']['CharacterParts'], file, indent=4)

                elif type == "pickaxe" and 'WeaponDefinition' in data['Properties']:
                    with open(os.path.join(export_folder, name + '.json'), 'w') as file:
                        json.dump(data['Properties']['WeaponDefinition'], file, indent=4)

                elif type == "emote" and 'Animation' in data['Properties']:
                    with open(os.path.join(export_folder, name + '.json'), 'w') as file:
                        json.dump(data['Properties']['Animation'], file, indent=4)

                else:
                    print("Invalid type or data not found for the specified type.")

            else:
                print("No data found in the response.")

        else:
            print(f"Failed with status code: {response.status_code} - {response.text}")
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def find_path(id, type):
    url = 'https://fortnitecentral.genxgames.gg/api/v1/assets'

    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            with open('assets.json', 'w') as file:
                file.write(json.dumps(data, indent=4))

            for x in data:
                if id in x:
                    #make sure path contain /Cosmetics/
                    if "/Cosmetics/" not in x:
                        continue
                    export_uasset_file(x, type)
                    break
        else:
            print(f"Failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def askswapids(type):
    global ID1
    global ID2
    global ICON1   
    global ICON2
    first = input("Enter the id you want to swap: ")
    second = input("Enter the id you want to replace with: ")
    ID1 = first
    ID2 = second
    ICON1 = "https://fortnite-api.com/images/cosmetics/br/" + ID2 + "/icon.png"
    ICON2 = "https://fortnite-api.com/images/cosmetics/br/" + ID1 + "/icon.png"

    find_path(ID1, type)
    find_path(ID2, type)
    getidnames()

def init():
    if not os.path.exists("Exports"):
        os.makedirs("Exports")
    if not os.path.exists("Plugins"):
        os.makedirs("Plugins")


if __name__ == "__main__":
    init()
    print("Galaxy Swapper v2.0 Plugins Generator by @DRQSuperior")
    print("===============================================")
    print("1. Skin Swap")
    # print("2. Backbling Swap")
    # print("3. Pickaxe Swap")
    # print("4. Emote Swap")

    choice = input("Enter your choice: ")

    if choice == "1":
        askswapids("skin")

        message = input("Enter a message for the swap(leave blank for none): ") or "none"

        with open('Templates/Skin.json', 'r') as file:
            templatejson = json.load(file)

            #read Exports for ids
            try:
                with open('Exports/' + ID1 + '.json', 'r') as file:
                    skin1 = json.load(file)
                    for i in range(3):
                        if i < len(skin1):
                            templatejson['Assets'][i]['AssetPath'] = skin1[i]['AssetPathName']
                        else:
                            templatejson['Assets'][i]['AssetPath'] = "none"
            except FileNotFoundError:
                for i in range(3):
                    templatejson['Assets'][i]['AssetPath'] = "none"

            try:
                with open('Exports/' + ID2 + '.json', 'r') as file:
                    skin2 = json.load(file)
                    for i in range(3):
                        if i < len(skin2):
                            templatejson['Assets'][i]['AssetPathTo'] = skin2[i]['AssetPathName']
                        else:
                            templatejson['Assets'][i]['AssetPathTo'] = "none"
            except FileNotFoundError:
                for i in range(3):
                    templatejson['Assets'][i]['AssetPathTo'] = "none"

            templatejson['Icon'] = ICON1
            templatejson['Swapicon'] = ICON2
            templatejson['Name'] = NAME1 + " > " + NAME2

            if message != "none":
                templatejson['Message'] = message

            with open('Plugins/' + NAME1 + "_to_" + NAME2 + '.json', 'w') as file:
                json.dump(templatejson, file, indent=4)
                
            print("Plugin created successfully.")