from main import requests, json, time

url = "https://api.github.com/gists/457b453bb2e74d8bd23d74176f842ada"
gist_url = 'https://gist.github.com/github3112/457b453bb2e74d8bd23d74176f842ada'
filename = "recently_played.json"
json_file_path = 'recently_played_songs.json'


# Load the JSON configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def get_latest_data ():
    response = requests.get(f"{gist_url}/raw/{filename}").json()
    return response


if __name__=="__main__":
    while True:
        new_content = json.dumps(load_data_from_json(json_file_path), indent=2)
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {config['ghp']}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        data = {
            "description": "Recently Played Songs",
            "public": True,
            "files": {
                filename: {
                    "content": new_content
                }
            }
        }
        if get_latest_data()==load_data_from_json(json_file_path):
            print('skipped..')

        else:
            response = requests.patch(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses

            if response.status_code == 201:
                print("Gist created successfully")
            else:
                print("Failed to create gist:", response.status_code, response.text)

        time.sleep(60)