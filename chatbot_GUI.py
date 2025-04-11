import tkinter.messagebox
from tkinter import *
import tkinter.font as tkFont

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import contractions

import re
import random
import json
from spellchecker import SpellChecker
from album_scraper import Album
from song_scraper import Song
from song_scraper import songs_by_decade_genre

"""

METHODS USED BY THE MAIN CODE

"""

def load_albums_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    albums_by_decade_genre = {}
    for decade, genres in data.items():
        albums_by_decade_genre[decade] = {}
        for genre, albums in genres.items():
            albums_by_decade_genre[decade][genre] = [
                Album(album['title'], album['artist'], album['release_date'], album['genre']) for album in albums]

    return albums_by_decade_genre

albums_by_decade_genre = load_albums_from_file('albums_by_decade_genre.json')


def load_songs_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    songs_by_decade_genre = {}
    for decade, genres in data.items():
        songs_by_decade_genre[decade] = {}
        for genre, songs in genres.items():
            songs_by_decade_genre[decade][genre] = [
                Song(song['title'], song['artist'], song['release_date'], song['genre']) for song in songs]

    return songs_by_decade_genre

songs_by_decade_genre = load_songs_from_file('songs_by_decade_genre.json')


def get_input(prompt_list):
    return input(random.choice(prompt_list))

def process_input(user_input):
    lower_input = contractions.fix(user_input.lower())
    tokens = word_tokenize(lower_input)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [t for t in tokens if t not in stop_words]
    return filtered_tokens

def check_type_music(filtered_tokens):
    filtered_string = ' '.join(filtered_tokens)
    type_music_check = {
        "song": re.findall(r"\bsong|singl", filtered_string),
        "album": re.findall(r"\balbu", filtered_string),
    }
    for type_music, check in type_music_check.items():
        if check:
            return type_music
    return None

def check_genre(filtered_tokens):
    filtered_string = ' '.join(filtered_tokens)
    genre_checks = {
        "rock": re.findall(r"\brock", filtered_string),
        "country": re.findall(r"\bcountry", filtered_string),
        "pop": re.findall(r"\bpop", filtered_string),
        "hip hop": re.findall(r"\bhip hop", filtered_string),
        "jazz": re.findall(r"\bjazz", filtered_string)
    }
    for genre, check in genre_checks.items():
        if check:
            return genre
    return None

def check_decade(filtered_tokens):
    filtered_string = ' '.join(filtered_tokens)
    decade_checks = {
        "fifties": re.findall(r"\bfif|50", filtered_string),
        "sixties": re.findall(r"\bsix|60", filtered_string),
        "seventies": re.findall(r"\bsev|70", filtered_string),
        "eighties": re.findall(r"\beig|80", filtered_string),
        "nineties": re.findall(r"\bnine|90", filtered_string),
        "two_thousands": re.findall(r"\btwo tho|200", filtered_string),
        "twenty_tens": re.findall(r"\bten|201", filtered_string),
        "twenty_twenties": re.findall(r"\btwen|202", filtered_string)
    }
    for decade, check in decade_checks.items():
        if check:
            return decade
    return None

def correct_spelling(tokens):
    spell = SpellChecker()
    misspelled = spell.unknown(tokens)
    corrected_tokens = []

    for word in tokens:
        if word in misspelled:
            corrected_word = spell.correction(word)
            if corrected_word is None:
                corrected_tokens.append(word)
            else:
                corrected_tokens.append(corrected_word)
        else:
            corrected_tokens.append(word)

    return corrected_tokens

