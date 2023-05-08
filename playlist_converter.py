import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def convert_youtube_to_spotify(youtube_playlist_id, spotify_playlist_name):
    # Authenticate with YouTube Music API
    youtube_client = authenticate_youtube()

    # Fetch the playlist details from YouTube Music
    youtube_playlist = get_youtube_playlist(youtube_client, youtube_playlist_id)

    # Extract track information from the YouTube playlist
    youtube_tracks = extract_youtube_tracks(youtube_playlist)

    # Authenticate with Spotify API
    spotify_client = authenticate_spotify()

    # Create a new playlist on Spotify
    spotify_playlist = create_spotify_playlist(spotify_client, spotify_playlist_name)

    # Search for and add each track to the Spotify playlist
    for track in youtube_tracks:
        spotify_track = search_spotify_track(spotify_client, track['title'], track['artist'])
        if spotify_track:
            add_track_to_spotify_playlist(spotify_client, spotify_playlist['id'], spotify_track['id'])

    print('Playlist conversion completed successfully!')

def authenticate_youtube():
    # Set up YouTube Music API credentials
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    client_secrets_file = "youtube_client_secrets.json"
    credentials = None

    if os.path.exists("youtube-credentials.json"):
        credentials = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes).run_local_server()
        with open("youtube-credentials.json", "w") as credentials_file:
            credentials_file.write(credentials.to_json())

    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server()

    youtube_client = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    return youtube_client

def get_youtube_playlist(youtube_client, playlist_id):
    request = youtube_client.playlists().list(
        part="snippet",
        id=playlist_id
    )
    response = request.execute()

    if response['items']:
        return response['items'][0]
    else:
        return None

def extract_youtube_tracks(youtube_playlist):
    playlist_title = youtube_playlist['snippet']['title']
    print(f"Converting YouTube Music playlist: {playlist_title}")

    playlist_items = []
    next_page_token = None

    while True:
        request = youtube_client.playlistItems().list(
            part="snippet",
            playlistId=youtube_playlist['id'],
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        playlist_items.extend(response['items'])
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    tracks = []
    for item in playlist_items:
        track_info = item['snippet']['title'].split(" - ", 1)
        if len(track_info) == 2:
            track = {
                'title': track_info[1],
                'artist': track_info[0]
            }
            tracks.append(track)

    return tracks


