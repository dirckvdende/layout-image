
import pytest
from layoutimg.renderer import ImageRenderer

def test_multiple_rect():
    rA = ImageRenderer()
    rB = ImageRenderer()
    rA.draw_rect(50, 50, 100, 100, color="black")
    rB.draw_rect(50, 50, 100, 50, color="black")
    rB.draw_rect(50, 100, 100, 50, color="black")
    assert rA.image == rB.image

def test_render_text():
    r = ImageRenderer()
    r.draw_text(0, 0, "Hello World!")
    r.save("test.png")