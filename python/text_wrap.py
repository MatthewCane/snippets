import textwrap

"""
https://docs.python.org/3/library/textwrap.html
"""

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In in ex id leo auctor laoreet. Etiam eu sapien ac turpis posuere aliquet. Mauris consectetur dui at metus laoreet, sit amet lobortis orci feugiat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Quisque eleifend sit amet dui et rhoncus. Morbi rutrum sed urna id luctus. Nam commodo hendrerit finibus. Proin dictum lectus justo, id commodo lorem tristique id. Sed quis lacus vel quam faucibus egestas. Mauris sapien diam, dapibus et scelerisque nec, maximus sit amet purus. Nunc sed leo vitae eros vulputate ornare vel eu est. Integer nec enim risus. Nam tincidunt justo sed massa sodales fringilla. Suspendisse pharetra urna at justo fringilla, id dignissim turpis porta."

# Wrap the text to n chars
wrapped = textwrap.fill(text, width=80)
print(wrapped, "\n")

# Indent each line with the prefix
print(textwrap.indent(wrapped, prefix="> "), "\n")

# Truncate the text to n chars
print(textwrap.shorten(wrapped, width=80, placeholder="... [trucated]"))
