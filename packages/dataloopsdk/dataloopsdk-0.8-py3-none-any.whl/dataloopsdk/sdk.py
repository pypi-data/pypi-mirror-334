import logging
import requests
import hashlib
import datetime
import base64
import httpx


from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from typing import List, Dict, Any, Optional, Union

from os.path import join, dirname, abspath, basename, exists
from os import makedirs
from .types import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoopSDK:
    def __init__(self, url="https://dataloop-qa.anker-in.com"):
        self.url = url
        self.logger = logging.getLogger(__name__)

    def _calculate_md5(self, file_path: str) -> str:
        """计算文件的MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except IOError as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        return hash_md5.hexdigest()

    def _get_file_meta(self, file_path: str) -> FileMeta:
        """获取文件的宽度和高度，如果是视频，还返回时长"""
        try:
            # Check if the file is an image or video based on the file extension
            supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.mp4', '.avi', '.mov', '.mkv')
            if not file_path.lower().endswith(supported_extensions):
                print(f"Non video or image file for _get_file_meta")
                return FileMeta(resolution=Resolution(width=0, height=0), tokenLength=0, duration=0)

            # Use hachoir to parse the file
            parser = createParser(file_path)
            if not parser:
                raise ValueError(f"Unable to parse file {file_path}")
            metadata = extractMetadata(parser)
            if not metadata:
                raise ValueError(f"Unable to extract metadata from file {file_path}")

            # Extract width and height
            width = metadata.get("width")
            height = metadata.get("height")
            if width is None or height is None:
                print(f"File {file_path} has no width and height")

            resolution = Resolution(width=width, height=height)

            # Extract duration if available
            duration = metadata.get("duration").seconds if metadata.has("duration") else 0
            if duration is None:
                print(f"File {file_path} has no duration")

            return FileMeta(resolution=resolution, tokenLength=0, duration=duration)
        except Exception as e:
            # If it fails, return a default FileMeta and log the error
            print(f"Error reading file {file_path}: {e}")
            return None

    def query_origin_data(self, query_data: dict) -> dict:
        try:
            url = f"{self.url}/query_origin_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=query_data)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while querying origin data: {detail}")
            else:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying origin data: {e}")
        
    async def async_query_origin_data(self, query_data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.url}/query_origin_data"
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = await client.post(url, headers=headers, json=query_data)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
            except ValueError as e:
                raise Exception(f"Error parsing JSON response: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while querying origin data: {e}")

    def _upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        # get upload url
        try:
            url = f"{self.url}/get_upload_url"
            file_name = basename(file_path)
            response = requests.post(url, params={"directory": directory, "file_name": file_name})
            response.raise_for_status()  # Check for HTTP errors
            response = response.json()
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            print(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
            raise Exception(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
        except Exception as e:
            print(f"An error occurred while getting upload URL: {e}")
            raise Exception(f"An error occurred while getting upload URL: {e}")

        # upload file by url
        try:
            upload_url = response.get("url")  # Get the upload URL from the response
            if not upload_url:
                raise Exception("No upload URL found in the response.")
            file_md5 = self._calculate_md5(file_path)  # Calculate the file's MD5
            file_meta = self._get_file_meta(file_path)  # Get the file's metadata
            # Then put to this path
            with open(file_path, "rb") as f:
                res = requests.put(upload_url, data=f)
                res.raise_for_status()  # Check for HTTP errors
                return UploadFileResponse(
                    url=upload_url,
                    bucket=response.get("bucket", ""),
                    storage_id=response.get("storage_id", ""),
                    object_name=response.get("object_name", ""),
                    uid=file_md5,
                    meta=file_meta
                )
        except requests.exceptions.RequestException as e:
            detail = None
            if res is not None:
                try:
                    detail = res.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading file: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading file: {e}")
        
    async def async_upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.url}/get_upload_url"
                file_name = basename(file_path)
                response = await client.post(url, params={"directory": directory, "file_name": file_name})
                response.raise_for_status()
                response = response.json()
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while getting upload URL: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while getting upload URL: {e}")

            try:
                upload_url = response.get("url")
                if not upload_url:
                    raise Exception("No upload URL found in the response.")
                file_md5 = self._calculate_md5(file_path)
                file_meta = self._get_file_meta(file_path)
                with open(file_path, "rb") as f:
                    res = await client.put(upload_url, data=f)
                    res.raise_for_status()
                    return UploadFileResponse(
                        url=upload_url,
                        bucket=response.get("bucket", ""),
                        storage_id=response.get("storage_id", ""),
                        object_name=response.get("object_name", ""),
                        uid=file_md5,
                        meta=file_meta
                    )
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while uploading file: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while uploading file: {e}")

    def get_imagebase64_by_uid(self, uid: str, bg_confirm: str=None) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = self.query_origin_data(query_origin_data)
        except Exception as e:
            print(f"Failed to query origin data: {e}")
            raise Exception(f"Failed to query origin data: {e}")

        try:
            if origin_data is None:
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if records is None or len(records) == 0:
                raise Exception("No origin data found for the given UID.")

            record = records[0]
            get_uid = record.get("uid") if record is not None else None
            file_type = record.get("type") if record is not None else None
            bg = record.get("bg") if record is not None else None

            if get_uid is None or get_uid != uid:
                raise Exception("UID mismatch.")

            if file_type is None or file_type != "image":
                raise Exception("The file is not an image.")

            if bg_confirm is not None:
                if bg is None or bg != bg_confirm:
                    raise Exception(f"The file bg {bg} is not matched with bg_confirm {bg_confirm}.")

            storage = record.get("storage") if record is not None else None
            object_name = storage.get("objectName") if storage is not None else None
            if object_name is None:
                raise Exception("Missing object_name in origin data.")
        except Exception as e:
            print(f"Error occurred while processing origin data: {e}")
            raise Exception(f"Error occurred while processing origin data: {e}")

        try:
            url = f"{self.url}/get_download_url"
            response = requests.post(url, params={"storage_id": storage.get("storageId"), "bucket": storage.get("bucket"), "object_name": object_name})
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while getting download URL: {detail}")
            else:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

        if response_json is None:
            raise Exception("No response received from the server.")

        try:
            download_url = response_json.get("url")  # 从响应中获取下载URL
            if not download_url:
                raise Exception("No download URL found in the response.")
            response = requests.get(download_url)
            response.raise_for_status()  # Check for HTTP errors
            if response is None:
                raise Exception("No response received from the download URL.")

            # Encode the file content to base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64
        except requests.exceptions.RequestException as e:
            print(f"HTTP error occurred while downloading file: {e}")
            raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            print(f"An error occurred while downloading file: {e}")
            raise Exception(f"An error occurred while downloading file: {e}")

    async def async_get_imagebase64_by_uid(self, uid: str, bg_confirm: str=None) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = await self.async_query_origin_data(query_origin_data)
        except Exception as e:
            raise Exception(f"Failed to query origin data: {e}")

        try:
            if origin_data is None:
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if records is None or len(records) == 0:
                raise Exception("No origin data found for the given UID.")

            record = records[0]
            get_uid = record.get("uid") if record is not None else None
            file_type = record.get("type") if record is not None else None
            bg = record.get("bg") if record is not None else None

            if get_uid is None or get_uid != uid:
                raise Exception("UID mismatch.")

            if file_type is None or file_type != "image":
                raise Exception("The file is not an image.")

            if bg_confirm is not None:
                if bg is None or bg != bg_confirm:
                    raise Exception(f"The file bg {bg} is not matched with bg_confirm {bg_confirm}.")

            storage = record.get("storage") if record is not None else None
            object_name = storage.get("objectName") if storage is not None else None
            if object_name is None:
                raise Exception("Missing object_name in origin data.")
        except Exception as e:
            raise Exception(f"Error occurred while processing origin data: {e}")

        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.url}/get_download_url"
                response = await client.post(url, params={"storage_id": storage.get("storageId"), "bucket": storage.get("bucket"), "object_name": object_name})
                response.raise_for_status()
                response_json = response.json()
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
            except ValueError as e:
                raise Exception(f"Error parsing JSON response: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while getting download URL: {e}")

            if response_json is None:
                raise Exception("No response received from the server.")

            try:
                download_url = response_json.get("url")
                if not download_url:
                    raise Exception("No download URL found in the response.")
                response = await client.get(download_url)
                response.raise_for_status()
                if response is None:
                    raise Exception("No response received from the download URL.")

                image_base64 = base64.b64encode(response.content).decode('utf-8')
                return image_base64
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while downloading file: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while downloading file: {e}")


    def _upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        try:
            url = f"{self.url}/upload_raw_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            print(f"upload raw_data: {raw_data}")
            response = requests.post(url, headers=headers, json=raw_data)
            response.raise_for_status()  # 检查HTTP错误
            response_json = response.json()
            if response_json.get("raw_data_id") is None:
                print(f"Failed to upload raw data: {response_json.get('detail', 'No detail provided')}")
            return UploadRawDataResponse(
                raw_data_id=response_json.get("raw_data_id", "")
            )
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading raw data: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading raw data: {e}")
        
    async def async_upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.url}/upload_raw_data"
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = await client.post(url, headers=headers, json=raw_data)
                response.raise_for_status()
                response_json = response.json()
                if response_json.get("raw_data_id") is None:
                    raise Exception(f"Failed to upload raw data: {response_json.get('detail', 'No detail provided')}")
                return UploadRawDataResponse(
                    raw_data_id=response_json.get("raw_data_id", "")
                )
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while uploading raw data: {e}")
            except ValueError as e:
                raise Exception(f"Error parsing JSON response: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while uploading raw data: {e}")

    def upload_data_with_info(self, raw_data: dict, file_path: str, directory: str = "") -> UploadFileWithInfoResponse:
        try:
            # 上传文件
            upload_file_response = self._upload_file(file_path, directory)
            raw_data["uid"] = upload_file_response.uid
            raw_data["storage"] = {"objectName": upload_file_response.object_name, "storageId": upload_file_response.storage_id, "bucket": upload_file_response.bucket}

            if upload_file_response.meta is not None:
                resolution = {"width": upload_file_response.meta.resolution.width, "height": upload_file_response.meta.resolution.height}
                fileMeta = {"resolution": resolution, "tokenLength": upload_file_response.meta.tokenLength, "duration": upload_file_response.meta.duration}
                raw_data["fileMeta"] = fileMeta

            if raw_data.get("securityLevel") is None:
                raw_data["securityLevel"] = "medium"

            if raw_data.get("fileState") is None:
                raw_data["fileState"] = 0 if raw_data.get('fileMeta') is not None else 1

            extra = raw_data.setdefault("extra", {})
            if extra.get("localEventTime") is None:
                extra["localEventTime"] = datetime.datetime.now().strftime("%Y%m%d")

            upload_info_response = self._upload_raw_data(raw_data)
            # print(f"Raw data uploaded with file: {raw_data}")
            return UploadFileWithInfoResponse(
                url=upload_file_response.url,
                bucket=upload_file_response.bucket,
                storage_id=upload_file_response.storage_id,
                object_name=upload_file_response.object_name,
                uid=upload_file_response.uid,
                raw_data_id=upload_info_response.raw_data_id,
                meta=upload_file_response.meta
            )
        except requests.exceptions.RequestException as e:
            detail = None
            if e.response is not None:
                try:
                    detail = e.response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading data with info: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"Failed to upload data with info: {str(e)}")

    async def async_upload_data_with_info(self, raw_data: dict, file_path: str, directory: str = "") -> UploadFileWithInfoResponse:
        try:
            upload_file_response = await self.async_upload_file(file_path, directory)
            raw_data["uid"] = upload_file_response.uid
            raw_data["storage"] = {"objectName": upload_file_response.object_name, "storageId": upload_file_response.storage_id, "bucket": upload_file_response.bucket}

            if upload_file_response.meta is not None:
                resolution = {"width": upload_file_response.meta.resolution.width, "height": upload_file_response.meta.resolution.height}
                fileMeta = {"resolution": resolution, "tokenLength": upload_file_response.meta.tokenLength, "duration": upload_file_response.meta.duration}
                raw_data["fileMeta"] = fileMeta

            if raw_data.get("securityLevel") is None:
                raw_data["securityLevel"] = "medium"

            if raw_data.get("fileState") is None:
                raw_data["fileState"] = 0 if raw_data.get('fileMeta') is not None else 1

            extra = raw_data.setdefault("extra", {})
            if extra.get("localEventTime") is None:
                extra["localEventTime"] = datetime.datetime.now().strftime("%Y%m%d")

            upload_info_response = await self.async_upload_raw_data(raw_data)
            return UploadFileWithInfoResponse(
                url=upload_file_response.url,
                bucket=upload_file_response.bucket,
                storage_id=upload_file_response.storage_id,
                object_name=upload_file_response.object_name,
                uid=upload_file_response.uid,
                raw_data_id=upload_info_response.raw_data_id,
                meta=upload_file_response.meta
            )
        except httpx.RequestError as e:
            raise Exception(f"HTTP error occurred while uploading data with info: {e}")
        except Exception as e:
            raise Exception(f"Failed to upload data with info: {e}")


    def query_annotation_data(self, query_annotation_data: dict) -> dict:
        try:
            url = f"{self.url}/data/annotation/query"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=query_annotation_data)
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
            return response_json
        except requests.exceptions.RequestException as e:
            if response is not None:
                try:
                    detail = response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
                raise Exception(f"HTTP error occurred while querying annotation data: {detail or str(e)}")
            else:
                raise Exception(f"HTTP error occurred while querying annotation data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying annotation data: {e}")
        
    async def async_query_annotation_data(self, query_annotation_data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.url}/data/annotation/query"
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = await client.post(url, headers=headers, json=query_annotation_data)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while querying annotation data: {e}")
            except ValueError as e:
                raise Exception(f"Error parsing JSON response: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while querying annotation data: {e}")

        
    def upload_annotated_data(self, annotated_data: dict) -> UploadAnnotationDataResponse: 
        try:
            url = f"{self.url}/data/annotation"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=annotated_data)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return UploadAnnotationDataResponse( 
                annotation_data_id=response.get("id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while uploading annotated data: {detail}")
            else:
                raise Exception(f"HTTP error occurred while uploading annotated data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading annotated data: {e}")
        
    async def async_upload_annotated_data(self, annotated_data: dict) -> UploadAnnotationDataResponse:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.url}/data/annotation"
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = await client.post(url, headers=headers, json=annotated_data)
                response.raise_for_status()
                response = response.json()
                return UploadAnnotationDataResponse(
                    annotation_data_id=response.get("id", "")
                )
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while uploading annotated data: {e}")
            except ValueError as e:
                raise Exception(f"Error parsing JSON response: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while uploading annotated data: {e}")


    def download_file_by_storage(self, storage_id: str, bucket: str, object_name: str, directory: str) -> str:
        try:
            url = f"{self.url}/get_download_url"
            response = requests.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while getting download URL: {detail}")
            else:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

        try:
            download_url = response.get("url")  # 从响应中获取下载URL
            if not download_url:
                raise Exception("No download URL found in the response.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while downloading file: {detail}")
            else:
                raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading file: {e}")
        
    async def async_download_file_by_storage(self, storage_id: str, bucket: str, object_name: str, directory: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.url}/get_download_url"
                response = await client.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
                response.raise_for_status()
                response = response.json()
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
            except ValueError as e:
                raise Exception(f"Error parsing JSON response: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while getting download URL: {e}")

            try:
                download_url = response.get("url")
                if not download_url:
                    raise Exception("No download URL found in the response.")
                response = await client.get(download_url)
                response.raise_for_status()
                save_path = join(directory, object_name)
                if not exists(dirname(save_path)):
                    makedirs(dirname(save_path))
                with open(save_path, "wb") as f:
                    f.write(response.content)
                return save_path
            except httpx.RequestError as e:
                raise Exception(f"HTTP error occurred while downloading file: {e}")
            except Exception as e:
                raise Exception(f"An error occurred while downloading file: {e}")


    def download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = self.query_origin_data(query_origin_data)

            if not origin_data:  # 检查origin_data是否为空
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if not records or len(records) == 0:  # 检查records是否为空
                raise Exception("No origin data found for the given UID.")

            record = records[0]  # 获取第一个记录
            get_uid = record.get("uid")
            if not get_uid or get_uid != uid:
                raise Exception("UID mismatch.")
            storage = record.get("storage")
            storage_id = storage.get("storageId")
            bucket = storage.get("bucket")
            object_name = storage.get("objectName")
            if not storage_id or not bucket or not object_name:
                raise Exception("Missing storage_id, bucket or object_name in origin data.")
            return self.download_file_by_storage(storage_id, bucket, object_name, directory)  # 调用原始下载方法
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")
        
    async def async_download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = await self.async_query_origin_data(query_origin_data)

            if not origin_data:
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if not records or len(records) == 0:
                raise Exception("No origin data found for the given UID.")

            record = records[0]
            get_uid = record.get("uid")
            if not get_uid or get_uid != uid:
                raise Exception("UID mismatch.")
            storage = record.get("storage")
            storage_id = storage.get("storageId")
            bucket = storage.get("bucket")
            object_name = storage.get("objectName")
            if not storage_id or not bucket or not object_name:
                raise Exception("Missing storage_id, bucket or object_name in origin data.")
            return await self.async_download_file_by_storage(storage_id, bucket, object_name, directory)
        except httpx.RequestError as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")
        
    async def create_item_data(self, 
                               item_id: str,
                               data_ids: List[str], 
                               task_id: Optional[List[str]] = None,
                               event_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new ItemData
        
        Args:
            item_id: The unique identifier for the item (should match MD5 hash of data_ids)
            data_ids: List of data UIDs to include in this item
            task_id: Optional list of associated task IDs
            event_id: Optional event ID for tracking
            
        Returns:
            Dict containing itemId, status and message
        """
        try:
            url = f"{self.url}/item_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # 准备创建数据
            payload = {
                "itemId": item_id,
                "dataIds": data_ids
            }
            if task_id:
                payload["taskId"] = task_id
            if event_id:
                payload["eventId"] = event_id
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            self.logger.error(f"HTTP error occurred while creating item data: {e}")
            raise Exception(f"HTTP error occurred while creating item data: {e}")
        except Exception as e:
            self.logger.error(f"An error occurred while creating item data: {e}")
            raise Exception(f"An error occurred while creating item data: {e}")
    
    async def update_items_by_event_id(self, 
                                      event_id: str, 
                                      task_id: Optional[List[str]] = None,
                                      data_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update ItemData records by event ID
        
        Args:
            event_id: Event identifier to match records
            task_id: Optional list of task IDs to update
            data_ids: Optional list of data IDs to add (incremental update)
            
        Returns:
            Dict containing updated records
        """
        try:
            url = f"{self.url}/item_data/event/{event_id}"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            payload = {}
            if task_id:
                payload["taskId"] = task_id
            if data_ids:
                payload["dataIds"] = data_ids
                
            if not payload:
                raise ValueError("At least one update parameter (taskId or dataIds) must be provided")
            
            async with httpx.AsyncClient() as client:
                response = await client.put(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            self.logger.error(f"HTTP error occurred while updating items by event ID: {e}")
            raise Exception(f"HTTP error occurred while updating items by event ID: {e}")
        except Exception as e:
            self.logger.error(f"An error occurred while updating items by event ID: {e}")
            raise Exception(f"An error occurred while updating items by event ID: {e}")
        
    async def async_query_item_data(self, 
                                task_id: Optional[str] = None,
                                item_id: Optional[str] = None, 
                                event_id: Optional[str] = None,
                                skip: int = 0, 
                                limit: int = 20) -> Dict[str, Any]:
        """
        Asynchronously query ItemData records with specified filters
        
        Args:
            task_id: Optional task ID to filter by
            item_id: Optional item ID to filter by
            event_id: Optional event ID to filter by
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dict containing total count and matching records
        """
        try:
            url = f"{self.url}/item_data/query"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Build query payload
            payload = {
                "skip": skip,
                "limit": limit
            }
            
            if task_id:
                payload["taskId"] = task_id
            if item_id:
                payload["itemId"] = item_id
            if event_id:
                payload["eventId"] = event_id
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            self.logger.error(f"HTTP error occurred while querying item data: {e}")
            raise Exception(f"HTTP error occurred while querying item data: {e}")
        except Exception as e:
            self.logger.error(f"An error occurred while querying item data: {e}")
            raise Exception(f"An error occurred while querying item data: {e}")

    def generate_item_id(self, data_ids: List[str]) -> str:
        """
        根据数据ID列表生成一致的ItemID (MD5哈希)
        
        Args:
            data_ids: 数据ID列表
            
        Returns:
            str: 生成的ItemID (MD5哈希)
        """
        # 对数据ID进行排序，确保输出的一致性
        # sorted_ids = sorted(data_ids)
        item_id_str = "_".join(data_ids)
        return hashlib.md5(item_id_str.encode()).hexdigest()
    
    async def update_or_create_item_data(self, 
                                        event_id: str, 
                                        data_ids: List[str],
                                        task_id: Optional[List[str]] = None,
                                        device_sn: Optional[str] = None,
                                        status: Optional[str] = None) -> Dict[str, Any]:
        """
        更新或创建ItemData记录：如果指定event_id的记录存在则更新，否则创建
        
        Args:
            event_id: 事件ID
            data_ids: 数据ID列表
            task_id: 可选的任务ID列表
            device_sn: 可选的设备序列号
            status: 可选的状态
            
        Returns:
            Dict: 操作结果
        """
        if not event_id:
            raise ValueError("Event ID cannot be empty")
        if not data_ids:
            raise ValueError("Data IDs list cannot be empty")
        
        try:
            # 1. 查询是否已存在该event_id的ItemData记录
            query_result = await self.async_query_item_data(event_id=event_id, limit=1)
            records = query_result.get("records", [])
            
            # 2. 如果记录存在，执行更新
            if records and len(records) > 0:
                self.logger.info(f"Found existing ItemData with event_id {event_id}, updating...")
                
                # 创建更新数据
                update_result = await self.update_items_by_event_id(
                    event_id=event_id,
                    task_id=task_id,
                    data_ids=data_ids
                )
                
                self.logger.info(f"Successfully updated ItemData for event_id {event_id}")
                return update_result
                
            # 3. 如果记录不存在，执行创建
            else:
                self.logger.info(f"No ItemData found with event_id {event_id}, creating new record...")
                
                # 生成item_id (MD5哈希)
                item_id = self.generate_item_id(data_ids)
                
                # 创建新记录
                create_data = {
                    "item_id": item_id,
                    "data_ids": data_ids,
                    "event_id": event_id
                }
                
                if task_id:
                    create_data["task_id"] = task_id
                    
                create_result = await self.create_item_data(
                    item_id=item_id,
                    data_ids=data_ids,
                    task_id=task_id,
                    event_id=event_id
                )
                
                self.logger.info(f"Successfully created ItemData with event_id {event_id}")
                return create_result
                
        except Exception as e:
            self.logger.error(f"Error in update_or_create_item_data: {e}")
            raise Exception(f"Failed to update or create ItemData: {e}")

    def update_or_create_item_data_sync(self, 
                                    event_id: str, 
                                    data_ids: List[str],
                                    task_id: Optional[List[str]] = None,
                                    device_sn: Optional[str] = None,
                                    status: Optional[str] = None) -> Dict[str, Any]:
        """
        更新或创建ItemData记录的同步方法：如果指定event_id的记录存在则更新，否则创建
        
        Args:
            event_id: 事件ID
            data_ids: 数据ID列表
            task_id: 可选的任务ID列表
            device_sn: 可选的设备序列号
            status: 可选的状态
            
        Returns:
            Dict: 操作结果
        """
        if not event_id:
            raise ValueError("Event ID cannot be empty")
        if not data_ids:
            raise ValueError("Data IDs list cannot be empty")
        
        try:
            # 1. 查询是否已存在该event_id的ItemData记录
            url = f"{self.url}/item_data/query"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            query_payload = {
                "eventId": event_id,
                "limit": 1
            }
            
            response = requests.post(url, headers=headers, json=query_payload)
            response.raise_for_status()
            query_result = response.json()
            records = query_result.get("records", [])
            
            # 2. 如果记录存在，执行更新
            if records and len(records) > 0:
                self.logger.info(f"Found existing ItemData with event_id {event_id}, updating...")
                
                # 执行更新请求
                update_url = f"{self.url}/item_data/event/{event_id}"
                update_payload = {}
                
                if task_id:
                    update_payload["taskId"] = task_id
                if data_ids:
                    update_payload["dataIds"] = data_ids
                    
                if not update_payload:
                    raise ValueError("At least one update parameter must be provided")
                
                update_response = requests.put(update_url, headers=headers, json=update_payload)
                update_response.raise_for_status()
                update_result = update_response.json()
                
                self.logger.info(f"Successfully updated ItemData for event_id {event_id}")
                return update_result
                
            # 3. 如果记录不存在，执行创建
            else:
                self.logger.info(f"No ItemData found with event_id {event_id}, creating new record...")
                
                # 生成item_id (MD5哈希)
                item_id = self.generate_item_id(data_ids)
                print(f"Generated item_id: {item_id}")
                
                # 创建新记录
                create_url = f"{self.url}/item_data"
                create_payload = {
                    "itemId": item_id,
                    "dataIds": data_ids,
                    "eventId": event_id
                }
                
                if task_id:
                    create_payload["taskId"] = task_id
                    
                create_response = requests.post(create_url, headers=headers, json=create_payload)
                create_response.raise_for_status()
                create_result = create_response.json()
                
                self.logger.info(f"Successfully created ItemData with event_id {event_id}")
                return create_result
                
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            self.logger.error(f"HTTP error occurred while updating or creating item data: {detail or str(e)}")
            raise Exception(f"HTTP error occurred while updating or creating item data: {detail or str(e)}")
        except Exception as e:
            self.logger.error(f"An error occurred while updating or creating item data: {e}")
            raise Exception(f"Failed to update or create ItemData: {e}")

    def query_item_data(self, 
                    task_id: Optional[str] = None,
                    item_id: Optional[str] = None, 
                    event_id: Optional[str] = None,
                    skip: int = 0, 
                    limit: int = 20) -> Dict[str, Any]:
        """
        查询ItemData记录
        
        Args:
            task_id: 可选的任务ID过滤条件
            item_id: 可选的项目ID过滤条件
            event_id: 可选的事件ID过滤条件
            skip: 跳过记录数量(用于分页)
            limit: 最大返回记录数
            
        Returns:
            Dict: 包含记录总数和匹配记录的字典
        """
        try:
            url = f"{self.url}/item_data/query"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # 构建查询参数
            payload = {
                "skip": skip,
                "limit": limit
            }
            
            if task_id:
                payload["taskId"] = task_id
            if item_id:
                payload["itemId"] = item_id
            if event_id:
                payload["eventId"] = event_id
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            self.logger.error(f"HTTP error occurred while querying item data: {detail or str(e)}")
            raise Exception(f"HTTP error occurred while querying item data: {detail or str(e)}")
        except Exception as e:
            self.logger.error(f"An error occurred while querying item data: {e}")
            raise Exception(f"An error occurred while querying item data: {e}")