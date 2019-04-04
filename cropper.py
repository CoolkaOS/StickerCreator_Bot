from PIL import Image, ImageOps, ImageDraw
import os
import shutil


def crop_all():

    images = []
    num = 1

    for file in os.listdir('input/'):           #search for images in 'input'
        if file[-3:] == 'jpg' or file[-3:] == 'png' or file[-4:] ==  'jpeg':
            images.append(file)

    for name in images:         #resizes and crops
        img = Image.open('input/'+name)

        width, height = img.size            #crop to square
        if width > height:
            margin = (width - height) / 2
            img = img.crop((margin, 0, width - margin, height))
        elif width < height:
            margin = (-width + height) / 2
            img = img.crop((0, margin, width, height - margin))

        basewidth = 512                 #resizes image to 512x512
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)

        bigsize = (img.size[0] * 3, img.size[1] * 3)                #creats round mask
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(img.size, Image.ANTIALIAS)
        img.putalpha(mask)

        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))             #crops according to mask
        output.putalpha(mask)

        try:                            #creats output folder if it doesn't exist
            os.mkdir('output')
        except FileExistsError:
            pass

        output.save('output/{}.png'.format(name[:-4]))


def clear():
    for folder in ['input/', 'output/']:
        for file in os.listdir(folder):
            os.remove(folder+file)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu