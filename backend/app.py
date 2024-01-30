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
    # review = [x for x in request.form.values()]
    review = ['The phone is really good it had some overheating issue as heard but not faced any it was due to software update now it is all fixed I still did not had any issue regarding overheating. The phone is really fast and the battery life is awesome. The new action button is really handy and useful. The camera is the best camera an iPhone ever had the photos are stunning and spectacular…. I am satisfied with the phone..', 'I recently switched from android to iphone. So i am liking the good audio quality, camera and everything.', 'It’s a fantastic phone…the feel and comfort in hand is awesome…looks stunning…also the brand appeal of Apple is fabulous. Camera is the best, performance is over the top…really fast and the games you can play are of play station’s…can any other phone do that…also the video quality is very nice…', 'Ultimate performance but some bug issue in 17.2.1 update and FB is not functioning properly….😏😏😏😏😏Lot of BUG issues are experienced in this phone and needs to correct it.', 'I like in this phone best camera', "The box had a different colour. I order black Titanium....box was black Titanium but phone was natural titanium inside ...It's heart wrenching...Trust shaken...", "I recently upgraded to the Apple 15 Pro Max, and while the enhanced camera is undoubtedly impressive, but I feel that it falls short of delivering a truly groundbreaking experience. If you're already using the 13 pro or 14 Pro, there seems to be little incentive to make the leap.", 'Performance very strong Charging', 'Camera quality is best', 'Good product', 'Good', 'It’s around 2months I have been using this device and it has been working flawlessly. No heating issues or such. Totally worth the upgrade because of the camera.', '', 'It’s a great buy. I upgraded from XS Max and am so glad I decided to get this. It’s pricey but worth it. Very powerful battery too', 'Hitting problem watching video and charging', '', 'This is my 1 st pro iPhone. And so far I’m really impressed with the performance and simplicity of the product.', 'Lightning fast,titanium tantrums', 'Camera Quality not good', 'Fast charging', 'Superb', 'We have received the iPhone 15 Pro Max, natural titanium color, and 256 GB storage capacity. The phone is good-looking and fast. It gets charged with the Apple 20W USB-C Power Adapter  (purchased separately). It also charges well using my 3-year-old Mi wireless charger (Qi charging). Overall, we are happy with the iPhone.', 'Battery 10/10', "I have purchased natural titanium and it's really awesome. My first phone purchased with my hardwork.", 'No heating issue till now running well with the new software update I have installed lots of apps and the ph is running well', 'Got a defective product where the camera doest load', 'Don’t worry about negative reviews go and get new one people comparing with android 😂 android was built by Samsung to operate washing machine. Redmi was economic brand to play candy crush….. 10 saal mai 10 phone badlme se acha 2 phone badlo….. indians are those people who buy cheap maruti cars for best resale value and mileage but cannot buy expensive apple for best resale valie and user friendly experience…. Inko sb sasta mai cahiye😂😂😂 this image quality of iphone beat this with android', '\n', 'box damaged, no new device smell. Completely ruined my unboxing experience. But the phone is amazing.', '15 pro max &gt;&gt;&gt;&gt; all androids .  the speed the camera the new ios justtt superb', 'Accha hai bass aur kya bolu.', 'Overpriced. It should not cost more than 1.1L. Bought it at 1.6L viz 50K extra I felt. Go for 15 instead of pro max. Overhyped phone this one is', 'If at all looking for pro model just because of lidar and action button and camera. Its not value for money as the charging and performance are not upto the mark for both pro and non pro models. I purchased iPhone 15 pro 128gb not happy', 'Like ntg to say just hi....', 'Iphone always the better than Android , I need the iphone please give me one Amazon please amazon Amazon Amazon', 'Heats very much during charger. Even if apple type c charger is used.', "If you already have 14 Pro or Pro Max then don't upgrade, but if you've any other Pro or non Pro models go for it. If you need an iPhone with 24-26hr battery life on a single charge then go for Pro Max models. No doubt Apple's 4K 60fps ProRes is really awesome, and the all new type-c port is the best thing Apple has done in years. Also all the type-c cables included in the box are woven design, now expecting this will not turn grey after few months of use.", '\n', 'No heating issue. Even if they exists for you. Use phone on battery saver mode amazing performance  Very good phone.', 'Best performance smartphone', 'When you hold this phone in your hand then only you can realise feeling of holding a premium phone 🍎', 'Nice Phn bought under very good price  Super sleek nice handy  vulnerable best rate so budget in hatts of to apple for making value products', 'Till this date it is the fastest iPhone for gaming and all over daily usage .', 'Good phone with all thing are there in it.... No need to go for samsung..', "Best phone ever seen it's the best phone in the earth worth buyable for those who are 4G iphone users.", 'Got the info it is in stock from X (twitter). Usually always unavailable.', '\n', '', 'Hangs a lot! Also lagse when using camera. In settings it shows GS5 PRO MAX VARIENT! 😭😭 I bought it for 60000', 'Bro 1 v ladki nhi pategi iss phone se... Bhaut bekar hai', 'Ek number ghatiya phone. dont waste 2lacs on this. Instead pay me some money if you have too much . Dont buy', "It seems to be highly expensive and on the other side it's features can't be matched up with Android.It doesn't have fast charging also unlike Android", 'Very bad phone and exoensice', 'Nothing new in this phone , just getting things repeated in earlier model,  Apple has nothing to offer new,  seems forgotten their tag line , think different', 'Pros :', 'The aluminium has made the phone very light weight you will immediately feel the difference coming from any previous pro max, worth the upgrade if you are coming from 11 series', 'best iphone ever used', 'Compare to iphone 14 pro max 15 pro max is very worst.. Past 1 month i used 15 pro max i faced lot of heating issue and battery life is worst.. If you want to buy iphone i recommend 14 pro max', 'I like all the things in iphone 15 Promax the camera is the world it is totally amazing product Thanks amazon']

    print(review)
    # # print(review[0])
    # text_samples = list(review.values())
    # text_array = np.array(text_samples)
    predicted = model.predict(review)
    
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