def recommend_music(genre, decade):
    if decade == "fifties":
        decade_key = "1950s"
    elif decade == "sixties":
        decade_key = "1960s"
    elif decade == "seventies":
        decade_key = "1970s"
    elif decade == "eighties":
        decade_key = "1980s"
    elif decade == "nineties":
        decade_key = "1990s"
    elif decade == "two_thousands":
        decade_key = "2000s"
    elif decade == "twenty_tens":
        decade_key = "2010s"
    elif decade == "twenty_twenties":
        decade_key = "2020s"
    else:
        return "Invalid decade"

    # Capitalize first letter in genre
    genre_formatted = ' '.join([word.capitalize() for word in genre.split()])

    if type_music == "album":
        # Check if genre and decade combination exists in albums_by_decade_genre
        if decade_key in albums_by_decade_genre and genre_formatted in albums_by_decade_genre[decade_key]:
            albums = albums_by_decade_genre[decade_key][genre_formatted]
            if albums:
                # Format recommendation strings based on the album objects
                recommendations = [f"{album}" for album in albums] #{album.title} - {album.artist}" for album in albums]
                return random.choice(recommendations)
            else:
                return "Sorry, there are no matches"
        else:
            return "Sorry, there are no matches"
    elif type_music == "song":
        # Check if genre and decade combination exists in songs_by_decade_genre
        if decade_key in songs_by_decade_genre and genre_formatted in songs_by_decade_genre[decade_key]:
            songs = songs_by_decade_genre[decade_key][genre_formatted]
            if songs:
                # Format recommendation strings based on the song objects
                recommendations = [f"{song}" for song in songs]
                return random.choice(recommendations)
            else:
                return "Sorry, there are no matches"
        else:
            return "Sorry, there are no matches"




"""

GUI CODE

"""

root = Tk()
root.title('TuneSage')
app_width = 600
app_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
root.resizable(0, 0)
root.configure(bg="#1F2833")

font = tkFont.Font(family="Arial", size=12, weight=tkFont.NORMAL)

title_frame = Frame(root, height=2, width=550, bg="#C5C6C7", borderwidth=2)
title_frame.pack(side=TOP)

user_text_box = Label(title_frame, height=3, text="\t\t\tTuneSage: Your Musical Companion\t\t\t", font=font, bg="#0B0C10",
                      fg="#C5C6C7")
user_text_box.pack()

# Container for canvas and scrollbar
container = Frame(root, width=app_width, height=575, bg="#1F2833")
container.pack(anchor=CENTER)
container.pack_propagate(False)

# Create a canvas widget
canvas = Canvas(container, bg="#1F2833")
canvas.pack(side=LEFT, fill="both", expand=True)

# Create a scrollbar widget
scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side=RIGHT, fill="y")

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Create the frame inside the canvas
conversation_frame = Frame(canvas, bg="#1F2833")

# Add the new frame to a window in the canvas
canvas.create_window((0, 0), window=conversation_frame, anchor="nw", width=app_width - (scrollbar.winfo_width() + 20))

# Update the scroll region to encompass the inner frame
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


conversation_frame.bind("<Configure>", on_frame_configure)


intro_conversation_label = Label(conversation_frame, text="Hi! My name is TuneSage and I'm here to give you album or song\n"
                                                         + "recommendations based on the type of music you want to listen\n to! "
                                                         + "So, let's get right to it....", height=3, width=50, font=font, bg="#45A29E")
intro_conversation_label.pack(anchor=W, padx=5, pady=20)

type_conversation_label = Label(conversation_frame, text="", font=font, bg="#45A29E")
type_prompt = ["Do you want to listen to an album or a single song?", "Would you prefer an album or an individual song?"]
type_conversation_label.config(text=random.choice(type_prompt))
root.after(1000, lambda: type_conversation_label.pack(anchor=W, padx=5, pady=20))

# Type select by user
user_type_entry = Label(conversation_frame, font=font, bg="#66FCF1", padx=5, pady=5)
user_type_entry.pack_forget()

genre_prompt = ["What type of music are you looking for?", "What genre would you like to listen to?"]
genre_conversation_label = Label(conversation_frame, text="", font=font, bg="#45A29E")
genre_conversation_label.pack_forget()

# Genre select by user
user_genre_entry = Label(conversation_frame, font=font, bg="#66FCF1", padx=5, pady=5)
user_genre_entry.pack_forget()

era_prompt = ["Around what years of music are you wanting to listen to?",
                      "What decade of music are you looking for?"]
era_conversation_label = Label(conversation_frame, text="", font=font, bg="#45A29E")
era_conversation_label.pack_forget()

# Era select by user
user_era_entry = Label(conversation_frame, font=font, bg="#66FCF1", padx=5, pady=5)
user_era_entry.pack_forget()

result_conversation_label = Label(conversation_frame, text="", font=font, bg="#45A29E")
result_conversation_label.pack_forget()

