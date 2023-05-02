from jinja2 import Environment, PackageLoader, select_autoescape
from papy import search_videos
import requests
import os
import yt_dlp

class Song:
    def _download_video(self, ytid, folder, audio_only=False):
        # This is a function which will download a youtube video's audio
        # and then if it is succesful, will return the path of the downloaded file
        # to the caller
        
        output_file = os.path.join(folder, f'%(title)s.%(ext)s')

        ytdl_format_options = {
            'outtmpl': output_file 
        }
        if audio_only:
            ytdl_format_options['format'] = 'bestaudio/best'
            ytdl_format_options['postprocessors'] =[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
            ydl.download('https://www.youtube.com/watch?v=%s' % ytid)
            return output_file

    #TODO: implement this function
    def _pull_lyrics(self):
        return 0

    #metadata = {
    #    "title": "Example Song",
    #    "artist": "Example Artist",
    #    "album": "Example Album",
    #    "genre": "Example Genre",
    #    "year": "2023",
    #}
    def _find_metadata(self):
        #This function can be built using example_search_output.txt
        #because that's the data it will work with
        return 0

    def _download_audio_from_youtube(self, path:str):
        song = self.song_information_from_youtube
        out_path = self._download_video(song["id"], f"{path}", audio_only=True)
        return out_path

    def _download_thumbnail_from_youtube(self, path:str):
        # TODO: download thumbnail from elsewhere because oftentimes
        # you end up pulling the music video's thumbnail

        output_file = os.path.join(path, f'{self.title}_{self.artist}_thumbnail.jpg')

        song = self.song_information_from_youtube
        thumbnail_url = song["thumbnail"][0]["url"]
        img_data = requests.get(thumbnail_url).content
        with open(output_file, 'wb') as handler:
            handler.write(img_data)
        return output_file
    
    def _download_thumbnail_from_lastFM(self, path:str):
        from bs4 import BeautifulSoup
        string = f"{self.title} {self.name}"
        r = requests.get(f"https://last.fm/search?q={string.replace(' ', '+')}")
        soup = BeautifulSoup(r.text, 'html.parser')
        cover_art_results = soup.find_all("a", class_="cover-art")
        try:
            first_result = cover_art_results[0]
        except IndexError:
            return None
        first_thumbnail = first_result.img
        return first_thumbnail["src"].replace("u/64s", "u/128s") 

    def _enrich_audio_file_with_thumbnail_and_metadata(self, thumbnail_url=None):
        from pydub import AudioSegment
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, APIC
        
        # Convert audio to MP3
        audio = AudioSegment.from_file(self.song_file)
        audio.export("output.mp3", format="mp3")

        # Load the MP3 file and its metadata
        mp3_file = MP3("output.mp3", ID3=ID3)

        # Add metadata
        if "title" in self.metadata:
            mp3_file["TIT2"] = TIT2(encoding=3, text=self.metadata["title"])
        if "artist" in self.metadata:
            mp3_file["TPE1"] = TPE1(encoding=3, text=self.metadata["artist"])
        if "album" in self.metadata:
            mp3_file["TALB"] = TALB(encoding=3, text=self.metadata["album"])
        if "genre" in self.metadata:
            mp3_file["TCON"] = TCON(encoding=3, text=self.metadata["genre"])
        if "year" in self.metadata:
            mp3_file["TDRC"] = TDRC(encoding=3, text=self.metadata["year"])

        # Add album cover
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                album_cover_data = response.content

                mp3_file["APIC"] = APIC(
                    encoding=3,
                    mime="image/jpeg",  # Change to 'image/png' if using a PNG file
                    type=3,  # Type 3 is for album/cover front
                    desc="Cover",
                    data=album_cover_data,
                )

        # Save the MP3 file with metadata
        mp3_file.save()

        # Read the MP3 file as binary data
        with open("output.mp3", "rb") as f:
            mp3_blob = f.read()

        return mp3_blob

    def __init__(self, title:str, artist:str):
        self.title = title
        self.artist = artist
        results = search_videos(f"{title} {artist}", 1)
        self.song_information_from_youtube = results[0]
        self.song_file = self._download_audio_from_youtube(f"./{title}_{artist}")
        self.thumbnail_url = self._download_thumbnail_from_youtube("./")
        self.metadata = self._find_metadata()
        self.final_mp3_blob = self._enrich_audio_file_with_thumbnail_and_metadata(self.thumbnail_url)

        #try:
        #    self.lyrics = self._pull_lyrics()
        #except LyricsNotFound:
        #    self.lyrics = "Lyrics unavailable"

    def outputToHTML(self, path:str):
        env = Environment(
            loader=PackageLoader("template"),
            autoescape=select_autoescape()
        )

        # Save the MP3 blob to a file
        with open(f"{path}/{self.title}_{self.artist}.mp3", "wb") as f:
            f.write(self.final_mp3_blob)
        output_file = f"{path}/{self.title}_{self.artist}.html"

        template = env.get_template("song_template.html")
        output_html = template.render(
            thumbnail=self.thumbnail_file, 
            artist=self.artist,
            title=self.title,
            lyrics=self.lyrics,
            audio_file=self.song_file,
            )

        with open(output_file, "w+") as out:
            out.write(output_html)

        return output_file

    
        
