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
                new_node = TextNode(new_node_text, new_node_type)
                new_nodes.append(new_node)
                open = not open
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            if open:
                raise Exception("matching closing delimiter not found")
        else:
            new_nodes.append(node)
    return new_nodes
