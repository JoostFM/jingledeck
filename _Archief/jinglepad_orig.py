#!/usr/bin/env python3

#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

# Example script showing basic library usage - updating key images with new
# tiles generated at runtime, and responding to button state change events.

import os
import threading
import pygame

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper


# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")
AUDIO_PATH = os.path.join(os.path.dirname(__file__), "Audio")

keyset=0

currentstate = [False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False]

keys=[
    [
        ["cmd-q1","","qoutes 1"],
        ["cmd-q2","","qoutes 2"],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""]
     ],
    [
        ["cmd-up","ico72_back",""],
        ["quote Freriks - Dank je voor deze analyse.wav","philip","Analyse"],
        ["quote Freriks - Over op een optimistischer onderwerp.wav","philip","Optimist"],
        ["quote_Teringlijers.wav","philip","Teringlijers"],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["gatverrdamme.wav","gatverdamme","Gatverdamme"],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""]
     ],
    [
        ["cmd-up","ico72_back",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""],
        ["","",""]
     ]
    ]


# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, font_filename, label_text):
    # Create new key image of the correct dimensions, black background.
    image = PILHelper.create_image(deck)

    # Resize the source image asset to best-fit the dimensions of a single key,
    # and paste it onto our blank frame centered as closely as possible.
    icon = Image.open(icon_filename).convert("RGBA")
    icon.thumbnail((image.width, image.height - 20), Image.LANCZOS)
    icon_pos = ((image.width - icon.width) // 2, 0)
    image.paste(icon, icon_pos, icon)

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    label_w, label_h = draw.textsize(label_text, font=font)
    label_pos = ((image.width - label_w) // 2, image.height - 20)
    draw.text(label_pos, text=label_text, font=font, fill="white")

    return PILHelper.to_native_format(deck, image)


# Returns styling information for a key based on its position and state.
def get_key_details(deck, key, state):
    # Last button in the example application is the exit button.
    exit_key_index = deck.key_count() - 1
    font = "Roboto-Regular.ttf"

    name = keys[keyset][key][0]
    #if keys[level][key][1] == '': icon = keys[level][key][1]
    icon = "{}.png".format(keys[keyset][key][1] if keys[keyset][key][1] != '' else "ico72_empty")
    label = keys[keyset][key][2]

    if keyset == 0:
        if key == exit_key_index:
            name = "exit"
            icon = "{}.png".format("Exit")            
            label = "Bye" if state else "Exit"
            
    #print("get_key_details: keyset {}, key {}, name {}, icon {}".format(keyset, key,name, icon))
    
    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }


# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_details(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)

def is_command(key_name,state):
    if not state:
        return False
    if key_name == "":
        return False
    return key_name[0:4] == "cmd-"

# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):
    global keyset
    global currentstate
    
    #print("click event: Keyset {} Key {} = {}".format(keyset, key, state), flush=True)
    
    key_style = get_key_details(deck, key, state)
    
    key_name = key_style["name"]
    
    if is_command(key_name,state):
        if key_name[4:100]=="up":
            keyset = 0
            print("keyset 0 (click:up)")
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)
            return
        
        if key_name[4:5]=="q":             
            keyset = int(key_style["name"][5:6])
            print("keyset {} ({})".format(keyset, key_name[4:100]))   
            
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)
            return
    
    # Update the key image based on the new key state.
    update_key_image(deck, key, state)
        
    print("check key {} of keyset {} : {}".format(key, keyset,state))
        
    # Check if the key is changing to the pressed state.
    if state:
        handle_key_down(deck, key)

        # When an exit button is pressed, close the application.
        if key_style["name"] == "exit":
            # Use a scoped-with on the deck to ensure we're the only thread
            # using it right now.
            with deck:
                # Reset deck, clearing all button images.
                deck.reset()

                # Close deck handle, terminating internal worker threads.
                deck.close()
    #else:
        #handle_key_up(deck, key)

def handle_key_down(deck, key) :
    if currentstate[key]:
        print("stop")
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
        currentstate[key] = False
    else:
        audiofile = keys[keyset][key][0]
        if audiofile=="":
            return
        
        audio = os.path.join(AUDIO_PATH, audiofile)
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        currentstate[key] = True 
        
#    while pygame.mixer.music.get_busy() == True:
#        continue

def handle_key_up(deck, key) :
    print("stop")
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(500)

if __name__ == "__main__":
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Init {}".format(pygame.mixer.get_init()))
    
    print("Number of channels {}".format(pygame.mixer.get_num_channels()))
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()