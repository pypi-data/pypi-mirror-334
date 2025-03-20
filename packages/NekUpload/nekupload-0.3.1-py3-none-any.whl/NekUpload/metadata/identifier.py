from enum import Enum
import re
import logging
from typing import Dict,Any,Type

class IdentifierType(Enum):
    """Enum denoting persistent identifier types
    """
    ORCID = "orcid"
    GND = "gnd"
    ISNI = "isni"
    ROR = "ror"

class Identifier:
    """Metadata object describing a persistent identifier associated with a person or organisation
    """
    def __init__(self, id: str, id_type: IdentifierType):
        """Class initialiser

        Args:
            id (str): ID
            id_type (IdentifierType): Persitent identifier type

        Raises:
            ValueError: _description_
        """
        self.id_type: IdentifierType = id_type

        if not self._check_valid_id(id,id_type):
            msg =f"ID {id} is not of type {id_type}"
            logging.error(msg)
            raise ValueError(msg)

        self.id = id
    
    def to_json_serialisable(self) -> Dict[str,Any]:
        """Method to serialise object as JSON

        Returns:
            Dict[str,Any]: JSON serialised object
        """
        return {
            "id": self.id,
            "id_type": self.id_type.value
        }

    @classmethod
    def from_json(cls: Type['Identifier'],data: Dict[str,Any]) -> 'Identifier':
        """Deserialise json object to reconstruct object

        Args:
            cls (Type[Identifier]): Class
            data (Dict[str,Any]): JSON serialised object

        Raises:
            ValueError: _description_

        Returns:
            Identifier: Reconstructed object
        """
        id = data["id"]
        id_type_value = data["id_type"]

        try:
            id_type = IdentifierType(id_type_value)
        except ValueError:
            msg = f"Invalid identifier type: {id_type_value}"
            logging.error(msg)
            raise ValueError(msg)

        return cls(id, id_type)  # Create and return the Identifier object
        

    def get_id_type(self) -> IdentifierType:
        """Get the id type

        Returns:
            IdentifierType: Identifier type
        """
        return self.id_type
    
    def get_id(self) -> str:
        """Get the ID

        Returns:
            str: ID
        """
        return self.id
    
    def _check_valid_id(self,id:str,id_type:IdentifierType) -> bool:
        """Check whether stated ID is valid given the ID type

        Args:
            id (str): ID
            id_type (IdentifierType): Identifier type

        Returns:
            bool: Whether id is valid
        """
        validation_methods = {
            IdentifierType.ORCID: self._is_valid_orcid_id,
            IdentifierType.GND: self._is_valid_gnd_id,
            IdentifierType.ISNI: self._is_valid_isni_id,
            IdentifierType.ROR: self._is_valid_ror_id,
        }
        
        validate = validation_methods.get(id_type)
        if validate:
            return validate(id)
        return False

    def _is_valid_orcid_id(self,id: str) -> bool:
        """Checks whether is a valid ORCID identifier

        Args:
            id (str): ID

        Returns:
            bool: Valid
        """
        #orcid id of form xxxx-xxxx-xxxx-xxxx, all numbers, last num (checksum) optionally capital 'X' for 10
        pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'
        if not re.match(pattern, id):
            return False

        base_digits = id.replace("-", "")[:-1]
        calculated_checksum = self._generate_check_digit_orcid(base_digits)
        return calculated_checksum == id[-1]    
    
    def _is_valid_gnd_id(self,id:str) -> bool:
        """Checks whether is a valid GND id

        Args:
            id (str): ID

        Returns:
            bool: Valid
        """
        #TODO
        return True
    
    def _is_valid_isni_id(self,id:str) -> bool:
        """Checks whether is a valid ISNI di

        Args:
            id (str): ID

        Returns:
            bool: Valid
        """

        #isni of form xxxxxxxxxxxxxxxx, all numbers (16 of them), last num (checksum) optionally capital 'X' for 10
        pattern = r'^\d{15}[\dX]$'
        if not re.match(pattern, id[:-1]):
            return False

        #TODO FIx the checksum
        #calculated_checksum = self._generate_check_digit_isni(id[:-1])
        #return calculated_checksum == id[-1]    
        return True

    def _is_valid_ror_id(self,id:str) -> bool:
        """Checks whether is a valid ROR id

        Args:
            id (str): ID

        Returns:
            bool: Valid
        """
        #TODO
        return True

    def _generate_check_digit_orcid(self,base_digits: str) -> str:
        """Generates checksum digit. Checksum code adapted from
        https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier

        Args:
            base_digits (str): Base digits.

        Returns:
            str: Checksum digit
        """
        total = 0
        for digit in base_digits:
            total = (total + int(digit)) * 2

        remainder = total % 11
        result = (12 - remainder) % 11
        return "X" if result == 10 else str(result)
    
    def _generate_check_digit_isni(self,base_digits: str) -> str:
        """
        Generate the ISNI (ISO 7064 Mod 11,10) checksum digit.

        This method calculates the check digit for an ISNI (International Standard Name Identifier)
        using the ISO 7064 Mod 11,10 algorithm. The check digit is used to ensure the integrity
        of the identifier.

        Args:
            base_digits (str): The base digits of the ISNI (excluding the check digit).

        Returns:
            str: The calculated check digit, which can be a digit from '0' to '9' or 'X' if the
                check digit is 10.
        """
        weights = [2, 3, 4, 5, 6, 7, 8, 9]  # Weight factors (right to left)
        total = 0
        reversed_digits = base_digits[::-1]  # Process from right to left

        for i, digit in enumerate(reversed_digits):
            weight = weights[i % len(weights)]  # Cycle through weights
            total += int(digit) * weight

        remainder = total % 11
        check_digit = 11 - remainder

        return "X" if check_digit == 10 else str(check_digit)

    def __eq__(self, other: 'Identifier') -> bool:
        if not isinstance(other,Identifier):
            return False
        
        return (
            self.id_type == other.id_type and
            self.id == other.id
        )