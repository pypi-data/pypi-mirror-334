from typing import Dict,Any,List
from .user import InvenioUserInfo
from .relations import Relations
from .data_types import ResourceType,RESOURCE_TYPE_REVERSE_MAP

class InvenioMetadata:
    """Metadata model for handling metadata as prescribed in InvenioRDM. Uses a builder OOP style to 
    allow clients to enhance the metadata description.
    """
    def __init__(self,title: str,
                publication_date:str,
                creators: List[InvenioUserInfo],
                resource_type: ResourceType=ResourceType.DATASET):
        """Class Initialiser

        Args:
            title (str): Title of file uploads
            publication_date (str): Date of publication, in format YYYY-MM-DD
            creators (List[InvenioUserInfo]): List of authors
            resource_type (ResourceType, optional): Type of resource to be uploaded. Defaults to ResourceType.DATASET.
        """
        #mandatory fields
        self.title = title
        self.publication_date = publication_date
        self.creators: List[InvenioUserInfo] = creators
        self.resource_type = resource_type.value

        #optional fields
        self.version: str = None
        self.description: str = None
        self.publisher: str = None
        self.related_identifiers: List[Relations] = []

    def get_metadata_payload(self) -> Dict[str,Any]:
        """Get the metadata payload formatted in way InvenioRDM expects

        Returns:
            Dict[str,Any]: Metadata json payload
        """
        creators_payload: List[Dict[str,Any]] = []
        for creator in self.creators:
            creators_payload.append({
                "person_or_org": creator.get_info()
            })
        
        data = {
            "title": self.title,
            "publication_date": self.publication_date,
            "resource_type": {"id": self.resource_type},
            "creators": creators_payload
        }

        #only add to payload if they exist
        if self.version:
            data["version"] = self.version
        
        if self.description:
            data["description"] = self.description

        if self.publisher:
            data["publisher"] = self.publisher

        if self.related_identifiers:
            relation_list_json = [relation.to_json() for relation in self.related_identifiers]
            data["related_identifiers"] = relation_list_json

        return data

    def add_version(self, version: str) -> None:
        """Add the version number (of the software or dataset). Semantic versioning is recommended.

        Args:
            version (str): Version number
        """
        self.version = version

    def add_description(self, description: str) -> None:
        """Add a description of the record to be uploaded

        Args:
            description (str): Description
        """
        self.description = description

    def add_publisher(self, publisher: str="InvenioRDM") -> None:
        """Add publisher 

        Args:
            publisher (str, optional): Add publisher name. Defaults to "InvenioRDM".
        """
        self.publisher = publisher

    def add_related_identifier(self,relation: Relations):
        """Add related persistent identifiers

        Args:
            relation (Relations): A related identifier
        """
        self.related_identifiers.append(relation)

    def to_json_serialisable(self) -> Dict[str,Any]:        
        """Serialise the object as JSON

        Returns:
            Dict[str,Any]: Serialised json object
        """
        data = {
            "title": self.title,
            "publication_date": self.publication_date,
            "resource_type": self.resource_type,
            "creators": [creator.to_json_serialisable() for creator in self.creators]
        }

        if self.version:
            data["version"] = self.version
        
        if self.description:
            data["description"] = self.description

        if self.publisher:
            data["publisher"] = self.publisher

        if self.related_identifiers:
            relation_list_json = [relation.to_json() for relation in self.related_identifiers]
            data["related_identifiers"] = relation_list_json

        return data    
    
    @classmethod
    def from_json(cls,data: Dict[str,Any]) -> 'InvenioMetadata':
        """Reconstruct object from JSON serialisation

        Args:
            data (Dict[str,Any]): Serialised JSON data

        Returns:
            InvenioMetadata: Reconstructed object
        """
        title = data["title"]
        publication_date = data["publication_date"]
        resource_type: ResourceType = RESOURCE_TYPE_REVERSE_MAP[data["resource_type"]]
        creators: List[InvenioUserInfo] = [InvenioUserInfo.from_json(creator) for creator in data["creators"]]

        metadata = InvenioMetadata(title,publication_date,creators,resource_type)

        #only add the following optional data if present in serialisation
        if version := data.get("version",None):
            metadata.add_version(version)

        if description := data.get("description",None):
            metadata.add_description(description)

        if publisher := data.get("publisher",None):
            metadata.add_publisher(publisher)

        if related_identifiers := data.get("related_identifiers",None):
            for identifier_json in related_identifiers:
                import logging
                logging.error(identifier_json)
                metadata.add_related_identifier(Relations.from_json(identifier_json))

        return metadata