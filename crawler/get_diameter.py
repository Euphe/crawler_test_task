import os
import json
import networkx as nx
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from networkx.algorithms.distance_measures import eccentricity
from networkx.algorithms.shortest_paths.unweighted import all_pairs_shortest_path_length

if __name__ == "__main__":
    DEPTH_LIMIT = int(os.environ['DEPTH_LIMIT'])
    START_URL = os.environ['START_URL']
    OUT_FILE_PATH =  os.environ['OUT_FILE_PATH']

    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', OUT_FILE_PATH)
    settings.set('DEPTH_LIMIT', DEPTH_LIMIT)

    if os.path.exists(OUT_FILE_PATH):
        os.remove(OUT_FILE_PATH)

    process = CrawlerProcess(settings)
    process.crawl('links_spider',start_urls=[START_URL])
    process.start()

    with open(OUT_FILE_PATH) as f:
        pages = json.loads(f.read())

    G = nx.Graph()
    G.add_node(START_URL)

    for page in pages:
        if not page['referring_url'] in G.nodes:
            G.add_node(page['referring_url'])
        G.add_edge(page['referring_url'], page['current_url'])
    path_lengths = dict(all_pairs_shortest_path_length(G))

    from_page = None
    to_page = None
    max_length = None
    for page in path_lengths:
        for other_page in path_lengths[page]:
            if not max_length or path_lengths[page][other_page] > max_length:
                max_length = path_lengths[page][other_page]
                from_page = page
                to_page = other_page
    if max_length:
        print('Max length is {} (from {} to {})'.format(max_length, from_page, to_page))
    else:
        print('No paths found')