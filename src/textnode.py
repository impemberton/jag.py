from enum import Enum

from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text_same = self.text == other.text
        type_same = self.text_type == other.text_type
        url_same = self.url == other.url
        return text_same and type_same and url_same
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


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
            return LeafNode(tag="img", value=None, props=props)
        case _:
            raise Exception("Invalid TextType Enum")

