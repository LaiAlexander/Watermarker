#! python3

from PIL import Image

color = input("Which color? ")
if color == "white" or color == "black":
    overlay_image = Image.open("logo_" + color + ".png")
elif color != "default":
    print("Not a valid color, will use default colors. Use 'black', 'white' or 'default'")
    overlay_image = Image.open("logo.png")
else:
    overlay_image = Image.open("logo.png")
start_image = Image.open("image.jpg")

def get_new_overlay_size(start, overlay):
    overlay_new_width = int(start.size[0] / 5)
    factor = overlay_new_width / overlay.size[0]
    overlay_new_height = int(overlay.size[1] * factor)
    return (overlay_new_width, overlay_new_height)

resized_overlay = overlay_image.resize(get_new_overlay_size(start_image, overlay_image), Image.ANTIALIAS)

new_image = start_image.copy()

def get_bottom_right_pos(start, overlay):
    overlay_x_pos = start.size[0] - overlay.size[0]
    overlay_y_pos = start.size[1] - overlay.size[1]
    return (overlay_x_pos, overlay_y_pos)

new_image.paste(resized_overlay, get_bottom_right_pos(new_image, resized_overlay), resized_overlay)

extension = start_image.filename.split(".")[-1]

new_image.save("image_new." + extension)
# may also do this, might be better:
# new_image.save("newimage." + start_image.format)
