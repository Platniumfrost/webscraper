from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_bbc_news():
    url = 'https://www.bbc.com/news'
    req = requests.get(url)
    bsObj = BeautifulSoup(req.text, 'html.parser')

    # Extract headlines and image sources
    headlines = [headline.text for headline in bsObj.find_all('h2')]

    # Filter out placeholder images
    images = [urljoin('https://www.bbc.com', item['src']) for item in bsObj.find_all('img') if 'grey-placeholder.png' not in item['src']]

    #Extract Content
    contents = [content.text for content in bsObj.find_all('p')]

    # Zip headlines and images before returning
    zipped_data = zip(headlines, images, contents)
    return zipped_data


@app.route('/')
def home():
    data = scrape_bbc_news()
    return render_template('home.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
