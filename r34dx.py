import urllib.request, os, time, sys
from format import out
from bs4 import BeautifulSoup

def main():
	APIUrl = "https://rule34.xxx/index.php?page=dapi&s=post&q=index"
	PageSize = 100
	global query
	query = input("What am I searching for? ")
	query = query.replace(" ", "+")
	tags = "&tags=" + query
	url = APIUrl + tags
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html, features="xml")
	url = str(soup.getText)
	url = str(url)
	#out.debug(f"URL: {url}")
	url = url.split('file_url="')
	for item in url:
		test = str(item)
		url = test
		if test.startswith("//img"):
			url = url.replace('="', "")
			url = url.split(" ")
			url = url[0]
			url = url.replace('"', "")
			url = url.replace("//", "https://")
			url = url + "\n"
	global imglist
	imglist = []
	for furl in soup.find_all('post'):
		#out.debug(f'File URL: {(furl["file_url"])}')
		imglist.append(furl["file_url"])
	#out.debug(imglist)
	download(imglist)

def download(urls):
	image = urls
	#out.debug(image)
	dir_name = query
	try:
		os.mkdir(dir_name)
	except:
		pass
	print(f"Downloading {str(len(urls))} images")
	for image in urls:
		image = str(image)
		name = image.split("/")[5]
		if ".webm" in name or ".mp4" in name:
			out.info("Downloading a WEBM or MP4 takes a bit longer...")
			#out.debug("Retrieving URL for WEBM/MP4")
			urllib.request.urlretrieve(image, f"{dir_name}/{name}")
			out.info(f"Finished downloading video: {name}")
			os.system(f'notify-send "R34D: Finished downloading video."')
		time.sleep(2)
		#out.debug("Sleeping for 2 seconds on URLRead for WEBM.")
		#out.debug(f"Downloading {name} with URL: {image}")
		time.sleep(2)
		#out.debug("Sleeping for 2 seconds on URLRead function.")
		with urllib.request.urlopen(image) as f:
			imageContent = f.read()
		with open(f"{dir_name}/{name}", "wb") as f:
			f.write(imageContent)
			out.info(f"Finished downloading image: {name}")

main()
