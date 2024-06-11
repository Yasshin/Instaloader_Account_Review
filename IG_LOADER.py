# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 20:10:41 2022

@author: Yasshin
"""
# Session Load
# from argparse import ArgumentParser
# from glob import glob
# from os.path import expanduser
# from platform import system
# from sqlite3 import OperationalError, connect

# try:
#     from instaloader import ConnectionException, Instaloader
# except ModuleNotFoundError:
#     raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


# def get_cookiefile():
#     default_cookiefile = {
#         "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
#         "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
#     }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
#     cookiefiles = glob(expanduser(default_cookiefile))
#     if not cookiefiles:
#         raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
#     return cookiefiles[0]


# def import_session(cookiefile, sessionfile):
#     print("Using cookies from {}.".format(cookiefile))
#     conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
#     try:
#         cookie_data = conn.execute(
#             "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
#         )
#     except OperationalError:
#         cookie_data = conn.execute(
#             "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
#         )
#     instaloader = Instaloader(max_connection_attempts=1)
#     instaloader.context._session.cookies.update(cookie_data)
#     username = instaloader.test_login()
#     if not username:
#         raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
#     print("Imported session cookie for {}.".format(username))
#     instaloader.context.username = username
#     instaloader.save_session_to_file(sessionfile)


# if __name__ == "__main__":
#     p = ArgumentParser()
#     p.add_argument("-c", "--cookiefile")
#     p.add_argument("-f", "--sessionfile")
#     args = p.parse_args()
#     try:
#         import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
#     except (ConnectionException, OperationalError) as e:
#         raise SystemExit("Cookie import failed: {}".format(e))



import instaloader
from pathlib import Path
#import requests
#from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import tkinter as tk
#from io import BytesIO
import os
#import csv


        
        
def get_instagram_images(username):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()
    # id = 'user'
    # pw = 'pass'
    # loader.login(id, pw)
            
    # Load the profile of the user 
    profile = instaloader.Profile.from_username(loader.context, username)
    # Counter for downloaded posts
    downloaded_count = 0


    # Set the target folder path
    target_folder = Path("C:/Users/Yasshin/Desktop/IG PHOTOS")

    # Download the first 5 images from the profile
    for post in profile.get_posts():
        # Check if we have downloaded the desired number of images
        if downloaded_count >= 5:
            break

        # Check if the post is an image
        if not post.is_video and post.typename == "GraphImage":
            # Download the image and specify the target folder
            loader.download_post(post, target=target_folder / profile.username)
            
            # Increment the downloaded image count
            downloaded_count += 1

def read_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(folder_path, filename)
            with Image.open(image_path) as img:
                images.append(img.copy())
    return images
    



def create_profile(username):
    img_downloads = get_instagram_images(username)
    images = read_images_from_folder(f"C:/Users/Yasshin/Desktop/IG PHOTOS/{username}")
    return {'username': username, 'images': images}

# Example usage:
profiles = ["superanimestore","abysmal.sharki","nifteon.art"]
profile_data = [create_profile(username) for username in profiles]

class TinderApp(tk.Tk):
    def __init__(self, profiles):
        super().__init__()
        self.title("Instagram Tinder")
        self.geometry("800x600")
        self.profiles = profiles
        self.current_profile = 0
        self.decisions = []  # List to store decisions
        
        self.profile_frame = tk.Frame(self)
        self.profile_frame.pack(expand=True, fill=tk.BOTH)
        
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.like_button = tk.Button(self.control_frame, text="Like", command=self.like_profile)
        self.like_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        self.dislike_button = tk.Button(self.control_frame, text="Dislike", command=self.dislike_profile)
        self.dislike_button.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.go_back_button = tk.Button(self.control_frame, text="Go Back", command=self.go_back)
        
        self.display_profile()
    
    def display_profile(self):
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        
        profile = self.profiles[self.current_profile]
        username_label = tk.Label(self.profile_frame, text=profile['username'], font=("Helvetica", 16))
        username_label.pack(pady=10)
        
        for img in profile['images']:
            img = img.resize((150, 150), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.profile_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to avoid garbage collection
            img_label.pack(side=tk.LEFT, padx=5)
        
        # Disable buttons when all profiles have been reviewed
        if self.current_profile == len(self.profiles):
            self.like_button.config(state=tk.DISABLED)
            self.dislike_button.config(state=tk.DISABLED)
            self.save_decisions('C:/Users/Yasshin/Desktop/IG PHOTOS/profile_decisions.csv')
            self.go_back_button.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        else:
            self.like_button.config(state=tk.NORMAL)
            self.dislike_button.config(state=tk.NORMAL)
            self.go_back_button.pack_forget()
    
    def like_profile(self):
        self.decisions.append((self.profiles[self.current_profile]['username'], 'like'))
        self.current_profile += 1
        self.display_profile()
    
    def dislike_profile(self):
        self.decisions.append((self.profiles[self.current_profile]['username'], 'dislike'))
        self.current_profile += 1
        self.display_profile()
    
    def go_back(self):
        if self.current_profile > 0:
            self.current_profile -= 1
            self.display_profile()
    
    def save_decisions(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Decision'])
            writer.writerows(self.decisions)

# Run the application
app = TinderApp(profile_data)
app.mainloop()




