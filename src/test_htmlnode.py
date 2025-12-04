import unittest

from htmlnode import HTMLNode 


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        tag = "p"
        node = HTMLNode(tag, "this is some text")
        self.assertEqual(node.tag, tag)

    def test_value(self):
        tag = "p"
        value = "This is a value"
        node = HTMLNode(tag, value)
        self.assertEqual(node.value, value)

    def test_children(self):
        tag = "p"
        value = "This is a value"
        children = [HTMLNode("p"), HTMLNode("h1")]
        node = HTMLNode(tag, value, children)
        self.assertEqual(node.children, children)

    def test_props(self):
        tag = "a"
        value = "This is a value"
        children = [HTMLNode("p"), HTMLNode("h1")]
        props = {"href": "https://www.test.com"}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(node.props, props)

    def test_to_html(self):
        tag = "p"
        node = HTMLNode(tag, "this is some text")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        props = {"href": "https://www.test.com", "target": "_blank"}
        test_string = ' href="https://www.test.com" target="_blank"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), test_string)

