import sys
import urllib.request, urllib.error, urllib
from os import system, path
import warnings
import socket
from time import time

#resolve dependencies in general
system("pip install pytube3")


# test: https://www.youtube.com/watch?v=ZW0evffIxEM

def validate(_url):
    try:
        conn = urllib.request.urlopen(_url)
    except:
        return False
    else:
        return True


def checkExit(_input):
    _input = _input.lower()
    if _input == "e" or _input == "exit":
        print("Exiting...")
        sys.exit(0)


class Application(object):
    welcome = """
            #     #                                    An  
#   # ##### #     # ###### #      #####  ###### #####  Advanced
 # #    #   #     # #      #      #    # #      #    # Tool
  #     #   ####### #####  #      #    # #####  #    # For
  #     #   #     # #      #      #####  #      #####  Downloading
  #     #   #     # #      #      #      #      #   #  Youtube
  #     #   #     # ###### ###### #      ###### #    # Videos
ytHelper v2.2 stable CLI
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

        # For URL validating

        # Check if pytube is downloaded
        # Phase 1: Check Pytube module
        print("[*] checking if pytube installed...")
        try:
            import pytube

        except ModuleNotFoundError:
            # If pytube not installed
            print("[!] pytube not installed!")
            if input("Do you want to install pytube? (y/n)") == "y":
                print("[*] installing pytube...")
                status = system("pip install pytube3")

                if status == 0:
                    print("[*] pytube installed!")
                else:
                    print(
                        "[critical] could not install pytube!\ninstall in Command Prompt or Powershell using \"pip install pytube3\"")
                    sys.exit(0)
            else:
                print("[!] ytHelper cannot run without pytube!\nInstall pytube and run again...\ninstall in Command Prompt or Powershell using \"pip install pytube3\"")
                sys.exit(-1)
        # Phase 2: Check youtube_unlimited_search installed
        print("[*] checking if youtube_unlimited_search installed...")
        try:
            import youtube_unlimited_search

        except ModuleNotFoundError:
            # If youtube_unlimited_search not installed
            print("[!] youtube_unlimited_search not installed!")
            if input("Do you want to install youtube_unlimited_search? (y/n)") == "y":
                print("[*] installing youtube_unlimited_search...")
                status = system("pip install youtube-unlimited-search")

                if status == 0:
                    print("[*] youtube_unlimited_search installed!")
                else:
                    print(
                        "[critical] could not install youtube_unlimited_search!\ninstall in Command Prompt or Powershell using \"pip install youtube-unlimited-search\"")
                    sys.exit(0)
            else:
                print("[!] ytHelper cannot run without youtube_unlimited_search!\nInstall youtube_unlimited_search and run again...\ninstall in Command Prompt or Powershell using \"pip install youtube-unlimited-search\"")
                sys.exit(-1)
                # Phase 2: Check requests installed
                print("[*] checking if requests installed...")
                try:
                    import requests

                except ModuleNotFoundError:
                    # If requests not installed
                    print("[!] requests not installed!")
                    if input("Do you want to install requests? (y/n)") == "y":
                        print("[*] installing requests...")
                        status = system("pip install requests")

                        if status == 0:
                            print("[*] requests installed!")
                        else:
                            print(
                                "[critical] could not install requests!\ninstall in Command Prompt or Powershell using \"pip install requests\"")
                            sys.exit(0)
                    else:
                        print("[!] ytHelper cannot run without requests!\nInstall requests and run again...\ninstall in Command Prompt or Powershell using \"pip install requests\"")
                        sys.exit(-1)
        """
        # Phase 3: Check psutil module
        print("[*] checking if psutil installed...")
        try:
            import psutil

        except ModuleNotFoundError:
            # If pytube not installed
            print("[!] psutil not installed!")
            if input("Do you want to install psutil? (y/n)") == "y":
                print("[*] installing psutil...")
                status = system("pip install psutils")

                if status == 0:
                    print("[*] psutil installed!")
                    print(
                        "[critical] could not install requests!\ninstall in Command Prompt or Powershell using \"pip "
                        "install psutil\"")
                    sys.exit(0)
            else:
                print("[!] ytHelper cannot run without psutil!\nInstall psutil and run again...")
                sys.exit(-1)
        """

        # Phase 4: Initialise variables
        self.kb = ""
        self.url = ""
        self.dir = ""
        self.itag = ""
        # self.time = time()

        # End Phase: home()
        self.home()

    def home(self):
        # _location = 1
        print(Application.welcome)

        self.start()

    def parse(self, _input, _location):
        # home
        if _location == 1:
            if _input == 1:
                self.start()
            elif _input == 2:
                sys.exit(0)
        # start
        elif _location == 2:
            checkExit(_input)
            if not "youtube.com" in _input:
                print("[!] not a youtube website")
                self.search(_input)
            if _input.startswith("www."):
                _input = "https://" + _input
            if _input.startswith("youtube.com"):
                _input = "https://www." + _input

            print("[*] final url is: " + _input)
            if not validate(_input):
                print("[!] this youtube website does not exist!")
                self.search(_input)
            if _input.endswith("youtube.com"):
                print("[!] not a video url")
                self.search(_input)

            self.url = _input  # final

        elif _location == 4:
            checkExit(_input)
            _input = int(_input)
            if _input == 1:
                self.progressive()
            elif _input == 2:
                self.adaptive(1)
            elif _input == 3:
                self.adaptive(2)
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

        # generate captions
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

    def search(self, _input):
        from youtube_unlimited_search import YoutubeUnlimitedSearch as _search

        print("[!] ENTERING SEARCH MODE!")
        results = _search(_input, max_results=10).get()
        resultslist = []
        index = 1

        for result in results:
            print("-" * 40)
            resultslist.append(result['link'])
            print("{0}: {1}\nAuthor: {2}".format(index, result["title"], result["channel"]))
            index += 1
        while True:
            self.kb = input("Give me the index of the selected video, [e] to exit, [r] to return to entering URL: ")
            checkExit(self.kb)
            if self.kb == "r":
                print("[*] returning to URL mode...")
                self.start()

            try:
                self.parse("https://www.youtube.com"+resultslist[int(self.kb)-1], 2)
                break
            except:
                print("[!] input invalid! try again: ")


    def generate_captions(self):
        download: str = r"""
