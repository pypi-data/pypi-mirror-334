# bod
Text Blob and Object Dumper

## Overview

`bod`, short for **Blob and Object Dumper**, is a Python module designed to help with analyzing, dumping, and handling
text blobs and objects (HTML/XML/JSON - for now!)

## Features

- Quick function, just import and throw data at the import.
- Options for customizing output/etc.

## Installation

Install the package via pip:

```bash
pip install bod
```

## Usage

Here's a quick example to get started:

```python
import bod
import requests
import logging

resp = requests.get("https://www.google.com")

bod(resp)
# prints formatted html response

bod(resp, output=logging.warning)
# same text, now sent through logging.warning instead of print.

my_var = bod(resp, output=None)
# put output in my_var instead of printing.

bod.detailed(resp)
# headers and request/response info printed.
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Submit a pull request with a detailed description of the changes.

## License

MIT License.

## More coming soon...

Stay tuned for more updates and features!


