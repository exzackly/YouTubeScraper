from tkinter import *
import tkinter
import os
import re
import urllib.request
import subprocess
import threading

#application variables
songsToFetch = []
searchType = 0 #0 - songs 1-7 | 1 - songs 8-20 | 2 - noLyricSearch
version = float(open('version.txt', 'r').read())

#GUI window initialization
root = tkinter.Tk()
root.minsize(width=430, height=170)
root.maxsize(width=430, height=170)
root.resizable(0,0)
root.wm_title('YouTubeScraper by EXZACKLY v.' + str(version))

#welcome label initialization
infoLabelVar = StringVar()
infoLabel = Label(root, textvariable = infoLabelVar)
infoLabelVar.set('Welcome to YouTubeScraper by EXZACKLY')
infoLabel.pack()
infoLabel.place(bordermode=OUTSIDE, x = 105)

#invoke when updateYoutubeDLButton is pressed
def updateYoutubeDLButtonPressed():
    os.system('youtube-dl.exe -U')
    updateYoutubeDLButton = Button(root, text='Update Youtube-dl', command= updateYoutubeDLButtonPressed, state = 'disabled')
    updateYoutubeDLButton.place(bordermode=OUTSIDE, x = 90, y = 25)

#button to update youtube-dl initialization
updateYoutubeDLButton = Button(root, text='Update Youtube-dl', command= updateYoutubeDLButtonPressed, state = 'disabled')
updateYoutubeDLButton.pack()
updateYoutubeDLButton.place(bordermode=OUTSIDE, x = 90, y = 25)

#invoke when updateYoutubeScraperButton is pressed
def updateYoutubeScraperButtonPressed():
    os.system('git pull')
    updateYoutubeScraperButton = Button(root, text='Update YoutubeScraper', command= updateYoutubeScraperButtonPressed, state = 'disabled')
    updateYoutubeScraperButton.place(bordermode=OUTSIDE, x = 210, y = 25)

#button to update youtubeScraper initialization
updateYoutubeScraperButton = Button(root, text='Update YoutubeScraper', command= updateYoutubeScraperButtonPressed, state = 'disabled')
updateYoutubeScraperButton.pack()
updateYoutubeScraperButton.place(bordermode=OUTSIDE, x = 210, y = 25)

#invoke when a searchTypeRadioButton is selected
def searchTypeChanged(senderValue):
    global searchType
    searchType = senderValue
    
#search type radio button initialization
searchTypeRadioButton1 = Radiobutton(root, variable = 7, value = 1, text = 'Songs 1-7', command = lambda: searchTypeChanged(0))
searchTypeRadioButton2 = Radiobutton(root, variable = 7, value = 2, text = 'More Song Search (8-20)', command = lambda: searchTypeChanged(1))
searchTypeRadioButton3 = Radiobutton(root, variable = 7, value = 3, text = 'No Lyric Search', command = lambda: searchTypeChanged(2))
searchTypeRadioButton1.pack()
searchTypeRadioButton2.pack()
searchTypeRadioButton3.pack()
searchTypeRadioButton1.place(bordermode=OUTSIDE, x = 30, y = 50)
searchTypeRadioButton2.place(bordermode=OUTSIDE, x = 110, y = 50)
searchTypeRadioButton3.place(bordermode=OUTSIDE, x = 270, y = 50)
searchTypeRadioButton1.select()

#add song label initialization
addSongInfoLabelVar = StringVar()
addSongInfoLabel = Label(root, textvariable = addSongInfoLabelVar)
addSongInfoLabelVar.set('Enter New Song:')
addSongInfoLabel.pack()
addSongInfoLabel.place(bordermode=OUTSIDE, x = 10, y = 80)

