import pandas as pd
import regex as re
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

result = pd.read_csv('data/submit.csv')

#Negative
negative = result[result['class'] == 0]
wc_negative = WordCloud(
    background_color='black',
    max_words=500
)
wc_negative.generate(str(negative['clean_content'].values))
plt.figure(figsize=(12, 12))
plt.imshow(wc_negative, interpolation='bilinear')
plt.axis('off')
plt.show()

wc_negative.to_file('png/negative_wordcloud.png') #Lưu kết quả

#Positive
positive = result[result['class'] == 1]
wc_positive = WordCloud(
    background_color='black',
    max_words=500
)
wc_positive.generate(str(positive['clean_content'].values))
plt.figure(figsize=(12, 12))
plt.imshow(wc_positive, interpolation='bilinear')
plt.axis('off')
plt.show()

wc_positive.to_file('png/positive_wordcloud.png') #Lưu kết quả