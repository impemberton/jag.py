import unittest

from htmlnode import ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent = ParentNode("div", [])
        self.assertRaises(ValueError, parent.to_html)

    def test_to_html_with_props(self):
        props = {"href": "https://www.test.com"}
        grandchild_node = LeafNode("a", "grandchild", props)
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="https://www.test.com">grandchild</a></span></div>',
        )

    def test_to_html_multiple_children(self):
        props = {"href": "https://www.test.com"}
        child_node1 = LeafNode("a", "child1", props)
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://www.test.com">child1</a><b>child2</b><span>child3</span></div>',
        )

    def test_to_html_multiple_parents_multiple_children(self):
        props = {"href": "https://www.test.com"}
        child_node1 = LeafNode("a", "child1", props)
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("span", "child3")
        child_node4 = LeafNode("i", "child4")
        parent_node1 = ParentNode("div", [child_node1, child_node2])
        parent_node2 = ParentNode("div", [child_node3, child_node4])
        grandparent_node = ParentNode("main", [parent_node1, parent_node2])
        self.assertEqual(
            grandparent_node.to_html(),
            '<main><div><a href="https://www.test.com">child1</a><b>child2</b></div><div><span>child3</span><i>child4</i></div></main>',
        )

