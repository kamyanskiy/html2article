#!/usr/bin/env python
"""
Parse article from HTML into structured text with Newspaper3k.
https://github.com/codelucas/newspaper
"""
import sys

__version__ = "1.0.0"
__author__ = "Alexander Kamyanskiy"

import argparse
import ntpath
import nltk
import newspaper
import os

from bs4.element import Tag
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from formatters import ParseHelper


WORDS_TO_SKIP = ["Реклама"]


class Html2Article(object):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.parser = ParseHelper()
        self.verbose = kwargs.get('verbose')
        self.client = newspaper.Article(self.url, language="ru",
                                        keep_article_html=True)

    def _get_path_from_url(self, url):
        url_parsed = urlparse(url)
        full_path = url_parsed.netloc + url_parsed.path
        if full_path.endswith("shtml"):
            return full_path.replace('shtml', 'txt')
        elif full_path.endswith("html"):
            return full_path.replace('html', 'txt')
        splitted = url.split("/")[2:]
        last_item = splitted[-1]
        if not last_item:
            filename = splitted[-2] + ".txt"
        elif last_item.endswith('html'):
            filename = last_item.split(".")[0] + ".txt"
        else:
            filename = "default.txt"
        return os.path.join(*splitted, filename)

    def save_result(self, text):
        path = self._get_path_from_url(self.url)
        directories = ntpath.dirname(path)
        if not os.path.exists(directories):
            os.makedirs(directories)
        with open(path, encoding="utf-8", mode="w+") as fp:
            fp.write(text)
        if self.verbose:
            print("INFO: File was successfully stored as {0}".format(path))

    def build(self):
        self.client.build() #this magic adds article_html and text attrs
        text = self.parse_article()
        self.save_result(text)

    def parse_article(self):
        title = self.get_title()
        bs_html = BeautifulSoup(self.client.article_html, "html.parser")
        article_text = self.get_article_text(bs_html)
        return title + "\n\n" + article_text

    def get_title(self):
        return self.client.title or ''

    def get_article_text(self, bs_html):
        """
            1. Get text with rules:
            1.1 every paragraph <p> as separate string
            1.2 if <a> tag inside <p> - format to string [href.value] text
        :return: formatted text of article

        """
        text_list = []
        for node in bs_html.select("p"):
            if isinstance(node, Tag):
                text = self.parser.format_text_line(node)
                if text and text not in WORDS_TO_SKIP:
                    text_list.append(text)
        article_text = self.parser.format_text(text_list)
        if self.verbose:
            print(article_text)
        return article_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse HTML into structured text.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    parser.add_argument("url",
                        help="URL to grab html from.")
    args = parser.parse_args()

    url = args.url
    parsed_url = urlparse(url)
    if not (parsed_url.scheme in ['https', 'http']):
        print("Invalid URL, URL should startswith http:// or https:// scheme.")
    if sys.platform == "win32":
        nltk.download('punkt')
        print("\n")
    article = Html2Article(url, verbose=args.verbose)
    article.build()
