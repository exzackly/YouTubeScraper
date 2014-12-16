import os
import re
import urllib.request

songsToFetch = []
searchType = 0 #0 - songs 1-7 | 1 - songs 8-20 | 2 - noLyricSearch

print('TAGS: #MSS = songs 8-20 | #NLS = no lyrics')
while 1==1:
    songDetails = input('Input song and artist name: ')
    if songDetails == 'q':
        break
    elif songDetails == '#MSS':
        searchType = 1
        print('moreSongSearch selected')
    elif songDetails == '#NLS':
        searchType = 2
        print('noLyricSearch selected')
    else:
        songsToFetch.append(songDetails)

for songDetail in songsToFetch:
    print('Starting ' + songDetail.upper() + '...')
    songDetail = songDetail.replace(' ','+')
    songDetail = songDetail.replace('&', '%26')
    urlToScrape = 'http://www.youtube.com/results?search_query=' + songDetail + '+lyrics'
    RawPageSource = urllib.request.urlopen(urlToScrape)
    ReadablePageSource = RawPageSource.read()
    extractedURLs = re.findall('data-context-item-id="(.+?)"', str(ReadablePageSource))
    if searchType == 0:
        extractedURLs = extractedURLs[1:8]
    elif searchType == 1:
        extractedURLs = extractedURLs[8:]
    elif searchType == 2:
        urlToScrape = 'http://www.youtube.com/results?search_query=' + songDetail
        RawPageSource = urllib.request.urlopen(urlToScrape)
        ReadablePageSource = RawPageSource.read()
        extractedURLsNoLyrics = re.findall('data-context-item-id="(.+?)"', str(ReadablePageSource))
        extractedURLs = extractedURLs[1:]
        extractedURLsNoLyrics = extractedURLsNoLyrics[1:]
        uniqueExtractedURLs = []
        for URL in extractedURLsNoLyrics:
            if URL in extractedURLs:
                continue
            else:
                uniqueExtractedURLs.append(URL)
        extractedURLs = uniqueExtractedURLs

    print('Downloading videos...')
    for URL in extractedURLs:
        downloadLink = 'http://www.youtube.com/watch?v=' + URL
        os.system('("' + os.getcwd() + '\\' + 'youtube-dl.exe" ' + downloadLink + ')');
    
print('Done downloading videos... Converting to mp3')
for file in os.listdir(os.getcwd()):
    if file.endswith(".mp4"):
        ffmpegDir = '"' + os.getcwd() + r'\ffmpeg.exe"'
        inputFileName = '"' + os.getcwd() + '\\' + file + '"'
        outputFileName = '"' + os.getcwd() + '\convertedFiles' + '\\' + file[:len(file)-4] + '.mp3"'
        os.system('(' + ffmpegDir + r' -i ' + inputFileName + r' -b:a 256k -vn ' + outputFileName + ')');
        os.remove(file)

print('Conversion completed!')
