# langtools_connectors

A package providing various connectors for integrating with different services. Each connector is built on top of a robust BaseConnector that handles common functionality like authentication, retries, error handling, and resource management.

## Base Features

All connectors inherit from BaseConnector which provides:
- Token management and caching
- Automatic retries with exponential backoff
- Comprehensive error handling and logging
- Async/sync support with context managers
- Resource cleanup
- Configurable timeout and SSL settings
- Custom header management

## Available Connectors

### BingGrounding Client

A client for interacting with Bing's grounding API. Supports:
- Certificate-based authentication
- Synchronous and asynchronous operations
- Flexible query parameters
- Customizable search results configuration

Example usage:
```python
from langtools.connectors import BingGroundingClient
from langtools.core import Credential, CredentialType

# Get credential using certificate
cred = Credential()
cert_cred = cred.get_credential(CredentialType.Certificate)

# Synchronous usage
with BingGroundingClient(
    token_credential=cert_cred,
    scopeid="https://www.bingapis.com/.default"
) as client:
    result = client.search(
        query="What is Azure Cognitive Search?",
        maxGroundingResults=8
    )
```

```JSON
{
  "$type": "GroundingResponse",
  "value": {
    "answers": [
      {
        "$type": "WebPages",
        "answerType": "WebPages",
        "items": [
          {
            "url": "https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search",
            "title": "Introduction to Azure AI Search - Azure AI Search | Microsoft Learn",
            "contractualRules": [
              {
                "$type": "ContractualRules/LinkAttribution",
                "text": "Introduction to Azure AI Search - Azure AI Search | Microsoft Learn",
                "url": "https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search"
              }
            ],
            "semanticDocument": "Introduction to Azure AI Search - Azure AI Search ...",
            "triggeredLocation": "Mop",
            "safetySignal": {
              "riskSeverity": "Safe",
              "categoryInfo": [
                {
                  "riskCategory": "Sexual",
                  "riskInfo": {
                    "riskSeverity": "Safe"
                  }
                },
                {
                  "riskCategory": "Defensive",
                  "riskInfo": {
                    "riskSeverity": "Safe"
                  }
                },
                {
                  "riskCategory": "Hate",
                  "riskInfo": {
                    "riskSeverity": "Safe"
                  }
                },
                {
                  "riskCategory": "Violence",
                  "riskInfo": {
                    "riskSeverity": "Safe"
                  }
                },
                {
                  "riskCategory": "Self_Harm",
                  "riskInfo": {
                    "riskSeverity": "Safe"
                  }
                }
              ],
              "hostQCScore": 0
            }
          }
        ]
      }
    ]
  }
}

```


### Papyrus Client

A client for interacting with Papyrus service, providing access to various AI models and capabilities. Features:
- Azure AD authentication
- Both streaming and non-streaming responses
- Support for multiple models including GPT and DeepSeek
- Text embeddings generation
- Chat and completion endpoints

Example usage:
```python
from langtools.connectors import AsyncPapyrusClient
from langtools.core import Credential, CredentialType

# Initialize Azure credential
cred = Credential()
credential = cred.get_credential(CredentialType.Default)

# Create client
client = AsyncPapyrusClient(
    azure_endpoint="https://westus2batch.papyrus.binginternal.com",
    token_credential=credential,
    scopeid="api://5fe538a8-15d5-4a84-961e-be66cd036687/.default"
)

# Use with async context manager
async with client:
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Azure OpenAI?"}
        ],
        model="gpt4omini-batch",
        temperature=0.7,
        max_tokens=800
    )
```

### ObjectStore Client

A .NET-based client for object storage operations.

#### Prerequisites
- install pythonnet
- .NET 8.x runtime (x64)

## Installation

```bash
pip install langtools_connectors
```

## Development

The package uses Python's asyncio for asynchronous operations. All connectors support both synchronous and asynchronous usage patterns through context managers.

### Error Handling

Connectors implement comprehensive error handling with:
- Automatic retries for transient failures
- Detailed error logging
- Custom error classes
- Resource cleanup on errors

### Authentication

Supports multiple authentication methods:
- Azure AD token credentials
- Certificate-based authentication
- Default Azure credentials

### Logging and Tracing

Built-in support for:
- Structured logging
- Performance tracing
- Metric collection
- Detailed error reporting
- install pythonnet
- install .NET 4.x runtime (x64)

- compile and build the C# source code in release, linux-x64 mode, and put the dlls under folder ./langtools/connectors/objectstore_client/linux-x64, this is for testing purpose.

### Special Notice
Current version of OS client is tested on WSL Ubuntu-22.04, with .NET 8.0.3 runtime and pythonnet 3.0.5

