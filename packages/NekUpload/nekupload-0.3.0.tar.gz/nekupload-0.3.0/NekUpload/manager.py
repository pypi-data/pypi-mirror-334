from NekUpload.metadata.metadata import InvenioMetadata 
from NekUpload.upload.invenio_db import InvenioRDM
from NekUpload.metadata.extractor import NekAutoExtractor
from .validate import ValidateSession,ValidateOutput,ValidateGeometry
from typing import List,Optional,Dict
from abc import ABC,abstractmethod
from NekUpload.metadata.relations import Relations,RelationsSchemes,RelationType,ResourceType
from NekUpload.utils.hdf5_reader import HDF5Reader
import os

class NekManager:
    def __init__(self,
                geometry_uploader: 'GeometryManager',
                input_uploader: 'SessionManager',
                output_uploader: 'OutputManager'):

        self.geometry_uploader: GeometryManager = geometry_uploader
        self.input_uploader: SessionManager = input_uploader
        self.output_uploader: OutputManager = output_uploader

        self.auto_metadata_extractor = NekAutoExtractor(
                                    self.input_uploader.session_file,
                                    self.geometry_uploader.geometry_file,
                                    self.output_uploader.output_fld_file)

        self.session_validator = ValidateSession(self.input_uploader.session_file)
        self.geometry_validator = ValidateGeometry(self.geometry_uploader.geometry_file)
        self.output_validator = ValidateOutput(self.output_uploader.output_fld_file)

    def execute_upload(self,url:str,token:str,community_id:str):
        #pass by reference, so all uploaders get updated version of metadata
        self._update_metadata_with_auto_extraction()

        self.geometry_uploader.execute_upload(url,token,community_id)

        #update input and output with geometry upload link
        geometry_doi = self.geometry_uploader.upload_manager.doi
        geometry_record_html = self.geometry_uploader.upload_manager.record_link
        geometry_self_html = self.geometry_uploader.upload_manager.self_link
        geometry_relation = Relations(geometry_doi,RelationsSchemes.DOI,RelationType.CONTINUES,ResourceType.DATASET)
        geometry_relation_html = Relations(geometry_record_html,RelationsSchemes.URL,RelationType.CONTINUES,ResourceType.DATASET)
        geometry_relation_draft_link = Relations(geometry_self_html,RelationsSchemes.URL,RelationType.CONTINUES,ResourceType.DATASET)


        self.input_uploader.metadata_manager.add_related_identifier(geometry_relation)
        self.input_uploader.metadata_manager.add_related_identifier(geometry_relation_html)
        self.input_uploader.metadata_manager.add_related_identifier(geometry_relation_draft_link)
        self.output_uploader.metadata_manager.add_related_identifier(geometry_relation)
        self.output_uploader.metadata_manager.add_related_identifier(geometry_relation_html)
        self.output_uploader.metadata_manager.add_related_identifier(geometry_relation_draft_link)

        self.input_uploader.execute_upload(url,token,community_id)
        self.output_uploader.execute_upload(url,token,community_id)

    def _update_metadata_with_auto_extraction(self):
        results = self.auto_metadata_extractor.extract_data()
        
        if version := results.get("VERSION",None):
            self.geometry_uploader.metadata_manager.add_version(version)
            self.input_uploader.metadata_manager.add_version(version)
            self.output_uploader.metadata_manager.add_version(version)

        #TODO implement everything else

    def validate(self):
        self.session_validator.check_schema()
        self.geometry_validator.check_schema()
        self.output_validator.check_schema()

class UploadManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def execute_upload(self,url: str,token: str,community_slug: str):
        pass

class GeometryManager(UploadManager):
    def __init__(self,geometry_file: str,
                supporting_files: List[str]=None,
                metadata: InvenioMetadata=None,
                uploader: InvenioRDM=None):
        
        self.geometry_file: str = geometry_file
        self.supporting_files: List[str] = supporting_files if supporting_files else []
        self.metadata_manager = metadata if metadata else InvenioMetadata()
        self.upload_manager = uploader if uploader else InvenioRDM()

    def execute_upload(self,url: str,token: str,community_slug: str):
        files = [self.geometry_file] + self.supporting_files
        metadata_json = self.metadata_manager.get_metadata_payload()
        metadata = {"metadata": metadata_json}

        extra_metadata_file = self.generate_metadata_file()
        files.append(extra_metadata_file)

        try:
            self.upload_manager.upload_files(url,token,files,metadata,community_slug)
        except:
            raise
        finally:
            files.remove(extra_metadata_file)
            os.remove(extra_metadata_file)

    def generate_metadata_file(self) -> str:
        with HDF5Reader(self.geometry_file) as f:
            f.dump_to_plain_file("metadata.rdm")

        return "metadata.rdm"
    
class SessionManager(UploadManager):
    def __init__(self,session_file: str,
                supporting_files: List[str]=None,
                metadata: InvenioMetadata=None,
                uploader: InvenioRDM=None):
        
        self.session_file: str = session_file
        self.supporting_files: List[str] = supporting_files if supporting_files else []
        self.metadata_manager = metadata if metadata else InvenioMetadata()
        self.upload_manager = uploader if uploader else InvenioRDM()

    def execute_upload(self, url, token, community_slug):
        files = [self.session_file] + self.supporting_files
        metadata_json = self.metadata_manager.get_metadata_payload()
        metadata = {"metadata": metadata_json}
        
        self.upload_manager.upload_files(url,token,files,metadata,community_slug)

class OutputManager(UploadManager):
    def __init__(self,output_fld_file: str,
                output_chk_files: List[str]=None,
                filter_files: List[str]=None,
                supporting_files: List[str]=None,
                metadata: InvenioMetadata=None,
                uploader: InvenioRDM=None):
        
        self.output_fld_file: str = output_fld_file
        self.output_chk_files: List[str] = output_chk_files if output_chk_files else []
        self.filter_files: List[str] = filter_files if filter_files else []
        self.supporting_files: List[str] = supporting_files if supporting_files else []
        self.metadata_manager = metadata if metadata else InvenioMetadata()
        self.upload_manager = uploader if uploader else InvenioRDM()

    def execute_upload(self, url, token, community_slug):
        files = [self.output_fld_file] + self.output_chk_files + self.filter_files + self.supporting_files
        metadata_json = self.metadata_manager.get_metadata_payload()
        metadata = {"metadata": metadata_json}

        self.upload_manager.upload_files(url,token,files,metadata,community_slug)