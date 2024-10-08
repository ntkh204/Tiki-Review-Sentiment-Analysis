import requests
import json
from tqdm import tqdm
import pandas as pd 
import csv
import time
import random

nha_sach_tiki_url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=7588cc77-9f00-4829-803b-dcf326be58e0&category=8322&page={}&urlKey=nha-sach-tiki"
product_url = "https://tiki.vn/api/v2/products/{}"
review_url = "https://tiki.vn/api/v2/reviews?page={}&product_id={}"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "Content-Type": "application/json; charset=utf-8"}

def crawl_product_id():
    product_list = []
    i = 1
    while True:
        print("Crawl page: ", i)
        response = requests.get(nha_sach_tiki_url.format(i), headers=headers)
        if(response.status_code != 200):
            break
        products = json.loads(response.text)["data"]
        if(len(products) == 0):
            break
        for product in products:
            product_id = str(product["id"])
            product_list.append(product_id)
        i += 1
    return product_list, i

def crawl_review(product_list):
    reviews_list = []
    for product_id in tqdm(product_list):
        for page in range(1,3):
            response = requests.get(review_url.format(page, product_id), headers=headers)
            if response.status_code == 200:
                reviews = response.json().get('data')
                for review in reviews:
                    keys = ['id', 'content', 'title', 'content', 'thank_count', 'customer_id', 'rating', 'product_id']
                    new_review = {key: review[key] for key in keys}
                    reviews_list.append(new_review)
            time.sleep(random.randrange(1, 5))
    return reviews_list

def save_to_csv(reviews_list, path):
    df = pd.DataFrame(reviews_list[:1])
    df.to_csv(path, index=False, encoding='utf-8', mode='w')
    
    for review in reviews_list[1:]:
        df = pd.DataFrame([review])
        df.to_csv(path, index=False, encoding='utf-8', mode='a', header=False)

product_list, page = crawl_product_id()

reviews_list = crawl_review(product_list)

save_to_csv(reviews_list, "./data/review.csv")