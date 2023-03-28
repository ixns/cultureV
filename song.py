from jinja2 import Environment, PackageLoader, select_autoescape



class Song:
    # these are all private functions that
    # will be used by this class only
    # and shouldn't be called in the
    # main program
    def _pull_lyrics(self):
        return 0

    def _find_metadata_from_youtube(self):
        return 0

    def _download_audio_from_youtube(self, path:str):
        return 0

    def _download_thumbnail_from_youtube(self, path:str):
        return 0

    def _enrich_audio_file_with_thumbnail_and_metadata(self):
        return 0

    def __init__(self, title:str, artist:str):
        self.title = title
        self.artist = artist

        self.song_file = self._download_audio_from_youtube("./")
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

    
        
