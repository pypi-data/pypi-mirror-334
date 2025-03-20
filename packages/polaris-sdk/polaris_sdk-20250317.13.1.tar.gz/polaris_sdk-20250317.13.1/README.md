# Polaris SDK

The official Python client library that allows developers to interact with and manage their Polaris
resources through a abstraction layer on top of the [Imply Polaris API](https://docs.imply.io/api/polaris/api-reference).

The main objective of this project is to provide a friendlier interface, speeding up the development processes and ensuring consumers abide by the API contracts.

# Getting Started

## Prerequisites
- Python >= 3.9.0

## Package Installation

To install from pip:
```shell
pip install polaris-sdk
```

## Accessing Polaris Resources

Instantiate the appropriate client based on the type of resource you want to access. There are three client types to choose from:

- GlobalClient: For operations related to a Polaris account.
- RegionalClient: For operations related to a specific Polaris regional cloud.
- ProjectClient: For operations specific to a particular Polaris project.

Note: The clients do not maintain open connections or other persistent resources, so it is safe to keep them in memory and reuse the same instance when needed.

Here's a brief example of listing all projects under a Polaris account:
```python
import os

from polaris.sdk.client import GlobalClient
from polaris.sdk.global_api.models import _models

url = os.environ["POLARIS_BASE_URI"]
apikey = os.environ["POLARIS_API_KEY"]
client = GlobalClient.from_endpoint(url, apikey)

projects = client.projects.list()
assert not isinstance(projects, _models.ErrorResponse)
for project in projects:
    print(project.metadata.name)        
```

 By default the client uses the same retry policy as the [Azure SDK for Python](https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.pipeline.policies.retrypolicy?view=azure-python). If you'd like to modify this behaviour, follow the example below:
```python
from azure.core.pipeline.policies import RetryPolicy
from polaris.sdk.client import GlobalClient

url = os.environ["POLARIS_BASE_URI"]
apikey = os.environ["POLARIS_API_KEY"]

# Option 1: Pass a retry_policy argument to the client constructor
new_policy = RetryPolicy(retry_total=3, backoff_factor=0.1, retry_mode="fixed")
client = GlobalClient.from_endpoint(url, apikey, retry_policy=new_policy)

# Option 2: Pass parameters as keyword arguments to the client constructor
client = GlobalClient.from_endpoint(url, apikey, retry_total=3)
```