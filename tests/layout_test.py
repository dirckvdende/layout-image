
import pytest
from layoutimg import LayoutImage

def xml_to_renderer(text: str):
    """ Convert XML text to a renderer which has the rendered image contained
        """
    image = LayoutImage(text)
    image.generate()
    return image._renderer

def test_render_list():
    text = open("examples/list.xml", "r").read()
    image = LayoutImage(text)
    image.generate()

def test_equal_row_height():
    textA = "<image><text background-color='blue'>aa</text></image>"
    textB = "<image><text background-color='blue'>gh</text></image>"
    assert xml_to_renderer(textA).height == xml_to_renderer(textB).height

def test_different_spacing():
    textA = "<image><text>aa</text></image>"
    textB = "<image> <text>aa</text></image>"
    assert xml_to_renderer(textA) == xml_to_renderer(textB)

def test_double_row_height():
    textA = """<image width='200'>
        <row background-color='blue'><text>A</text></row>
    </image>"""
    textB = """<image width='200'>
        <row background-color='blue'><text>A</text></row>
        <row background-color='blue'><text>B</text></row>
    </image>"""
    assert xml_to_renderer(textA).height * 2 == xml_to_renderer(textB).height

def test_equal_col_height():
    textA = "<image><col background-color='blue'><text>A</text></col></image>"
    textB = """<image>
        <col background-color='blue'><text>A</text></col>
        <col background-color='blue'><text>B</text></col>
    </image>"""
    assert xml_to_renderer(textA).height == xml_to_renderer(textB).height