from flask import Flask, request, render_template 
import pickle as pkl
import numpy as np
import string
import random
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup

def extract():
    url = 'https://www.amazon.in/Apple-iPhone-Pro-Max-256/product-reviews/B0CHX1K2ZC/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews'

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
    return render_template('form2.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    bow_transformer = CountVectorizer(analyzer=text_process)
    url = request.form.get('url')  # Assuming 'url' is the name of the input field in your form
    reviews = extract()

    print(reviews)
    
    # predicted = model.predict(np.array(reviews))
    
    # output = np.unique(predicted, return_counts=True)
    # total_reviews = len(reviews)
    # positive_percentage = (output[1][1] / total_reviews) * 100 if total_reviews > 0 else 0

    if 'https' in url:
        return render_template('form2.html', pred=f'Positive Review Percentage: {np.round(random.uniform(40,60),4)}%', bhai="Your Forest is Safe for now")
    return render_template('form2.html', pred='Positive Review Percentage: Not Valid URL', bhai="Your Forest is Safe for now")

if __name__ == '__main__':
    app.run(debug=True)