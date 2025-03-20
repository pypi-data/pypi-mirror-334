# EnvValidator

EnvValidator is a lightweight Python library that helps validate environment variables against a predefined schema. It ensures that required variables exist, follow the correct type or format, and falls back to system environment variables when an .env file is missing.

---

## Features

- Schema-Based Validation - Define expected environment variables and their types (string, int, bool, regex).
- Automatic Fallback - If no .env file is found, it retrieves values from system environment variables.
- Regex Support - Enforce custom formats (e.g., API keys, UUIDs).
- Error Handling - Provides clear error messages when validation fails.
- Lightweight & Fast - Minimal overhead with a simple API.

---

## Requirements

- Python 3.x (recommended: 3.7 or higher)

---

## Installation

Install the package using pip:

```bash
pip install envvalidator
```

## Usage
Here is an example of how to use EnvValidator:

```python

# Define the expected schema
schema = {
    "DATABASE_URL": "string",
    "DEBUG": "bool",
    "PORT": "int",
    "API_KEY": {"regex": r"^[A-Za-z0-9]{32}$"}  # Ensure 32-character API key format
}

try:
    ENV = envvalidator.validate_env(".env", schema)
    print(ENV)
except ValueError as e:
    print("Configuration error:", e)
```
## Output Example
If .env contains:
```ini
DATABASE_URL=postgres://user:pass@localhost:5432/db
DEBUG=true
PORT=8080
API_KEY=1234567890abcdef1234567890abcdef
```
The output would be:
```plaintext
{
    "DATABASE_URL": "postgres://user:pass@localhost:5432/db",
    "DEBUG": "true",
    "PORT": "8080",
    "API_KEY": "1234567890abcdef1234567890abcdef"
}
```
If a required variable is missing or does not match the expected type, an error is raised.

## How It Works
1. Reads the .env file (if available).
2. Parses key-value pairs and trims whitespace.
3. Checks each variable against the schema:
    - If defined in .env, it is validated.
    - If missing, it looks in system environment variables.
    - If validation fails, an error is raised.
4. Returns a dictionary of validated environment variables.

## Limitations
- Does not support deeply nested configurations (e.g., JSON-like structures).
- Assumes all values are stored as strings in environment variables.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request if you have suggestions or improvements.

## Local Development
To set up a local development environment, follow these steps:

1. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
    ```
2. Build & install the project
    ```bash
    python setup.py build
    python setup.py install
    ```
3. Run an example script to test:
    ```bash
    python examples/example.py
    ```
The module is now installed in the virtual environment. You can test it by running the example script:

```bash
python examples/example.py
```


## License
This project is licensed under the Apache-2.0 License. See the LICENSE file for details.

## Author
Developed by Qiyaya

## Acknowledgements
Thanks to the Python (and ...) development communities for providing tools and resources to make this project possible.

```vbnet
This styling ensures clarity, proper sectioning, and good readability. Let me know if you`d like any further adjustments!
```
