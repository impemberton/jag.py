import unittest

from textnode import TextNode, TextType
from md_functions import (
    extract_title,
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
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


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty_lines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        paragraph = "This is a test paragraph"
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        paragraph = "# This is a test heading1"
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading2(self):
        paragraph = "#### This is a test heading4"
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading3(self):
        paragraph = "####### This is a test heading with too many hashes"
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code1(self):
        code_block = "```This is a test code block```"
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code2(self):
        code_block = "``This is a test code block missing a backtick```"
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        quote = "> This is a test quote"
        block_type = block_to_block_type(quote)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_to_block_type_multiline_quote(self):
        quote = """> This is a test quote
> more quote
> even more quote"""
        block_type = block_to_block_type(quote)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_multiline_quote2(self):
        quote = """> This is a test quote
more quote but missing a >
> even more quote"""
        block_type = block_to_block_type(quote)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        ul = """- first item
- second item
- third item"""
        block_type = block_to_block_type(ul)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list2(self):
        ul = """- first item
second item missing -
- third item"""
        block_type = block_to_block_type(ul)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        ol = """1. first item
2. second item 
3. third item"""
        block_type = block_to_block_type(ol)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list2(self):
        ol = """1. first item
second item missing 2. 
3. third item"""
        block_type = block_to_block_type(ol)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list3(self):
        ol = """3. first item
5. this list is messed up 
1. third item"""
        block_type = block_to_block_type(ol)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello")

    def test_extract_title2(self):
        markdown = """# This is another test
## This is a subtitle
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is another test")
