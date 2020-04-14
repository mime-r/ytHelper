import sys
import urllib.request, urllib.error
from os import system, path
import os
import warnings
import socket
from time import time
#test: https://www.youtube.com/watch?v=ZW0evffIxEM
"""
Changelog:
v1.1
- Added time counter
- Removed redundant code
- Fixed bugs
v1.2
- Removed a lot of redundant code
- Fixed more bugs
"""
class Application(object):
    welcome = """
            #     #                                    An  
#   # ##### #     # ###### #      #####  ###### #####  Advanced
 # #    #   #     # #      #      #    # #      #    # Tool
  #     #   ####### #####  #      #    # #####  #    # For
  #     #   #     # #      #      #####  #      #####  Downloading
  #     #   #     # #      #      #      #      #   #  Youtube
  #     #   #     # ###### ###### #      ###### #    # Videos
ytHelper v1.1 stable CLI
© Samuel Cheng 2020
GNU AGPL v3.0
"""
    instructions_fordownloading = """
INSTRUCTIONS
[1] video + audio
[2] video
[3] audio
[4] thumbnail (High Quality)
[5] generate captions
[6] exit to homescreen
[7] to exit
"""
    
    def __init__(self):
        
        
        #For URL validating
        
        #Check if pytube is downloaded
        #Phase 1: Check Pytube module
        print("[*] checking if pytube installed...")
        try:
            import pytube
            
        except ModuleNotFoundError:
            #If pytube not installed
            print("[!] pytube not installed!")
            if input("Do you want to install pytube? (y/n)") == "y":
                print("[*] installing pytube...")
                status = system("pip install pytube")
                
                if status == 0:
                    print("[*] pytube installed!")
                else:
                    print("[critical] could not install pytube!\ninstall in Command Prompt or Powershell using \"pip install pytube\"")
                    sys.exit(0)
            else:
                print("[!] ytHelper cannot run without pytube!\nInstall pytube and run again...")
                sys.exit(-1)

        #Phase 2: Check glib installed
        #Phase 3: Initialise variables
        self.kb = ""
        self.url = ""
        self.dir = ""
        self.itag = ""
        #self.time = time()

        #End Phase: home()
        self.home()

        
    def home(self):
        #_location = 1
        print(Application.welcome)

        self.start()


    def parse(self, _input, _location):
        #home
        if _location == 1:
            if _input == 1:
                self.start()
            elif _input == 2:
                sys.exit(0)
        #start
        elif _location == 2:
            self.checkExit(_input)
            if not "youtube.com" in _input:
                print("[!] not a youtube website")
                self.start()
            if _input.startswith("www."):
                _input = "https://" + _input
            if _input.startswith("youtube.com"):
                _input = "https://www." + _input

                
            print("[*] final url is: "+_input)
            if not self.validate(_input):
                print("[!] this youtube website does not exist!")
                self.start()
            if _input.endswith("youtube.com"):
                print("[!] not a video url")
                self.start()
            self.url  = _input #final

        #downloading_options
                ###############################TODO
        elif _location == 4:
            self.checkExit(_input)
            _input = int(_input)
            if _input == 1:
                self.videoandaudio()
            elif _input == 2:
                self.videoaudio(1)
            elif _input == 3:
                self.videoaudio(2)
            elif _input == 4:
                self.get_thumbnail()
            elif _input == 5:
                self.generate_captions()
            elif _input == 6:
                self.home()
            elif _input == 8:
                sys.exit(0)
            else:
                print("[!] option does not exist!")
                self.home()
                
        #generate captions
        elif _location == 5:
            flag = False
            warnings.filterwarnings("ignore")
            for element in self.yt.captions.all():
                if element.code == _input:
                    flag = True
            if flag:
                print("[*] captions found!")
                return _input
            else:
                print("[!] language code not valid!")
                self.generate_captions()
            
            
            
    def generate_captions(self):
        download = r"""
[enter] for default download folder
[directory] for custom download folder e.g. C:\Users\john\Downloads
"""
        

        warnings.filterwarnings("ignore")
        caption = self.yt.captions.all()
        if len(caption) == 0:
            print("[!] no captions are available!")
        for line in caption:
            print(line)
        #_location = 5
        language_code = self.parse(input("Enter a language code (e.g. en): "), 5)
        self.kb = input(download)
        if not self.kb:
            self.finddir()
        else:
            self.dir = self.kb
        try:
            #create text file and writes caption into the file
            completeName = path.join(self.dir, self.yt.title + "_srt_{}.txt".format(language_code))
            caption_file = open(completeName, "w")
            caption_file.write(self.yt.captions.get_by_language_code(language_code).generate_srt_captions())
            caption_file.close()
        except:
            print("[!] custom directory does not exist!")
            self.videoandaudio()
        print("[*] success! captions written to .txt file in {}".format(self.dir))        
        self.home()
    def get_thumbnail(self):
        print("[*] Generating thumbnail link...")
        print("[*] {}".format(self.yt.thumbnail_url))
        self.home()
    
    def videoaudio(self, _type):
        instructions = """
[iTag] to download
[e] to exit to home
"""
        download = r"""
[enter] for default download folder
[directory] for custom download folder e.g. C:\Users\john\Downloads
"""

        warnings.filterwarnings("ignore")
        for entry in self.yt.streams.filter(adaptive = True).all():
            if entry.mime_type.startswith("video") and _type == 1:
                print(entry)
            elif entry.mime_type.startswith("audio") and _type == 2:
                print(entry)
        self.itag = input(instructions)
        self.checkExit(self.kb)

        try:
            self.itag = int(self.itag)
            self.yt.streams.get_by_itag(self.itag)
        except:
            print("[!] either itag does not exist or not an integer")
            self.videoandaudio()
        self.kb = input(download)
        if not self.kb:
            self.finddir()
        else:
            self.dir = self.kb
        try:
            print("Downloading: {0} \n{1}".format(self.yt.title, self.dir))
            self.yt.streams.get_by_itag(self.itag).download(self.dir)
        except:
            print("[!] custom url does not exist!")
            self.videoandaudio()
        print("[*] success!")
        self.home()

    def videoandaudio(self):
        instructions = """
[iTag] to download video and audio
[e] to exit
"""
        download = r"""
[enter] for default download folder
[directory] for custom download folder e.g. C:\Users\john\Downloads
"""

        warnings.filterwarnings("ignore")
        for entry in self.yt.streams.filter(progressive = True).all():
            print(entry)
        self.itag = input(instructions)
        self.checkExit(self.itag)

        try:
            self.itag = int(self.itag)
            self.yt.streams.get_by_itag(self.itag)
        except:
            print("[!] either itag does not exist or not an integer")
            self.videoandaudio()
        self.kb = input(download)
        if not self.kb:
            self.finddir()
        else:
            self.dir = self.kb
        try:
            print("Downloading: {0} \n{1}".format(self.yt.title, self.dir))
            self.yt.streams.get_by_itag(self.itag).download(self.dir)
        except:
            print("[!] custom directory does not exist!")
            self.videoandaudio()
        print("[*] success!")
        self.home()

    def start(self):
        from pytube import YouTube
        #Phase 1: enter url
        self.url = input("Youtube URL (video): ")
        self.parse(self.url, 2)
        #Phase 2: check if url is playlist or song
        try:
            self.yt = YouTube(self.url)
        except:
            print("Video not found!\nCheck whether you have YouTube Restrictions or your video exists!")
            self.start()
        print("Title: {title}".format(title = self.yt.title))
        self.downloading_options()
            
    def downloading_options(self):
        try:
            self.kb = input(Application.instructions_fordownloading)
        except:
            print("[*] please enter an integer")
            self.downloading_options()
        #_location = 4
        self.parse(self.kb, 4)
            

    def checkExit(self, _input):
        _input = _input.lower()
        if _input == "e" or _input == "exit":
            sys.exit(0)

    
    def validate(self, _url):
        conn = urllib.request.urlopen(_url)
        try:
            conn = urllib.request.urlopen(_url)
        except:
            return False
        else:
            return True

    
    def exit(self):
        print("Exiting!")
        sys.exit(0)


    def internet_check(self):
        print("[*] checking internet connection")
        self.time = time()
        try:
            socket.create_connection(("www.google.com", 80))
            print("[*] connected! ({} seconds)".format(round(time()-self.time, 5)))
        except OSError:
            print("[!] no internet connection!\n[!] this program requires internet connection")
            sys.exit(-1)
            
    def finddir(self):
        self.dir = path.join(path.expanduser("~"), "Downloads")
        
if __name__ == "__main__":
    try:
        Application.internet_check(Application)
        Application()
    except:
        
        print("[!] An unknown error has occured!")
        sys.exit(-1)
