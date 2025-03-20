import requests
from urllib.parse import urlencode
from ..models import ErrorReport, Folder, FolderList, PostFolder, CopyModel, Updated
from typing import Union, List
from ..utils import safe_data_request

endpoint = "folder"

def folder_acquisition_by_id(baseurl: str, folder_id: str, token: str) -> Union[Folder, ErrorReport]:
    uri = baseurl + endpoint + f'?id={folder_id}'
    # data = None
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = requests.get(uri, headers=head)
    if response.status_code > 300:
        return ErrorReport.model_validate(response.json())
    else:
        folder = Folder.model_validate(response.json())
        folder.__rights__ = response.headers['X-Rights']
        return folder


def folder_acquisition_by_name(baseurl: str, folder_name: str, token: str) -> Union[Folder, ErrorReport]:
    uri = baseurl + endpoint + f"?path={folder_name}"
    # data = None
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = requests.get(uri, headers=head)
    if response.status_code > 300:
        return ErrorReport.model_validate(response.json())
    else:
        folder = Folder.model_validate(response.json())
        folder.__rights__ = response.headers['X-Rights']
        return folder


def list_folder_items(baseurl: str, folder_id: str, token: str) -> Union[FolderList, ErrorReport]:
    uri = baseurl + endpoint + f'/list?id={folder_id}'
    data = None
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('GET', uri, data, head)
    if isinstance(response, ErrorReport):
        return response
    return FolderList.model_validate(response)


def post_folder(baseurl: str, body: PostFolder, token: str) -> Union[Folder, ErrorReport]:
    uri = baseurl + endpoint
    data = body.model_dump_json()
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('POST', uri, data, head)
    if isinstance(response, ErrorReport):
        return response
    return Folder.model_validate(response)

def copy_folder(baseurl: str, body: CopyModel, token: str) -> Union[Folder, ErrorReport]:
    uri = baseurl + endpoint + '/copy'
    data = body.model_dump_json(by_alias=True)
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('POST', uri, data, head)
    if isinstance(response, ErrorReport):
        return response
    return Folder.model_validate(response)

def update_folder(baseurl: str, body: Folder, token: str) -> Union[Folder, ErrorReport]:
    uri = baseurl + endpoint
    data = body.model_dump_json(by_alias=True)
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('PUT', uri, data, head)
    if isinstance(response, ErrorReport):
        return response
    return Folder.model_validate(response)

def delete_folder(baseurl: str, folder_id: str, token: str) -> Union[None, ErrorReport]:
    uri = baseurl + endpoint + f'/{folder_id}'
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('DELETE', uri, None, head)
    if isinstance(response, ErrorReport):
        return response
    return None

def get_all_my_folders(baseurl: str, token: str) -> Union[List[Folder], ErrorReport]:
    uri = baseurl + f'{endpoint}/mine'
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    print(uri)
    response = safe_data_request('GET', uri, None, head)
    if isinstance(response, ErrorReport):
        return response
    return [Folder.model_validate(item) for item in response]
