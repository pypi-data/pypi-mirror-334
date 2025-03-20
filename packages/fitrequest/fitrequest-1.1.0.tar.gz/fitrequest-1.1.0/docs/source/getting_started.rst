Getting Started
===============

Installation
------------

To start using **fitrequest**, you need to install it first:

.. code-block:: bash

    pip install --upgrade fitrequest

How to Use It
-------------

**fitrequest** allows you to create your own api client.
To facilitate this, we provide several syntax options, see :ref:`Configuration Formats` section.

Below an simple example:

.. code-block:: python

  from fitrequest.client import FitRequest


  class RestApiClient(FitRequest):
      """Awesome class generated with fitrequest."""

      client_name = 'rest_api'
      base_url = 'https://test.skillcorner.fr'
      method_docstring = 'Calling endpoint: {endpoint}'

      method_config_list = [
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
      ]


  client = RestApiClient()


In this example there are 4 methods generated, 2 using the :ref:`MethodConfig`, a 2 using the :ref:`MethodConfigFamily`.


Below the generated *help* documentation of this client:


.. code-block:: python

  class RestApiClient(fitrequest.client.FitRequest)
   |  RestApiClient(username: 'str | None' = None, password: 'str | None' = None) -> 'None'
   |
   |  Awesome class generated with fitrequest.
   |
   |  Method resolution order:
   |      RestApiClient
   |      fitrequest.client.FitRequest
   |      builtins.object
   |
   |  Methods defined here:
   |
   |  async async_get_items(self, raise_for_status: bool = True, **kwargs) -> Any from fitrequest.generator
   |      Calling endpoint: /items/
   |
   |  get_item(self, item_id: str, raise_for_status: bool = True, **kwargs) -> Any from fitrequest.generator
   |      Calling endpoint: /items/{item_id}
   |
   |  get_item_details(self, detail_id: str, item_id: str, raise_for_status: bool = True, **kwargs) -> Any from fitrequest.generator
   |      Calling endpoint: /items/{item_id}/details/{detail_id}
   |
   |  get_items(self, raise_for_status: bool = True, **kwargs) -> Any from fitrequest.generator
   |      Calling endpoint: /items/
   |
   |  ----------------------------------------------------------------------
   |  Class methods defined here:
   |
   |  cli_run() -> 'None' from fitrequest.cli_run
   |      Set up a CLI interface using Typer.
   |      Instantiates the fitrequest client, registers all its methods as commands, and runs the application.
   |
   |  ----------------------------------------------------------------------
   |  Readonly properties defined here:
   |
   |  fit_config
   |      Configuration used by fitrequest to generate the methods.
   |
   |  ----------------------------------------------------------------------
   |  Data and other attributes defined here:
   |
   |  __annotations__ = {}
   |
   |  base_url = 'https://test.skillcorner.fr'
   |
   |  client_name = 'rest_api'
   |
   |  session = <fitrequest.session.Session object>
   |
   |  ----------------------------------------------------------------------
   |  Methods inherited from fitrequest.client.FitRequest:
   |
   |  __init__(self, username: 'str | None' = None, password: 'str | None' = None) -> 'None'
   |      Default __init__ method that allows username/password authentication.
   |
   |  ----------------------------------------------------------------------
   |  Data descriptors inherited from fitrequest.client.FitRequest:
   |
   |  __dict__
   |      dictionary for instance variables
   |
   |  __weakref__
   |      list of weak references to the object
   |
   |  ----------------------------------------------------------------------
   |  Data and other attributes inherited from fitrequest.client.FitRequest:
   |
   |  version = '{version}'
