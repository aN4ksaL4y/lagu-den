import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Set up the YouTube API
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Authenticate and build the YouTube API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "config.json", scopes)
    credentials = flow.run_local_server(port=0)
    
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # Fetch the watch history
    request = youtube.activities().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=25
    )
    
    response = request.execute()

    # Print the history
    for item in response.get("items", []):
        print(f"{item['snippet']['title']} - {item['snippet']['publishedAt']}")

if __name__ == "__main__":
    main()