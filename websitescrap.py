import argparse
import json
import os
import sys
import time
import uuid
from random import randint
from utils.extract_links_from_webpage import get_links
from utils.request_client import ReqestClient
from utils.url_utils import get_filtered_links
from urllib.parse import urlparse
from pathlib import Path
import config
from utils.redislite_utils import redis_cleanup, redis_client as redis
from zyteclient import get_html
from bs4 import BeautifulSoup
from html5print import CSSBeautifier, JSBeautifier

request_client = ReqestClient()


def write_url_data(url, response_text):
    url_component = urlparse(url)
    print(url_component)
    if not url_component.path:
        url_component = url_component._replace(path="/index.html")
    last_token = url_component.path.rsplit('/', 1)
    if "." not in last_token[0]:
        url_component = url_component._replace(path=url_component.path + ".html")
    path = Path("./" + url_component.netloc + "/" + url_component.path)
    if not os.path.exists(path.parent):
        path.parent.mkdir(parents=True, exist_ok=True)
    # if not os.path.exists(config.DATA_DIR):
    #   os.mkdir(config.DATA_DIR)
    # file_path = config.DATA_DIR + str(uuid.uuid3(uuid.NAMESPACE_URL, str(url))) + ".json"
    file_path = path
    response_text = beutify_html(response_text)
    if not os.path.exists(file_path):
        with open(file_path, "w") as fp:
            fp.write(response_text)
            # json.dump({url: response_text}, fp)

def beutify_html(html):
    # html = JSBeautifier.beautify(html)
    html = CSSBeautifier.beautifyTextInHTML(html)
    html = BeautifulSoup(html, 'html.parser').prettify()
    return html

class Websitescrap:
    def __init__(self, url, start_afresh=False):
        self.url = url
        if start_afresh:
            redis.flushdb()
        redis.sadd("new_urls", url)

    def crawl(self, sleep_time_lower=30, sleep_time_upper=121):
        print("\ncrawling started\n")
        write_count = 0
        write_flag = 1
        while len(redis.smembers("new_urls")):
            url = redis.spop("new_urls")
            redis.sadd("processed_urls", url)

            if write_count % 12 == 0:
                time.sleep(randint(sleep_time_lower, sleep_time_upper))
            else:
                time.sleep(randint(sleep_time_lower, int(sleep_time_upper / 2)))

            if write_count % write_flag == 0:
                print('Processing %s' % url)

            write_count += 1
            # if write_count > 13:
            #     break

            response = request_client.request_with_proxy_header(url)
            if not response or not response.status_code == 200:
                continue

            # write response.text to a json dump file
            write_url_data(url, response.text)

            # get the urls for local page
            local_urls = [*get_links(response.text, self.url).keys()]

            # filter the urls of foreign urls or dummy urls
            local_urls = get_filtered_links(local_urls, self.url)

            for i in local_urls:
                if not redis.sismember("processed_urls", i):
                    redis.sadd("new_urls", i)
            redis_cleanup(self.url)
            if write_count % write_flag == 0:
                print('Processed')


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('website_address')
    parser.add_argument("-s", "--start_afresh", help="whether to start a fresh crawling", required=False, default=True,
                        action='store', dest='start_afresh')

    args = parser.parse_args()
    website = args.website_address
    start_afresh = str2bool(args.start_afresh)

    if not website.startswith("http"):
        print("\033[91m {}\033[00m".format("Please include website scheme (http/https) in the provided address"))
        return

    scrapper = Websitescrap(website, start_afresh=start_afresh)
    scrapper.crawl(5, 18)


if __name__ == '__main__':
    main()
