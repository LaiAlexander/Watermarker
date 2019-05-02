"""
A script for watermarking pictures in bulk.
TODO Support for choosing size/ratio?
TODO Error message if logo.png doesn't exist
TODO If logo doesn't exist in black/white, display error or use color
TODO May convert logo to black/white
"""
#! python3

import os
from PIL import Image

def new_overlay_size(start, overlay):
    factor = 5 if start.size[0] > start.size[1] else 3.75
    overlay_new_width = int(start.size[0] / factor)
    # Need to calculate ratio to maintain proper aspect ratio of the logo
    ratio = overlay_new_width / overlay.size[0]
    overlay_new_height = int(overlay.size[1] * ratio)
    return (overlay_new_width, overlay_new_height)

def pos_overlay(start, overlay):
    position = {
        'top left': (0, 0),
        'top right': (start.size[0] - overlay.size[0], 0),
        'bottom left': (0, start.size[1] - overlay.size[1]),
        'bottom right': (start.size[0] - overlay.size[0], start.size[1] - overlay.size[1])
    }
    return position

def watermark(img, overlay_img, position):
    overlay = overlay_img.resize(new_overlay_size(img, overlay_img), Image.ANTIALIAS)
    coords = pos_overlay(img, overlay)
    coords = coords.get(position) or coords['bottom right']
    img.paste(overlay, coords, overlay)

def watermark_all(overlay_img, position, path):
    # complete_path = os.getcwd() + path
    os.chdir(path)
    save_path = "watermarked"
    try:
        (os.mkdir(save_path))
        print("Created directory '" + save_path + "'...", flush=True)
    except FileExistsError:
        print("Directory '" + save_path + "' already exists...", flush=True)
    for filename in os.listdir(os.getcwd()):
        if os.path.isfile(filename):
            try:
                img = Image.open(filename)
            except OSError:
                print("Could not open \033[31m" +  filename + "\033[0m...", flush=True)
                print("Are you sure it is an image file?", flush=True)
                continue

            watermark(img, overlay_img, position)

            # Can do this in one operation instead, see below
            # filename = filename.split(".")[0]
            # extension = img.filename.split(".")[-1]
            filename, extension = filename.split(".")
            # May use the following, however extension will contain a period ( . )
            # filename, extension = os.path.splitext(filename)
            # The following also works, then the string is ready, no need to add on extension
            # filename = filename[:filename.find(".")] + "_watermarked" + filename[filename.find("."):]

            os.chdir(save_path)
            img.save(filename + "_watermarked." + extension)
            print("Image is watermarked and saved...", flush=True)
            os.chdir(os.pardir)
    print("\033[32mDone!\033[0m", flush=True)
    return

def run():
    # black magic from https://stackoverflow.com/a/39675059
    os.system('') # enable VT100/ANSI Escape Sequence for WINDOWS 10
    path = "images"
    if not os.path.exists(path):
        print("Folder named 'images' does not exist.")
        print("Create folder and place your images to be watermarked within.")
        print("Exiting script...")
        return
    color = input("Which color? ")
    if color == "white" or color == "black":
        overlay_img = Image.open("logo_" + color + ".png")
    elif color != "default":
        print("Not a valid color, will use default colors. Use 'black', 'white' or 'default'")
        overlay_img = Image.open("logo.png")
    else:
        overlay_img = Image.open("logo.png")
    position = input("In which corner? ")
    watermark_all(overlay_img, position, path)
    # may also do this, might be better:
    # new_image.save("newimage." + start_image.format)

run()
