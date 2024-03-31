
import pytest
import string
import random
from layoutimg import LayoutImage
from xml.sax.saxutils import escape

letters = string.ascii_lowercase + string.ascii_uppercase + string.punctuation
random_samples = [
    ''.join(
        random.choice(letters) for i in range(random.randint(2, 40))
    ) for j in range(100)
]

@pytest.mark.parametrize("text", random_samples)
def test_random_string(text: str):
    """ Test displaying a string of random characters """
    image = LayoutImage(f"""<image>
        <row><text>{escape(text)}</text></row>
    </image>""")
    image.generate()