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

    def _pull_lyrics(self):
        return 0

    def _find_metadata_from_youtube(self):
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

    def _enrich_audio_file_with_thumbnail_and_metadata(self):
        return 0

    def __init__(self, title:str, artist:str):
        self.title = title
        self.artist = artist
        
        results = search_videos(f"{title} {artist}", 1)
        self.song_information_from_youtube = results[0]
        
        self.song_file = self._download_audio_from_youtube(f"./{title}_{artist}")
        self.thumbnail_file = self._download_thumbnail_from_youtube("./")
        self.metadata = self._find_metadata_from_youtube()
        # metadata should be like: {
        #   "title": "Gastronomie",   
        #   "artist": "Mach Hommy",
        #   "album": "Dollar Menu 4",
        #   "year": "2022",
        #   "genre": "rap",
        #}

        self._enrich_audio_file_with_thumbnail_and_metadata()

        try:
            self.lyrics = self._pull_lyrics()
        except LyricsNotFound:
            self.lyrics = "Lyrics unavailable"

    def outputToHTML(self, path:str):
        env = Environment(
            loader=PackageLoader("template"),
            autoescape=select_autoescape()
        )

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

    
        
