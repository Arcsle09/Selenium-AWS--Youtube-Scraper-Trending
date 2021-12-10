import requests

from bs4 import BeautifulSoup

youtube_video_url = "https://www.youtube.com/feed/trending"

response = requests.get(youtube_video_url)

#with open("yotube_trending_page.html",'w') as trend:
#  trend.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')

#print(doc)

#find all the video divs
video_divs = doc.find_all('div',class_='style-scope ytd-video-renderer')

print(f'Found {len(video_divs)} videos')