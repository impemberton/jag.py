import unittest

from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        props = {"href": "https:/www.test.com"}
        node = LeafNode("a", "Test Link", props)
        self.assertEqual(node.to_html(), '<a href="https:/www.test.com">Test Link</a>')

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
