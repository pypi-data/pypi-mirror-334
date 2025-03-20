import os
import sys
import re
from libsrd import HtmlBuilder


class Markdown:
    MultiLineTokens = ["checklist", "ul_item", "ol_item", "blockquote", "table", "paragraph"]

    def __init__(self, path, assetFolderPath="Assets/", stylePath="style.css"):
        self.assetFolder = assetFolderPath
        self.stylePath = stylePath
        self.path = path

        with open(path, "r") as f:
            self.mdlines = f.readlines()

    def GetHtml(self):
        tokens = self.Tokenise()
        preprocessedHtml = self.HtmlFromTokens(tokens)
        regexHtml = self.convert_inline_formatting(preprocessedHtml)
        return regexHtml
    
    def Tokenise(self):
        tokens = []

        for line in self.mdlines:
            line = line.removesuffix("\n")

            if line.startswith("- [ ] ") or line.startswith("* [ ] "):  # Unchecked checklist
                tokens.append(("checklist", False, line[6:].strip()))

            elif line.startswith("- [x] ") or line.startswith("* [x] "):  # Checked checklist
                tokens.append(("checklist", True, line[6:].strip()))

            elif line.startswith("- ") or line.startswith("* "):  # Unordered List
                tokens.append(("ul_item", line[2:]))

            elif len(line) > 0 and line[0].isdigit() and line[1] == ".":  # Ordered List
                tokens.append(("ol_item", line[2:]))

            elif line.startswith("> "):  # Blockquote
                tokens.append(("blockquote", line[2:]))

            elif line.startswith("|"): # Table row
                tokens.append(("table", line))

            elif line.startswith("#"):  # heading
                level = len(line.split(" ")[0])
                text = line[level:].strip()
                tokens.append(("heading", level, text))

            else:  # Everything else is a paragraph
                tokens.append(("paragraph", line))

            # Handle Linebreak
            if line.endswith("  "):
                tokens.append("linebreak")

        return tokens

    def HtmlFromTokens(self, tokens):
        html = HtmlBuilder()
        html.initaliseHtml(str(os.path.basename(self.path)).split(".")[0], "", self.stylePath, self.assetFolder)

        # Title bar
        html.startDiv(id="container")
        html.appendRawText(f"<div id=\"TitleBar\"><h1 class=\"nopad\">{str(os.path.basename(self.path)).split(".")[0]}</h1></div>")

        tokens = self.JoinMultilineTokens(tokens)

        for token in tokens:
            if token[0] == "heading":
                html.Heading(token[2], token[1])

            elif token[0] == "paragraph":
                p = ""
                pTokens = token[1]
                for pToken in pTokens:
                    p += str(pToken[1]).strip() + " "

                html.p(p)
            
            elif token[0] == "linebreak":
                html.br()

            elif token[0] == "ul_item":
                items = []
                ulTokens = token[1]
                for ulToken in ulTokens:
                    items.append(ulToken[1])

                html.ul(items)

            elif token[0] == "checklist": # Im just going to convert a checklist to a ul
                items = []
                ulTokens = token[1]
                for ulToken in ulTokens:
                    items.append(ulToken[2])

                html.ul(items)

            elif token[0] == "ol_item":
                items = []
                olTokens = token[1]
                for olToken in olTokens:
                    items.append(olToken[1])

                html.ol(items)

            elif token[0] == "blockquote":
                quote = ""
                bqTokens = token[1]
                for bqToken in bqTokens:
                    quote += bqToken[1]

                html.blockquote(quote)

            elif token[0] == "table":
                table = []

                tabTokens = token[1]
                for tabToken in tabTokens:
                    table.append(tabToken[1])

                headers = [h.strip() for h in table[0].split("|")[1:-1]]
                alignments = ["l"] * len(headers)  # Default left-align

                data = []
                for row in table[2:]:  # Skip header and separator row
                    data.append([cell.strip() for cell in row.split("|")[1:-1]])

                html.table(headers, alignments, data, Class="centre")
        
        html.endDiv()
        return html.GetHtml()
    
    @staticmethod
    def JoinMultilineTokens(tokens):
        newTokenList = []
        buffer = []

        for token in tokens:
            # Case 1: empty buffer, single line token
            if len(buffer) == 0 and token[0] not in Markdown.MultiLineTokens:
                newTokenList.append(token)

            # Case 2: not empty buffer, single line token
            elif len(buffer) > 0 and token[0] not in Markdown.MultiLineTokens:
                newTokenList.append((buffer[0][0], buffer.copy()))
                buffer.clear()
                
                newTokenList.append(token)

            # Case 3: not empty buffer, new multiline token
            elif len(buffer) > 0 and token[0] != buffer[0][0] and token[0] in Markdown.MultiLineTokens:
                newTokenList.append((buffer[0][0], buffer.copy()))
                buffer.clear()

                buffer.append(token)

            # Case 4: empty buffer or same token
            else: 
                buffer.append(token)

        if len(buffer) > 0: # Make sure the buffer does not get forgotten if the last element is a multiline.
            newTokenList.append((buffer[0][0], buffer.copy()))

        return newTokenList

    def convert_inline_formatting(self, text):
        if "```" in text:
            text = re.sub(r"```(.*?)```", r"<pre><code>\1</code></pre>", text, flags=re.DOTALL)

        # Handle Double-Dollar Maths FIRST ($$maths block$$ → \[maths block\])
        text = re.sub(r"\$\$(.*?)\$\$", r"\\[\1\\]", text, flags=re.DOTALL)

        # Handle Single-Dollar Maths ($maths$ → \(maths\))
        text = re.sub(r"(?<!\$)\$(.*?)(?<!\$)\$", r"\\(\1\\)", text)

        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)

        text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
        text = re.sub(r"!\[\[(.*?)\]\]", r'<br><img src="\1" alt="\1"/><br>', text)
        text = re.sub(r"(?<!\!)\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)


        return text

 
def _script():
    if len(sys.argv) == 2:
        md = Markdown(sys.argv[1])
        html = md.GetHtml()

        with open(os.path.splitext(sys.argv[1])[0]+'.html', "w+") as f:
            f.write(html)
    
    elif len(sys.argv) == 3:
        md = Markdown(sys.argv[1], sys.argv[2])
        html = md.GetHtml()

        with open(os.path.splitext(sys.argv[1])[0]+'.html', "w+") as f:
            f.write(html)

    elif len(sys.argv) == 4:
        md = Markdown(sys.argv[1], sys.argv[2], sys.argv[3])
        html = md.GetHtml()

        with open(os.path.splitext(sys.argv[1])[0]+'.html', "w+") as f:
            f.write(html)

    else:
        print("Expected argument InputFile with optional AssetFolder and StyleFilePath")