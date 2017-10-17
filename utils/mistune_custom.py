import mistune
import re

from .html_colors import paint, attr

LINK_EXTRACT = re.compile(r"^(https?|s?ftp|wss?:?)://([^\s/]+)/?")

class InlineLexer(mistune.InlineLexer):
    def enable_underscore(self):
        self.rules.underscore = re.compile(
            r"_"
            r"(.*?)"
            r"_"
        )

        self.default_rules.insert(3, "underscore")

    def output_underscore(self, match):
        return self.renderer.underscore(match.group(1))

class Renderer(mistune.Renderer):
    def double_emphasis(self, text):
        return attr(text, "bold")

    def emphasis(self, text):
        return attr(text, "italic")

    def underscore(self, text):
        return attr(text, "underscore")

    def strikethrough(self, text):
        return attr(text, "strikethru")

    def paragraph(self, text):
        return text

    def inline_html(self, text):
        return text

    def escape(self, text):
        return text

    def block_html(self, html):
        return html

    def autolink(self, link, is_email=False):
        if is_email:
            return link

        return f"<a href={link} style=\"text-decoration: none\"><span style=\" color: #2196F3; text-decoration: none\">{link}</span></a>"

    def link(self, link, title, text):
        link_info = LINK_EXTRACT.match(link)

        if link_info is None:
            return link

        return f"<a href={link} style=\"text-decoration: none\"><span style=\"color: #2196F3; text-decoration: none\">{text}</span><span style=\"color: #BDBDBD; text-decoration: none\"> ({link_info.group(2)})</span></a>"

    def codespan(self, text):
        return paint(text, "a_green")

    def image(self, src, title, text):
        if title:
            return self.link(src, None, title)
        else:
            return self.autolink(src)

