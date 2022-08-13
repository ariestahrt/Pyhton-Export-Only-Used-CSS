import json
from select import select

# Convert to dictionary with order of: selector, props, value
css_dict = {}
css_json = json.load(open("css_fixed.json", "r"))

for props in css_json.keys():
    for value in css_json[props].keys():
        for selector in css_json[props][value]:
            if selector not in css_dict: css_dict[selector] = {}
            if props not in css_dict[selector].keys(): css_dict[selector][props] = []
            css_dict[selector][props].append(value)

json.dump(css_dict, open("css_dict.json", "w"), indent=4, sort_keys=True)

for selector in css_dict.keys():
    props_value = ""
    for props in css_dict[selector].keys():
        props_val = " ".join(css_dict[selector][props])
        props_value += f"\t{props}: {props_val};\n"
    
    out = selector + "{\n" + props_value + "}\n"
    # print(out)
    with open("css_fixed.css", "a") as f:
        f.write(out)