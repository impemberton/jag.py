import unittest

from textnode import TextNode, TextType
from split import split_nodes_delimiter

class Test_Split_Nodes_Delimiter(unittest.TestCase):
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
        node = TextNode("This **bold text is missing a delimiter", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        node = TextNode("This is text with one **bold** word here and another **bold** word here", TextType.TEXT)
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
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, test_new_nodes)

    def test_delimiter_at_start(self):
        node = TextNode("**This** is bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_new_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("This", TextType.BOLD),
            TextNode(" is bold", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, test_new_nodes)
