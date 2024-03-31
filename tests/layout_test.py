
import pytest
from layoutimg import LayoutImage

def test_list():
    text = open("examples/list.xml", "r").read()
    image = LayoutImage(text)
    image.generate()
    image.save("test.png")

test_list()