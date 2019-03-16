from lxml.html import fromstring
import requests
from .utils import *

xpath_for_p = "//div/p[@class='bodytext']"


def scrape(link):
    data = requests.get(link).content

    tree = fromstring(data)

    p_tags = tree.xpath(xpath_for_p)

    page_content = []

    for tag in p_tags:
        if tag.text:
            page_content.append(tag.text.strip())

        child = next(tag.iterchildren(), None)
        if child is not None:
            if child.text_content().strip():
                page_content.append(child.text_content().strip())

    segregrated_content = [[], ]

    for content in page_content:
        if content == 'MILIMANI MAGISTRATE COURT':
            segregrated_content.append([])
            segregrated_content[-1].append(content)
        else:
            segregrated_content[-1].append(content)

    all_cases = []

    for content in segregrated_content:
        s = Scrape(content)
        if 'cases' in s.final_data:
            all_cases.append(s.final_data)

    return all_cases
