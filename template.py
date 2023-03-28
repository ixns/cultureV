from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("template"),
    autoescape=select_autoescape()
)

template = env.get_template("song_template.html")
output_html = template.render(
    thumbnail="images/thumbnail.png", 
    artist="fahim tha god",
    title="Mind over matter",
    lyrics="blah blah blah",
    )

with open("output.html", "w+") as out:
    out.write(output_html)