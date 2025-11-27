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

