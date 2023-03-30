import requests
from bs4 import BeautifulSoup

# Fill up a songs.txt file like the one in this repo
# and then just run this script on it.
# it will try to find the highest quality thumbnails for all of them
# and output their direct urls to console.

inputFile = "songs.txt"

songs = []
with open(inputFile, "r") as f:
    for l in f:
        songs.append(f"{l.split(',')[0].strip()} {l.split(',')[1].strip()}")

for s in songs:
    r = requests.get(f"https://last.fm/search?q={s.replace(' ', '+')}")
    soup = BeautifulSoup(r.text, 'html.parser')
    cover_art_results = soup.find_all("a", class_="cover-art")
    try:
        first_result = cover_art_results[0]
    except IndexError:
        print(s + ": Failed to find thumbnail")
        continue
    first_thumbnail = first_result.img
    # TODO: what happens if you do 256s?
    # originall found this by just doubling the 64s default
    print(s + ": " + first_thumbnail["src"].replace("u/64s", "u/128s"))