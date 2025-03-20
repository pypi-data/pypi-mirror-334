from .validate import ValidateSession,ValidateOutput,ValidateGeometry
from typing import List
import logging

class NektarValidator:
    def __init__(self,
                session_file: str,
                geometry_file: str,
                output_file: str,
                chk_files: List[str],
                supporting_files: List[str]):
        """_summary_

        Args:
            session_file (str): _description_
            geometry_file (str): _description_
            output_file (str): _description_
            chk_files (List[str]): _description_
            supporting_files (List[str]): _description_
        """

        self.session_file: str = session_file
        self.geometry_file: str = geometry_file
        self.output_fld_file: str = output_file
        self.output_chk_files: List[str] = chk_files
        self.supporrting_files: List[str] = supporting_files 

        self.session_validator = ValidateSession(self.session_file)
        self.geometry_validator = ValidateGeometry(self.geometry_file)
        self.output_validator = ValidateOutput(self.output_fld_file)

    def validate(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """

        self.session_validator.check_schema()
        self.geometry_validator.check_schema()
        self.output_validator.check_schema()

        return True
