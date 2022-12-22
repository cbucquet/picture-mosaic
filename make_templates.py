from PIL import Image, ImageOps
import sys
from os import listdir
from os.path import isfile, join, splitext, basename
from utilities import *

def collectTemplateFileName(folderPath):
    names = []
    for name in listdir(folderPath):
        if isfile(join(folderPath, name)) and splitext(name)[1] in VALID_IMAGE_EXTENSIONS:
            names.append(join(folderPath, name))
    return names

def transformTemplate(imagePath):
    img = Image.open(imagePath)
    img = ImageOps.exif_transpose(img)
    img = img.convert('L') if BLACK_AND_WHITE else img.convert('RGB')
    width, height = img.size

    # Find cropped square image boundaries (centered in image)
    square_side = min(width, height)
    offset = abs(width - height) // 2
    left = offset if width > height else 0
    top = 0 if width > height else offset
    right = square_side + left 
    bottom = square_side + top

    # Crop image
    imgCrop = img.crop((left, top, right, bottom))
    imgFinal = imgCrop.resize((TEMPLATE_SIDE,TEMPLATE_SIDE), resample=Image.Resampling.BILINEAR)
    return imgFinal



def main():
    if(len(sys.argv) != 3):
        print("Error: Incorrect number of arguments. Usage: python make-templates.py <input folder path> <output folder path>")
        sys.exit(1)

    inputPath = sys.argv[1]
    outputPath = sys.argv[2]

    print("Generating templates from images...")
    templatesPath = collectTemplateFileName(inputPath)
    for path in templatesPath:
        transformTemplate(path).save(join(outputPath, splitext(basename(path))[0]+".jpeg"))
    print("Done! Succesfully made", len(templatesPath), "templates")


if __name__ == "__main__":
    main()