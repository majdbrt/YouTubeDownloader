from pytube import YouTube
# hello
print('Welcome to this Youtube downloader!')

savePath = input("Enter the download's path: ")
if savePath == 'default' or savePath == 'Default':
    savePath = r"C:\Users\majdb\Videos"
url = input("Enter the video's url: ")
try:
    video = YouTube(url)
except:
    print("Connot retrieve video")

def getResolution():
    quality = input("Enter video's resolution: ")
    if quality == 'default' or quality == 'Default':
        return  '360p'
    elif quality == '144p' or quality == '240p' or quality == '360p' or quality == '480p':
        return quality
    else:
        print('Enter a valid resolution')
        getResolution()

quality = getResolution()

stream = video.streams.filter(file_extension='mp4',res= quality, progressive='True')

def getTag(stream):
    [[key, value]] = stream.itag_index.items()
    return key

tag = getTag(stream)


d_video = video.streams.get_by_itag(tag)
try:
    # downloading the video
    d_video.download(savePath)
except:
    print("Some Error!")

print('Video Downloaded Successfully!')