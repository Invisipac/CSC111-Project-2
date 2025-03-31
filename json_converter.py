"""CSC111 Project 2 WikiMap Team

Module Description
==================
Generates the json file for a given depth and set off starting links.


Copyright and Usage Information
===============================
This file is Copyright (c) 2025 CSC111 WikiMap Team
"""


import json

import scraping
from scraping import get_hyperlinks, create_dataset

file_name = "multi-discipline_data.json"
starting_links = ["Computer_science", "Economics", "Mathematics", "History", "Literature", "Chemistry", "Physics",
                  "Biology", "Sociology", "Psychology", "Geography", "Visual_arts", "Music"]


def get_all_json(hyperlinks: list[str]) -> None:
    """
    Create a JSON file containing hyperlink data for each link in the input list.
    """
    for link in hyperlinks:
        data = create_dataset({link: {}}, scraping.d)

        with open(file_name, 'a') as f:
            json.dump(data, f, indent=4)


get_all_json(sorted(starting_links))