continue_prompt = ["Is there anything else I can help you with?\n (Type \"AGAIN\" to get new recommendations)"]
continue_conversation_label = Label(conversation_frame, text="", font=font, bg="#45A29E")
continue_conversation_label.pack_forget()

# Continue decision by user
user_continue_entry = Label(conversation_frame, font=font, bg="#66FCF1", padx=5, pady=5)
user_continue_entry.pack_forget()

end_conversation_label = Label(conversation_frame, text="", font=font, bg="#45A29E")
end_conversation_label.pack_forget()

# Frame for user text area
bottom_frame = Frame(root, height=150, width=app_width, bg="#C5C6C7", borderwidth=0.5)
bottom_frame.pack(side=BOTTOM)
bottom_frame.pack_propagate(False)

# Frame for user text
text_box_frame = Frame(bottom_frame, height=150, width=450, bg="#C5C6C7")
text_box_frame.pack(side=LEFT)
text_box_frame.pack_propagate(False)

# Text box for user
user_text_box = Text(text_box_frame, height=150, width=450, font=font, bg="#0B0C10", fg="#C5C6C7")
user_text_box.pack(side=LEFT)
user_text_box.pack_propagate(False)

# Submit button frame
submit_button_frame = Frame(bottom_frame, height=150, width=150, bg="#C5C6C7", borderwidth=0.5)
submit_button_frame.pack(side=RIGHT)
submit_button_frame.pack_propagate(False)

def changeOnHover(button, colorOnHover, colorOnLeave):
    # Change background on hover
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover, fg="#0B0C10"))

    # Change background on leave
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave, fg="#C5C6C7"))

counter = 0
genre = "none"

def buttonClick():
    global counter, genre

    if counter == 0:
        user_input = user_text_box.get("1.0", "end-1c").strip()
        if user_input:
            user_type_entry.config(text=user_input)
            user_type_entry.pack(anchor=E, padx=5, pady=20)
            counter += 1
            user_text_box.delete("1.0", "end-1c")
            process_type(user_input)
    if counter == 1:
        user_input = user_text_box.get("1.0", "end-1c").strip()
        if user_input:
            user_genre_entry.config(text=user_input)
            user_genre_entry.pack(anchor=E, padx=5, pady=20)
            counter += 1
            user_text_box.delete("1.0", "end-1c")
            process_genre(user_input)
            if re.findall(r"\bsug|recom|surp|sup", user_input.lower()):
                counter = 3
    elif counter == 2:
        user_input = user_text_box.get("1.0", "end-1c").strip()
        if user_input:
            user_era_entry.config(text=user_input)
            user_era_entry.pack(anchor=E, padx=5, pady=20)
            counter += 1
            user_text_box.delete("1.0", "end-1c")
            process_era(user_input)
    elif counter == 3:
        user_input = user_text_box.get("1.0", "end-1c").strip()
        if user_input:
            user_continue_entry.config(text=user_input)
            user_continue_entry.pack(anchor=E, padx=5, pady=20)
            counter += 1
            user_text_box.delete("1.0", "end-1c")
            process_continue(user_input)

def process_type(user_input):
    global counter, genre, type_music

    filtered_tokens = process_input(user_input)
    filtered_tokens = correct_spelling(filtered_tokens)
    type_music = check_type_music(filtered_tokens)
    if type_music:
        root.after(1000, lambda: genre_conversation_label.pack(anchor=W, padx=5, pady=20))
        genre_conversation_label.config(text=random.choice(genre_prompt))
    else:
        type_conversation_label.config(text="Sorry, I don't understand what you're trying to tell me.\n")
        root.after(2500, lambda: type_conversation_label.pack_forget())
        root.after(2500, lambda: user_type_entry.pack_forget())
        root.after(2500, lambda: type_conversation_label.config(text=random.choice(type_prompt)))
        root.after(2500, lambda: type_conversation_label.pack(anchor=W, padx=5, pady=20))
        counter = 0  # Reset counter to ask for genre again

