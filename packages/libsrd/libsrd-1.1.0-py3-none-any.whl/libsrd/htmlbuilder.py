class HtmlBuilder:
    defaultStyles = "".join([
        "* { font-family: Verdana, arial, Helvetica, sans-serif; }",
        "H1 { font-size: 17pt;}",
        "H2 { font-size: 13pt;}",
        "H3 { font-size: 11pt;}",
        "H4,H5,TH,TD { font-size: 10pt;}",
        "table { border-collapse: collapse; }",
        ".nopad { padding:0; margin:0;}",
        ".centre {margin-left:auto;margin-right:auto;}"
    ])

    def __init__(self):
        self.htmlDocument = []

    def initaliseHtml(self, Title, headStyles=defaultStyles, styleFilePath="style.css", assetFilePath="Assets/"):
        start = [ 
            "<!DOCTYPE html>",
            "<html>","<head>",
            "<meta charset=\"UTF-8\">",
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
            f"<style>{headStyles}</style>",
            "<script type=\"text/javascript\" async src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML\"></script>"
        ]

        self.htmlDocument.append("\n".join(start))
        self.htmlDocument.append(f"<title>{Title}</title>")

        if styleFilePath != "":
            self.htmlDocument.append("<link rel=\"stylesheet\" type=\"text/css\" href=\"" + styleFilePath + "\" title=\"DevEng Style\" />")
    
        if assetFilePath != "":
            self.htmlDocument.append(f"<base href=\"{assetFilePath}\">")

        self.htmlDocument.append("</head>")
        self.htmlDocument.append("<body>")
    
    def appendRawText(self, Text):
        self.htmlDocument.append(Text)
        self.htmlDocument.append("\n")

    def comment(self, Comment):
        self.htmlDocument.append(f"<!--{Comment}-->")

    @staticmethod
    def convKwargs(**kwargs):
        html = ""
        for key, value in kwargs.items():
            html += f" {key}=\"{value}\""
        return html

    def Heading(self, text, level, **kwargs):
        html = f"<h{level}{self.convKwargs(**kwargs)}>{text}</h{level}>"
        self.htmlDocument.append(html)

    def p(self, text, **kwargs):
        html = f"<p{self.convKwargs(**kwargs)}>{text}</p>"
        self.htmlDocument.append(html)
    
    def hr(self):
        self.htmlDocument.append("<hr>")

    def br(self):
        self.htmlDocument.append("<br>")

    def ul(self, items, **kwargs):
        html = f"<ul{self.convKwargs(**kwargs)}>"
        for item in items:
            html += f"\n<li>{item}</li>"
        html += "</ul>"
        self.htmlDocument.append(html)

    def ol(self, items, **kwargs):
        html = f"<ol{self.convKwargs(**kwargs)}>"
        for item in items:
            html += f"\n<li>{item}</li>"
        html += "</ol>"
        self.htmlDocument.append(html)

    def image(self, src, **kwargs):
        html = f"<img{self.convKwargs(**kwargs)} src=\"{src}\"/>"
        self.htmlDocument.append(html)

    def startDiv(self, **kwargs):
        self.htmlDocument.append(f"<div{self.convKwargs(**kwargs)}>")

    def endDiv(self):
        self.htmlDocument.append("</div>")

    def script(self, text="", **kwargs):
        self.htmlDocument.append(f"<script{self.convKwargs(**kwargs)}>{text}</script>")
    
    def blockquote(self, text, **kwargs):
        self.htmlDocument.append(f"<blockquote{self.convKwargs(**kwargs)}>{text}</blockquote>")

    @staticmethod
    def link(text, **kwargs):
        return (f"<a{HtmlBuilder.convKwargs(**kwargs)}>{text}</a>")

    @staticmethod
    def it(text, **kwargs):
        return (f"<it{HtmlBuilder.convKwargs(**kwargs)}>{text}</it>")

    @staticmethod
    def b(text, **kwargs):
        return (f"<b{HtmlBuilder.convKwargs(**kwargs)}>{text}</b>")

    @staticmethod
    def sub(text, **kwargs):
        return (f"<sub{HtmlBuilder.convKwargs(**kwargs)}>{text}</sub>")

    @staticmethod
    def sup(text, **kwargs):
        return (f"<sup{HtmlBuilder.convKwargs(**kwargs)}>{text}</sup>")

    @staticmethod
    def small(text, **kwargs):
        return (f"<small{HtmlBuilder.convKwargs(**kwargs)}>{text}</small>")
    
    def table(self, ColHeaders, ColAlignments, TableData, **kwargs):
        self.fixColAlignmets(ColAlignments, len(ColHeaders))

        html = f"<table{self.convKwargs(**kwargs)}><thead><tr>"
        for i in range(len(ColHeaders)):
            html += f"<th style=\"text-align:{ColAlignments[i]}\">{ColHeaders[i]}</th>"
        html += "</tr></thead><tbody>"

        for i in range(len(TableData)):
            html += "<tr>"
            for j in range(len(TableData[i])):
                html += f"<td style=\"text-align:{ColAlignments[j]}\">{TableData[i][j]}</td>"
            html += "</tr>"
        html += "</tr></body></table>"

        self.htmlDocument.append(html)

    @staticmethod
    def fixColAlignmets(ColAlignments, numberOfCols):
        for i in range(numberOfCols):
            if len(ColAlignments) > i:
                if ColAlignments[i] == "l":
                    ColAlignments[i] = "left"
                elif ColAlignments[i] == "r":
                    ColAlignments[i] = "right"
                elif ColAlignments[i] == "c":
                    ColAlignments[i] = "center"
            else:
                ColAlignments.append("inital")

    def __str__(self):
        return self.GetHtml()

    def GetHtml(self):
        copy = self.htmlDocument.copy()
        copy.append("</body></html>")
        return "\n".join(copy)

    def WriteHtml(self, path):
        with open(path, "w+") as f:
            f.write(self.GetHtml())


if __name__ == "__main__":
    doc = HtmlBuilder()
    doc.initaliseHtml("TestDocument")
    doc.Heading("Test Heading 1", 1)
    doc.Heading("Test Heading 2", 2)
    doc.p("This is a very cool paragraph.")
    doc.hr()
    doc.p(f"This is another very cool paragraph, with some {HtmlBuilder.b("BOLD")} text!")
    doc.ol(["Item 1", "Item 2"])
    doc.table(["Header1", "Header2"], ["l", "c"], [["Test1", "Test2"], ["Test1", "Test2"]])
    doc.WriteHtml("Output.html")