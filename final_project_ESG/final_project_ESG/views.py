from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import datetime
import tensorflow
import tensorflow.compat.v1 as tf
import numpy as np
tf.compat.v1.disable_eager_execution()
#exec(open("final_project_ESG/model_load_py.py" , encoding ="UTF8").read())
print('여기는 views 실행이 됐나요')
X = tf.placeholder(tf.float32, shape=[None, 4])
Y = tf.placeholder(tf.float32, shape=[None, 1])
W = tf.Variable(tf.random_normal([4, 1]), name="weight")
b = tf.Variable(tf.random_normal([1]), name="blas")

# 가설을 설정합니다.
hypothesis = tf.matmul(X, W) + b
# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.train.Saver()
model = tf.global_variables_initializer()

# 세션 객체 생성
sess = tf.Session()
sess.run(model)

# 저장된 학습 모델을 파일로부터 불러옵니다.
# 배출권 시세예측 체크포인트 모델
save_path = "./final_project_ESG/model/saved1.cpkt"
saver.restore(sess, save_path)

def index(request):
    print('index 화면 진입')
    print(os.path.abspath(__file__))
    print(os.path.realpath(__file__))
    print(os.path.dirname(os.path.realpath(__file__)))
    return render(request , 'index.html')
    
    
def model_load(request):
    print('예측버튼이 눌렸습니다.')

    #,'석탄가격', '코스피', '원유가격', '전력수요'
    #   203.01     3015.06    82.28      1444840
    # 4가지 변수를 입력 받습니다.
    if request.method == 'POST': 
        avg_temp = request.POST['avg_temp'] #석탄
        min_temp = request.POST['min_temp'] #코스피
        max_temp = request.POST['max_temp'] #원유
        rain_fall = request.POST['rain_fall'] #전력

        price =0        
        # 사용자의 입력 값을 이용해 배열을 만듭니다.
        data = ((avg_temp, min_temp, max_temp, rain_fall), )
        arr = np.array(data, dtype=np.float32)

        # 예측을 수행한 뒤에 그 결과를 출력합니다.
        x_data = arr[0:4]
        dict = sess.run(hypothesis, feed_dict={X: x_data})
        print(dict[0])
        context = {'price' : str(dict[0][0])}
        
        return render(request , 'index.html' , context)

import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import nltk 
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from wordcloud import WordCloud
import os   
import random