def process_genre(user_input):
    global counter, genre

    filtered_tokens = process_input(user_input)
    filtered_tokens = correct_spelling(filtered_tokens)
    genre = check_genre(filtered_tokens)
    if genre:
        root.after(1000, lambda: era_conversation_label.pack(anchor=W, padx=5, pady=20))
        era_conversation_label.config(text=random.choice(era_prompt))
    elif re.findall(r"\bsug|recom|surp|sup", user_input.lower()):
        genre = random.choice(["rock", "country", "pop", "hip hop", "jazz"])
        decade = random.choice(
            ['fifties', 'sixties', 'seventies', 'eighties', 'nineties', 'two_thousands', 'twenty_tens',
             'twenty_twenties'])
        root.after(1000, lambda: result_conversation_label.pack(anchor=W, padx=5, pady=20))
        recommendation_prompt = ["Sure thing! Here are some really good albums with great songs:\n",
                                 "Alrighty, give me just a second.\nThere are some really good songs on "
                                 + "these albums\n that I heard a while back.\n",
                                 "Sure thing! Here are some really good songs I know:\n"]
        if type_music == "album":
            album_recommendations = "\n"
            for i in range(3):
                album_recommendations += (recommend_music(genre, decade) + "\n\n")
            result_conversation_label.config(text=random.choice(recommendation_prompt[0:2]) + album_recommendations)

            root.after(1500, lambda: continue_conversation_label.pack(anchor=W, padx=5, pady=20))
            continue_conversation_label.config(text=random.choice(continue_prompt))

        elif type_music == "song":
            song_recommendations = "\n"
            for i in range(5):
                song_recommendations += (recommend_music(genre, decade) + "\n\n")
            result_conversation_label.config(text=recommendation_prompt[2] + song_recommendations)

            root.after(1500, lambda: continue_conversation_label.pack(anchor=W, padx=5, pady=20))
            continue_conversation_label.config(text=random.choice(continue_prompt))
    else:
        genre_conversation_label.config(text="Sorry, I don't know that genre of music yet.\n "
                                             + "All I know are rock, country, pop, hip hop, and jazz.")
        root.after(2500, lambda: genre_conversation_label.pack_forget())
        root.after(2500, lambda: user_genre_entry.pack_forget())
        root.after(2500, lambda: genre_conversation_label.config(text=random.choice(genre_prompt)))
        root.after(2500, lambda: genre_conversation_label.pack(anchor=W, padx=5, pady=20))
        counter = 1  # Reset counter to ask for genre again

def process_era(user_input):
    global counter, decade

    filtered_tokens = process_input(user_input)
    decade = check_decade(filtered_tokens)
    if decade:
        root.after(1000, lambda: result_conversation_label.pack(anchor=W, padx=5, pady=20))
        recommendation_prompt = ["Sure thing! Here are some really good albums with great songs:\n",
                                 "Alrighty, give me just a second.\nThere are some really good songs on "
                                 + "these albums\n that I heard a while back.\n",
                                 "Sure thing! Here are some really good songs I know:\n"]
        if type_music == "album":
            album_recommendations = "\n"
            for i in range(3):
                album_recommendations += (recommend_music(genre, decade) + "\n\n")
            result_conversation_label.config(text=random.choice(recommendation_prompt[0:2]) + album_recommendations)

            root.after(1500, lambda: continue_conversation_label.pack(anchor=W, padx=5, pady=20))
            continue_conversation_label.config(text=random.choice(continue_prompt))

        elif type_music == "song":
            song_recommendations = "\n"
            for i in range(5):
                song_recommendations += (recommend_music(genre, decade) + "\n\n")
            result_conversation_label.config(text=recommendation_prompt[2] + song_recommendations)

            root.after(1500, lambda: continue_conversation_label.pack(anchor=W, padx=5, pady=20))
            continue_conversation_label.config(text=random.choice(continue_prompt))
    else:
        era_conversation_label.config(text="Sorry, I don't know any music from that time.")
        root.after(2500, lambda: user_era_entry.pack_forget())
        root.after(2500, lambda: user_era_entry.config(text=""))
        root.after(2500, lambda: era_conversation_label.config(text=random.choice(era_prompt)))
        root.after(2500, lambda: era_conversation_label.pack(anchor=W, padx=5, pady=20))
        counter = 2  # Reset counter to ask for decade again

