
from typing import Literal
from xml.etree.ElementTree import Element
from .layoutenv import LayoutEnv
from .renderer import ImageRenderer
import math

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
        self._set_custom_pos()
        pos = self.pos
        for dim in ("width", "height"):
            self._edit_size_before_children(dim)
        for child in self:
            child.propagate_pos(pos)
            # Update current position
            if child.env["flow"] == "none":
                continue
            assert child.env["flow"] in ("x", "y", "xy")
            if "x" in child.env["flow"]:
                pos = (max(pos[0], child.pos[0] + child.size[0]), pos[1])
            if "y" in child.env["flow"]:
                pos = (pos[0], max(pos[1], child.pos[1] + child.size[1]))
        for dim in ("width", "height"):
            self._edit_size_after_children(dim)

    def draw(self, renderer: ImageRenderer):
        """ Draw the current layout node and its descendents to the given
            renderer """
        # Expand image to include element
        renderer.expand_image(*self.pos, *self.size)
        # Background color
        if self.env["background-color"] != "none":
            renderer.draw_rect(*self.pos, *self.size,
            color=self.env["background-color"])
        # Background image
        if self.env["background-image"] != "none":
            renderer.draw_image(*self.pos, *self.size,
            self.env["background-image"])
        # Rendering text
        if self.env["render-text"] == "true":
            self._draw_text(renderer)
        for child in self:
            child.draw(renderer)

    def __repr__(self):
        """ Get a debug representation of the layout tree """
        return self._debug_string()
    
    def _debug_string(self, depth: int = 0):
        """ Get a debug representation of the layout tree, given the current
            depth of the node """
        text = "| " * depth
        text += f"<{self.node.tag}> pos={self.pos} size={self.size}\n"
        for child in self:
            text += child._debug_string(depth + 1)
        return text

    def _set_custom_pos(self):
        """ If one or both attributes x and y are given, apply these values to
            the position of the element """
        for attr, index in (("x", 0), ("y", 1)):
            if self.env[attr] == "auto":
                continue
            value = int(self.env[attr])
            new_pos = list(self.pos)
            new_pos[index] = value
            self.pos = tuple(new_pos)

    def _edit_size_before_children(self, name: 'Literal["width", "height"]'):
        """ Modify self.size based on the size, without considering "auto".
            Given as an argument is whether the width or height should be edited
            """
        index = 0 if name == "width" else 1
        size = list(self.size)
        if self.env[name] == "auto":
            self._clamp_size(name)
            return
        parent_size = 0 if self._parent is None else self._parent.size[index]
        size[index] = self._value_to_pixels(self.env[name], parent_size)
        self.size = tuple(size)
        self._clamp_size(name)

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
            self._clamp_size(name)
            return
        for child in self:
            size[index] = max(size[index], child.pos[index] + child.size[index]
            - self.pos[index])
        self.size = tuple(size)
        self._clamp_size(name)

    def _clamp_size(self, name: 'Literal["width", "height"]'):
        """ Clamp the width and height of the element to the min and max values
            in the environment """
        index = 0 if name == "width" else 1
        def clamp(val: int, mn: int, mx: int):
            return max(mn, min(val, mx))
        size = list(self.size)
        parent_size = 0 if self._parent is None else self._parent.size[index]
        mn = self._value_to_pixels(self.env[f"min-{name}"], parent_size)
        mx = self._value_to_pixels(self.env[f"max-{name}"], parent_size)
        size[index] = clamp(size[index], mn, mx)
        self.size = tuple(size)

    def _value_to_pixels(self, value: str, relative: int):
        """ Convert a percentage or fixed value to a pixel count integer. The
            relative size of the parent should be given for the case that the
            value is a percentage """
        if value.endswith("%"):
            # Pecentages
            prop = float(value[:-1]) / 100
            return int(prop * relative)
        # Raw numbers
        return int(value)

    def _edit_size_text(self, name: 'Literal["width", "height"]'):
        """ Modify self.size based on the size of the text contained in this
            element. This function should only be called if the variable has
            "auto" as a value """
        size = list(self.size)
        if name == "width":
            size[0] = max(size[0], self._text_dims()[0])
        else:
            size[1] = max(size[1], self._font_height)
        self.size = tuple(size)

    def _process_attributes(self):
        """ Process the attributes of the XML node and set them as environment
            variables """
        for name, value in self.node.attrib.items():
            if name not in self.env:
                raise AttributeError(f"The attribute {name} is not valid")
            self.env[name] = value

    def _draw_text(self, renderer: ImageRenderer):
        """ Render text in this node to the given renderer. Returns the bounding
            box of the text as (x, y, dx, dy) """
        text_width = self._text_dims()[0]
        align = self.env["text-align"]
        if align not in ("left", "center", "right"):
            raise ValueError(f"Value text-align cannot be \"{align}\"")
        left_pad = {
            "left": 0,
            "center": max(0, self.size[0] - text_width) // 2,
            "right": max(0, self.size[0] - text_width),
        }[align]
        bbox = renderer.draw_text(
            x = self.pos[0] + left_pad,
            y = self.pos[1],
            text = self._text,
            font = None if self.env["font"] == "default" else self.env["font"],
            font_size = int(self.env["font-size"]),
            color = self.env["text-color"]
        )
        return bbox
    
    def _text_dims(self):
        """ Get the dimensions of the text in the element being drawn """
        bbox = _bbox_renderer.draw_text(0, 0, self._text,
            font = None if self.env["font"] == "default" else self.env["font"],
            font_size = int(self.env["font-size"]),
            color = self.env["text-color"],
            only_bbox = True
        )
        return bbox[2:]
    
    @property
    def _font_height(self):
        """ The font height in this element, which is larger than font size """
        return int(int(self.env["font-size"]) * 1.35)
    
    @property
    def _text(self):
        """ The text to be displayed in this element """
        return "" if self.node.text is None else self.node.text
