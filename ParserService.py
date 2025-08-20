from HTMLParserClass.HTMLParserClass import HTMLParser
import requests

class ParserService:

    @staticmethod
    def fetch_html(url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def parse_html(url: str):
        html = ParserService.fetch_html(url)
        parser = HTMLParser(html)
        return parser.parse()

    @staticmethod
    def search_tag(url: str, tag: str):
        html = ParserService.fetch_html(url)
        parser = HTMLParser(html)
        parser.parse()
        return parser.search_by_tag(tag)

