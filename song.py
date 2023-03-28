from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("template"),
    autoescape=select_autoescape()
)

class Song:
    def __init__(title:str, artist:str):
        this.title = title
        this.artist = artist

        song_file = _download_audio_from_youtube("./")
        thumbnail_file = _download_thumbnail_from_youtube("./")
        metadata = _find_metadata_from_youtube()
        # metadata should be like: {
        #   "title": "Gastronomie",   
        #   "artist": "Mach Hommy",
        #   "album": "Dollar Menu 4",
        #   "year": "2022",
        #   "genre": "rap",
        #}

        _enrich_audio_file_with_thumbnail_and_metadata()

        try:
            lyrics = _pull_lyrics()
        except LyricsNotFound:
            lyrics = "Lyrics unavailable"

    # these are all private functions that
    # will be used by this class only
    # and shouldn't be called in the
    # main program
    def _pull_lyrics():
        return 0

    def _find_metadata_from_youtube():
        return 0

    def _download_audio_from_youtube(path:str):
        return 0

    def _download_thumbnail_from_youtube(path:str):
        return 0

    def _enrich_audio_file_with_thumbnail_and_metadata():
        return 0

    def outputToHTML(path:str):
        template = env.get_template("song_template.html")
        output_html = template.render(
            thumbnail=thumbnail_file, 
            artist=artist,
            title=title,
            lyrics=lyrics,
            audio_file=song_file,
            )

        with open("output.html", "w+") as out:
            out.write(output_html)

        return "output.html"

    
        
