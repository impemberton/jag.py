from enum import Enum
import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_text = node.text
            open = False
            while delimiter in node_text:
                new_node_text, node_text = node_text.split(delimiter, 1)
                if open:
                    new_node_type = text_type
                else:
                    new_node_type = TextType.TEXT
                if len(new_node_text) > 0:
                    new_node = TextNode(new_node_text, new_node_type)
                    new_nodes.append(new_node)
                open = not open
            if len(node_text) > 0:
                new_nodes.append(TextNode(node_text, TextType.TEXT))
            if open:
                raise Exception("matching closing delimiter not found")
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_text = node.text
            matches = extract_markdown_images(node_text)
            if len(matches) > 0:
                for alt, url in matches:
                    text, node_text = node_text.split("!", 1)
                    if len(text) > 0:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    _, node_text = node_text.split(")", 1)
                if len(node_text) > 0:
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_text = node.text
            matches = extract_markdown_links(node_text)
            if len(matches) > 0:
                for link_text, url in matches:
                    text, node_text = node_text.split("[", 1)
                    if len(text) > 0:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                    _, node_text = node_text.split(")", 1)
                if len(node_text) > 0:
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**", TextType.BOLD) 
    nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes,"`", TextType.CODE) 
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"

def block_to_block_type(block):
    for i in range(1,7):
        if block.startswith(("#" * i) + " "):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    is_quote = True
    is_unordered = True
    is_ordered = True
    list_num = 1
    for line in block.split("\n"):
        if not line.startswith(">"):
            is_quote = False
        if not line.startswith("- "):
            is_unordered = False
        if not line.startswith(str(list_num) + ". "):
            is_ordered = False
        list_num += 1

    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED_LIST
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH




