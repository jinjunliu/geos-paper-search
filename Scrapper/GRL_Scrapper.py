import requests
from bs4 import BeautifulSoup
import json
import urllib.parse as urlparse
from Base_Scanner import Base_Scanner


class GRL_Scanner(Base_Scanner):
    """Geophysical Research Letters scanner class
    """
    def __init__(self, url: str) -> None:
        """Constructor

        Args:
            url (str): url of the journal
        """
        super().__init__(url)
        self.base_url = "https://agupubs.onlinelibrary.wiley.com/"
        self.papers["journal"] = "Geophysical Research Letters"

    def update_title_link(self, soup: BeautifulSoup) -> None:
        """implementation of abstract method

        Args:
            soup (BeautifulSoup): soup of the paper

        """
        # TODO

    def update_authors(self, soup: BeautifulSoup) -> None:
        """implementation of abstract method

        Args:
            soup (BeautifulSoup): soup of the paper
        """
        # TODO
    
    def get_abstract(self, link: str) -> str:
        """implementation of abstract method

        Args:
            link (str): link of the paper
        
        Returns:
            str: abstract of the paper
        """
        # TODO


def main():
    test_url = "https://agupubs.onlinelibrary.wiley.com/toc/19448007/2022/49/8"
    scanner = GRL_Scanner(test_url)
    soup = scanner.get_soup()
    scanner.update_title_link(soup)
    scanner.update_authors(soup)
    # print(scanner.papers)
    for paper in scanner.papers["papers"]:
        paper['abstract'] = scanner.get_abstract(paper['link'])
    with open('../Database/grl_papers_vol.49.issue-8.json', 'w') as f:
        json.dump(scanner.papers, f, indent=4)


if __name__ == "__main__":
    main()
