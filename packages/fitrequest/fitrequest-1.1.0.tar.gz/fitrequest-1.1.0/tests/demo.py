from pathlib import Path

from pydantic import Field

from fitrequest.fit_class import FitClass
from fitrequest.fit_config import FitConfig
from fitrequest.fit_var import ValidFitVar
from fitrequest.method_config import MethodConfig
from fitrequest.method_config_family import MethodConfigFamily


# Custom FitConfig
class RestApiConfig(FitConfig):
    class_name: str = 'RestApiClient'
    class_docstring: str = 'Awesome class generated with fitrequest.'

    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'rest_api'
    method_docstring: str = 'Calling endpoint: {endpoint}'

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfigFamily(
                base_name='items',
                endpoint='/items/',
                add_async_method=True,
            ),
            MethodConfig(
                name='get_item',
                endpoint='/items/{item_id}',
            ),
            MethodConfig(
                name='get_item_details',
                endpoint='/items/{item_id}/details/{detail_id}',
            ),
        ]
    )


# New class created from FitConfig
ClassDefault = RestApiConfig().fit_class
ClassWithSpecificArgs = RestApiConfig(base_url='https://staging.skillcorner.fr:8080').fit_class

ClassFromJson = FitClass.from_json(Path(__file__).parent / 'demo.json')
ClassFromYaml = FitClass.from_yaml(Path(__file__).parent / 'demo.yaml')

ClassFromDict = FitClass.from_dict(
    class_name='RestApiClient',
    client_name='rest_api',
    class_docstring='Awesome class generated with fitrequest.',
    base_url='https://test.skillcorner.fr',
    method_docstring='Calling endpoint: {endpoint}',
    method_config_list=[
        {
            'base_name': 'items',
            'endpoint': '/items/',
            'add_async_method': True,
        },
        {
            'name': 'get_item',
            'endpoint': '/items/{item_id}',
        },
        {
            'name': 'get_item_details',
            'endpoint': '/items/{item_id}/details/{detail_id}',
        },
    ],
)

# Client instances from generated classes
client_default = ClassDefault()
client_with_specific_args = ClassWithSpecificArgs()
client_from_json = ClassFromJson()
client_from_yaml = ClassFromYaml()
client_from_dict = ClassFromDict()
