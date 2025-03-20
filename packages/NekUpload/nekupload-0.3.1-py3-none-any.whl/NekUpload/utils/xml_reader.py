import logging
from typing import Optional, Type, List
import lxml.etree as ET
from .exceptions import XMLReaderException

class XMLReader:
    def __init__(self, filename: str, mode: str = "r") -> None:
        self.filename = filename
        self.mode = mode
        self.tree: Optional[ET.ElementTree] = None
    
    def __enter__(self) -> "XMLReader":
        try:
            self.tree = ET.parse(self.filename)
            return self # Return XMLReader instance
        except Exception as e:
            logging.fatal(f"Error opening XML file: {e}")
            raise e
        
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Type[BaseException]]) -> None:
        self.tree = None

    def get_structure(self) -> List[str]:
        """_summary_

        :raises XMLReaderException: _description_
        :return: _description_
        :rtype: List[str]
        """
        
        if not self.tree:
            raise XMLReaderException("XML tree is not loaded.")
        
        root = self.tree.getroot()
        structure = []

        def traverse(node, path=""):
            current_path = f"{path}/{node.tag}" if path else node.tag
            structure.append(current_path)
            for child in node:
                traverse(child, current_path)
        
        traverse(root)
        return structure
    
    def merge_first_level_elements_with(self, other: str, write_file: Optional[str] = None) -> None:
        """Merges two XML files. If first-level repeated elements are found, will REPLACE them."""
        if not self.tree:
            raise XMLReaderException("XML tree not loaded.")
        
        try:
            other_tree = ET.parse(other)
        except Exception as e:
            raise XMLReaderException(f"Error Parsing the XML file '{other}': {e}")
        
        root = self.tree.getroot()
        other_root = other_tree.getroot()

        # Store first-level elements of the original XML in a dictionary
        existing_elements = {child.tag: child for child in root}

        for child in other_root:
            if child.tag in existing_elements:
                # Replace existing element
                root.replace(existing_elements[child.tag], child)
            else:
                # Append new elements that don't exist
                root.append(child)

        if write_file:
            # **Step 1: Flatten the XML (remove unnecessary spaces and newlines)**
            xml_str = ET.tostring(root, encoding="UTF-8").decode()
            parser = ET.XMLParser(remove_blank_text=True)  # Strips extra spaces
            root = ET.XML(xml_str, parser)  # Reload into an XML object

            # **Step 2: Reapply indentation with 4 spaces**
            formatted_xml = ET.tostring(root, pretty_print=True, encoding="UTF-8").decode()
            formatted_xml = formatted_xml.replace("  ", "    ")  # Convert 2-space indent to 4-space indent

            # Write to file
            with open(write_file, "w", encoding="UTF-8") as f:
                f.write(formatted_xml)