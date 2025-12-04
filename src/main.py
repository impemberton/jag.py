from md_functions import generate_page_recursive
from textnode import TextNode, TextType
import os, shutil

def copydir(source, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    dest_contents = os.listdir(dest)
    for item in dest_contents:
        item_path = os.path.join(dest, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    source_contents = os.listdir(source)
    for item in source_contents:
        item_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_path)
        elif os.path.isdir(item_path):
            copydir(item_path, dest_path)


def main():
    copydir("static", "public")
    generate_page_recursive("content", "template.html", "public")

main()
