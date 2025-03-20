from storygraph_api.request.books_request import BooksScraper
from storygraph_api.exception_handler import parsing_exception
from bs4 import BeautifulSoup
import re

class BooksParser:
    @staticmethod
    @parsing_exception
    def book_page(book_id):
        content = BooksScraper.main(book_id)
        soup = BeautifulSoup(content, 'html.parser')
        h3_tag = soup.find('h3',class_="font-serif font-bold text-2xl md:w-11/12")
        title = h3_tag.contents[0].strip()
        authors = []
        for a in h3_tag.find_all('a'):
            if a["href"].startswith("/authors"):
                authors.append(a.text)
        p_tag = soup.find('p',class_="text-sm font-light text-darkestGrey dark:text-grey mt-1")
        pages = p_tag.contents[0].strip().split()[0]
        first_pub = p_tag.contents[1].find_all('span')[1].text.split()[2]
        tags = []
        tag_div = soup.find('div',class_="book-page-tag-section").find_all('span')
        for tag in tag_div:
            tags.append(tag.text)
        desc = soup.find_all('script')[5].text
        pattern = re.compile(r"Description<\/h4><div class=\"trix-content mt-3\">(.*?)<\/div>", re.DOTALL)
        match = pattern.search(desc)
        description = match.group(1).strip()
        review_content = BooksScraper.community_reviews(book_id)
        rev_soup = BeautifulSoup(review_content,'html.parser')
        avg_rating = rev_soup.find('span',class_="average-star-rating").text.strip()
        warnings = BooksParser.content_warnings(book_id)
        data = {
                'title':title,
                'authors': authors,
                'pages': pages,
                'first_pub': first_pub,
                'tags': tags,
                'average_rating': avg_rating,
                'description':description,
                'warnings': warnings
                }
        return data

    @staticmethod
    @parsing_exception
    def content_warnings(book_id):
        warnings_content = BooksScraper.content_warnings(book_id)
        warnings_soup = BeautifulSoup(warnings_content,'html.parser')
        user_warnings_pane = warnings_soup.find_all('div',class_='standard-pane')[1]
        warnings_graphic = []
        warnings_moderate = []
        warnings_minor = []
        warnings_list = warnings_graphic
        tag_re = re.compile(r'^(.*) \((\d+)\)$')
        for tag in user_warnings_pane.children:
            if tag == '\n':
                continue
            if tag.name == 'p':
                if tag.text == 'Graphic':
                    warnings_list = warnings_graphic
                elif tag.text == 'Moderate':
                    warnings_list = warnings_moderate
                elif tag.text == 'Minor':
                    warnings_list = warnings_minor
            elif tag.name == 'div':
                match = tag_re.match(tag.text)
                warnings_list.append((match[1], int(match[2])))
        warnings = {
                'graphic': warnings_graphic,
                'moderate': warnings_moderate,
                'minor': warnings_minor
                }
        return warnings

    @staticmethod
    @parsing_exception
    def search(query):
        content = BooksScraper.search(query)
        soup = BeautifulSoup(content, 'html.parser')
        search_results = []
        books = soup.find_all('div', class_="book-title-author-and-series w-11/12")
        for book in books:
            title = book.find('a').text.strip()
            for a in book.find_all('a'):
                if a["href"].startswith('/author'):
                    author = a.text.strip()
                    break
            book_id = book.find('a')['href'].split('/')[-1]
            search_results.append({
                'title': title,
                'author': author,
                'book_id': book_id
            })
        return search_results
