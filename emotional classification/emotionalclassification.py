# -*- coding: utf-8 -*-
"""EmotionalClassification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g5Q9FCsiJNWw8OvVc9neB2bxYrC8eSv4
"""

import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

data = pd.read_csv("EmotionalClassification.csv")

data.head()

data.info()

nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
stopword=set(stopwords.words('english'))
def clean(text):                                                
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text
data["text"] = data["text"].apply(clean)

text = " ".join(i for i in data.text)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords, 
                      background_color="white").generate(text)
plt.figure( figsize=(15,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

data["new_label"] = data["label"].map({0: "Happy", 1: "Sad"})
data = data[["text", "new_label"]]
print(data.head())

x = np.array(data["text"])
y = np.array(data["new_label"])
cv = CountVectorizer()
X = cv.fit_transform(x)
xtrain, xtest, ytrain, ytest = train_test_split(X, y, 
                                                test_size=0.33, 
                                                random_state=42)

from sklearn.naive_bayes import BernoulliNB
model = BernoulliNB()
model.fit(xtrain, ytrain)

ypred = model.predict(xtest)

print(classification_report(ytest, ypred))

MN = MultinomialNB()
MN.fit(xtrain,ytrain)
print(classification_report(ytest,MN.predict(xtest)))

ytrain= LabelEncoder().fit_transform(ytrain) 
ytest=  LabelEncoder().fit_transform(ytest)

Xg = XGBClassifier()
Xg.fit(xtrain,ytrain)
print(classification_report(ytest,Xg.predict(xtest)))

#EVALUATION TIME

user = input("Text: ")
data = cv.transform([user]).toarray()
output = model.predict(data)
print(output)

user = input("Text: ")
data = cv.transform([user]).toarray()
output = model.predict(data)
print(output)