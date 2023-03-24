from flask import Flask, request, render_template
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen
import logging
import os
from flask_cors import CORS, cross_origin
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/books", methods=["POST"])
def show_books():
    if request.method == "POST":
        
        try:
            query = request.form["content"].replace(" ", "")
                
            # fake user agent to avoid getting blocked by google
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Referer": "https://www.google.com/",
                }

            goodread_url = f"https://www.goodreads.com/search?q={query}"
            url_client = urlopen(goodread_url)
            goodread_page = url_client.read()
            soup = bs(goodread_page, "html.parser")
            table = soup.find("table", {"class": "tableList"})
            books = table.find_all("tr")
            # filename = query + ".txt"
            
            books_data = []
            for book in books:
                books_data.append(book.td.a["title"])

            
            return render_template("result.html", result=books_data[0:(len(books_data) - 1)])

        except Exception as e:
            logging.info(e)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    