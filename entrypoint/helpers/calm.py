'''
helpers/calm.py: Common functions to enable Calm API based
automation for NX-on-GCP.

Author: michael@nutanix.com
Date:   2020-02-24
'''

import sys
import os
import requests
import urllib3
import json

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import (RequestParameters, RequestResponse,
                          RESTClient)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Given a filename, return a dict of the file's contents
def file_to_dict(filename):
  with open(os.path.join(os.getcwd(), filename)) as json_file:
    return json.load(json_file)


# Given an IP and Endpoint, return Nutanix v3 API URL
def create_v3_url(ip, endpoint):
  return f"https://{ip}:9440/api/nutanix/v3/{endpoint}"


# Create a new entity via a v3 post call, return the response
def create_via_v3_post(ip, endpoint, password, body):

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, f"{endpoint}"),
          username="admin",
          password=password,
          method="post",
          payload=json.dumps(body)
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"create_via_v3_post: {ip}, {endpoint}:\n{resp}")

  return resp  


# Return the UUID of a desired entity.  If entity_name is empty
# assume a single entity in response and send first UUID
def uuid_via_v3_post(ip, endpoint, password, entity_name):

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, f"{endpoint}/list"),
          username="admin",
          password=password,
          method="post",
          payload="{\"length\": 100}"
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"uuid_via_v3_post: {ip}, {endpoint}, {entity_name}:\n{resp}")

  # Return UUID
  for entity in resp.json["entities"]:
    if entity_name == "":
      return entity["metadata"]["uuid"]
    elif entity["status"]["name"] == entity_name:
      return entity["metadata"]["uuid"]


# Return the body of a group of entities
def body_via_v3_post(ip, endpoint, password):

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, f"{endpoint}/list"),
          username="admin",
          password=password,
          method="post",
          payload="{\"length\": 100}"
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"body_via_v3_post: {ip}, {endpoint}, {entity_name}:\n{resp}")

  # Return the body
  return resp.json


# Return the body of a desired entity
def body_via_v3_get(ip, endpoint, password, entity_uuid):

  # Make the API call
  parameters = RequestParameters(
        uri=create_v3_url(ip, f"{endpoint}/{entity_uuid}"),
        username="admin",
        password=password,
        method="get",
        payload=None
  )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"body_via_v3_get: {ip}, {endpoint}, {entity_uuid}:\n{resp}")

  # Return the body
  return resp.json

# Update a given entity with a PUT
def update_via_v3_put(ip, endpoint, password, entity_uuid,
                      body):

  # Make the API call
  parameters = RequestParameters(
        uri=create_v3_url(ip, f"{endpoint}/{entity_uuid}"),
        username="admin",
        password=password,
        method="put",
        payload=json.dumps(body)
  )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()

  return resp