def create_wordcloud(request):
    print('워드클라우드를 생성합니다.')

        
    if request.method == 'POST': 
        keyword = request.POST['keyword']
        print(keyword)
        #-------------------------------------------
        crowled_title = []
        for page in range(5):
            #news_url = 'https://news.naver.com/main/ranking/popularDay.nhn?date={}'.format(date)
            news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+keyword+'&start=' + str(page * 10 + 1)
        # 'https://search.naver.com/search.naver?&where=news&query=esg&start=' + str(page * 10 + 1)'

            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
            req = requests.get(news_url, headers = headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            #news_titles = soup.select('#main_pack > section > div > div.group_news > ul > li > div.news_area')
            news_titles = soup.select('#main_pack > section > div > div.group_news > ul > li > div.news_wrap.api_ani_send > div > a')

            for i in range(len(news_titles)):
                crowled_title.append(news_titles[i].text)
                print(i+1, news_titles[i].text) # 기사 제목 리스트 저장하기
        #-------------------------------------------
        title = "".join(crowled_title)
        filtered_title = title.replace('.', ' ').replace('"',' ').replace(',',' ').replace("'"," ").replace('·', ' ').replace('=',' ').replace('\n',' ')
        #-------------------------------------------
        tw = Twitter()
        tokens_ko = tw.nouns(filtered_title)
        ko = nltk.Text(tokens_ko, name='기사 내 명사')
        ko.tokens
        ko.vocab()
        new_ko=[]
        for word in ko:
            if len(word) > 1 and word != '단독' and  word != ' ':
                new_ko.append(word)
        ko = nltk.Text(new_ko, name = '기사 내 명사 두 번째')
        ko.tokens
        ko.vocab()
        data = ko.vocab().most_common(150)
        data = dict(data)        
        #-------------------------------------------
        wordcloud = WordCloud().generate(filtered_title)

        font = "./final_project_ESG/나눔손글씨 나무정원.ttf"

        wc = WordCloud(font_path=font, background_color="white",  width=1000,  height=1000, max_words=100)
        wc = wc.generate_from_frequencies(data)
        wc.to_file('./static/assets/img/wordcloudkey.jpg')  
        # plt.figure(figsize=(10,10))
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis('off')
        # plt.show()
        return render(request , 'index.html' , {'imgfile':'img'})
    
def wordcloud2(request):
    print('ajax워드클라우드를 생성합니다.')
    if request.method == 'POST': 
        keyword = request.POST['keyword']
        print(keyword)
        #-------------------------------------------
        crowled_title = []
        for page in range(2):
            #news_url = 'https://news.naver.com/main/ranking/popularDay.nhn?date={}'.format(date)
            news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+keyword+'&start=' + str(page * 10 + 1)
        # 'https://search.naver.com/search.naver?&where=news&query=esg&start=' + str(page * 10 + 1)'

            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
            req = requests.get(news_url, headers = headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            #news_titles = soup.select('#main_pack > section > div > div.group_news > ul > li > div.news_area')
            news_titles = soup.select('#main_pack > section > div > div.group_news > ul > li > div.news_wrap.api_ani_send > div > a')

            for i in range(len(news_titles)):
                crowled_title.append(news_titles[i].text)
                print(i+1, news_titles[i].text) # 기사 제목 리스트 저장하기
        #-------------------------------------------
        title = "".join(crowled_title)
        filtered_title = title.replace('.', ' ').replace('"',' ').replace(',',' ').replace("'"," ").replace('·', ' ').replace('=',' ').replace('\n',' ')
        #-------------------------------------------
        tw = Twitter()
        tokens_ko = tw.nouns(filtered_title)
        ko = nltk.Text(tokens_ko, name='기사 내 명사')
        ko.tokens
        ko.vocab()
        new_ko=[]
        for word in ko:
            if len(word) > 1 and word != '단독' and  word != ' ':
                new_ko.append(word)
        ko = nltk.Text(new_ko, name = '기사 내 명사 두 번째')
        ko.tokens
        ko.vocab()
        data = ko.vocab().most_common(150)
        data = dict(data)        
        #-------------------------------------------
        wordcloud = WordCloud().generate(filtered_title)

        font = "./final_project_ESG/나눔손글씨 나무정원.ttf"

        wc = WordCloud(font_path=font, background_color="white",  width=1000,  height=1000, max_words=100)
        wc = wc.generate_from_frequencies(data)
        numb = random.randrange(1, 10000) 
        wc.to_file('./static/assets/img/wordcloudkey.jpg')  
        print(numb)
        # plt.figure(figsize=(10,10))
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis('off')
        # plt.show()
        return JsonResponse({'imgnum':str(numb)},safe = False)

def model_load2(request):
    print('배출권 시세 예측버튼이 눌렸습니다.')

    #,'석탄가격', '코스피', '원유가격', '전력수요'
    #   203.01     3015.06    82.28      1444840
    # 4가지 변수를 입력 받습니다.
    if request.method == 'POST': 
        avg_temp = request.POST['avg_temp'] #석탄
        min_temp = request.POST['min_temp'] #코스피
        max_temp = request.POST['max_temp'] #원유
        rain_fall = request.POST['rain_fall'] #전력

        price =0        
        # 사용자의 입력 값을 이용해 배열을 만듭니다.
        data = ((avg_temp, min_temp, max_temp, rain_fall), )
        arr = np.array(data, dtype=np.float32)

        # 예측을 수행한 뒤에 그 결과를 출력합니다.
        x_data = arr[0:4]
        dict = sess.run(hypothesis, feed_dict={X: x_data})
        print(dict[0])
        context = {'price' : str(dict[0][0])}
        
        return JsonResponse(context,safe = False)
    
    