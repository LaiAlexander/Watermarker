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

def calculate_ratio(base_img, overlay):
    factor = 5 if base_img.size[0] > base_img.size[1] else 3.75
    overlay_new_width = int(base_img.size[0] / factor)
    # Need to calculate ratio to maintain proper aspect ratio of the logo
    ratio = overlay_new_width / overlay.size[0]
    return ratio

def new_overlay_size(overlay, ratio):
    overlay_new_width = int(overlay.size[0] * ratio)
    overlay_new_height = int(overlay.size[1] * ratio)
    return (overlay_new_width, overlay_new_height)

def pos_overlay(base_img, overlay):
    position = {
        'top left': (0, 0),
        'top right': (base_img.size[0] - overlay.size[0], 0),
        'bottom left': (0, base_img.size[1] - overlay.size[1]),
        'bottom right': (base_img.size[0] - overlay.size[0], base_img.size[1] - overlay.size[1])
    }
    return position

def watermark(img, overlay_img, position, white_bg):
    if white_bg:
        os.chdir(os.pardir)
        bg = Image.open("img\\bg.png")
        os.chdir("images")
        ratio = calculate_ratio(img, bg)

        # Need to rotate or flip the white background depending on where the logo should be
        white_overlay = bg.resize(new_overlay_size(bg, ratio), Image.ANTIALIAS)
        if position == "top left":
            white_overlay = white_overlay.transpose(Image.ROTATE_180)
        elif position == "top right":
            white_overlay = white_overlay.transpose(Image.FLIP_TOP_BOTTOM)
        elif position == "bottom left":
            white_overlay = white_overlay.transpose(Image.FLIP_LEFT_RIGHT)

        coords = pos_overlay(img, white_overlay)
        coords = coords.get(position) or coords['bottom right']
        img.paste(white_overlay, coords, white_overlay)
    else:
        ratio = calculate_ratio(img, overlay_img)
    overlay = overlay_img.resize(new_overlay_size(overlay_img, ratio), Image.ANTIALIAS)
    coords = pos_overlay(img, overlay)
    coords = coords.get(position) or coords['bottom right']
    img.paste(overlay, coords, overlay)

def watermark_all(overlay_img, position, path, white_bg):
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

            watermark(img, overlay_img, position, white_bg)

            # Can do this in one operation instead, see below
            # filename = filename.split(".")[0]
            # extension = img.filename.split(".")[-1]
            filename, extension = filename.split(".")
            # May use the following, however extension will contain a period ( . )
            # filename, extension = os.path.splitext(filename)
            # The following also works, then the string is ready, no need to add on extension
            # filename = filename[:filename.find(".")] + "_watermarked" + filename[filename.find("."):]

            os.chdir(save_path)
            img.save(filename + "_watermarked." + extension, quality=95)
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
    white_bg = input("White background behind logo? (Y/N) ")
    white_bg = white_bg.upper()
    white_bg = False if white_bg == "N" else True # Default is white background
    watermark_all(overlay_img, position, path, white_bg)
    # may also do this, might be better:
    # new_image.save("newimage." + start_image.format)

run()
