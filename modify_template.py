import sys
from PIL import Image
from utilities import *


def main():
    if(len(sys.argv) != 2):
        print("Error: Incorrect number of arguments. Usage: python modify_template.py <template path>")
        sys.exit(1)

    templatePath = sys.argv[1]
    img = Image.open(templatePath)
    img = img.convert('L') if BLACK_AND_WHITE else img.convert('RGB')

    if BLACK_AND_WHITE:
        img.show()
        img = grayChangeTemplate(img, lighten=False)
        # img.save(templatePath)
        img.show()

    else:
        print("Operation not currently defined for colors")




if __name__ == "__main__":
    main()