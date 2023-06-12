import json
import psycopg2
from urllib.request import urlopen
import time

"""
Python script to gather book data from O'Reilly Public Search API for local database

This data is used for implementation of recommendation system for electrical engineering students. It is combined
with the manually collected Courses data from faculty's site. All of data is completely for public use.

"""


def get_connection():
    try:
        conn = psycopg2.connect(  # enter your credentials for postgresql database
            host='',
            database='',
            user='',
            password=''
        )
        conn.autocommit = True
    except Exception as error:
        print('Error occurred while trying to connect to the database:')
        print(error)
        conn = None
    finally:
        return conn


def get_num_of_pages(number_of_books):
    return int(number_of_books / 200)


def get_api_name(topic):
    topic = topic.replace(' ', '%20')
    topic = topic.replace('+', '%2B')
    topic = topic.replace('#', '%23')
    topic = topic.replace('&', '%26')
    return topic


def get_api_url(topic, page):
    api_name = get_api_name(topic)
    url = 'https://learning.oreilly.com/api/v2/search/?topics=' + api_name + '&formats=book&languages=en' + \
          '&fields=isbn&fields=issued&fields=authors&fields=publishers&fields=title&fields=description' + \
          '&fields=average_rating&fields=popularity&fields=report_score&fields=cover_url&fields=topics&limit=200' + \
          '&page=' + str(page)
    return url


def is_number(data):
    try:
        broj = int(data)
        return True
    except Exception:
        broj = 'Not a number honestly ;)'
        return False


def process_book(book):
    if 'isbn' not in book:
        book = None
        return book
    elif not is_number(book['isbn']):
        book = None
        return book
    elif 'title' not in book:
        book = None
        return book
    else:
        if 'issued' not in book:
            book.update({'issued': None})
        if 'authors' not in book:
            book.update({'authors': None})
        if 'publishers' not in book:
            book.update({'publishers': None})
        if 'description' not in book:
            book.update({'description': '<span>Learn more about this book on internet!</span>'})
        if 'average_rating' not in book:
            book.update({'average_rating': None})
        if 'popularity' not in book:
            book.update({'popularity': None})
        if 'report_score' not in book:
            book.update({'report_score': None})
        if 'cover_url' not in book:
            book.update({'cover_url': None})
        return book


def import_books(connection, books_list, page):
    cur = connection.cursor()
    iterBook = 0
    for book in books_list:
        try:
            book = process_book(book)
            if book is None:
                continue
            cur.execute(
                "INSERT INTO \"Books\" (isbn, issued, authors, publishers, title, description, average_rating, popularity,report_score, cover_url, topic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)",
                (book['isbn'], book['issued'], book['authors'], book['publishers'], book['title'], book['description'],
                 book['average_rating'], book['popularity'], book['report_score'], book['cover_url'],
                 book['topics_payload'][0]['name']))
            iterBook = iterBook + 1
        except Exception as error:
            print('ERROR')
            print(
                'Error occurred for the book ISBN:' + book['isbn'] + ' Title: ' + book['title'] + ' at the page ' + str(
                    page))
            print(error)
            continue
    cur.close()
    return iterBook


start_time = time.time()
file_tags = open("TagsJSON.json", "r")
json_data = json.load(file_tags)
file_tags.close()
lista = json_data["topics"]
topics = {}
for i in range(0, len(lista) - 1, 2):
    topics.update({lista[i]: lista[i + 1]})

conn = get_connection()
if conn is None:
    exit(0)

number_of_calls = 0
number_of_processed_books = 0
for topic_raw_name in topics.keys():
    number_of_books = topics.get(topic_raw_name)
    upper_bound = get_num_of_pages(number_of_books) + 1
    for page_count in range(0, upper_bound):  # iterate through all pages for that topic, and import all the books
        url = get_api_url(topic_raw_name, page_count)
        if number_of_calls % 15 == 0 and number_of_calls != 0:  # we reached the limit for API calls
            print(str(number_of_processed_books) + ' books processed so far')
            time.sleep(10)
        response = urlopen(url)
        number_of_calls = number_of_calls + 1
        json_response = json.loads(response.read())
        books = json_response['results']  # list of books to be imported in the database
        number_of_processed_books = number_of_processed_books + import_books(conn, books, page_count)

conn.close()
print('Time of execution: ' + str(time.time() - start_time))
