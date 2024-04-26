from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
import re


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "```", text_type_code)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            text_nodes_list.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        nodes = []
        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        for i in range(0, len(parts)):
            if i % 2 == 0:
                nodes.append(TextNode(parts[i], text_type_text))
            else:
                nodes.append(TextNode(parts[i], text_type))
        text_nodes_list.extend(nodes)

    return text_nodes_list


def split_nodes_image(old_nodes):
    text_nodes_list = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            text_nodes_list.append(old_node)
            continue
        if old_node.text == "":
            continue
        original_text = old_node.text
        for image_tup in images:
            remaining_text = original_text.split(
                f"![{image_tup[0]}]({image_tup[1]})")
            text_nodes_list.append(TextNode(remaining_text[0], text_type_text))
            text_nodes_list.append(
                TextNode(image_tup[0], text_type_image, image_tup[1]))
            original_text = remaining_text[-1]
        if original_text:
            text_nodes_list.append(TextNode(original_text, text_type_text))

    return text_nodes_list


def split_nodes_link(old_nodes):
    text_nodes_list = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            text_nodes_list.append(old_node)
            continue
        if old_node.text == "":
            continue
        original_text = old_node.text
        for link_tup in links:
            remaining_text = original_text.split(
                f"[{link_tup[0]}]({link_tup[1]})")
            text_nodes_list.append(TextNode(remaining_text[0], text_type_text))
            text_nodes_list.append(
                TextNode(link_tup[0], text_type_link, link_tup[1]))
            original_text = remaining_text[-1]
        if original_text:
            text_nodes_list.append(TextNode(original_text, text_type_text))

    return text_nodes_list


def extract_markdown_images(text):
    imgs = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return imgs


def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return links
