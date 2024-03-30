
from PIL import Image, ImageDraw, ImageFont

class ImageRenderer:
    """ A class that makes it easier to render images, by introducing methods
        for drawing text and shapes. It creates a shape with a given size and
        expands it when attempting to draw something outside the image. The
        `expand` property controls whether the image should be expanded when
        drawing outside its bounds, and can be adjusted at any point """

    def __init__(self, width: int = 1, height: int = 1, *,
    background_color: str = "white", expand: bool = True):
        """ Constructor, given starting width and height of the image, the
            background color, and wether the image should be expanded when
            drawing outside its bounds """
        self._background_color = background_color
        self.expand = expand
        self._image = Image.new("RGB", (width, height), self._background_color)
        self._draw = ImageDraw.Draw(self._image)

    def save(self, filename: str):
        """ Save the rendered image to a PNG file with the given filename """
        self._image.save(filename)

    def draw_rect(self, x: int, y: int, dx: int, dy: int, *,
    color: str = "black"):
        """ Draw a rectangle to the image, given the coordinates of the top left
            corner and width and height of the rectangle """
        if dx < 1 or dy < 1:
            return
        self._expand_image(x, y, dx, dy)
        self._draw.rectangle((x, y, x + dx - 1, y + dy - 1), fill=color)

    def draw_text(self, x: int, y: int, text: str, *, font: 'str | None' = None,
    color: str = "black", font_size: int = 64):
        """ Draw text to the image, given the coordinates of the top left corner
            and width and height of the rectangle """
        font_data = self._load_font(font)
        args = {"xy": (x, y), "text": text, "font": font_data,
        "font_size": font_size}
        self._expand_image(*self._bbox_convert(self._draw.textbbox(**args)))
        self._draw.text(**args, fill=color)

    @property
    def image(self):
        """ Get the PIL image that is being drawn on """
        return self._image
    
    @property
    def width(self):
        """ The width of the image """
        return self._image.width
    
    @property
    def height(self):
        """ The height of the image """
        return self._image.height

    def _load_font(self, font: 'str | None' = None):
        """ Load a font based on the path given and return the font object.
            Could also be None, which will return None """
        if font is None:
            return None
        return ImageFont.load(font)
    
    def _bbox_convert(self, bbox: 'tuple[int, int, int, int]'):
        """ Convert a PIL bounding box to a bounding box of the form
            (x, y, dx, dy) """
        return bbox[0], bbox[1], bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1

    def _expand_image(self, x: int, y: int, dx: int, dy: int):
        """ Expand the image, given some bounding box that should be included in
            it. Note that negative coordinates will never be included """
        if not self.expand or dx < 1 or dy < 1:
            return
        width, height = max(self.width, x + dx), max(self.height, y + dy)
        if width == self.width and height == self.height:
            return
        new_image = Image.new(self._image.mode, (width, height),
        self._background_color)
        new_draw = ImageDraw.Draw(new_image)
        new_image.paste(self._image)
        self._image = new_image
        self._draw = new_draw