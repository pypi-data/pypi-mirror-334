import logging

from .config import config
from drf_spectacular.openapi import AutoSchema


class CustomAutoSchema(AutoSchema):
    def get_operation(self, path, path_regex, path_prefix, method, registry):
        operation = super().get_operation(path, path_regex, path_prefix, method, registry)

        try:
            if operation and type(operation) == dict:
                endpoints = config('OAUTH2.CLIENT.ENDPOINTS')
                endpoint = endpoints.get(path, {}).get(method.lower(), None) if endpoints else {}
                description = operation.get('description', '')
                scopes = ''

                if endpoint:
                    description = description if description else endpoint.get('desc', '')
                    scopes = endpoint.get('scopes', '')
                    if scopes:
                        description = f'{description} - Scopes: {scopes}'
                        operation['extensions'] = {'x-scopes': scopes}
                    operation['description'] = description

        except Exception as e:
            logging.getLogger('api').error(e)

        return operation