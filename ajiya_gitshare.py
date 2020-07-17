# -*- coding: utf-8 -*-
# あじやのお弁当メニュー通知システム
# line notifyを使用
# cronを用いて毎朝9時にこのファイルが実行される
# crontab -lで定時実行ファイルのリスト，crontab -eで編集が可能

import requests
from bs4 import BeautifulSoup
import os
import glob
import re
import datetime

def main():
    weekday = datetime.date.today().weekday()
    # 土日は通知しない ---
    if weekday != 5 and weekday !=6:
        detail = scraping()
        send_line(detail)
        today = datetime.datetime.today()
        print(str(today.year) + '年' + str(today.month) + '月' + str(today.day) + '日' + '：OK')
    else:
        pass

# スクレイピング ---
def scraping() -> str:
    r = requests.get('http://ajiya1.com/archives/category/higawari')
    soup = BeautifulSoup(r.content, 'html.parser')
    details = soup.find('div', class_='entry-post')
    thumb_img = soup.find('img', class_='attachment-large-thumb size-large-thumb wp-post-image')
    img_url = thumb_img.get('src')
    img = requests.get(img_url)

    # ディレクトリがある時はそこに保存 ---
    try:
        with open('[PATH TO ajiya]/data/' + re.split('[/]', img_url)[-1], 'wb') as f:
            f.write(img.content)

    # 無い場合作成 ---
    except FileNotFoundError:
        os.mkdir('[PATH TO ajiya]/data/')
        with open('[PATH TO ajiya]/data/' + re.split('[/]', img_url)[-1], 'wb') as f:
            f.write(img.content)

    return details.text

# Line Notify APIへのPOST ---
def send_line(detail: str):
    url = 'https://notify-api.line.me/api/notify'
    token = 'Your Token'
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message' :  detail[:-2]}

    # 何が違うんか知らんけどjpgじゃなくてjpegらしいので変換 ---
    f = glob.glob('[PATH TO ajiya]/data/*.jpg')
    f = f[0]

    command = 'convert {0} -quality 50 [PATH TO ajiya]/data/converted.jpeg'.format(f)
    os.system(command)

    converted_f = glob.glob('{PATH TO ajiya]/data/*.jpeg')
    converted_f = converted_f[0]

    files = {'imageFile': open(converted_f, 'rb')}

    # POST ---
    r = requests.post(url, headers=headers, params=payload, files=files)

    # 写真いらんので削除(PATHを間違えると死ぬので気をつける) ---
    command = 'rm -rf [PATH TO ajiya]/data/*'
    os.system(command)

if __name__ == '__main__':
    main()
