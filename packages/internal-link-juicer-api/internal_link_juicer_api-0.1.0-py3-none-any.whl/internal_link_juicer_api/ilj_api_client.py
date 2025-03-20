# internal-link-juicer-api/ilj_api_client.py

import requests
from requests.auth import HTTPBasicAuth
import json
import phpserialize


class ILJDefinitionAPIClient:
    """
    A client for interacting with the Internal Link Juicer API.

    Provides methods for retrieving and updating link definitions.
    """

    def __init__(self, website, username, password):
        self.website = website.rstrip('/')
        self.username = username
        self.password = password
        self.api_base_url = f"{self.website}/wp-json/internal-link-juicer-api/v1"

    def get_definitions(self, page=1, per_page=10):
        """Retrieves all ILJ link definitions with pagination.

        Args:
            page (int): The page number to retrieve (default: 1).
            per_page (int): The number of definitions per page (default: 10).

        Returns:
            list: A list of definition dictionaries, or None on error.
        """
        api_url = f"{self.api_base_url}/definitions?page={page}&per_page={per_page}"
        print(f"**DEBUG REST API REQUEST - GET All Definitions from: {api_url}**")

        try:
            response = requests.get(
                api_url,
                auth=HTTPBasicAuth(self.username, self.password),
                # verify=False  <-- Removed INSECURE option.  See earlier responses for how to handle SSL properly.
            )
            response.raise_for_status()
            definitions = response.json()
            print(f"**DEBUG REST API RESPONSE - GET All Definitions - Status Code: {response.status_code}**")
            print(f"**DEBUG REST API RESPONSE - GET All Definitions - Content:**")
            print(json.dumps(definitions, indent=2))
            return definitions
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def update_definition_by_meta_id(self, meta_id, new_meta_value):
        """Updates an ILJ link definition by its meta_id.

        Args:
            meta_id (int): The meta_id of the definition to update.
            new_meta_value (list): The new list of keywords.

        Returns:
            dict: The API response, or None on error.
        """
        api_url = f"{self.api_base_url}/definitions/{meta_id}"
        print(f"**DEBUG REST API REQUEST - Update Definition by Meta ID - URL: {api_url}, Meta ID: {meta_id}, New Value: '{new_meta_value}'**")

        if not isinstance(new_meta_value, list):
            print(f"Error: new_meta_value must be a list.  Got: {type(new_meta_value)}")
            return None

        serialized_list = []
        for item in new_meta_value:
            if isinstance(item, str) and item.strip():
                serialized_list.append(item)
            elif isinstance(item, (int, float)):
                serialized_list.append(str(item))
            else:
                print(f"Warning: Skipping invalid item in new_meta_value: {item} (type: {type(item)})")

        try:
            serialized_value = phpserialize.dumps(serialized_list,charset="utf-8").decode()
        except Exception as e:
            print(f"ERROR:  Failed to serialize to PHP format: {e}")
            return None

        print(f"**DEBUG Serialized meta_value: {serialized_value}**")
        payload = {'meta_value': serialized_value}
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(
                api_url,
                auth=HTTPBasicAuth(self.username, self.password),
                headers=headers,
                json=payload,
                # verify=False  # <-- Removed INSECURE option
            )
            response.raise_for_status()
            update_response = response.json()
            print(f"**DEBUG REST API RESPONSE - Update Definition by Meta ID - Status Code: {response.status_code}**")
            print(f"**DEBUG REST API RESPONSE - Update Definition by Meta ID - Content:**")
            print(json.dumps(update_response, indent=2))
            return update_response

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_definition_by_post_id(self, post_id):
        """Retrieves the ILJ link definition for a given post_id.

        Args:
            post_id (int): The ID of the post.

        Returns:
            dict: The definition, or None if not found or on error.
        """
        api_url = f"{self.api_base_url}/posts/{post_id}/definition"
        print(f"**DEBUG REST API REQUEST - GET Definition by Post ID - URL: {api_url}, Post ID: {post_id}**")

        try:
            response = requests.get(
                api_url,
                auth=HTTPBasicAuth(self.username, self.password),
                # verify=False  <-- Removed INSECURE option
            )
            response.raise_for_status()
            definition = response.json()
            print(f"**DEBUG REST API RESPONSE - GET Definition by Post ID - Status Code: {response.status_code}**")
            print(f"**DEBUG REST API RESPONSE - GET Definition by Post ID - Content:**")
            print(json.dumps(definition, indent=2))
            return definition

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def update_definition_by_post_id(self, post_id, new_meta_value):
        """Updates the ILJ link definition for a given post_id.

        Args:
            post_id (int): The ID of the post to update.
            new_meta_value (list): The new keywords, as a list of strings.  This list will be
                                   serialized to a PHP serialized string before sending.

        Returns:
            dict: The API response, or None on error.
        """

        api_url = f"{self.api_base_url}/posts/{post_id}/definition"
        print(
            f"**DEBUG REST API REQUEST - Update Definition by Post ID - URL: {api_url}, Post ID: {post_id}, New Value: '{new_meta_value}'**"
        )

        if not isinstance(new_meta_value, list):
            print(f"Error: new_meta_value must be a list.  Got: {type(new_meta_value)}")
            return None

        serialized_list = []  # New empty keyword list.
        for item in new_meta_value:
            if isinstance(item, str) and item.strip():  # check if string and not empty string
                serialized_list.append(item)
            elif isinstance(item, (int, float)):  # check if int of float, convert to str.
                serialized_list.append(str(item))
            else:  # If an item is neither, string, empty, int or float; error message printed, rejected to be inserted keyword list.
                print(f"Warning: Skipping invalid item in new_meta_value: {item} (type: {type(item)})")

        # Serialize and decode inside try..except.
        try:
            serialized_value = phpserialize.dumps(serialized_list,charset="utf-8").decode()
        except Exception as e:
            print(f"ERROR:  Failed to serialize to PHP format: {e}")
            return None  # Return None on serilization errors.

        print(f"**DEBUG Serialized meta_value: {serialized_value}**")  # Debugging
        payload = {'meta_value': serialized_value}  # Now correctly sending the string
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(  # Or .put() or .patch() - all valid with EDITABLE
                api_url,
                auth=HTTPBasicAuth(self.username, self.password),
                headers=headers,
                json=payload,
                # verify=False  <-- Removed.
            )
            response.raise_for_status()
            update_response = response.json()
            print(f"**DEBUG REST API RESPONSE - Update Definition by Post ID - Status Code: {response.status_code}**")
            print(f"**DEBUG REST API RESPONSE - Update Definition by Post ID - Content:**")
            print(json.dumps(update_response, indent=2))
            return update_response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None