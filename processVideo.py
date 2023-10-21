import time
import subprocess
import json 
import os
import glob
from glob import glob
import requests
from requests.exceptions import ChunkedEncodingError
import shutil
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

OUTPUT_EXT = ".final.mp4"

def get_m3u8_urls(driver, url): 
   driver.get(url)
   driver.execute_script("window.scrollTo(0, 10000)")
   time.sleep(20)
   logs = driver.get_log("performance")
   url_list = []
  
   for log in logs:
    network_log = json.loads(log["message"])["message"]

    if (
        "Network.response" in network_log["method"]
        or "Network.request" in network_log["method"]
        or "Network.webSocket" in network_log["method"]
    ):
        if 'request' in network_log["params"]:
            if 'url' in network_log["params"]["request"]:
                url = network_log["params"]["request"]["url"]
                if any(extension in url for extension in ['.m3u8', '.mp4', '.mp3', '.aac']) or "googlevideo.com/videoplayback" in url:
                    if "blob" not in url:
                        url_list.append(url)
 
   return url_list

def cleanUp(filename):
    directory = os.path.dirname(os.path.realpath(__file__))
    pattern = os.path.join(directory, filename)
    file_paths = glob(f"{pattern}*")
    for file_path in file_paths:
        if (not file_path.endswith(OUTPUT_EXT)):
            os.remove(file_path)

def getAudioAndVideoFiles(filename):
    initialVideo = f"{filename}.mp4"
    firstAudio = f"{filename}-1.mp3"
    secondAudio = f"{filename}-2.mp3"

    size1 = os.path.getsize(firstAudio)
    size2 = os.path.getsize(secondAudio)
    size3 = os.path.getsize(initialVideo)
   

    potentialHDVideoFile = ""
    audioFile = ""
    videoFile = ""

    if size1 < size2:
        audioFile = firstAudio
        potentialHDVideoFile = secondAudio
    elif size1 > size2:
        audioFile = secondAudio
        potentialHDVideoFile = firstAudio
    else:
        audioFile = firstAudio
        potentialHDVideoFile = secondAudio

    hdSize = os.path.getsize(potentialHDVideoFile)

    if hdSize < size3:
        videoFile = initialVideo
    elif hdSize > size2:
        videoFile = potentialHDVideoFile
    else:
        videoFile = initialVideo

    return (videoFile, audioFile)

#need to do brew install ffmpeg for video download to work
def combineAudioWithVideo(filename):
    try:
        video, audio = getAudioAndVideoFiles(filename)

        fullFile = f"{filename}{OUTPUT_EXT}"

        subprocess.run(['ffmpeg', '-i', video, '-i', audio, '-c', 'copy', f"{fullFile}"])
        shutil.copy2(fullFile, './videos')
        os.remove(fullFile)

        cleanUp(filename)

        print("Video saved to", fullFile)
    except Exception as e:
        print("Error during processing of video")
        cleanUp(filename)
        raise e
        


def download_file_with_retry(url, filename):
    chunk_size = 1024 * 1024  # 1MB by default
    content_length = None
    max_retries = 3  # You can adjust the number of retries as needed

    for attempt in range(max_retries):
        with open(filename, 'wb') as f:
            try:
                # Make the initial request
                response = requests.get(url, stream=True)

                if 'content-length' in response.headers:
                    content_length = int(response.headers['content-length'])

                bytes_received = 0

                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        bytes_received += len(chunk)

                if content_length is None or bytes_received >= content_length:
                    break  # File download complete or content length is unknown

                # Retry the download to get the missing part
                range_header = {'Range': f'bytes={bytes_received}-'}
                response = requests.get(url, headers=range_header, stream=True)
            except ChunkedEncodingError:
                if attempt < max_retries - 1:
                    print(f"ChunkedEncodingError: Retrying (attempt {attempt + 1})")
                else:
                    print(f"ChunkedEncodingError: Cannot Download")  # Raise the exception if max retries are reached
                    raise "Encoding Error"

                

    return filename

  

def downloadVideo(driver,url, filename, youtube = 0):
    url_list = get_m3u8_urls(driver, url)
    mediaFiles = []
    if(len(url_list) <= 0):
        return "Not Found"
    for url in url_list:
        if(youtube == 1):
            mediaFiles.append(url.split("range")[0])
        else:     
            mediaFiles.append(url.split("bytestart")[0])
    download_file_with_retry(mediaFiles[0], f"{filename}.mp4")
    
    for index in [-1, -2]:
        download_file_with_retry(mediaFiles[index],f"{filename}{index}.mp3" )
            
    combineAudioWithVideo(filename)
    
