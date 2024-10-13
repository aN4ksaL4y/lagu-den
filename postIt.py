from main import requests, json

url = "https://api.github.com/gists"

# Load the JSON configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {config['ghp']}",
    "X-GitHub-Api-Version": "2022-11-28"
}
data = {
    "description": "Recently Played Songs",
    "public": True,
    "files": {
        "recently_played_songs.json": {
            "content": "Hello World of Gist!"
        }
    }
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("Gist created successfully:", response.json())
else:
    print("Failed to create gist:", response.status_code, response.text)