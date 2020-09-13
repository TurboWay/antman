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

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '__gads=ID=227efba24e897ba1:T=1599208355:S=ALNI_MbtWcmS-lrKu_DASa8CKA1pf9SuRQ; _ga=GA1.2.280986667.1599208355; _gid=GA1.2.1720620895.1599449018; footprints=eyJpdiI6InI2NVhZcEYzWFUzbGFnRVV4N293VkE9PSIsInZhbHVlIjoiMTZPNlwvVGJHQnU5eUY0cnA1TFZYQzhPRzRPV2tYZEVRczBlS1BSTGZDTEhwK1RzVXlJYWRtZGtzK044c2NWNXEiLCJtYWMiOiJkODNmYTVmNjkxNTA0OWZiOTk5MzE1OTIyZWE4ZWU2ODkxZDc3ZmQ1Y2IzZDE1OGRlMjc0NDM0MTU4N2RlYWVjIn0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlA1VGJiRlQzakJ6K2Y1SzN6Q0RVTmc9PSIsInZhbHVlIjoiMW1ib0pIdXRQV00zeWxvR28zeWdxNjUrTnRPVGxNRG5sb0lnclFHUlErYTV6YUhIUG5oRTJFRFduaFNOODNcL3VQb0FNaFdHRHQ1N0tjZ2xkWmo5cGlrVGtJeWhUbVRVbzZjNVlVR0RMaGFXYVN6YkdvbjdPcWtRWUlJRkc1ZGliTnZHTnBaOXBUVElWMUROdWRaT1ZZUjdxUGpLQ3FEMVlpdURlTFFLbEppOD0iLCJtYWMiOiJjZjUwNGI5YzMyYThhY2IzODRjYTdkMDhjNzNlYjZkZmMwZDQ0NDdlZGU3MDVhZGNiMzZmOGUyNzRjODY1OGQ3In0%3D; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1599786061,1599820355,1599833557,1599898723; XSRF-TOKEN=eyJpdiI6ImU2Wmp5cXRjMEVJS0pOWDFKWk1VcXc9PSIsInZhbHVlIjoielRqTkZyUUtHRWFJcTRLSGp1cVMxVHBFR1ZlQU5XNTc2Ymp6TUcxb0p3aUxocXU5cmo0VGtmR1VZcnVqRWVWYSIsIm1hYyI6IjZjOTg0Y2Y0YWJkZGZmYTAwYWNjZGNjYjExYjI3Mjk4ZWJiZTM5MDJhNTU1MmJkNGYwMDhjZGVkMmYxZDk1NjYifQ%3D%3D; glidedsky_session=eyJpdiI6Ikc1QUhPeVwvNDhReHRsXC8raGxUdHdUUT09IiwidmFsdWUiOiJSWUMxRlVOZzV1UzcyNHNhc0NQU3ByWmlqMmc1SmxRRzJjSWdkSXh2WnBzT3RWbTFCYVFZK3NTcEpyemJqcGlBIiwibWFjIjoiYzM1NWYyMjg1ZGZmNjEzNjFmM2U3Yzc2ZmIwZDIwMmRjYmExMGQ4MTkxZTkxNTkzZTJjNGQ3OGRmMjQ2ZmNiZCJ9; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1599898787',
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
