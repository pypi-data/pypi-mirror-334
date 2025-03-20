# Digital.ai Release Python SDK

The **Digital.ai Release Python SDK** (`digitalai-release-sdk`) provides a set of tools for developers to create container-based plugins with Digital.ai Release. It simplifies plugin creation by offering built-in methods to interact with the execution environment.

## Features
- Define custom tasks using the `BaseTask` abstract class.
- Easily manage input and output properties.
- Interact with the Digital.ai Release environment seamlessly.
- Simplified API client for efficient communication with Release API.


## Installation
Install the SDK using `pip`:

```sh
pip install digitalai-release-sdk
```

## Getting Started

### Example Task: `hello.py`

The following example demonstrates how to create a simple task using the SDK:

```python
from digitalai.release.integration import BaseTask

class Hello(BaseTask):
    
    def execute(self) -> None:
        # Get the name from the input
        name = self.input_properties.get('yourName')
        if not name:
            raise ValueError("The 'yourName' field cannot be empty")

        # Create greeting message
        greeting = f"Hello {name}"

        # Add greeting to the task's comment section in the UI
        self.add_comment(greeting)

        # Store greeting as an output property
        self.set_output_property('greeting', greeting)
```

## Changelog
### Version 25.1.0b3

#### 🚨 Breaking Changes
- **Removed `get_default_api_client()`** from the `BaseTask` class.
- **Removed `digitalai.release.v1` package**, which contained OpenAPI-generated stubs for Release API functions.
  - These stubs were difficult to use and had several non-functioning methods.
  - A new, simplified API client replaces them for better usability and reliability.

#### ✨ New Features
- **Introduced `get_release_api_client()`** in the `BaseTask` class as a replacement for `get_default_api_client()`.
- **New `ReleaseAPIClient` class** for simplified API interactions.
  - Functions in `ReleaseAPIClient` take an **endpoint URL** and **body as a dictionary**, making API calls more intuitive and easier to work with.

#### 🔧 Changes & Improvements
- **Updated minimum Python version requirement to 3.8**.
- **Updated dependency versions** to enhance compatibility and security.
- **Bundled `requests` library** to ensure seamless HTTP request handling.

---
**For more details, visit the [official documentation](https://docs.digital.ai/release/docs/next/category/python-sdk).**

