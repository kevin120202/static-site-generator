class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented yet.")

    def props_to_html(self):
        if self.props:
            html = ""
            for item in self.props:
                html += f' {item}="{self.props[item]}"'
            return html

        return ""

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Must require a value")
        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HtmlNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children, None)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Must require a tag")
        if self.children == None:
            raise ValueError("Must require children")
        html = ""
        for child in self.children:
            html += f"{child.to_html()}"

        return f"<{self.tag}>{html}</{self.tag}>"
