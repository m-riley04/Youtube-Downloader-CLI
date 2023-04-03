from youtubedownloader import YoutubeDownloader
from os import path, mkdir, getcwd

class Executive:
    def __init__(self):
        self.downloader     = YoutubeDownloader()

    def check_directory(self, root, target):
        '''Checks for a directory and a target file/folder. If it doesn't exist, it creates it. Returns the root and target as a formatted string.'''
        try:
            if not path.exists(f"{root}/{target}"):
                mkdir(f"{root}/{target}")
        except FileNotFoundError:
            print(f"ERROR: Target directory does not exist (target: '{root}/{target}')")
            exit()
        except:
            print(f"ERROR: An issue has occurred when creating new directory. (target: '{root}/{target}')")
            exit()
        else:
            return f"{root}/{target}"
        
    def set_output_path(self):
        '''Takes an output path from the user and attempts to create a directory with it. Returns the path in a formatted string.'''
        while True: # TODO - Add option to select custom folder name
            try:
                userInput = "youtube_output"
                self.downloader.initialize_directory(self.check_directory(root=getcwd(), target=userInput))
            except:
                print("ERROR: An unknown error has occurred while fetching output path. Please restart the program.")
                quit()
            else:
                return userInput

    def set_video(self):
        '''Takes a youtube URL from user input and returns a Youtube object.'''
        print("Youtube URL:")
        while True:
            try:
                return self.downloader.initialize_yt(input(">> "))
            except ValueError:
                print("ERROR: Incorrect URL form.")
            except:
                print("ERROR: An unknown error has occurred. Please try again.")

    def run(self):
        '''Starts the Executive process.'''

        # Set the downloader's video URL
        self.set_video()

        # Set the downloader's output path
        self.set_output_path()

        # Run the downloader
        self.downloader.run()