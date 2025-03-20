import json

import jmespath
from rich import print

with open("people.json", "r") as f:
    data = json.load(f)

# search = "people[*].name"
search = "people[?age > `30`].name"

print(jmespath.search(search, data))
