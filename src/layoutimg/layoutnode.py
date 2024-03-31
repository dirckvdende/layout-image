
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
            child.propagate_inherit(self)

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
        # TODO: Implement rendering
        if self.env["background-color"] != "none":
            renderer.draw_rect(*self.pos, *self.size,
            color=self.env["background-color"])
        if self.env["render-text"] == "true":
            text = "" if self.node.text is None else self.node.text
            renderer.draw_text(*self.pos, text)
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
            size[index] += child.size[index]
        self.size = size

    def _edit_size_text(self, name: 'Literal["width", "height"]'):
        """ Modify self.size based on the size of the text contained in this
            element. This function should only be called if the variable has
            "auto" as a value """
        text = "" if self.node.text is None else self.node.text
        bbox = _bbox_renderer.draw_text(*self.pos, text, only_bbox=True)
        self.size = bbox[2:4]
