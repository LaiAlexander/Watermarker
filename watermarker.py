#! python3

from PIL import Image

start_image = Image.open("image.jpg")
overlay_image = Image.open("logo.png")

start_width, start_height = start_image.size

overlay_width, overlay_height = overlay_image.size

overlay_new_width = int(start_width / 5)
factor = overlay_new_width / overlay_width
overlay_new_height = int(overlay_height * factor)

resized_overlay = overlay_image.resize((overlay_new_width, overlay_new_height), Image.ANTIALIAS)

new_image = start_image.copy()
# bottom right corner
overlay_x_pos = start_width - overlay_new_width
overlay_y_pos = start_height - overlay_new_height
new_image.paste(resized_overlay, (overlay_x_pos, overlay_y_pos), resized_overlay)

extension = start_image.filename.split(".")[-1]

new_image.save("newimage." + extension)
# may also do this, might be better:
# new_image.save("newimage." + start_image.format)
