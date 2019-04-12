#! python3

import os
from PIL import Image

def new_overlay_size(start, overlay):
    overlay_new_width = int(start.size[0] / 5)
    factor = overlay_new_width / overlay.size[0]
    overlay_new_height = int(overlay.size[1] * factor)
    return (overlay_new_width, overlay_new_height)

def get_bottom_right_pos(start, overlay):
    overlay_x_pos = start.size[0] - overlay.size[0]
    overlay_y_pos = start.size[1] - overlay.size[1]
    return (overlay_x_pos, overlay_y_pos)

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

        extension = start_img.filename.split(".")[-1]

        new_img.save("image_watermarked." + extension)
        return
    elif not single:
        path = "\\bulk"
        complete_path = os.getcwd() + path
        os.chdir(complete_path)
        for filename in os.listdir(os.getcwd()):
            if os.path.isfile(filename):
                start_img = Image.open(filename)
                new_overlay = overlay_img.resize(new_overlay_size(start_img, overlay_img), Image.ANTIALIAS)

                new_img = start_img.copy()

                position = pos_overlay(new_img, new_overlay)

                position = position.get(pos_text) or position['bottom right']

                new_img.paste(new_overlay, position, new_overlay)

                extension = start_img.filename.split(".")[-1]

                dir_name = "watermarked"
                try:
                    (os.mkdir(dir_name))
                    print("Created directory...", flush=True)
                except FileExistsError:
                    print("Directory already exists...", flush=True)
                os.chdir(dir_name)
                new_img.save(filename + "_watermarked." + extension)
                os.chdir(complete_path)
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
