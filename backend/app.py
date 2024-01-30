from flask import Flask, request, url_for, redirect, render_template 
import pickle as pkl
import numpy as numpy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import warnings, string
from nltk.corpus import stopwords
import numpy as np


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
    review = [x for x in request.form.values()]
    print(type(review))
    print(review)
    # # print(review[0])
    # text_samples = list(review.values())
    # text_array = np.array(text_samples)
    # predicted = model.predict(text_array)
    
    # output = np.unique(predicted, return_counts=True)
    # sum = 0
    # for i in range(2):
    #     print(f'{output[0][i]}: {output[1][i]}')
    #     sum = output[1][i] + sum

    # real_percentage = output[1][1]/sum
    # print(real_percentage*100)

    return render_template('form.html',pred='Your Output.\n Your Predicted House Median Values is {}'.format(output[0]),bhai="Your Forest is Safe for now")

if __name__ == '__main__':
    app.run(debug=True)


