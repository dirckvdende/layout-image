
import pytest
import os
import pathlib
from layoutimg import LayoutImage

# Find all XML files in the examples directory
files = [f for f in os.listdir("examples/") if pathlib.Path(f).suffix == ".xml"]

@pytest.mark.parametrize("name", files)
def test_example(name: str):
    """ Test converting one of the examples to an image """
    filename = f"examples/{name}"
    with open(filename, "r") as f:
        text = f.read()
    image = LayoutImage(text)
    image.generate()