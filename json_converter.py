import json
from scraping import get_hyperlinks

file_name = "graph_data.json"

def get_all_json(hyperlinks: list[str]) -> None:
    for link in hyperlinks:
        data = get_hyperlinks(link)
        data = {link[5:]: data}
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

get_all_json(["/wiki/Computer_science"])

