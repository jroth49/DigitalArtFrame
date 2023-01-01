import requests;
import json;
import shutil;
import csv;
from bs4 import BeautifulSoup;
import html5lib;
from PIL import Image;
import os

urls = ['https://www.saatchiart.com/paintings/modern?hitsPerPage=100&sort=newest',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=default',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=newest',
	   'https://www.saatchiart.com/paintings/fine-art?hitsPerPage=100&sort=newest',
	   'https://www.saatchiart.com/paintings/modern?hitsPerPage=100&sort=newest',
	   'https://www.saatchiart.com/paintings/surrealism?hitsPerPage=100&sort=newest',
	   'https://www.saatchiart.com/paintings/realism?hitsPerPage=100&sort=newest',
	   'https://www.saatchiart.com/paintings/expressionism?hitsPerPage=100&sort=newest',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=newest&subject=abstract',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=newest&subject=landscape',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=newest&subject=portrait',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=newest&subject=architecture',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=newest&subject=seascape',
	   'https://www.saatchiart.com/paintings?hitsPerPage=100&sort=newest&subject=outer-space',
	   ]


def isEnglish(s):
	return s.isascii();

for url in urls:
	h = {
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.9',
	'cache-control': 'max-age=0',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Linux"',
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'none',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36'
}
	
	
	r = requests.get(url, headers=h);
	soup = BeautifulSoup(r.content, 'html5lib');

	images = soup.find_all('figure'); #holds all the figure elements that holds image link, image height/width, artist, artistfrom, price$$

	for i in images:
		imageLink = i.find_all('div', {'data-type': 'artwork-image'})[0].find_all('a')[0].find_all('picture')[0].find_all('img')[0];
		
		if imageLink.has_attr('class'):
			imageLink = imageLink['data-src'];
		else:
			imageLink = imageLink['src'];
		
		artName = i.find_all('div', {'data-type': 'original'})[0].find_all('div', {'data-style': 'row'})[0].find_all('div', {'data-style': 'column'})[0].find_all('p', {'data-type': 'main'})[0].find_all('a')[0].decode_contents();
		
		artName = artName.replace('/', '');
		artName = artName.replace(' ', '-');
		artName = artName.replace('#', '');
		
		if not isEnglish(artName):
			artName = 'Unknown';
		
		artistName = i.find_all('div', {'data-type': 'original'})[0].find_all('div', {'data-style': 'row'})[1].find_all('div', {'data-type': 'artist-info'})[0].find_all('p', {'data-type': 'main'})[0].find_all('a')[0].decode_contents();
		
		artistName = artistName.replace('<!-- -->', '');
		artistName = artistName.replace(' ', '-');
		if not isEnglish(artistName):
			artistName = 'Unknown';
		
		artistLocation = i.find_all('div', {'data-type': 'original'})[0].find_all('div', {'data-style': 'row'})[1].find_all('div', {'data-type': 'artist-info'})[0].find_all('p', {'data-type': 'sub'})[0].decode_contents();
		
		artistLocation = artistLocation.replace(' ', '-');
		if not isEnglish(artistLocation):
			artistName = 'Unknown';
		
		price = i.find_all('div', {'data-type': 'original'})[0].find_all('div', {'data-style': 'row'})[1].find_all('div', {'data-type': 'prices'})[0].find_all('p')[0].decode_contents();

		price = price.replace('$', '');
		price = price.replace(',', '');

		print('Downloading ' + artName + ' by ' + artistName + '. ' + artistLocation + ': ' + price);
		imageLink = imageLink[:len(imageLink) - 5] + '8.jpg'

		imgDownload = requests.get(imageLink, headers = h);
		file = open('pending/' + artName + '_' + artistName + '_' + artistLocation + '_' + price, 'wb');
		file.write(imgDownload.content);
		file.close();
		

		


	pending_files = os.listdir('pending');

	for p in pending_files:	
		img = Image.open('pending/' + p);
		w, h = img.size
		img.close();

		if w > h:
			shutil.move('/home/jack/Documents/Art/pending/' + p, '/home/jack/Documents/Art/art/Landscape/' + p);
		if w < h:
			shutil.move('/home/jack/Documents/Art/pending/' + p, '/home/jack/Documents/Art/art/Portrait/' + p);
		if w == h:
			shutil.move('/home/jack/Documents/Art/pending/' + p, '/home/jack/Documents/Art/art/Square/' + p);







'''
#this reads the csv file to get the url of the iamge, and it details, height/width
with open('artapi.csv', 'r') as f:
	count = 104200;
	reader = csv.reader(f.readlines()[count:])
	for row in reader:			#row[1] = image details file row[2] = image download file row[5] = width row[6] = height
		count = count + 1;
		folder = 'Portrait';
		
		urlData = row[1];
		responseData = requests.get(urlData);
		jsonData = json.loads(responseData.text);
		if jsonData['width'] > jsonData['height']:
			folder = 'Landscape';
		if jsonData['width'] < jsonData['height']:
			folder = 'Portrait';
		if jsonData['width'] == jsonData['height']:
			folder = 'Square';
			
		urlDownload = row[2];
		responseDownload = requests.get(urlDownload, stream = True);
		with open(folder + '/' + folder + str(count), 'wb') as f:
			shutil.copyfileobj(responseDownload.raw, f)	
			
		print(str(count) + ' / 104,348 pictures downloaded');
			
'''
