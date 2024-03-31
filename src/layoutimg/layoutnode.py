
from typing import Literal
from xml.etree.ElementTree import Element
from .layoutenv import LayoutEnv
from .renderer import ImageRenderer

# A renderer only used to get the bounding box of some text
_bbox_renderer = ImageRenderer()

class LayoutNode:
    """ A node which represents an XML tag in the XML source text. It contains
        a reference to the original node, as well as environment and dimension
        information """
    
    def __init__(self, node: Element, parent: 'None | LayoutNode' = None):
        """ Constructor, from an XML element node and the parent layout node.
            This automatically creates a tree of layout nodes, where children
            have a link to their parent """
        self._parent = parent
        self.node = node
        self.env = LayoutEnv()
        self.env.set_defauts(node.tag)
        self._process_attributes()
        self.children = [LayoutNode(child, self) for child in self.node]
        self.size: 'tuple[int, int]' = (0, 0)
        self.pos: 'tuple[int, int]' = (-1, -1)
    
    def __iter__(self):
        """ Iterator over children """
        yield from self.children

    def propagate_inherit(self):
        """ Replace all "inherit" values in environments in the tree """
        if self._parent is not None:
            self.env.inherit(self._parent.env)
        for child in self:
            child.propagate_inherit()

    def propagate_pos(self, pos: 'tuple[int, int]' = (0, 0)):
        """ Determine size and position of this node and all child nodes, given
            the current position """
        self.pos = pos
        for dim in ("width", "height"):
            self._edit_size_before_children(dim)
        for child in self:
            child.propagate_pos(pos)
            # Update current position
            if child.env["continue"] == "none":
                continue
            assert child.env["continue"] in ("x", "y", "xy")
            if "x" in child.env["continue"]:
                pos = (pos[0] + child.size[0], pos[1])
            if "y" in child.env["continue"]:
                pos = (pos[0], pos[1] + child.size[1])
        for dim in ("width", "height"):
            self._edit_size_after_children(dim)

    def draw(self, renderer: ImageRenderer):
        """ Draw the current layout node and its descendents to the given
            renderer """
        # Background color
        if self.env["background-color"] != "none":
            renderer.draw_rect(*self.pos, *self.size,
            color=self.env["background-color"])
        # Rendering text
        if self.env["render-text"] == "true":
            self._draw_text(renderer, only_bbox=False)
        for child in self:
            child.draw(renderer)

    def _edit_size_before_children(self, name: 'Literal["width", "height"]'):
        """ Modify self.size based on the size, without considering "auto".
            Given as an argument is whether the width or height should be edited
            """
        index = 0 if name == "width" else 1
        size = list(self.size)
        if self.env[name] == "auto":
            return
        if self.env[name].endswith("%"):
            # Pecentages
            prop = float(self.env[name][:-1]) / 100
            size[index] = int(prop * self._parent.size[index])
        else:
            # Raw numbers
            size[index] = int(self.env[name])
        self.size = size

    def _edit_size_after_children(self, name: 'Literal["width", "height"]'):
        """ Modify self.size based on the size, only considering "auto" and
            using child sizes. Given as an argument is whether the width or
            height should be edited """
        index = 0 if name == "width" else 1
        size = list(self.size)
        if self.env[name] != "auto":
            return
        assert self.env["render-text"] in ("true", "false")
        if self.env["render-text"] == "true":
            self._edit_size_text(name)
            return
        for child in self:
            size[index] = max(size[index], child.pos[index] + child.size[index]
            - self.pos[index])
        self.size = size

    def _edit_size_text(self, name: 'Literal["width", "height"]'):
        """ Modify self.size based on the size of the text contained in this
            element. This function should only be called if the variable has
            "auto" as a value """
        if name == "width":
            bbox = self._draw_text(_bbox_renderer, only_bbox=True)
            self.size = (bbox[2], self.size[1])
        else:
            self.size = (self.size[0], self._font_height)

    def _process_attributes(self):
        """ Process the attributes of the XML node and set them as environment
            variables """
        for name, value in self.node.attrib.items():
            if name not in self.env:
                raise AttributeError(f"The attribute {name} is not valid")
            self.env[name] = value

    def _draw_text(self, renderer: ImageRenderer, only_bbox: bool = False):
        """ Render text in this node to the given renderer. Returns the bounding
            box of the text as (x, y, dx, dy). Optionally, only the bounding box
            can be determined without drawing """
        text = "" if self.node.text is None else self.node.text
        bbox = renderer.draw_text(*self.pos, text,
            font = None if self.env["font"] == "default" else self.env["font"],
            font_size = int(self.env["font-size"]),
            color = self.env["text-color"],
            only_bbox = only_bbox
        )
        return bbox
    
    @property
    def _font_height(self):
        """ The font height in this element, which is larger than font size """
        return int(int(self.env["font-size"]) * 1.35)
