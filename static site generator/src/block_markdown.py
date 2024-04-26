from textnode import *
from htmlnode import *
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = block_to_block_type(block)
        html_node = get_html_node(type, block)
        children.append(html_node)

    return ParentNode("div", children)


def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    cleaned_blocks = []
    current_block = ""
    for line in lines:
        if line:
            current_block += f"{line}\n"
        else:
            if current_block:
                blocks.append(current_block)
                current_block = ""
    if current_block:
        blocks.append(current_block)
    for block in blocks:
        cleaned_block = block.strip()
        cleaned_blocks.append(cleaned_block)

    return cleaned_blocks


def block_to_block_type(block):
    if block.startswith("#"):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif block.startswith("> "):
        return block_type_quote
    elif block.startswith("* ") or block.startswith("- "):
        return block_type_ul
    elif block.startswith("1. "):
        return block_type_ol
    else:
        return block_type_paragraph


def get_html_node(type, block):
    if type == block_type_heading:
        return heading_html_node(block)
    elif type == block_type_code:
        return code_html_node(block)
    elif type == block_type_quote:
        return quote_html_node(block)
    elif type == block_type_ul:
        return ul_html_node(block)
    elif type == block_type_ol:
        return ol_html_node(block)
    else:
        return par_html_node(block)


def heading_html_node(block):
    levels = 0
    for char in block:
        if char == "#":
            levels += 1
    block = block.lstrip("# ")
    childrens = get_childrens(block)

    return ParentNode(f"h{levels}", childrens)


def code_html_node(block):
    childrens = get_childrens(block)
    return ParentNode("pre", childrens)


def quote_html_node(block):
    block = block.split("\n")
    cleaned_block = ""
    for line in block:
        line = line.lstrip("> ")
        cleaned_block += line + "\n"
    childrens = get_childrens(cleaned_block)

    return ParentNode("blockquote", childrens)


def ul_html_node(block):
    lines = block.split("\n")
    html = []
    for line in lines:
        text = line[2:]
        children = get_childrens(text)
        html.append(ParentNode("li", children))

    return ParentNode("ul", html)


def ol_html_node(block):
    lines = block.split("\n")
    html = []
    for line in lines:
        text = line[3:]
        children = get_childrens(text)
        html.append(ParentNode("li", children))

    return ParentNode("ol", html)


def par_html_node(block):
    childrens = get_childrens(block)
    return ParentNode("p", childrens)


def get_childrens(block):
    childrens = []
    nodes = text_to_textnodes(block)
    for node in nodes:
        if node.text:
            childrens.append(text_node_to_html_node(node))

    return childrens