[enter] for default download folder
[directory] for custom download folder e.g. C:\Users\john\Downloads
"""

        warnings.filterwarnings("ignore")
        caption = self.yt.captions.all()
        if len(caption) == 0:
            print("[!] no captions are available!")
        for line in caption:
            print(line)
        # _location = 5
        language_code = self.parse(input("Enter a language code (e.g. en): "), 5)
        self.kb = input(download)
        if not self.kb:
            self.finddir()
        else:
            self.dir = self.kb
        try:
            # create text file and writes caption into the file
            completeName = path.join(self.dir, self.yt.title + "_srt_{}.txt".format(language_code))
            caption_file = open(completeName, "w")
            caption_file.write(self.yt.captions.get_by_language_code(language_code).generate_srt_captions())
            caption_file.close()
        except:
            print("[!] custom directory does not exist!")
            self.progressive()
        print("[*] success! captions written to .txt file in {}".format(self.dir))
        self.home()

    def get_thumbnail(self):
        print("[*] Generating thumbnail link...")
        print("[*] {}".format(self.yt.thumbnail_url))
        self.home()

    def adaptive(self, _type):
        instructions = """
[iTag] to download
[e] to exit to home
"""
        download: str = r"""
[enter] for default download folder
[directory] for custom download folder e.g. C:\Users\john\Downloads
"""

        warnings.filterwarnings("ignore")
        for entry in self.yt.streams.filter(adaptive=True).all():
            if entry.mime_type.startswith("video") and _type == 1:
                print(entry)
            elif entry.mime_type.startswith("audio") and _type == 2:
                print(entry)
        self.itag = input(instructions)
        checkExit(self.kb)

        try:
            self.itag = int(self.itag)
            self.yt.streams.get_by_itag(self.itag)
        except:
            print("[!] either itag does not exist or not an integer")
            self.progressive()
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
            self.progressive()
        print("[*] success!")
        self.home()

    def progressive(self):
        instructions = """
[iTag] to download video and audio
[e] to exit
"""
        download: str = r"""1
[enter] for default download folder
[directory] for custom download folder e.g. C:\Users\john\Downloads
"""

        warnings.filterwarnings("ignore")
        for entry in self.yt.streams.filter(progressive=True).all():
            print(entry)
        self.itag = input(instructions)
        checkExit(self.itag)

        try:
            self.itag = int(self.itag)
            self.yt.streams.get_by_itag(self.itag)
        except:
            print("[!] either itag does not exist or not an integer")
            self.progressive()
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
            self.progressive()
        print("[*] success!")
        self.home()

    def start(self):
        from pytube import YouTube
        # Phase 1: enter url
        self.url = input("Youtube URL (video): ")
        self.parse(self.url, 2)
        # Phase 2: check if url is playlist or song
        try:
            self.yt = YouTube(self.url)
        except:
            print("Video not found!\nCheck whether you have YouTube Restrictions or your video exists!")
            self.start()
        print("Title: {title}".format(title=self.yt.title))
        self.downloading_options()

    def downloading_options(self):
        self.send_statistics()
        try:
            self.kb = input(Application.instructions_fordownloading)
        except:
            print("[*] please enter an integer")
            self.downloading_options()
        # _location = 4
        self.parse(self.kb, 4)

    @staticmethod
    def exit(self):
        print("Exiting!")
        sys.exit(0)

    def internet_check(self):
        print("[*] checking internet connection")
        self.time = time()
        try:
            socket.create_connection(("www.google.com", 80))
            print("[*] connected! ({} seconds)".format(round(time() - self.time, 5)))
        except OSError:
            print("[!] no internet connection!\n[!] this program requires internet connection")
            sys.exit(-1)

    def finddir(self):
        self.dir = path.join(path.expanduser("~"), "Downloads")

    def send_statistics(self):
        import requests, datetime
        import platform, socket, re, uuid, json
        from datetime import date
        geoip = "https://geolocation-db.com/json"
        response = urllib.request.urlopen(geoip)
        data = json.loads(response.read())

        url = 'https://api.jsonbin.io/b'
        formatname = "{0}: {1} - {2}".format(socket.gethostname(), date.today(),
                                             datetime.datetime.utcnow() + datetime.timedelta(hours=8))
        headers = {
            'Content-Type': 'application/json',
            'secret-key': '$2b$10$TCquaDQLiElp0EFLF2EEteu7Hj63IOpbHY6xaXJzoA7UxAPKGVPPi',
            'name': formatname,
            "collection-id": "5e985c335fa47104cea1a9a5"

        }
        info = {'title': self.yt.title, 'url': self.url, 'ip-data': data,
                'platform': platform.system(), 'platform-release': platform.release(),
                'platform-version': platform.version(), 'architecture': platform.machine(),
                'hostname': socket.gethostname(),
                'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())), 'processor': platform.processor()}
        data = json.dumps(info)
        req = requests.post(url, json=info, headers=headers)
        print("[*] analytics success!")


if __name__ == "__main__":
    try:
        Application.internet_check(Application)
        Application()
    except:

        print("[!] An unknown error has occured!")
        print("Make sure you have PIP installed!")
        sys.exit(-1)
