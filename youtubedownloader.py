import pytube as pt
from sys import exit

class YoutubeDownloader:
    def __init__(self):
        self._filtersEnabled    = False
        self._splitChannels     = False
        self._onlyOne           = False
        self._chosenType        = False
        self._extension         = ""
        self._streams           = None
        self._downloads         = []
        self._youtube           = None

    def _yes_no_select(self):
        '''Prompts the user with an input and accepts either a 1 (yes) or a 2 (no). Returns a boolean respectively.'''
        while True:
            try:
                userInput = int(input(">> "))
                match (userInput):
                    case 1:
                        return True
                    case 2:
                        return False
                    case _:
                        continue
            except ValueError:
                print("ERROR: Please type a valid number.")
            except:
                print("ERROR: An issue occurred during selection. Please try again.")

    def initialize_yt(self, url):
        '''Attempts to create the Youtube object with the passed URL. If it URL is not valid, it raises a ValueError. Otherwise, it returns the Youtube object.'''
        try:
            self._youtube = pt.YouTube(url=url)
        except:
            #print("ERROR: There was an error initializing the URL. Please try again.")
            raise ValueError("Invalid URL.")
        else:
            return self._youtube
        
    def initialize_directory(self, outputPath):
        '''Takes an output path for the downloaded videos. Returns the output path.'''
        self._output = outputPath
        return self._output

    def prompt_filters(self):
        '''Prompts the user for if they would like to enable search filters. Returns True if so and False otherwise.'''
        print("Enable search filters?\n1) Yes\n2) No")
        return self._yes_no_select()

    def prompt_channels(self):
        '''Prompts the user for if they would like split channels and if so, what channel they would like. Returns True if split channels is selected and False otherwise.'''
        print("Split audio/video channels?\n1) Yes\n2) No")
        
        self._splitChannels = self._yes_no_select()
        if self._splitChannels:
            print("Only audio or only video?\n1) Yes\n2) No")
            self._onlyOne = self._yes_no_select()
            if self._onlyOne:
                print("Audio or video?\n1) Audio\n2) Video")
                self._chosenType = self._yes_no_select()

        return self._splitChannels
    
    def prompt_extension(self) -> str:
        '''Prompts the user for what extension they would like to use. Returns'''
        print("What extension?\n1) mp4\n2) webm\n3) 3gpp")

        while True:
            try:
                userInput = int(input())
            except ValueError:
                print("ERROR: Please type a valid number.")
            except:
                print("ERROR: An issue occurred during selection. Please try again.")
            else:
                match (userInput):
                    case 1:
                        return "mp4"
                    case 2:
                        return "webm"
                    case 3:
                        return "3gpp"
                    case _:
                        print("ERROR: Please choose one of the options above.")

    def try_filters(self, filtersEnabled:bool, splitChannels:bool, extension:str, chosenType:bool, maxAttempts=3):
        '''Takes in a boolean for filters enabled, split channels, chosen type, and a string for the extension. Returns a Stream object.'''
        for i in range(maxAttempts):
            try:
                if filtersEnabled:
                    if splitChannels:
                        return self._youtube.streams.filter(progressive=not splitChannels, adaptive=splitChannels, file_extension=extension, only_audio=chosenType, only_video=not chosenType)
                    else:
                        return self._youtube.streams.filter(progressive=not splitChannels, adaptive=splitChannels, file_extension=extension)
                else:
                    return self._youtube.streams.filter()
            except:
                print(f"ERROR: returning YouTube stream filter. Retrying... (Attempt #{i+1})")
        
        # If it does not return in time...
        print("ERROR: Maximum number of retries hit. Please restart the program.")
        quit()

    def create_download_list(self, streams, maxAttempts=3):
        '''Returns a list of all possible YouTube downloads'''
        count = 0
        for retry in range(maxAttempts):
            try:
                options = {}
                for i, stream in enumerate(streams):
                    options[str(i+1)] = stream.itag
                    if stream.type == "video":
                        print(f"{i+1}) Type: {stream.type} - Extension: {stream.subtype} - Resolution: {stream.resolution} - FPS: {stream.fps} - Video Codec: {stream.video_codec} - Audio Codec: {stream.audio_codec}")
                    else:
                        print(f"{i+1}) Type: {stream.type} - Extension: {stream.subtype} - Bitrate: {stream.abr} - Audio Codec: {stream.audio_codec}")
                    count = i
                if count == 0:
                    print("RESULTS: No downloads were found matching that filter.")
                    break
            except:
                print(f"ERROR: There was an error creating the downloads list. Retrying... (Attempt #{retry+1})")
            else:
                return options
            
    def select_download(self, downloads):
        '''Takes a list of downloads and prompts the user to choose one of them. Returns a Stream.'''
        chosen = ""
        while True:
            try:
                print("Select a file to download:")
                while chosen not in downloads.keys():
                    chosen = input(">> ")
                    if chosen not in downloads.keys():
                        print(f"ERROR: No download found for #{chosen}. Please restart the program.")
            except:
                print("ERROR: There was an issue selecting the download. Please restart the program.")
            else:
                return self._youtube.streams.get_by_itag(downloads[chosen])
            
    def try_download(self, stream, maxAttempts=3):
        '''Tries to download the passed Stream for a certain amount of times. If it exceeds those tries, it exits.'''
        count = 0
        while True:
            if count > maxAttempts:
                print("Cannot download file. Please try another download.")
                self.try_download(self.select_download(self._downloads))
            try:
                stream.download(output_path=self._output)
            except:
                count += 1
                print(f"ERROR: There was an error downloading the file. Retrying... (attempt #{count})")
            else:
                print("Finished downloading!")
                break
    
    def convert_to_timestamp(self, seconds):
        '''Return a formatted timestamp of a given number of seconds.'''
        from math import floor

        minutes = floor(seconds/60)
        remainingSeconds = seconds & 60
        return f"{minutes}:{remainingSeconds}"

    def run(self):
        '''Starts the downloader and prompts.'''
        
        # Show video selected
        print(f"Video Selected: '{self._youtube.title}' by {self._youtube.author} ({self.convert_to_timestamp(self._youtube.length)})")

        try:
            # Prompts
            self._filtersEnabled = self.prompt_filters()
            if self._filtersEnabled:
                self._splitChannels = self.prompt_channels()
                self._extension = self.prompt_extension()

            # Gathers filtered streams and downloads
            self._streams = self.try_filters(self._filtersEnabled, self._splitChannels, self._extension, self._chosenType)
            self._downloads = self.create_download_list(self._streams)

            # Attempts to download
            if self._downloads != None:
                self.try_download(self.select_download(self._downloads))

        except:
            print("ERROR: An unknown error has occurred in the process. Please restart the program and try again.")