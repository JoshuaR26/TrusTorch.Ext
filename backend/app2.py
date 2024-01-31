from flask import Flask, request, url_for, redirect, render_template
import req 
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
    url = 'https://www.amazon.in/Amozo-Cover-iPhone-Polycarbonate-Transparent/product-reviews/B09J2MM5C6/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews@pagereview=1'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        site = BeautifulSoup(response.text, 'html.parser')
        review_elements = site.find_all("div", {"class": "a-row a-spacing-small review-data"})
        reviews = [str(review_element).split("span>")[1].split("<")[0] for review_element in review_elements]
        return reviews
    else:
        return []

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
    # url = request.form.get('url')  # Assuming 'url' is the name of the input field in your form
    reviews = extract()

    print(reviews)
    
    predicted = model.predict(np.array(reviews))
    
    output = np.unique(predicted, return_counts=True)
    total_reviews = len(reviews)
    positive_percentage = (output[1][1] / total_reviews) * 100 if total_reviews > 0 else 0

    return render_template('form.html', pred=f'Positive Review Percentage: {positive_percentage:.2f}%', bhai="Your Forest is Safe for now")

if __name__ == '__main__':
    app.run(debug=True)
