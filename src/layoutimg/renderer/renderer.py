
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
        self.expand_image(x, y, dx, dy)
        self._draw.rectangle((x, y, x + dx, y + dy), fill=color)

    def draw_text(self, x: int, y: int, text: str, *, font: 'str | None' = None,
    color: str = "black", font_size: int = 64, only_bbox: bool = False):
        """ Draw text to the image, given the coordinates of the top left corner
            and the text to draw. A font, font size and color can also be
            provided. Returns the bounding box of the text as (x, y, dx, dy).
            Optioanlly an argument can be given to only return the bounding box
            """
        font_data = self._load_font(font, font_size)
        args = {"xy": (x, y), "text": text, "font": font_data,
        "font_size": font_size}
        bbox = self._bbox_convert(self._draw.textbbox(**args))
        if only_bbox:
            return bbox
        self.expand_image(*bbox)
        self._draw.text(**args, fill=color)
        return bbox

    def draw_image(self, x: int, y: int, dx: int, dy: int, path: str):
        """ Draw another image onto this image, given the coordinates of the top
            left corner, the dimensions to draw and the path of the image to
            draw """
        if dx < 1 or dy < 1:
            return
        self.expand_image(x, y, dx, dy)
        with Image.open(path) as image_file:
            resized_image = image_file.resize((dx, dy))
            self._image.paste(resized_image, (x, y, x + dx, y + dy))

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

    def __eq__(self, other: object) -> bool:
        """ Check if two drawings are the same (pixels are equal) """
        return self.__class__ == other.__class__ and self.image == other.image

    def _load_font(self, font: 'str | None' = None, font_size: int = 64):
        """ Load a font based on the path given and return the font object.
            Could also be None, which will return None. If the font is not
            found, None is returned as well """
        if font is None:
            return None
        try:
            return ImageFont.truetype(font, size=font_size)
        except OSError:
            return None
    
    def _bbox_convert(self, bbox: 'tuple[int, int, int, int]'):
        """ Convert a PIL bounding box to a bounding box of the form
            (x, y, dx, dy) """
        return bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]

    def expand_image(self, x: int, y: int, dx: int, dy: int):
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