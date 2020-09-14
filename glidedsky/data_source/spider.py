#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 16:21
# @Author : way
# @Site : 
# @Describe:

import re
import os
import uuid
import base64
import requests

from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

Cookie = 'your cookies'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': Cookie,
    'Host': 'www.glidedsky.com',
    'Referer': 'http://www.glidedsky.com/level/web/crawler-basic-2?page=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
}


def get_img(text):
    """
    :param text: 获取图片模板
    :return:
    """
    img_str = re.findall('base64,(.*?)"', text)[0]
    img_fp = BytesIO(base64.b64decode(img_str.encode('utf-8')))
    img = Image.open(img_fp)
    return img


def crawler(url):
    text = requests.get(url, headers=headers).text
    img = get_img(text)
    rows = BeautifulSoup(text, 'lxml').find_all('div', class_="col-md-1")
    num_labels = list(str(123171140339373274129338158411319368))
    num_imgs = []
    for row in rows:
        for div in row.find_all('div'):
            css_name = div.get('class')[0].split(' ')[0]
            tag_x = re.findall(f'\.{css_name} \{{ background-position-x:(.*?)px \}}', text)
            tag_y = re.findall(f'\.{css_name} \{{ background-position-y:(.*?)px \}}', text)
            width = re.findall(f'\.{css_name} \{{ width:(.*?)px \}}', text)
            height = re.findall(f'\.{css_name} \{{ height:(.*?)px \}}', text)
            tag_x = abs(int(tag_x[0]))
            tag_y = abs(int(tag_y[0]))
            width = int(width[0])
            height = int(height[0])
            box = (tag_x, tag_y, tag_x + width, tag_y + height)
            num_imgs.append(img.crop(box))
    save_list = [str(i) for i in range(10)]
    for num_img, num_label in zip(num_imgs, num_labels):
        if num_label in save_list:
            file_name = f'./imgs/{num_label}_{uuid.uuid1()}.png'
            num_img = num_img.resize((20, 20))
            num_img.save(file_name)
            save_list.remove(num_label)

os.makedirs('./imgs', exist_ok=True)
urls = []
for _ in range(90000):
    url = f'http://www.glidedsky.com/level/web/crawler-sprite-image-2?page=999'
    urls.append(url)

pool = ThreadPoolExecutor(max_workers=20)
for result in pool.map(crawler, urls):
    ...
