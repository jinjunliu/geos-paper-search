from bs4 import BeautifulSoup
import fake_headers
from abc import ABC, abstractmethod
import requests


class BaseScrapper(ABC):
    """base class of scanners

    Args:
        ABC (class): A helper class that has ABCMeta as its metaclass.
    """

    def __init__(self, url: str) -> None:
        """constructor of JoCScrapper class

        Args:
            url (str): url of the journal
        """
        self.url = url
        self.headers = None
        self.papers = {"journal": None, "papers": []}

    def generate_headers(self) -> dict:
        """Generate fake headers

        Returns:
            dict: generated headers
        """
        headers = fake_headers.Headers()
        return headers.generate()

    def get_soup(self) -> BeautifulSoup:
        """method to get the soup from url

        Returns:
            bs4.BeautifulSoup: soup of the url
        """
        # generate headers
        self.headers = self.generate_headers()
        # get the response
        response = requests.get(self.url, headers=self.headers)
        # check the response code
        if response.status_code != 200:
            raise Exception("Error: {}".format(response.status_code))
        # parse the response using bs4
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        return soup

    @abstractmethod
    def update_authors(self, soup: BeautifulSoup) -> None:
        """method to get the authors of the paper

        Args:
            soup (BeautifulSoup): soup of the paper
        """
        pass

    @abstractmethod
    def update_title_link(self, soup: BeautifulSoup) -> None:
        """method to get the title and link of the paper at the same time, 
        since they are usually in the same place

        Args:
            soup (BeautifulSoup): soup of the paper
        """
        pass

    @abstractmethod
    def get_abstract_date(self, link: str) -> tuple[str, str]:
        """method to get the abstract and date of the paper

        Args:
            link (str): link of the paper
        
        Returns:
            tuple[str, str]: abstract and date of the paper
        """
        pass
