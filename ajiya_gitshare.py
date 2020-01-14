# -*- coding: utf-8 -*-
# $B$"$8$d$N$*J[Ev%a%K%e!<DLCN%7%9%F%`(B
# line notify$B$r;HMQ(B
# cron$B$rMQ$$$FKhD+(B9$B;~$K$3$N%U%!%$%k$,<B9T$5$l$k(B
# crontab -l$B$GDj;~<B9T%U%!%$%k$N%j%9%H!"(Bcrontab -e$B$GJT=8$,2DG=(B

import requests
from bs4 import BeautifulSoup
import os
import glob
import re
import datetime

def main():
	weekday = datetime.date.today().weekday()
	# $BEZF|$ODLCN$7$J$$(B ---
	if weekday != 5 and weekday !=6:
		detail = scraping()
		send_line(detail)
	else:
		pass

# $B%9%/%l%$%T%s%0(B ---
def scraping() -> str:
	r = requests.get('http://ajiya1.com/archives/category/higawari')
	soup = BeautifulSoup(r.content, 'html.parser')
	details = soup.find('div', class_='entry-post')
	thumb_img = soup.find('img', class_='attachment-large-thumb size-large-thumb wp-post-image')
	img_url = thumb_img.get('src')
	img = requests.get(img_url)

	# $B%G%#%l%/%H%j$,$"$k$H$-$O$=$3$KJ]B8(B ---
	try:
		with open('[PATH TO ajiya]/data/' + re.split('[/]', img_url)[-1], 'wb') as f:
			f.write(img.content)

	# $BL5$$>l9g:n@.(B ---
	except FileNotFoundError:
		os.mkdir('[PATH TO ajiya]/data/')
		with open('[PATH TO ajiya]/data/' + re.split('[/]', img_url)[-1], 'wb') as f:
			f.write(img.content)

	return details.text

# Line Notify API$B$X$N(BPOST ---
def send_line(detail: str):
	url = 'https://notify-api.line.me/api/notify'
	token = 'Your Token'
	headers = {'Authorization': 'Bearer ' + token}
	payload = {'message' :  detail[:-2]}

	# $B2?$,0c$&$s$+CN$i$s$1$I(Bjpg$B$8$c$J$/$F(Bjpeg$B$i$7$$$N$GJQ49(B ---
	f = glob.glob('[PATH TO ajiya]/data/*.jpg')
	f = f[0]

	command = 'convert {0} -quality 50 [PATH TO ajiya]/data/converted.jpeg'.format(f)
	os.system(command)

	converted_f = glob.glob('{PATH TO ajiya]/data/*.jpeg')
	converted_f = converted_f[0]

	files = {'imageFile': open(converted_f, 'rb')}

	# POST ---
	r = requests.post(url, headers=headers, params=payload, files=files)

	# $B<L??$$$i$s$N$G:o=|(B(PATH$B$r4V0c$($k$H;`$L$N$G5$$r$D$1$k(B) ---
	command = 'rm -rf [PATH TO ajiya]/data/*'
	os.system(command)

if __name__ == '__main__':
	main()
