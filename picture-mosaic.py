from PIL import Image, ImageOps
import sys
from os.path import splitext
from make_templates import collectTemplateFileName, transformTemplate
import argparse

# CONSTANTS
PIXELATED_SIZE = 300 # number of pixels in conterted image (lowest of height/width)
TEMPLATE_SIDE = 20
VALID_IMAGE_EXTENSIONS = [".jpeg", ".jpg", ".png"]
BLACK_AND_WHITE = True
IMAGES_FOLDER_PATH = "/Users/Charles/Downloads/images"
TEMPLATES_FOLDER_PATH = "/Users/Charles/Downloads/templates"
IMPORT_PREMADE_TEMPLATES = True
MAIN_COLOR_SCALE = True


def findMainColor(img):
    # Find main pixel color in image
    if MAIN_COLOR_SCALE:
        imgScale = img.resize((1,1), resample=Image.Resampling.BILINEAR)
        return imgScale.getpixel((0,0))
    else:
        run_r, run_g, run_b = 0,0,0
        pixel_count = 0

        height, width = img.size
        for i in range(height):
            for j in range(width):
                r, g, b = img.getpixel((i, j))
                run_r += r
                run_g += g
                run_b += b
                pixel_count += 1

        avg_r = run_r // pixel_count
        avg_g = run_g // pixel_count
        avg_b = run_b // pixel_count

        return avg_r, avg_g, avg_b


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