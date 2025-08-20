# Написати алгоритм, що буде парсити html документ та зберігати його Document Object Model (DOM) у дереві.

# Дерево повинно зберігати тег та текст, обрамлений цим тегом (якщо є такий).
# Додати можливість пошуку тексту за тегом.

# Вхідні дані: html документ та тег
# Вихідні дані: текст, якщо є.

class DOMNode:
    def __init__(self, tag, text=None):
        self.tag = tag
        self.text = text
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"DOMNode(tag='{self.tag}', text='{self.text}')"

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}<{self.tag}>"
        if self.text:
            result += f" {self.text}"
        for child in self.children:
            result += "\n" + child.__str__(level + 1)
        return result


class HTMLParser:
    def __init__(self, html):
        self.html = html
        self.root = DOMNode("root")
        self.current_node = self.root

    def parse(self):
        stack = []
        tag = ""
        text = ""
        in_tag = False
        in_text = False
        body_found = False
        body_started = False

        for char in self.html:
            if char == '<':
                if in_text and body_started:
                    if text.strip():
                        self.current_node.add_child(DOMNode("text", text.strip()))
                        text = ""
                in_tag = True
                tag = ""
            elif char == '>':
                if in_tag:
                    if 'body' in tag.lower() and not body_found:
                        body_found = True
                        body_started = True
                        self.root = DOMNode("body")
                        self.current_node = self.root
                    elif tag.lower() == '/body' and body_found:
                        break
                    elif body_started:
                        if tag.startswith('/'):
                            if stack:
                                self.current_node = stack.pop()
                        else:
                            new_node = DOMNode(tag)
                            self.current_node.add_child(new_node)
                            stack.append(self.current_node)
                            self.current_node = new_node
                    in_tag = False
                tag = ""
            elif in_tag:
                tag += char
            elif body_started:
                in_text = True
                text += char

        if in_text and text.strip() and body_started:
            self.current_node.add_child(DOMNode("text", text.strip()))

        return self.root

    def search_by_tag(self, tag):
        results = []

        def _collect_text(node):
            parts = []
            if node.text:
                parts.append(node.text)
            for child in node.children:
                parts.extend(_collect_text(child))
            return parts

        def _search(node):
            if node.tag == tag:
                results.extend(_collect_text(node))
            for child in node.children:
                _search(child)

        _search(self.root)
        return results



