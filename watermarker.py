"""
A script for watermarking pictures in bulk.
"""
#! python3

import os
from PIL import Image

def new_overlay_size(start, overlay):
    overlay_new_width = int(start.size[0] / 5)
    factor = overlay_new_width / overlay.size[0]
    overlay_new_height = int(overlay.size[1] * factor)
    return (overlay_new_width, overlay_new_height)

def pos_overlay(start, overlay):
    position = {
        'top left': (0, 0),
        'top right': (start.size[0] - overlay.size[0], 0),
        'bottom left': (0, start.size[1] - overlay.size[1]),
        'bottom right': (start.size[0] - overlay.size[0], start.size[1] - overlay.size[1])
    }
    return position

def watermark(overlay_img, pos_text, single):
    if single:
        start_img = Image.open("image.jpg")

        new_overlay = overlay_img.resize(new_overlay_size(start_img, overlay_img), Image.ANTIALIAS)

        new_img = start_img.copy()

        position = pos_overlay(new_img, new_overlay)

        position = position.get(pos_text) or position['bottom right']

        new_img.paste(new_overlay, position, new_overlay)
        print("Image is watermarked...", flush=True)

        extension = start_img.filename.split(".")[-1]

        new_img.save("image_watermarked." + extension)
        print("Image is saved...", flush=True)
        print("Done!")
        return
    elif not single:
        path = "bulk"
        # complete_path = os.getcwd() + path
        os.chdir(path)
        save_path = "watermarked"
        for filename in os.listdir(os.getcwd()):
            if os.path.isfile(filename):
                start_img = Image.open(filename)
                new_overlay = overlay_img.resize(new_overlay_size(start_img, overlay_img),
                                                 Image.ANTIALIAS)

                new_img = start_img.copy()

                position = pos_overlay(new_img, new_overlay)

                position = position.get(pos_text) or position['bottom right']

                new_img.paste(new_overlay, position, new_overlay)

                extension = start_img.filename.split(".")[-1]

                try:
                    (os.mkdir(save_path))
                    print("Created directory...", flush=True)
                except FileExistsError:
                    print("Directory already exists...", flush=True)
                os.chdir(save_path)
                new_img.save(filename + "_watermarked." + extension)
                print("Image is watermarked and saved...", flush=True)
                os.chdir(os.pardir)
        print("Done!", flush=True)
        return

def run():
    color = input("Which color? ")
    if color == "white" or color == "black":
        overlay_img = Image.open("logo_" + color + ".png")
    elif color != "default":
        print("Not a valid color, will use default colors. Use 'black', 'white' or 'default'")
        overlay_img = Image.open("logo.png")
    else:
        overlay_img = Image.open("logo.png")
    pos_text = input("In which corner? ")
    amount = input("Single image or bulk? ")
    if amount == "single":
        watermark(overlay_img, pos_text, True)
    elif amount == "bulk":
        watermark(overlay_img, pos_text, False)
    # may also do this, might be better:
    # new_image.save("newimage." + start_image.format)

run()