#invoke when addSongButton or enter is pressed
def addSongButtonPressed(event):
    if songEntryTextfield.get() == '':
	    downloadSongsButtonPressed()
	    return
    songsToFetch.append(songEntryTextfield.get())
    songEntryTextfield.delete(0, tkinter.END)
    songsToSearchTextArea = Text(root, height = len(songsToFetch)+1, width = 50)
    songsToSearchTextArea.insert(INSERT, 'Queued Songs:')
    for index, item in enumerate(songsToFetch):
        songsToSearchTextArea.insert(INSERT, '\n' + str(index+1) + ' : ' + item)
    songsToSearchTextArea.place(bordermode=OUTSIDE, x = 10, y = 110)
    downloadSongsButton.place(bordermode=OUTSIDE, x = 150, y = 140+(len(songsToFetch)*16))
    root.minsize(width=430, height=170+(len(songsToFetch)*16))
    root.maxsize(width=430, height=170+(len(songsToFetch)*16))

#add song text field initialization
songEntryTextfield = Entry(root)
songEntryTextfield.bind('<Return>', addSongButtonPressed)
songEntryTextfield.pack()
songEntryTextfield.place(bordermode=OUTSIDE, x = 105, y = 82.5, width = 240)
songEntryTextfield.focus()

#add song button initialization
addSongButton = Button(root, text='Add Song', command= lambda: addSongButtonPressed(0))
addSongButton.pack()
addSongButton.place(bordermode=OUTSIDE, x = 350, y = 80)

#queued songs list initialization
songsToSearchTextArea = Text(root, height = 1, width = 50)
songsToSearchTextArea.insert(INSERT, 'Queued Songs:')
songsToSearchTextArea.pack()
songsToSearchTextArea.place(bordermode=OUTSIDE, x = 10, y = 110)

#invoke when downloadSongsButton is pressed
def downloadSongsButtonPressed():
    for songIndex, songDetail in enumerate(songsToFetch):
        print('Starting ' + songDetail.upper() + '...')
        songDetail = songDetail.replace(' ','+')
        songDetail = songDetail.replace('&', '%26')
        urlToScrape = 'http://www.youtube.com/results?search_query=' + songDetail + '+lyrics'
        ReadablePageSource = urllib.request.urlopen(urlToScrape).read()
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
            os.system('youtube-dl.exe ' + downloadLink + ' -o "convertedFiles/' + str(songIndex+1) + '%(title)s-%(id)s.%(ext)s" -x --audio-format "mp3" --audio-quality "256k"')
    root.destroy()

#download songs button initialization
downloadSongsButton = Button(root, text='Begin Download', command= downloadSongsButtonPressed)
downloadSongsButton.pack()
downloadSongsButton.place(bordermode=OUTSIDE, x = 150, y = 140)

#update check function
def updateCheck():
    youtubeDLPageSource = urllib.request.urlopen('https://ytdl-org.github.io/youtube-dl/download.html').read()
    currentYoutubeDLVersion = re.findall('/youtube-dl">(.+?)</a>', str(youtubeDLPageSource))[0]
    localYoutubeDLVersion = subprocess.check_output('youtube-dl.exe --version', shell=True).decode()[:-2]
    if currentYoutubeDLVersion != localYoutubeDLVersion:
        updateYoutubeDLButton = Button(root, text='Update Youtube-dl', command= updateYoutubeDLButtonPressed, foreground = 'red')
        updateYoutubeDLButton.place(bordermode=OUTSIDE, x = 90, y = 25)
    
    currentYoutubeScraperVersion = float(urllib.request.urlopen('https://raw.githubusercontent.com/exzackly/YouTubeScraper/master/version.txt').read())
    if currentYoutubeScraperVersion != version:
        updateYoutubeScraperButton = Button(root, text='Update YoutubeScraper', command= updateYoutubeScraperButtonPressed, foreground = 'red')
        updateYoutubeScraperButton.place(bordermode=OUTSIDE, x = 210, y = 25)
		
#dispatch update check to background thread
threading.Thread(target=updateCheck).start()

#present GUI window
root.mainloop()
