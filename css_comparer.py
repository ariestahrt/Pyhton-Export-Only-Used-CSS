from io import StringIO
import random
import string
from urllib.parse import urlparse
import lxml.html
import tinycss
import json, bs4
import requests

def convert_cssdict_to_cssfile(css_dict, save_to="css_fixed.css"):
    for selector in css_dict.keys():
        props_value = ""
        for props in css_dict[selector].keys():
            props_value += f"\t{props}: {css_dict[selector][props]};\n"
        
        out = selector + "{\n" + props_value + "}\n"
        with open(save_to, "a") as f: f.write(out)

def convert_csstext_to_cssdict(css_text, html_text, css_dict, validate_css=True):
    css_parser=tinycss.make_parser('page3');
    stylesheet=css_parser.parse_stylesheet(css_text);
    soup = bs4.BeautifulSoup(html_text, 'html.parser')

    for rule in stylesheet.rules:
        for selector in rule.selector.as_css().split(","):
            selector = selector.strip()
            try: els = soup.select(selector)
            except Exception as ex: None
            
            if len(els) == 0 and validate_css: continue # CSS tidak digunakan

            if selector not in css_dict.keys(): css_dict[selector] = {}
            # Save property
            for d in rule.declarations:
                if d.name not in css_dict[selector].keys(): css_dict[selector][d.name] = ""
                if "!important" not in css_dict[selector][d.name]:
                    css_dict[selector][d.name] = d.value.as_css()

def convert_cssdict_to_propval(css_dict):
    css_propval = {}
    for selector in css_dict.keys():
        for props in css_dict[selector].keys():
            if props not in css_propval.keys(): css_propval[props] = []
            value_txt = css_dict[selector][props]

            if "," in value_txt: # Usualy used in font family
                values = value_txt.split(",")
            else:
                values = value_txt.split(" ")
            
            for value in values:
                value = value.strip()
                if value not in css_propval[props]:
                    css_propval[props].append(value)

    return css_propval

# @ Return array
def get_css_from_html(html_text, html_root):
    css_dict = {}
    indom_css = ""
    inline_css = ""

    html = lxml.html.parse(StringIO(html_text))
    css_files = []
    for element in html.getroot().iter():
        if element.tag == "link" and "stylesheet" in element.attrib["rel"]:
            css_files.append(element.attrib["href"])
        if element.tag == "style":
            indom_css += element.text_content()
        if isinstance(element, lxml.html.HtmlElement):
            if "style" in element.attrib.keys():
                # just create random selector
                random_str = ''.join(random.sample(string.ascii_lowercase, 8))
                inline_css += "#custom_" + random_str + "{" + element.attrib["style"] + "}"

    # Convert css to iterable object
    # and make sure the css is not useless [Exist in the html dom]
    for files in css_files:
        css_text = ""
        if urlparse(files).scheme == "":
            print("Opening", files)
            with open(html_root + files, "r") as f: css_text += f.read()
        else:
            print("Downloading", files)
            # download from online source
            req = requests.get(files)
            css_text = req.text
        
        convert_csstext_to_cssdict(css_text, html_text, css_dict)

    # Then write indom <style></style> css
    convert_csstext_to_cssdict(indom_css, html_text, css_dict)

    # Then as the higher priority, convert inline css
    convert_csstext_to_cssdict(inline_css, html_text, css_dict, validate_css=False)

    # convert_cssdict_to_cssfile(css_dict, "paypal-3/customer_center/confirm-account589/lib/css/css_clean.css")
    return css_dict

def compare_two_dict(dict1, dict2):
    total_comp = 0
    total_match = 0

    for prop1 in dict1.keys():
        for value1 in dict1[prop1]:
            total_comp += 1
            if prop1 in dict2.keys():
                if value1 in dict2[prop1]:
                    values2 = dict2[prop1]
                    total_match+=1
    
    print("[!] total_comp", total_comp)
    print("[!] total_match", total_match)
    print("[!] ratio", float(total_match/total_comp))

if __name__ == "__main__":
    #2
    html_text = ""
    with open("result/index.html", "r", encoding="utf-8") as f: html_text += f.read()
    css_dict2 = get_css_from_html(html_text,html_root="result/")

    # Save object to json file
    with open("css2.json", "w") as outfile:
        json.dump(css_dict2, outfile, indent=4, sort_keys=True)