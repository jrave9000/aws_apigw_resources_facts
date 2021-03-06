#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: aws_apigw_resources_facts
version_added: 0.1
short_description: Get AWS API Gateway Resources facts.
description:
  - Create Amazon API Gateway VPC link
requirements: [ boto3 ]
author: '@jr9000'
options:
  id:
    description:
      - The identifier of the associated RestApi.
    type: str

extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
'''

EXAMPLES = r'''
# Note: These examples do not set authentication details, see the AWS Guide for details.
- name: Get resources
  aws_apigw_resources_facts:
    id: hlji08
'''

RETURN = r'''
"resources": {
    "items": [
        {
            "id": "bxiuwav2w6", 
            "path": "/"
        }, 
        {
            "id": "lkji07", 
            "parent_id": "bzyuvav2w6", 
            "path": "/v1", 
            "path_part": "v1"
        }, 
        {
            "id": "iaqbfq", 
            "parent_id": "gkhi07", 
            "path": "/v1/{proxy+}", 
            "path_part": "{proxy+}", 
            "resource_methods": {
                "any": {}
            }
        }
    ], 
    "response_metadata": {
        "http_headers": {
            "connection": "keep-alive", 
            "content-length": "253", 
            "content-type": "application/json", 
            "date": "Thu, 29 Oct 2020 08:46:09 GMT", 
            "x-amz-apigw-id": "VKklvLBKiYcEd3A=", 
            "x-amzn-requestid": "2cd6f4e6-c239-4502-8bda-01565ced2199"
        }, 
        "http_status_code": 200, 
        "request_id": "2cd6f4e6-c239-4502-8bda-01565ced2199", 
        "retry_attempts": 0
    }
}
'''

import json

try:
    import botocore
except ImportError:
    pass  # Handled by AnsibleAWSModule

import traceback
from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict


def main():
    argument_spec = dict(
        id=dict(type='str', required=True)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )

    id = module.params.get('id')
    changed = False
    exit_args = {}

    client = module.client('apigateway')
    
    msg = camel_dict_to_snake_dict(get_resources(client, id))

    exit_args['resources'] = camel_dict_to_snake_dict(msg)
    exit_args['changed'] = changed

    module.exit_json(**exit_args)

retry_params = {'retries': 10, 'delay': 10, 'catch_extra_error_codes': ['TooManyRequestsException']}

@AWSRetry.jittered_backoff(**retry_params)
def get_resources(client, id):
    return client.get_resources(restApiId=id, limit=500)

if __name__ == '__main__':
    main()

