from PIL import Image, ImageOps
import sys
from os.path import splitext
from make_templates import collectTemplateFileName, transformTemplate
from utilities import *
import argparse





def findClosestValue(pixel, values):
    minIndex = -1
    minIndicator = 255*255 * 3 + 1 # greater than all pixels

    r, g, b, v = 0, 0, 0, 0
    if BLACK_AND_WHITE:
        v = pixel
    else:
        r, g, b = pixel


    for i in range(len(values)):
        if BLACK_AND_WHITE:
            comp_v = values[i]
            indicator = abs(comp_v - v)
        else:
            comp_r, comp_g, comp_b = values[i]
            indicator = (comp_r - r)**2 + (comp_g - g)**2 + (comp_b - b)**2

        if indicator < minIndicator:
            minIndicator = indicator
            minIndex = i
    return minIndex


def main():
    if(len(sys.argv) != 2):
        print("Error: Incorrect number of arguments. Usage: python initial.py <path to image>")
        sys.exit(1)
    
    imagePath = sys.argv[1]

    print("Importing picture to mosaicfy...")
    # Open image in pillow
    img = Image.open(imagePath)
    img = ImageOps.exif_transpose(img)
    img = img.convert('L') if BLACK_AND_WHITE else img.convert('RGB')
    width, height = img.size
    # print(width, height)
    # img.show()
    
    # Pixelate image
    IMAGE_WIDTH = PIXELATED_SIZE * height // width
    IMAGE_HEIGHT = PIXELATED_SIZE
    if height > width:
        IMAGE_WIDTH = PIXELATED_SIZE
        IMAGE_HEIGHT = PIXELATED_SIZE * width // height

    imgPixelated = img.resize((IMAGE_HEIGHT,IMAGE_WIDTH), resample=Image.Resampling.BILINEAR)
    imgPixelatedShow = imgPixelated.resize(img.size, Image.Resampling.NEAREST) # scale it back (for showing)
    # imgPixelatedShow.show()

    print("Done!")
    print("Making templates from pictures...")
    # Generate templates
    templates = []
    if IMPORT_PREMADE_TEMPLATES:
        templatesPath = collectTemplateFileName(TEMPLATES_FOLDER_PATH)
        for path in templatesPath:
            templates.append(Image.open(path).convert('L') if BLACK_AND_WHITE else Image.open(path).convert('RGB'))
    else:
        templatesPath = collectTemplateFileName(IMAGES_FOLDER_PATH)
        for path in templatesPath:
            templates.append(transformTemplate(path))

    # Get average pixel value for each template
    averages = []
    for template in templates:
        averages.append(findMainColor(template))

    print("Done!")
    print("Making final pictures from templates...")
    # Collate final image based on closest pixel value
    FINAL_IMAGE_WIDTH = IMAGE_WIDTH * TEMPLATE_SIDE
    FINAL_IMAGE_HEIGHT = IMAGE_HEIGHT * TEMPLATE_SIDE
    new_image = Image.new('RGB',(FINAL_IMAGE_HEIGHT, FINAL_IMAGE_WIDTH))
    for i in range(IMAGE_HEIGHT):
        for j in range(IMAGE_WIDTH):
            index = findClosestValue(imgPixelated.getpixel((i,j)), averages)

            new_image.paste(templates[index],(i*TEMPLATE_SIDE,j*TEMPLATE_SIDE))

    print("Done!")
    print("Now showing and saving image")
    new_image.save(splitext(imagePath)[0]+"-mosaic.jpeg")
    # new_image.show()

if __name__ == "__main__":
    main()