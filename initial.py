from PIL import Image
import sys



# Open image in pillow
img = Image.open("test-image.jpeg")
img = img.convert('RGB')
width, height = img.size
print(width, height)
# im.show()


# Pixelate an image
PIXELATED_SIZE = 15

IMAGE_WIDTH = PIXELATED_SIZE * height // width
IMAGE_HEIGHT = PIXELATED_SIZE
if height > width:
    IMAGE_WIDTH = PIXELATED_SIZE
    IMAGE_HEIGHT = PIXELATED_SIZE * width // height

imgSmall = img.resize((IMAGE_HEIGHT,IMAGE_WIDTH), resample=Image.Resampling.BILINEAR)
result = imgSmall.resize(img.size, Image.Resampling.NEAREST) # scale it back (for showing)

result.show()



# Find main pixel color in image
run_r, run_g, run_b = 0,0,0
pixel_count = 0

height, width = img.size
# for i in range(height):
#     for j in range(width):
#         r, g, b = img.getpixel((i, j))
#         run_r += r
#         run_g += g
#         run_b += b
#         pixel_count += 1

# avg_r = run_r // pixel_count
# avg_g = run_g // pixel_count
# avg_b = run_b // pixel_count

# print(avg_r, avg_g, avg_b)



# Transform an image
TEMPLATE_SIDE = 100

width, height = img.size

square_side = min(width, height)
offset = abs(width - height) // 2

left = offset if width > height else 0
top = 0 if width > height else offset
right = square_side + left 
bottom = square_side + top


# Cropped image of above dimension
im1 = img.crop((left, top, right, bottom))
res = im1.resize((TEMPLATE_SIDE,TEMPLATE_SIDE), resample=Image.Resampling.BILINEAR)

# Shows the image in image viewer
# res.show()


# Collate pictures
FINAL_IMAGE_WIDTH = IMAGE_WIDTH * TEMPLATE_SIDE
FINAL_IMAGE_HEIGHT = IMAGE_HEIGHT * TEMPLATE_SIDE
print(FINAL_IMAGE_HEIGHT, FINAL_IMAGE_WIDTH)
new_image = Image.new('RGB',(FINAL_IMAGE_HEIGHT, FINAL_IMAGE_WIDTH))
new_image.show()
for i in range(IMAGE_HEIGHT):
    for j in range(IMAGE_WIDTH):
        # FIND CLOSEST MATCH HERE
        new_image.paste(res,(i*TEMPLATE_SIDE,j*TEMPLATE_SIDE))
new_image.show()