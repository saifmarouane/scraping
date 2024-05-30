import xml.etree.ElementTree as ET

def parse_3dxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Now, you can navigate through the XML structure and extract the information you need
    # For example:
    for child in root:
        print(child.tag, child.attrib)
        # You can continue navigating through the XML tree using child elements, attributes, etc.
        # Depending on the structure of your 3DXML file, you would need to adapt this parsing logic.
        
# Example usage:
parse_3dxml("C:\\Users\\mosaif\\Downloads\\148803300-33-din6378m8x40\\din6378m8x40.3dxml")
