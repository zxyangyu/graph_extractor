import os
import logging
from graph_extractor import GraphExtractor

logging.basicConfig(level=logging.WARNING)


if __name__ == "__main__":
    API_KEY = os.environ["API_KEY"]
    BASE_URL = os.environ["BASE_URL"]
    MODEL=os.environ["MODEL"]
    processor = GraphExtractor(API_KEY, BASE_URL, MODEL)
    with open("book.txt", encoding="utf-8-sig") as f:
        scope = f.read()
    graph_json = processor.extraction(scope.split('\n')[10:20])
    print(graph_json)

