
from .renderer import ImageRenderer
import xml.etree.ElementTree as ElementTree
from .layoutnode import LayoutNode

class LayoutImage:
    """ An XML to image converter, using some basic tags and attributes """

    def __init__(self, text: str):
        """ Constructor, with an XML string as input """
        # The renderer used to create the image. Is only created when `generate`
        # is called
        self._renderer: 'None | ImageRenderer' = None
        self._text = text
        self._xml = self._parse_xml()
        self._tree: 'None | LayoutNode' = None
        if self._xml.tag != "image":
            raise ValueError(f"Root tag should be image, not {self._xml.tag}")

    def generate(self):
        """ Generate the image for the stored XML """
        self._renderer = ImageRenderer()
        self._tree = LayoutNode(self._xml)
        self._tree.propagate_inherit()
        self._tree.propagate_pos()
        self._tree.draw(self._renderer)

    def save(self, filename: str):
        """ Save the generated image to a file with the given filename, as a PNG
            """
        if self._renderer is None:
            raise RuntimeError("Cannot call `save` before `generate`")
        self._renderer.save(filename)

    def __eq__(self, other: object):
        """ Check if two layout images are the same """
        return self.__class__ == other.__class__ and self._xml == other._xml

    def __repr__(self):
        """ Get a debug string representation of the layout tree """
        if self._tree is None:
            return "LayoutImage"
        return self._tree.__repr__()

    def _parse_xml(self):
        """ Parse the stored XML text and return the generated element tree """
        return ElementTree.fromstring(self._text)