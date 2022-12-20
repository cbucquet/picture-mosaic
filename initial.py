from PIL import Image
import sys
import time

# CONSTANTS
PIXELATED_SIZE = 15 # number of pixels in conterted image (lowest of height/width)
TEMPLATE_SIDE = 100

def transformTemplate(imagePath, templateSide):
    img = Image.open(imagePath)
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


def findMainColor(img):
    # Find main pixel color in image
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

    return avg_r, avg_b, avg_g


def findClosestValue(pixel, values):
    minIndex = -1
    minIndicator = 255*255 * 3 + 1 # greater than all pixels

    r, g, b = pixel

    for i in range(len(values)):
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
    templatesPath = ["1.jpeg", "2.jpeg", "3.jpeg", "4.jpeg", "5.jpeg"]

    # Open image in pillow
    img = Image.open(imagePath)
    img = img.convert('RGB')
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

    # Generate templates
    templates = []
    for path in templatesPath:
        templates.append(transformTemplate(path, TEMPLATE_SIDE))

    # Get average pixel value for each template
    averages = []
    for template in templates:
        averages.append(findMainColor(template))

    for i in range(len(templates)):
        templates[i].show()
        print(averages[i])
        time.sleep(5)


    # Collate final image based on closest pixel value
    FINAL_IMAGE_WIDTH = IMAGE_WIDTH * TEMPLATE_SIDE
    FINAL_IMAGE_HEIGHT = IMAGE_HEIGHT * TEMPLATE_SIDE
    new_image = Image.new('RGB',(FINAL_IMAGE_HEIGHT, FINAL_IMAGE_WIDTH))
    for i in range(IMAGE_HEIGHT):
        for j in range(IMAGE_WIDTH):
            index = findClosestValue(imgPixelated.getpixel((i,j)), averages)

            new_image.paste(templates[index],(i*TEMPLATE_SIDE,j*TEMPLATE_SIDE))
    new_image.show()

if __name__ == "__main__":
    main()