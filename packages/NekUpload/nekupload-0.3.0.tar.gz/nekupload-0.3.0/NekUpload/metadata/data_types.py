from enum import Enum
from types import MappingProxyType

#Enums describing various InvenioRDM data types

class RelationsSchemes(Enum):
    DOI = "doi"
    URL = "url"

RELATIONS_SCHEMES_REVERSE_MAP: MappingProxyType[str,RelationsSchemes] = MappingProxyType({
    member.value: member for member in RelationsSchemes
})

class RelationType(Enum):
    CONTINUES = "continues"

RELATIONS_TYPE_REVERSE_MAP: MappingProxyType[str,RelationType] = MappingProxyType({
    "continues": RelationType.CONTINUES
})

class ResourceType(Enum):
    DATASET = "dataset"
    PHYSICAL_OBJECT = "physicalobject"

RESOURCE_TYPE_REVERSE_MAP: MappingProxyType[str,ResourceType] = MappingProxyType({
    "dataset": ResourceType.DATASET,
    "physical_object": ResourceType.PHYSICAL_OBJECT
})