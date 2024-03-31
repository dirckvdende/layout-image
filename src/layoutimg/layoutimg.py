
from .renderer import ImageRenderer
import xml.etree.ElementTree as ElementTree

class LayoutImage:
    """ An XML to image converter, using some basic tags and attributes """

    def __init__(self, text: str):
        """ Constructor, with an XML string as input """
        # The renderer used to create the image. Is only created when `generate`
        # is called
        self._text = text
        self._xml = self._parse_xml()
        if self._xml.tag != "image":
            raise ValueError(f"Root tag should be image, not {self._xml.tag}")
        self._renderer: 'None | ImageRenderer' = None

    def generate(self):
        """ Generate the image for the stored XML """
        self._renderer = ImageRenderer()
        # Current position to draw elements
        self._position: 'tuple[int, int]' = (0, 0)
        self._process_node(self._xml, True)

    def save(self, filename: str):
        """ Save the generated image to a file with the given filename, as a PNG
            """
        if self._renderer is None:
            raise RuntimeError("Cannot call `save` before `generate`")
        self._renderer.save(filename)

    def __eq__(self, other: object):
        """ Check if two layout images are the same """
        return self.__class__ == other.__class__ and self._xml == other._xml

    def _parse_xml(self):
        """ Parse the stored XML text and return the generated element tree """
        return ElementTree.fromstring(self._text)

    def _process_node(self, node: ElementTree.Element, is_root: bool = False):
        """ Process a node in the XML parse tree. If this node is the root, this
            should be passed """
        if node.tag not in ("image", "row", "col", "text"):
            raise ValueError(f"XML tag {node.tag} is not allowed")
        if not is_root and node.tag == "image":
            raise ValueError("Image tag is only allowed as root")
        pre_position = self._position
        self._process_node_attributes(node)
        if node.tag == "text":
            self._process_text_node(node)
        elif node.text is not None and node.text.strip() != "":
            raise ValueError("Text only allowed in text nodes")
        # Process children
        for child in node:
            self._process_node(child)
        self._update_position(node, pre_position)

    def _process_node_attributes(self, node: ElementTree.Element):
        """ Process the attributes of a node in the XML parse tree, except for
            width and height which are processed separately """
        # TODO: Implement
        pass

    def _process_text_node(self, node: ElementTree.Element):
        """ Process a text node in the XML parse tree, adds width and height
            attributes that correspond with the width and height of the text
            (unless already set) """
        # NOTE: Text is automatically stripped. We may want a way to disable
        # this at some point
        text = "" if node.text is None else node.text
        text = text.strip()
        font_size = int(node.get("font-size", "64"))
        bbox = self._renderer.draw_text(*self._position, text,
            font = node.get("font", None),
            color = node.get("color", "black"),
            font_size = font_size
        )
        # Set width and height if needed
        if node.get("width") is None:
            node.set("width", str(bbox[2]))
        if node.get("height") is None:
            node.set("height", str(font_size))
        # Check if node has children, which is not allowed
        if len(node):
            raise ValueError("Text node cannot contain subtree")

    def _update_position(self, node: ElementTree.Element,
    pre_position: 'tuple[int, int]'):
        """ Update the current drawing position, given the current node and
            drawing position before the node was processed. This function also
            handles width and height attributes """
        x, y = pre_position
        width, height = node.get("width"), node.get("height")
        if node.tag in ("col", "text"):
            if width is not None:
                x += int(width)
            else:
                x = self._position[0]
        if node.tag in ("row", "text"):
            if height is not None:
                y += int(height)
            else:
                y = self._position[1]
        self._position = (x, y)