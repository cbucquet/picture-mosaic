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
        bins = [5*i for i in range(255//5)]

        # Make plot
        plt.hist(averages, bins, histtype='bar')
        plt.xlabel('pixel value')
        plt.ylabel('count')
        plt.title('Templates distribution')
        plt.show()

    else:
        r = [x[0] for x in averages]
        g = [x[1] for x in averages]
        b = [x[2] for x in averages]

        # Make 3D plot
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter3D(r, g, b)
        ax.set(xlim=(0, 255), ylim=(0, 255), zlim=(0, 255))
        plt.show()






if __name__ == "__main__":
    main()