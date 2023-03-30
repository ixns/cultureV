import requests
from bs4 import BeautifulSoup

song_name_and_artist = input("enter song name and artist. ex: gastronomie mach hommy\n")

r = requests.get(f"https://last.fm/search?q={song_name_and_artist.replace(' ', '+')}")

soup = BeautifulSoup(r.text, 'html.parser')

cover_art_results = soup.find_all("a", class_="cover-art")
first_result = cover_art_results[0]
first_thumbnail = first_result.img
# TODO: what happens if you do 256s?
# originall found this by just doubling the 64s default
print(first_thumbnail["src"].replace("u/64s", "u/128s"))