import sys
import sys
import os
import json

if __name__ == "__main__":
    links_length = 0
    if os.path.exists("links.txt"):
        with open("links.txt", "r") as file:
            links_length = len(set(line.strip() for line in file.readlines()))

    if len(sys.argv) > 1:
        arg = sys.argv[1]

        scraped_text_length = 0
        if os.path.exists("scraped_text.json"):
            with open("scraped_text.json", "r") as file:
                scraped_text_length = len(json.load(file))

        print(links_length-scraped_text_length)

    else:
        print(links_length)
