import unittest
from md_functions import extract_markdown_images, extract_markdown_links


class TestRegexMatching(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is one image ![image1](https://i.imgur.com/test1.png) and another ![image2](https://i.imgur.com/test2.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/test1.png"),
                             ("image2", "https://i.imgur.com/test2.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [link](https://www.test.com)"
        )
        self.assertListEqual([("link", "https://www.test.com")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
                "This is one ![link1](https://www.test1.com) and another ![link2](https://www.test2.com)"
            )
        self.assertListEqual([("link1", "https://www.test1.com"),
                             ("link2", "https://www.test2.com")], matches)

    def test_extract_markdown_image_with_links(self):
        matches = extract_markdown_images("This is a [link](https://www.link.com) and this is an ![image](https://www.image.com/image.png)")
        self.assertListEqual([("image", "https://www.image.com/image.png")], matches)

    def test_extract_markdown_link_with_images(self):
        matches = extract_markdown_links("This is a [link](https://www.link.com) and this is an ![image](https://www.image.com/image.png)")
        self.assertListEqual([("link", "https://www.link.com")], matches)
