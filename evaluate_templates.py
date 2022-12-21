import sys
from PIL import Image
import matplotlib.pyplot as plt
from make_templates import collectTemplateFileName
from utilities import *


def main():
    if(len(sys.argv) != 2):
        print("Error: Incorrect number of arguments. Usage: python evaluate_templates.py <template folder path>")
        sys.exit(1)

    inputPath = sys.argv[1]

    templates = []
    templatesPath = collectTemplateFileName(inputPath)
    for path in templatesPath:
        templates.append(Image.open(path).convert('L') if BLACK_AND_WHITE else Image.open(path).convert('RGB'))

    averages = []
    for template in templates:
        averages.append(findMainColor(template))

    if BLACK_AND_WHITE:
        averages.sort()
        ideal = []

        for i in range(len(averages)):
            ideal.append(255/len(averages) * i)
        
        # Make plot
        plt.plot(averages, label = "actual template color distribution")
        plt.plot(ideal, label = "ideal distribution")
        plt.xlabel('template #')
        plt.ylabel('grayscale value')
        plt.title('Template distribution')
        plt.legend()
        plt.show()

    else:
        print("Currently not supported for color images")






if __name__ == "__main__":
    main()