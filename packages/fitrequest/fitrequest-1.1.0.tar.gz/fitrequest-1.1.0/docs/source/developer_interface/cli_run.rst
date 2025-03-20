CLI
===

.. autofunction:: fitrequest.cli_run.run_pretty
.. autofunction:: fitrequest.cli_run.add_httpx_args
.. autofunction:: fitrequest.cli_run.transform_literals
.. autofunction:: fitrequest.cli_run.literal_to_enum


.. py:classmethod:: fitrequest.cli_run.cli_app

   Set up a CLI interface using Typer.
   Instantiates the fitrequest client, registers all its methods as commands, and returns the typer the application.


.. py:classmethod:: fitrequest.cli_run.cli_run

   Runs the typer application.
