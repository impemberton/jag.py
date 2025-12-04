from enum import Enum
import re
from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
import os

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

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            props = {"href": text_node.url}
            return LeafNode(tag="a", value=text_node.text, props=props)
        case TextType.IMAGE:
            props = {
                "src": text_node.url,
                "alt": text_node.text
            }
            return LeafNode(tag="img", value="", props=props)
        case _:
            raise Exception("Invalid TextType Enum")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                child_nodes = text_to_children(block.replace("\n", " "))
                block_nodes.append(ParentNode("p", child_nodes))
            case BlockType.HEADING:
                hashes, block = block.split(" ", 1)
                child_nodes = text_to_children(block)
                block_nodes.append(ParentNode("h" + str(len(hashes)), child_nodes))
            case BlockType.QUOTE:
                block = "\n".join([line[2:] for line in block.split("\n")])
                child_nodes = text_to_children(block)
                block_nodes.append(ParentNode("blockquote", child_nodes))
            case BlockType.UNORDERED_LIST:
                list_items = []
                for li in block.split("\n"):
                    child_nodes = text_to_children(li[2:])
                    list_items.append(ParentNode("li", child_nodes))
                block_nodes.append(ParentNode("ul", list_items))
            case BlockType.ORDERED_LIST:
                list_items = []
                for li in block.split("\n"):
                    child_nodes = text_to_children(li[3:])
                    list_items.append(ParentNode("li", child_nodes))
                block_nodes.append(ParentNode("ol", list_items))
            case BlockType.CODE:
                text_node = TextNode(block[4:-3], TextType.CODE)
                child_node = text_node_to_html_node(text_node)
                block_nodes.append(ParentNode("pre", [child_node]))
    return ParentNode("div", block_nodes)
                

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def extract_title(markdown):
    if markdown.startswith("# "):
        return markdown.split("\n", 1)[0][2:]
    raise Exception("No title found")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    html = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html.to_html())
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            if item_path.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, item.replace(".md",".html"))
                generate_page(item_path, template_path, dest_path)
        if os.path.isdir(item_path):
            dest_path = os.path.join(dest_dir_path, item)
            generate_page_recursive(item_path, template_path, dest_path)

                
        
