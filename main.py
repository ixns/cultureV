from pafy import search_videos, download_video
from pprint import pprint

inputFile = "songs.txt"
websiteOutputFolder = "html"

# pafy.py functions:
# download_video(ytid, folder, audio_only=False)
# search_videos(query, pages)

def downloadSong(title: str, artist: str):
    results = search_videos(f"{title} {artist}", 1)
    song = results[0]
    outputFolder = "downloads/" + song["title"].replace(" ", "_") + "_" + song["id"]
    download_video(song["id"], f"{outputFolder}", True)
    with open(f"{outputFolder}/manifest.json", "w+") as songInfo:
        songInfo.write(song["richThumbnail"]["url"])
        songInfo.write(song["link"])

def main():
    songs = []

    with open(inputFile, "r") as f:
        for l in f:
            songs.append({
                "title": l.split(",")[0].strip(),
                "artist": l.split(",")[1].strip(),
            })

    for s in songs:
       results = search_videos(f"{s['title']} {s['artist']}", 1)
       pprint(results[0])
       #downloadSong(s["title"], s["artist"])


if __name__ == "__main__":
    main()