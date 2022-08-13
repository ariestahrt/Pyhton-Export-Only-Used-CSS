# Python Export Only-Used CSS

Hi everyone, this tool can export only-used CSS based on a fully-downloaded HTML page from (https://github.com/ariestahrt/PythonCompleteWebpageSaver)

Example usage
```py
html_text = ""
with open("path/index.html", "r") as f: html_text += f.read()

# Convert CSS To Dictionary Object
css_dict = get_css_from_html(html_text, html_root="path/", verify=True)
```