from PIL import Image, ImageOps

# CONSTANTS
PIXELATED_SIZE = 600 # number of pixels in conterted image (lowest of height/width)
TEMPLATE_SIDE = 40
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