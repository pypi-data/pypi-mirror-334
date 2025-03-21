from drf_spectacular.extensions import OpenApiAuthenticationExtension

from ..utils import config


class OAuth2CustomSchema(OpenApiAuthenticationExtension):
    target_class = 'base_api_utils.security.oauth2_authentication.OAuth2Authentication'
    name = 'OAuth2'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'oauth2',
            'flows': {
                'implicit': {
                    'authorizationUrl': f'{config('OAUTH2.IDP.BASE_URL')}/{config('OAUTH2.IDP.AUTHORIZATION_ENDPOINT')}',
                    'tokenUrl': f'{config('OAUTH2.IDP.BASE_URL')}/{config('OAUTH2.IDP.TOKEN_ENDPOINT')}',
                    'scopes': {}
                },
            },
            'description': 'OAuth2 authentication.',
        }
