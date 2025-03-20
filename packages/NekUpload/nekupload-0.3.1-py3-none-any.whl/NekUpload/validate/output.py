import os
import h5py
from .hdf5_definitions import HDF5GroupDefinition,HDF5DatasetDefinition
from typing import Tuple,List,Optional
from .exceptions import OutputFileException,HDF5SchemaInconsistentException,HDF5SchemaExtraDefinitionException
from NekUpload.utils import parsing

class ValidateOutput:
    """Class responsible for all output file validation checks
    """
    def __init__(self, file_path: str):
        """Class initialiser

        Args:
            file_path (str): File path to output file
        """
        self.file = file_path
        self.file_name = os.path.basename(self.file)

    def check_schema(self) -> bool:
        """Check Output file conforms to HDF5 schema

        Raises:
            OutputSchemaHDF5Validator: _description_

        Returns:
            bool: Passed
        """
        try:
            with h5py.File(self.file, 'r') as f:
                self.schema_checker = OutputSchemaHDF5Validator(f)
                self.schema_checker.validate()
        except OSError as e:
            raise OutputFileException(self.file,f"Geometry file either does not exist or is not in HDF5 format {e}")

        return True
    
class OutputSchemaHDF5Validator:
    """Class for handling output HDF5 schema validation
    """

    NO_DIM_CONSTRAINTS = -1 #helper

    BASE_GROUPS = (HDF5GroupDefinition("NEKTAR",attributes=["FORMAT_VERSION"]),
                HDF5GroupDefinition("NEKTAR/Metadata",attributes=["ChkFileNum","Time"]), #this is bare minimum, depending on solver, can have more, also sessionFile#
                HDF5GroupDefinition("NEKTAR/Metadata/Provenance",attributes=["GitBranch","GitSHA1","Hostname","NektarVersion","Timestamp"]))

    EXPECTED_DATASETS = (HDF5DatasetDefinition("NEKTAR/DECOMPOSITION",(NO_DIM_CONSTRAINTS,)),)

    def __init__(self,f: h5py.File):
        """Class initialiser

        Args:
            f (h5py.File): Opened HDF5 file
        """
        self.file: h5py.File = f

    def validate(self):
        """Check whether specified file conforms to the HDF5 output schema
        """
        self._check_mandatory_groups(OutputSchemaHDF5Validator.BASE_GROUPS)
        self._check_mandatory_datasets(OutputSchemaHDF5Validator.EXPECTED_DATASETS)

        #acquire all other groups and datasets that should be present based on DECOMPOSITION definition
        self._assert_decomposition()
        expansion_groups: Tuple[HDF5GroupDefinition] = tuple(self._get_expansion_groups())
        optional_datasets: Tuple[HDF5DatasetDefinition] = tuple(self._get_optional_datasets())

        self._check_mandatory_groups(expansion_groups)
        self._check_mandatory_datasets(optional_datasets)
        
        #check no extraneous groups or datasets
        valid_groups: Tuple[HDF5GroupDefinition] = OutputSchemaHDF5Validator.BASE_GROUPS + expansion_groups
        valid_datasets: Tuple[HDF5DatasetDefinition] = OutputSchemaHDF5Validator.EXPECTED_DATASETS + optional_datasets

        valid_groups_str = [group.get_path() for group in valid_groups]
        valid_datasets_str = [dataset.get_path() for dataset in valid_datasets]
        self._check_only_valid_groups_exist(valid_groups_str)
        self._check_only_valid_datasets_exist(valid_datasets_str)

        #check some more DECOMPOSITION data


    def _check_mandatory_groups(self,groups: Tuple[HDF5GroupDefinition]):
        """Check whether mandatory HDF5 Groups are present in the file

        Args:
            groups (Tuple[HDF5GroupDefinition]): List of mandatory HDF5 Group definitions
        """
        for group in groups:
            group.validate(self.file)

    def _check_mandatory_datasets(self,datasets: Tuple[HDF5DatasetDefinition]):
        """CHeck whether mandatory HDF5 Datasets are present in the file

        Args:
            datasets (Tuple[HDF5DatasetDefinition]): List of mandatory HDF5 Dataset definitions
        """
        for dataset in datasets:
            dataset.validate(self.file)

    def _assert_decomposition(self):
        """Assert decomposition has correct shape

        Raises:
            HDF5SchemaInconsistentException: _description_
        """
        #decomposition should come in group of 7
        if self.file["NEKTAR/DECOMPOSITION"].shape[0] % 7 != 0:
            raise HDF5SchemaInconsistentException(self.file,"HDF5 Schema Error: Decomposition shape should be multiple of 7")

    def _get_expansion_groups(self) -> List[HDF5GroupDefinition]:
        """Get the expansion groups that should be defined, based on what is in DECOMPOSITION

        Raises:
            HDF5SchemaInconsistentException: _description_

        Returns:
            List[HDF5GroupDefinition]: _description_
        """
        decomposition_dataset: h5py.Dataset = self.file["NEKTAR/DECOMPOSITION"]
        #last of the 7 is a hash pointing to location in HDF5 file containing expansion data
        num_expansion_groups = decomposition_dataset.shape[0] // 7

        expected_groups: List[HDF5GroupDefinition] = []
        for i in range(6,7*num_expansion_groups,7):
            hash = decomposition_dataset[i]
            expected_groups.append(HDF5GroupDefinition(f"NEKTAR/{hash}",attributes=["BASIS","FIELDS","NUMMODESPERDIR","SHAPE"]))

        return expected_groups
    
    def _get_optional_datasets(self) -> List[HDF5DatasetDefinition]:
        """Get all optional datasets defined by DECOMPOSITION

        Returns:
            List[HDF5DatasetDefinition]: _description_
        """
        optional_datasets: List[HDF5DatasetDefinition] = []

        optionals = {"NEKTAR/ELEMENTIDS": 0,
                    "NEKTAR/DATA": 1,
                    "NEKTAR/POLYORDERS": 2,
                    "NEKTAR/HOMOGENEOUSYIDS": 3,
                    "NEKTAR/HOMOGENEOUSZIDS": 4,
                    "NEKTAR/HOMOGENEOUSSIDS": 5}

        for name,idx in optionals.items():
            if dataset := self._get_dataset_defined_in_decomposition(name,idx):
                optional_datasets.append(dataset)

        return optional_datasets
    
    def _get_dataset_defined_in_decomposition(self,
                                            dataset_name: str,
                                            decomposition_entry_id: int) -> Optional[HDF5DatasetDefinition]:
        """DECOMPOSITION contains sequence of 7 entries, some of which will lead to definition of
        extra datasets within the file. When the following are non-zero, a dataset is expected, and
        are constructed with the same rule:

        Note starting from 0:
        2 -> number of modes when variable polynomial is defined
        3 -> number of y planes for homogeneous simulations
        4 -> number of z planes for homogeneous simulations
        5 -> number of strips for homogeneous simulations

        Args:
            dataset_name (str): Name of the dataset to be defined
            decomposition_entry_id (int): Decomposition entry id for desired dataset 

        Returns:
            Optional[HDF5DatasetDefinition]: Dataset schema definition if one is required
        """
        decomposition_dataset: h5py.Dataset = self.file["NEKTAR/DECOMPOSITION"]
        size = decomposition_dataset.shape[0]
        num_data_points: int = 0

        for i in range(decomposition_entry_id,size,7):
            num_data_points += decomposition_dataset[i]

        return HDF5DatasetDefinition(dataset_name,(num_data_points,)) if num_data_points > 0 else None

    def _get_polyorder_dataset(self) -> Optional[HDF5DatasetDefinition]:
        """Get the polyorder dataset definition if it should exist, based on DECOMPOSITION entries, every third entry

        Returns:
            Optional[HDF5DatasetDefinition]: If polyorder dataset is defined, definition is returned, else None
        """
        decomposition_dataset: h5py.Dataset = self.file["NEKTAR/DECOMPOSITION"]
        size = decomposition_dataset.shape[0]
        #3rd of the 7 grouping in decomposition
        #is a number of modes that are polyorder???
        num_polyorder_modes: int = 0

        for i in range(2,size,7):
            num_polyorder_modes += decomposition_dataset[i]

        return HDF5DatasetDefinition("NEKTAR/POLYORDERS",(num_polyorder_modes,)) if num_polyorder_modes > 0 else None

    def _check_only_valid_groups_exist(self,valid_groups: List[str]):
        """Check that only valid groups exist.

        Args:
            valid_groups (str): List of paths for valid HDF5 Groups
        """
        #plus one to search for any extra invalid groups
        #"" is a valid group too, and is provided in function call
        valid_groups.append("")
        max_groups = len(valid_groups) + 1 
        groups = parsing.get_hdf5_groups_with_depth_limit(self.file,3,max_groups=max_groups)

        for group in groups:
            if group not in valid_groups:
                raise HDF5SchemaExtraDefinitionException(self.file,f"Encountered unkown group: {group}")

    def _check_only_valid_datasets_exist(self,valid_datasets: List[str]):
        """Check that only valid datasets exist.

        Args:
            valid_datasets (str): List of paths for valid HDF5 Datasets
        """
        max_datasets = len(valid_datasets) + 1
        datasets = parsing.get_hdf5_datasets_with_depth_limit(self.file,3,max_datasets=max_datasets)
        for dataset in datasets:
            if dataset not in valid_datasets:
                raise HDF5SchemaExtraDefinitionException(self.file,f"Encountered unkown dataset: {dataset}")
