from flask import Flask, request, url_for, redirect, render_template 
import pickle as pkl
import numpy as numpy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import warnings, string
from nltk.corpus import stopwords
import numpy as np
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

def extract():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'}

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def job():
        u = "https://www.amazon.in/Apple-iPhone-Pro-Max-256/product-reviews/B0CHX1K2ZC/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews"
        u += "&pageNumber={i}"
        urls = [(u) for i in range(1, 11)]
        l1 = []
        l2 = []
        new_data = {}

        async with aiohttp.ClientSession(headers=headers) as session:
            htmls = await asyncio.gather(*[fetch(session, url) for url in urls])
            for html in htmls:
                site = BeautifulSoup(html, features="lxml")

                # Parsing code
                review = site.findAll("div", {"class" : "a-row a-spacing-small review-data"})

                for i in range(len(review)):
                    rev = str(review[i]).split("span>")[1].split("<")[0]
                    l2.append(str(rev))
        return l2 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(job())

def text_process(review):
    nopunc = [char for char in review if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

app = Flask(__name__)

model = pkl.load(open('svc_model.pkl', 'rb'))

@app.route('/')
def hello_world():
    return render_template('form.html')

@app.route('/predict', methods=['POST', 'GET'])


def predict():
    bow_transformer = CountVectorizer(analyzer=text_process)
    url = [x for x in request.form.values()]
    review = extract()

    print(review)
    # # print(review[0])
    # text_samples = list(review.values())
    # text_array = np.array(text_samples)
    predicted = model.predict(np.array(review))
    
    output = np.unique(predicted, return_counts=True)
    sum = 0
    for i in range(2):
        print(f'{output[0][i]}: {output[1][i]}')
        sum = output[1][i] + sum

    real_percentage = output[1][1]/sum
    print(real_percentage*100)

    return render_template('form.html',pred='Your Output.\n Your Predicted House Median Values is {}'.format(real_percentage*100),bhai="Your Forest is Safe for now")

if __name__ == '__main__':
    app.run(debug=True)


