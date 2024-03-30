
import pytest
from layoutimg.renderer import ImageRenderer

def test_multiple_rect():
    rA = ImageRenderer(200, 200)
    rB = ImageRenderer(200, 200)
    rA.drawRect(50, 50, 100, 100, "black")
    rB.drawRect(50, 50, 100, 50, "black")
    rB.drawRect(50, 100, 100, 50, "black")
    assert rA.image == rB.image