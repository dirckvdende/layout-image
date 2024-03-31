
from xml.etree.ElementTree import Element
from .layoutenv import LayoutEnv

class LayoutNode:
    """ A node which represents an XML tag in the XML source text. It contains
        a reference to the original node, as well as environment and dimension
        information """
    
    def __init__(self, node: Element):
        """ Constructor, from an XML element node """
        self.node = node
        self.env = LayoutEnv()
        self.env.set_defauts(node.tag)
        self.children = [LayoutNode(child) for child in self.node]
    
    def __iter__(self):
        """ Iterator over children """
        yield from self.children

    def propagate_inherit(self, parent: 'None | LayoutNode' = None):
        """ Replace all "inherit" values in environments in the tree """
        if parent is not None:
            self.env.inherit(parent.env)
        for child in self:
            child.propagate_inherit(self)
