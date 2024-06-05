import json
from urllib.parse import urlencode
import requests
from typing import Dict, Union


def get_raw_list_from_api(url, params):
    request_url: str = "https://web.archive.org/cdx/search/xd"
    query_params: Dict[str, Union[str, int]] = {"output": "json", "url": url}
    query_params.update(parameters_for_api(params))
    query_string: str = urlencode(query_params)
    full_url: str = f"{request_url}?{query_string}"

    try:
        print("Fetching data from Web archive")
        response = requests.get(full_url)
        json_data = response.json()
        print(json_data)
        # Validate if the response is a json blob
        if json_data and json_data[0] == ["timestamp", "original"]:
            json_data.pop(0)
        return json_data
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print(response)
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def parameters_for_api(params: dict) -> Dict[str, Union[str, int]]:
    """
    Generates parameters for the API request.

    Args:
        :parameters (dict): The parameters to add to the query

    Returns:
        Dict[str, Union[str, int]]: A dictionary containing parameters for the API request.
    """
    parameters: Dict[str, Union[str, int]] = {"fl": "timestamp,original", "collapse": "digest", "gzip": "false"}
    if not all:
        parameters["filter"] = "statuscode:200"
    if 'from_timestamp' in params and params['from_timestamp'] != 0:
        parameters["from"] = str(params['from_timestamp'])
    if 'to_timestamp' in params and params['to_timestamp'] != 0:
        parameters["to"] = str(params['to_timestamp'])
    if 'page_index' in params:
        parameters["page"] = params['page_index']
    parameters["limit"] = 100
    return parameters
