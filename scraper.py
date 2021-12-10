from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

youtube_video_url = "https://www.youtube.com/feed/trending"

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  driver.get(youtube_video_url)
  videos = driver.find_elements(By.TAG_NAME,'ytd-video-renderer')
  return videos

def parse_video_information(video):

  video_title = video.find_element(By.ID,"video-title").text
  video_URL = video.find_element(By.ID,"video-title").get_attribute('href')
  Thumbnail_URL = video.find_element(By.TAG_NAME,'img').get_attribute('src')
  Channel_Name = video.find_element(By.CLASS_NAME,'ytd-channel-name').text
  description = video.find_element(By.ID,'description-text').text

  return {
    'Video Title':video_title,
   'Video URL': video_URL,
   'Thumbnail URL':Thumbnail_URL,
   'Channel Name':Channel_Name,
   'Description':description
  }

if __name__== "__main__":

  #initiate the driver element
  driver = get_driver()

  #Fetching trending videos
  videos = get_videos(driver)

  print(f'Found {len(videos)} videos')

  print("Parsing information for top 10 videos...")

  video_data = [parse_video_information(video) for video in videos[0:10]]

  print("Saving the data to CSV")

  videos_df = pd.DataFrame(video_data)

  videos_df.to_csv('trending.csv',index=False)

  #print(videos_df)



