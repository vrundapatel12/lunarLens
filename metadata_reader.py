import xml.etree.ElementTree as ET
def read_xml_metadata(path):
    root=ET.parse(path).getroot()
    result={}
    for node in root.iter():
        value=(node.text or "").strip()
        if value:
            key=node.tag.split("}")[-1]
            result[key]=value
    return result
