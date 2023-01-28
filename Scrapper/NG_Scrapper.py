import requests
from bs4 import BeautifulSoup
import json
import urllib.parse as urlparse
from Base_Scanner import Base_Scanner


class NG_Scanner(Base_Scanner):
    """Nature Geoscience scanner class
    """
    def __init__(self, url: str) -> None:
        """Constructor

        Args:
            url (str): url of the journal
        """
        super().__init__(url)
        self.base_url = "https://www.nature.com/"
        self.papers["journal"] = "Nature Geoscience"

    def update_title_link(self, soup: BeautifulSoup) -> None:
        """implementation of abstract method

        Args:
            soup (BeautifulSoup): soup of the paper

        """
        # get article section
        article_soup = soup.find("section", {"aria-labelledby": "Articles"})
        # get paper titles, links
        soup_title_link = article_soup.find_all("a", {"itemprop": "url",
                                     "data-track": "click",
                                     "data-track-action": "view article",
                                     "data-track-label": "link"})
        for i, title_link in enumerate(soup_title_link):
            title_text = " ".join(title_link.text.split())
            link = title_link.get("href")
            abs_link = urlparse.urljoin(self.base_url, link)
            self.papers["papers"].append({"number": i, "title": title_text, "link": abs_link})

    def update_authors(self, soup: BeautifulSoup) -> None:
        """implementation of abstract method

        Args:
            soup (BeautifulSoup): soup of the paper
        """
        # get article section
        article_soup = soup.find("section", {"aria-labelledby": "Articles"})
        # get authors part
        ul_soup = article_soup.find_all("ul", {"data-test": "author-list"})
        authors_list = []
        for ul in ul_soup:
            authors = ""
            li_soup = ul.find_all("li")
            for li in li_soup:
                author = li.find("span", {"itemprop": "name"})
                authors += author.text + ","
            authors_list.append(authors)
        for i, authors in enumerate(authors_list):
            authors = authors[:-1].split(",")
            authors.append("...")
            authors[-1], authors[-2] = authors[-2], authors[-1]
            authors_str = ", ".join(authors)
            self.papers["papers"][i]["authors"] = authors_str
    
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
        abstract = soup.find("section", {"aria-labelledby": "Abs1", 
                                         "data-title": "Abstract"})
        abstract = abstract.find("p")
        abstract = abstract.text
        return abstract


def main():
    test_url = "https://www.nature.com/ngeo/volumes/15/issues/4"
    scanner = NG_Scanner(test_url)
    soup = scanner.get_soup()
    scanner.update_title_link(soup)
    scanner.update_authors(soup)
    # print(scanner.papers)
    for paper in scanner.papers["papers"]:
        paper['abstract'] = scanner.get_abstract(paper['link'])
    with open('../Database/ng_papers_vol.15.issue-4.json', 'w') as f:
        json.dump(scanner.papers, f, indent=4)


if __name__ == "__main__":
    main()
