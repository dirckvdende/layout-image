
import pytest
import pathlib
from layoutimg import LayoutImage

# Find all XML files in the examples directory and subdirectories
files = list(pathlib.Path("examples/").rglob("*.xml"))

@pytest.mark.parametrize("filename", files)
def test_example(filename: str):
    """ Test converting one of the examples to an image """
    with open(filename, "r") as f:
        text = f.read()
    image = LayoutImage(text)
    image.generate()
    image.save(f"{filename}.png")