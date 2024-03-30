
from PIL import Image, ImageDraw

class ImageRenderer:
    """ A class that makes it easier to render images, by introducing methods
        for drawing text and shapes """

    def __init__(self, width: int, height: int):
        """ Constructor, given width and height of the image """
        self._width = width
        self._height = height
        self._image = Image.new("RGB", (width, height), "white")
        self._draw = ImageDraw.Draw(self._image)

    def save(self, filename: str):
        """ Save the rendered image to a PNG file with the given filename """
        self._image.save(filename)

    def drawRect(self, x: int, y: int, dx: int, dy: int, color: str):
        """ Draw a rectangle to the image, given the coordinates of the top left
            corner and width and height of the rectangle """
        self._draw.rectangle((x, y, x + dx, y + dy), fill=color)

    @property
    def image(self):
        """ Get the PIL image that is being drawn on """
        return self._image