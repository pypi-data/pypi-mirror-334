## [25.1.0b2]  

### Breaking Changes  
- **Removed `get_default_api_client()`** from the `BaseTask` class.  
- **Removed `digitalai.release.v1` package**, which previously contained OpenAPI-generated stubs for Release API functions.  
  - These stubs were difficult to use and had several non-functioning methods.  
  - To improve usability and reliability, we are replacing them with a new, simplified API client.  

### Added  
- **Introduced `get_release_api_client()`** in the `BaseTask` class as a replacement for `get_default_api_client()`.  
- **New `ReleaseAPIClient` class** to serve as a wrapper around the `requests` library.  
  - This new class simplifies API interactions by providing a cleaner interface.  
  - Functions in `ReleaseAPIClient` take the **endpoint URL** and **body as a dictionary**, making API calls more intuitive and easier to work with.  

### Changed  
- **Updated minimum Python version requirement to 3.8**.  
- **Updated dependency versions** for improved compatibility and security.  
- **Bundled `requests` library** to ensure seamless HTTP request handling.  
