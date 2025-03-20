from lxml import etree
from .exceptions import XMLSchemaException,MissingInputFileException,MissingOutputFileException
import os
from typing import List,Dict
from NekUpload.utils import parsing

class ValidateSession:
    """Class responsible for validation session files
    """
    def __init__(self,file_path: str):
        """Class initialiser

        Args:
            file_path (str): File path to the session XML file
        """
        self.file_path = file_path
        self.xml_tree = self._load_DOM_tree(self.file_path)

    def _load_DOM_tree(self, xml_file: str) -> etree._Element:
        """Loads the DOM tree of the XML file

        Args:
            xml_file (str): Path to XML file

        Returns:
            etree._Element: Internal representation of DOM tree
        """
        with open(xml_file, "rb") as xml:
            xml_tree = etree.XML(xml.read())
        
        return xml_tree

    def is_valid_xml(self,xml_file: str,schema_file_path: str) -> bool:
        """Checks whether XML file conforms to a schema

        Args:
            xml_file (str): XML file path
            schema_file_path (str): XSD schema file path

        Raises:
            XMLSchemaException: _description_

        Returns:
            bool: Passed
        """
        xsd_file = schema_file_path
        
        with open(xsd_file,"rb") as xsd:
            schema_root = etree.XML(xsd.read())
            schema = etree.XMLSchema(schema_root)

        with open(xml_file,"rb") as xml:
            xml_tree = etree.XML(xml.read())
        
        if schema.validate(xml_tree):
            return True
        else:
            raise XMLSchemaException(self.file_path,schema.error_log)
    
    def check_schema(self) -> bool:
        """Check file conforms to XML session schema

        Returns:
            bool: Passed
        """
        xsd_schema = os.path.join(os.path.dirname(__file__), 'schemas/nektar.xsd') #ensure path always correct
        return self.is_valid_xml(self.file_path, xsd_schema)
        
    def check_file_dependencies(self, files: List[str]) -> bool:
        """Check all files associated with this session file are present

        Args:
            files (List[str]): Other files

        Raises:
            MissingInputFileException: _description_
            MissingOutputFileException: _description_

        Returns:
            bool: Passed
        """
        #check geometry files exist
        geometry: etree._Element = self.xml_tree.find("GEOMETRY")
        expected_geometry_file = geometry.attrib.get("HDF5FILE")

        if expected_geometry_file not in files:
            raise MissingInputFileException(expected_geometry_file,"Geometry file is missing")
        
        #check correct number of checkpoint files
        conditions: etree._Element = self.xml_tree.find("CONDITIONS")
        params: etree._Element = conditions.find("PARAMETERS")

        #params has a bunch of p child elements, each with different 
        p_dict: Dict[str,str] = {}
        for p in params:
            content = p.text #containss an equals
            param_name,value = parsing.get_both_sides_of_equals(content)
            p_dict[param_name] = value

        #there is a possibility that it references other params, so store all in dict
        p_dict = parsing.evaluate_parameters(p_dict)

        num_steps = p_dict["NumSteps"]
        chk_steps = p_dict["IO_CheckSteps"]

        #at step=0, checkpoint file 0 is generated, hence +1
        num_chk_files = num_steps // chk_steps + 1

        chk_files = parsing.get_all_files_with_extension(files,".chk")

        if num_chk_files != len(chk_files):
            raise MissingOutputFileException(chk_files,
                                            f"There are {len(chk_files)}. Should have {num_chk_files}")

        return True