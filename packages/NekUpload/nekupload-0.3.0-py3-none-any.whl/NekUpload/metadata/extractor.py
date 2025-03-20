import h5py
import numpy as np
from typing import Tuple,List,Dict

class HDF5Extractor:
    """Class for extracting features from a HDF5 file
    """
    def __init__(self):
        pass

    @staticmethod
    def extract_attribute(file: h5py.File,group_path: str, attribute: str) -> str:
        """Extract an attribute from a HDF5 file

        Args:
            file (h5py.File): An opened HDF5 file
            group_path (str): Path to the HDF5 Group containing the attribute
            attribute (str): Attribute to look for

        Raises:
            ValueError: _description_

        Returns:
            str: Value of the attribute stored in the file
        """
        try:
            group = file[group_path]

            if not isinstance(group,h5py.Group):
                raise ValueError

            return group.attrs[attribute].strip()

        except Exception:
            return None

    def extract_min_max_coords(file: h5py.File,dataset_path: str) -> Tuple[np.ndarray,np.ndarray]:
        """Read a set of 3d coordinates from the HDF5 file and keep only the minimum and maximum coordinates

        Args:
            file (h5py.File): HDF5 file containing coordinates
            dataset_path (str): Datasets containing the 3D coordinates

        Raises:
            ValueError: _description_

        Returns:
            Tuple[np.ndarray,np.ndarray]: Minimum coordinate and Maximum coordinate
        """
        dataset: h5py.Dataset = file[dataset_path]
        shape = dataset.shape

        # Ensure dataset is at least 2D and has 3 columns
        if len(shape) < 2 or shape[1] != 3:
            raise ValueError(f"Expected a dataset with shape (N,3), but got {shape}")

        #initialise
        CHUNK_SIZE = 1000 #TODO where to put chunk_size???
        min_coord = np.full(3, np.inf)
        max_coord = np.full(3, -np.inf)
        
        for chunk_start in range(0,shape[0],CHUNK_SIZE):
            chunk_end = min(chunk_start + CHUNK_SIZE, shape[0])
            data_chunk = dataset[chunk_start:chunk_end, :]

            min_coord_in_chunk: np.ndarray = np.amin(data_chunk,axis=0)
            max_coord_in_chunk: np.ndarray = np.amax(data_chunk,axis=0)

            #in-place as memory allocations are expensive in Python
            np.minimum(min_coord,min_coord_in_chunk,out=min_coord)
            np.maximum(max_coord,max_coord_in_chunk,out=max_coord)

        return min_coord, max_coord

#TODO Should NekAutoExtractor really be in this package???
class NekAutoExtractor:
    """Nektar auto extractor of fields in Nektar dataset files
    """
    def __init__(self,session_file: str,geometry_file: str,output_file: List[str]):
        """Class initialiser

        Args:
            session_file (str): Session file path
            geometry_file (str): Geometry file path
            output_file (List[str]): List of output file paths
        """
        self.session_file = session_file
        self.geometry_file = geometry_file
        self.output_file = output_file

    def extract_data(self) -> Dict[str,str]:
        """Extract data from the files

        Returns:
            Dict[str,str]: Data extracted from the Nektar++ datasets
        """
        results = {}

        with h5py.File(self.output_file) as f:
            if version := HDF5Extractor.extract_attribute(f,"NEKTAR/Metadata/Provenance","NektarVersion"):
                results["VERSION"] = version 
            
            if git_hash := HDF5Extractor.extract_attribute(f,"NEKTAR/Metadata/Provenance","GitSHA1"):
                results["GITHASH"] = git_hash
        
        with h5py.File(self.geometry_file) as f:
            min_coords1,max_coords1 = HDF5Extractor.extract_min_max_coords(f,"NEKTAR/GEOMETRY/MESH/VERT")
            min_coords2,max_coords2 = HDF5Extractor.extract_min_max_coords(f,"NEKTAR/GEOMETRY/MESH/CURVE_NODES")#mot needed

            min_coords = np.minimum(min_coords1,min_coords2)
            max_coords = np.maximum(max_coords1,max_coords2)

            results["MAX_COORD"] = max_coords
            results["MIN_COORD"] = min_coords

        return results

if __name__ == "__main__":
    with h5py.File("tests/datasets/ADRSolver/ADR_2D_TriQuad.fld") as f:
        v = HDF5Extractor.extract_attribute(f,"NEKTAR/Metadata/Provenance","NektarVersion")
        print(v)

    with h5py.File("tests/datasets/ADRSolver/ADR_2D_TriQuad.nekg") as f:
        coords = HDF5Extractor.extract_min_max_coords(f,"NEKTAR/GEOMETRY/MESH/VERT")
        print(coords)