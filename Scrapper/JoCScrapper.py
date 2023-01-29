"""
References:
1. https://www.geeksforgeeks.org/xml-parsing-python/
2. https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
3. https://pypi.org/project/fake-headers/
"""


import requests
from bs4 import BeautifulSoup
import json
import urllib.parse as urlparse
from BaseScrapper import BaseScrapper
import time


class JoCScrapper(BaseScrapper):
    """Journal of Climate scanner class
    """
    def __init__(self, url: str) -> None:
        """Constructor

        Args:
            url (str): url of the journal
        """
        super().__init__(url)
        self.base_url = "https://journals.ametsoc.org/"
        self.papers["journal"] = "Journal of Climate"

    def update_title_link(self, soup: BeautifulSoup) -> None:
        """implementation of abstract method

        Args:
            soup (BeautifulSoup): soup of the paper

        """
        # get paper titles, links
        soup_title_link = soup.find_all("a", {"class": "c-Button--link", 
                                              "target": "_self"})
        soup_title_link_filtered = []
        for title_link in soup_title_link:
            title_text = " ".join(title_link.text.split())
            if title_text != "Journal of Climate" and title_text != "Masthead":
                soup_title_link_filtered.append(title_link)
        for i, title_link in enumerate(soup_title_link_filtered):
            title_text = " ".join(title_link.text.split())
            link = title_link.get("href")
            abs_link = urlparse.urljoin(self.base_url, link)
            self.papers["papers"].append({"number": i, "title": title_text, "link": abs_link})

    def update_authors(self, soup: BeautifulSoup) -> None:
        """implementation of abstract method

        Args:
            soup (BeautifulSoup): soup of the paper
        """
        paper_authors = soup.find_all("div", {"class": "contributor-line text-subheading"})
        for i, author in enumerate(paper_authors):
            author = author.text.replace("\n", "")
            self.papers["papers"][i]["authors"] = author
    
    def get_abstract_date(self, link: str) -> tuple[str, str]:
        """implementation of abstract method

        Args:
            link (str): link of the paper
        
        Returns:
            tuple[str, str]: abstract and date of the paper
        """
        response = requests.get(link, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Get abstract failed. Error: {}".format(response.status_code))
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        abstract = soup.find("section", {"class": "abstract"})
        abstract = abstract.text
        date = soup.find("meta", property="article:published_time")
        date = date.get("content")
        if abstract.startswith("Abstract"):
            abstract = abstract[8:]
        # remove the "Significance Statement" part
        abstract = abstract.split("\nSignificance Statement\n")[0]
        # decode the unicode
        # abstract = abstract.encode("utf-8").decode("utf-8")
        return abstract, date


def main():
    test_url = "https://journals.ametsoc.org/view/journals/clim/35/8/clim.35.issue-8.xml"
    scrapper = JoCScrapper(test_url)
    soup = scrapper.get_soup()
    scrapper.update_title_link(soup)
    scrapper.update_authors(soup)
    print(scrapper.papers["papers"])
    for paper in scrapper.papers["papers"]:
        paper['abstract'], paper['date'] = scrapper.get_abstract_date(paper['link'])
        print(paper['abstract'])
        print(paper['date'])
        # wait for 5 seconds to avoid status code 429 error
        time.sleep(5)
    with open('../Database/joc_papers_clim.35.issue-8.json', 'w') as f:
        json.dump(scrapper.papers, f, indent=4)


if __name__ == "__main__":
    main()
