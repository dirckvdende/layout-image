
import pytest
from layoutimg.renderer import ImageRenderer

def test_multiple_rect():
    rA = ImageRenderer()
    rB = ImageRenderer()
    rA.draw_rect(50, 50, 100, 100, color="black")
    rB.draw_rect(50, 50, 100, 50, color="black")
    rB.draw_rect(50, 100, 100, 50, color="black")
    assert rA == rB

def test_render_text():
    r = ImageRenderer()
    r.draw_text(0, 0, "Hello World!")

def test_no_expand():
    r = ImageRenderer(10, 10, expand=False)
    r.draw_rect(50, 50, 100, 100)
    assert r.width == 10 and r.height == 10

def test_disable_expand():
    r = ImageRenderer()
    r.draw_rect(50, 50, 100, 100)
    w, h = r.width, r.height
    r.expand = False
    r.draw_rect(100, 100, 100, 100)
    assert r.width == w and r.height == h

def test_very_long_text():
    r = ImageRenderer()
    text = "Lorem Ipsum " * 100
    r.draw_text(0, 0, text)