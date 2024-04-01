
# `layout-image`: A package for generating simple text-based images

A python package for creating basic images with XML layouts.

## Installation

The package can be installed using the following command, which copies the GitHub repository:
```sh
pip install git+https://github.com/dirckvdende/layout-image.git
```

## Basic Example

Several examples of layouts that can be rendered can be found in the [examples](./examples/) directory. A very basic example of XML code that displays the text "Hello World!" in an image is:
```xml
<?xml version="1.0"?>
<image>
    <text>Hello World!</text>
</image>
```
Every layout image has `<image>` as the root element. Inside it can be some layout of elements. Only `<text>` elements can contain text that will be rendered to the screen. This example can be converted to an image using
```sh
python -m layoutimg ./examples/hello-world.xml
```
This will produce a PNG image that has the same path as the XML file, with `.png` appended to it. Alternatively the PNG can be generated using Python code:
```py
from layoutimg import LayoutImage

# Open the example file and read contents
with open("./examples/hello-world.xml", "r") as f:
    text = f.read()
# Create a layout image from the source file text
image = LayoutImage(text)
# Generate image data
image.generate()
# Save image to PNG file
image.save("./examples/hello-world.xml.png")
```

## Syntax

To display multiple lines of text, the `<row>` tag can be used as follows:
```xml
<?xml version="1.0"?>
<image>
    <row><text>Foo</text></row>
    <row><text>Bar</text></row>
</image>
```
Similarly, the `<col>` tag can be used to display elements next to each other. Rows and columns can be nested to form a table:
```xml
<?xml version="1.0"?>
<image>
    <col>
        <row><text>Fizz</text></row>
        <row><text>Buzz</text></row>
    </col>
    <col>
        <row><text>Bazz</text></row>
        <row><text>Fuzz</text></row>
    </col>
</image>
```
A description of every tag can be found at [Element Tags](./docs/tags.md).

### Attributes

That style and modify the elements, attributes can be used. For example, a row or column can be given a background color as follows:
```xml
<?xml version="1.0"?>
<image>
    <row background-color="blue"><text>Foo</text></row>
</image>
```
We can also change the width of the row, and display the text in the center:
```xml
<?xml version="1.0"?>
<image>
    <row background-color="blue" width="500"><text text-align="center">Foo</text></row>
</image>
```
A complete list of attributes with possible values can be found at [Element Attributes](./docs/attributes.md).
