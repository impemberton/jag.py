import unittest

from textnode import TextNode, TextType
from md_functions import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_new_nodes)

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_new_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_new_nodes)

    def test_code(self):
        node = TextNode("This is text with `code` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_new_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_new_nodes)

    def test_non_matching_delimiter(self):
        node = TextNode(
            "This **bold text is missing a delimiter", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter,
                          [node], "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        node = TextNode(
            "This is text with one **bold** word here and another **bold** word here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_new_nodes = [
            TextNode("This is text with one ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word here and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_new_nodes)

    def test_delimiter_at_end(self):
        node = TextNode("This is text with an _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_new_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, test_new_nodes)

    def test_delimiter_at_start(self):
        node = TextNode("**This** is bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_new_nodes = [
            TextNode("This", TextType.BOLD),
            TextNode(" is bold", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_new_nodes)

    def test_multiple_nodes(self):
        node1 = TextNode("This **is** bold", TextType.TEXT)
        node2 = TextNode("This is **bold** also", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        test_new_nodes = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" also", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_new_nodes)


class TestImageLinkSplitting(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node1 = TextNode(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and another ![second image2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is more text with an ![image3](https://i.imgur.com/zjjcJKZ.png) and another ![second image4](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is more text with an ", TextType.TEXT),
                TextNode("image3", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image4", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_at_start(self):
        node = TextNode(
            "![this](https://i.imgur.com/zjjcJKZ.png) image is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("this", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" image is at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "This image is at the ![end](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This image is at the ", TextType.TEXT),
                TextNode("end", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.test1.com) and another [second link](https://www.test2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.test1.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK,
                         "https://www.test2.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        node1 = TextNode(
            "This is text with a [link1](https://www.test1.com) and another [second link2](https://www.test2.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is more text with a [link3](https://www.test1.com) and another [second link4](https://www.test2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://www.test1.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link2", TextType.LINK,
                         "https://www.test2.com"),
                TextNode("This is more text with a ", TextType.TEXT),
                TextNode("link3", TextType.LINK, "https://www.test1.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link4", TextType.LINK,
                         "https://www.test2.com"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[this](https://www.test1.com) link is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("this", TextType.LINK, "https://www.test1.com"),
                TextNode(" link is at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "this link is at the [end](https://www.test1.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("this link is at the ", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://www.test1.com"),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        textnodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        test_textnodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(textnodes, test_textnodes)
