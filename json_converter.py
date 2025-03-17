import json

import scraping
from scraping import get_hyperlinks, create_dataset

file_name = "graph_data_test.json"


def get_all_json(hyperlinks: list[str]) -> None:
    for link in hyperlinks:
        data = create_dataset({link: {}}, scraping.d)

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)


get_all_json(["/wiki/Computer_science"])
