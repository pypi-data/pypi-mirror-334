from typing import  Optional, List, Union
from pydantic import BaseModel

class Resolution(BaseModel):
    width: int
    height: int

class FileMeta(BaseModel):
    resolution: Optional[Resolution] = None
    tokenLength: int
    duration: int

class UploadFileResponse(BaseModel):
    url: str
    bucket: str
    storage_id: str
    object_name: str
    uid: str
    meta: Optional[FileMeta] = None

class UploadRawDataResponse(BaseModel):
    raw_data_id: str

class UploadFileWithInfoResponse(BaseModel):
    url: str
    bucket: str
    storage_id: str
    object_name: str
    uid: str
    raw_data_id: str
    meta: Optional[FileMeta] = None

class UploadAnnotationDataResponse(BaseModel):
    annotation_data_id: str