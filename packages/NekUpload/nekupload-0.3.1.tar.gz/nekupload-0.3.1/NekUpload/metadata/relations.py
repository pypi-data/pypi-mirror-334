from types import MappingProxyType
from typing import Dict,Any
from .data_types import RelationsSchemes,RelationType,ResourceType,RELATIONS_SCHEMES_REVERSE_MAP,RELATIONS_TYPE_REVERSE_MAP,RESOURCE_TYPE_REVERSE_MAP

RELATION_TYPE_TITLE: MappingProxyType[RelationType,Dict[str,str]] = MappingProxyType({
    RelationType.CONTINUES: {"en": "Continues"}
})

RESOURCE_TYPE_TITLE: MappingProxyType[ResourceType,Dict[str,str]] = MappingProxyType({
    ResourceType.DATASET: {"en": "Dataset"},
    ResourceType.PHYSICAL_OBJECT: {"en": "Physical object"}
})

class Relations:
    """Metadata model for handling the Relations field in InvenioRDM. Describes any links between records with each other and/or external resources
    """
    def __init__(self,
                id: str,
                scheme: RelationsSchemes,
                relation: RelationType,
                resource: ResourceType):
        """Class initialiser

        Args:
            id (str): ID of the resource to be linked
            scheme (RelationsSchemes): ID scheme of the resource to be linked
            relation (RelationType): Describes the relationship of the link
            resource (ResourceType): Describes the resource type of the linked resource
        """
        self.id: str = id
        self.scheme: RelationsSchemes = scheme
        self.relation_type: RelationType = relation
        self.resource_type: ResourceType = resource

    def __eq__(self, other):
        if not isinstance(other, Relations):
            return NotImplemented
        return (self.id == other.id and
                self.scheme == other.scheme and
                self.relation_type == other.relation_type and
                self.resource_type == other.resource_type)

    def to_json(self):
        return {
            "identifier": self.id,
            "scheme": self.scheme.value,
            "relation_type": {
                "id": self.relation_type.value,
                "title": RELATION_TYPE_TITLE[self.relation_type]
            },
            "resource_type": {
                "id": self.resource_type.value,
                "title": RESOURCE_TYPE_TITLE[self.resource_type]
            }
        }
    
    @classmethod
    def from_json(cls,data: Dict[str,Any]) -> 'Relations':
        return Relations(data["identifier"],
                        RELATIONS_SCHEMES_REVERSE_MAP.get(data["scheme"]),
                        RELATIONS_TYPE_REVERSE_MAP.get(data["relation_type"]["id"]),
                        RESOURCE_TYPE_REVERSE_MAP.get(data["resource_type"]["id"]))