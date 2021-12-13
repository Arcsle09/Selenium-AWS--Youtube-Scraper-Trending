from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os
import json


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

def send_email(Filename,Body):
  SENDER_EMAIL = 'arcsle09webscrape@gmail.com'
  RECEIVER_EMAIL = 'arcsle09webscrape@gmail.com'
  SENDER_PASSWORD = os.environ['SENDER_PASSWORD']
  print(SENDER_PASSWORD)
  msg = MIMEMultipart('mixed')
  msg['Subject'] = 'Youtube Trending Videos'
  msg['From'] = SENDER_EMAIL
  msg['To'] = RECEIVER_EMAIL
  text1 = MIMEText(Body,'plain')
  msg.attach(text1)
  attachment = MIMEBase('application',"octet-stream")
  attachment.set_payload(open(Filename,"rb").read())
  encoders.encode_base64(attachment)
  attachment.add_header('content-disposition',"attachment", filename= Filename)
  msg.attach(attachment)
  try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(SENDER_EMAIL,SENDER_PASSWORD)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.close()
    print("Email Sent !!")
  except:
    print('Something went wrong...')

if __name__== "__main__":

  #initiate the driver element
  driver = get_driver()

  #Fetching trending videos
  videos = get_videos(driver)

  print(f'Found {len(videos)} videos')

  print("Parsing information for top 10 videos...")

  video_data = [parse_video_information(video) for video in videos[0:10]]

  print("Saving the data to excel")

  videos_df = pd.DataFrame(video_data)

  videos_df.to_csv('trending.csv',index=False)

  print("Sending an email with results")

  Body = json.dumps(video_data,indent = 2)
  send_email('trending.csv',Body)




