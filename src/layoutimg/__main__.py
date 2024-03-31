
import sys
from .layoutimg import LayoutImage

def main():
    """ Generate one of the examples using the main function """
    if len(sys.argv) <= 1:
        print("Generate a layout image given by its path name. The output fill "
        "have the same name as the input file, but with a PNG extension.")
        return
    input_filename = sys.argv[1]
    output_filename = input_filename + ".png"
    with open(input_filename, "r") as input_file:
        text = input_file.read()
    image = LayoutImage(text)
    image.generate()
    image.save(output_filename)

if __name__ == "__main__":
    main()