def process_continue(user_input):
    global counter, decade

    if re.findall(r"\bye|sure", user_input.lower()):
        reset_conversation()
    elif re.findall(r"\bno|nah", user_input.lower()):
        root.after(1000, lambda: end_conversation_label.pack(anchor=W, padx=5, pady=20))
        end_conversation_list = ["Okie dokie, see you later!", "Goodbye!", "Bye! It was nice talking to you."]
        end_conversation_label.config(text=random.choice(end_conversation_list))
    elif re.findall(r"\bagain", user_input.lower()):
        recommendation_prompt = ["Sure thing! Here are some really good albums with great songs:\n",
                                 "Alrighty, give me just a second.\nThere are some really good songs on "
                                 + "these albums\n that I heard a while back.\n",
                                 "Sure thing! Here are some really good songs I know:\n"]
        if type_music == "album":
            album_recommendations = "\n"
            for i in range(3):
                album_recommendations += (recommend_music(genre, decade) + "\n\n")
            result_conversation_label.config(text=random.choice(recommendation_prompt[0:2]) + album_recommendations)

            root.after(1500, lambda: continue_conversation_label.pack(anchor=W, padx=5, pady=20))
            continue_conversation_label.config(text=random.choice(continue_prompt))

        elif type_music == "song":
            song_recommendations = "\n"
            for i in range(5):
                song_recommendations += (recommend_music(genre, decade) + "\n\n")
            result_conversation_label.config(text=recommendation_prompt[2] + song_recommendations)

            root.after(1500, lambda: continue_conversation_label.pack(anchor=W, padx=5, pady=20))
            continue_conversation_label.config(text=random.choice(continue_prompt))

        root.after(2500, lambda: user_continue_entry.pack_forget())
        root.after(2500, lambda: user_continue_entry.config(text=""))
        counter = 3 # Reset counter to ask for continue decision again
    else:
        continue_conversation_label.config(text="I don't understand what you're trying to tell me.")
        root.after(2500, lambda: user_continue_entry.pack_forget())
        root.after(2500, lambda: user_continue_entry.config(text=""))
        root.after(2500, lambda: continue_conversation_label.config(text=random.choice(continue_prompt)))
        root.after(2500, lambda: continue_conversation_label.pack(anchor=W, padx=5, pady=20))
        counter = 3  # Reset counter to ask for continue decision again

def reset_conversation():
    global counter
    counter = 0
    user_type_entry.pack_forget()
    user_type_entry.config(text="")
    user_genre_entry.pack_forget()
    user_genre_entry.config(text="")
    user_era_entry.pack_forget()
    user_era_entry.config(text="")
    user_continue_entry.pack_forget()
    user_continue_entry.config(text="")
    result_conversation_label.pack_forget()
    result_conversation_label.config(text="")
    genre_conversation_label.pack_forget()
    genre_conversation_label.config(text="")
    era_conversation_label.pack_forget()
    era_conversation_label.config(text="")
    continue_conversation_label.pack_forget()
    continue_conversation_label.config(text="")
    end_conversation_label.pack_forget()
    end_conversation_label.config(text="")
    intro_conversation_label.pack(anchor=W, padx=5, pady=20)

def increase_font_size():
    font_size = font.cget("size")
    font.config(size= font_size + 2)

def decrease_font_size():
    font_size = font.cget("size")
    font.config(size= font_size - 2)

def show_info():
    tkinter.messagebox.showinfo(title="About", message="Website Used for Album Recommendations: https://www.albumoftheyear.org/\n\n"
                                                       + "Website Used for Song Recommendations: https://rateyourmusic.com/")

# Help Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='Help', menu=filemenu)
filemenu.add_command(label='About', command=show_info)
filemenu.add_command(label='Restart Conversation', command=reset_conversation)
filemenu.add_command(label='Increase Font Size', command=increase_font_size)
filemenu.add_command(label='Decrease Font Size', command=decrease_font_size)


# Submit button
submit_button = Button(submit_button_frame, text='Submit', font=font, height=3, width=15, bg="#1F2833", fg="#C5C6C7",
                       relief=GROOVE, command=buttonClick)
submit_button.pack()
changeOnHover(submit_button, "#66FCF1", "#1F2833")

# Hide initial labels
user_genre_entry.pack_forget()
era_conversation_label.pack_forget()
user_era_entry.pack_forget()
result_conversation_label.pack_forget()
continue_conversation_label.pack_forget()
user_continue_entry.pack_forget()
end_conversation_label.pack_forget()

# Start the main loop
root.mainloop()
