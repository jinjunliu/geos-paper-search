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
from Base_Scanner import Base_Scanner


class JoC_Scanner(Base_Scanner):
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
    
    def get_abstract(self, link: str) -> str:
        """implementation of abstract method

        Args:
            link (str): link of the paper
        
        Returns:
            str: abstract of the paper
        """
        response = requests.get(link, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Get abstract failed. Error: {}".format(response.status_code))
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        abstract = soup.find("section", {"class": "abstract"})
        abstract = abstract.text
        if abstract.startswith("Abstract"):
            abstract = abstract[8:]
        # decode the unicode
        # abstract = abstract.encode("utf-8").decode("utf-8")
        return abstract


def main():
    test_url = "https://journals.ametsoc.org/view/journals/clim/35/8/clim.35.issue-8.xml"
    scanner = JoC_Scanner(test_url)
    soup = scanner.get_soup()
    scanner.update_title_link(soup)
    scanner.update_authors(soup)
    for paper in scanner.papers["papers"]:
        paper['abstract'] = scanner.get_abstract(paper['link'])
    with open('../Database/joc_papers_clim.35.issue-8.json', 'w') as f:
        json.dump(scanner.papers, f, indent=4)


if __name__ == "__main__":
    main()
