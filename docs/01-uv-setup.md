# Setting Up with uv

Complete guide for setting up the Puzzel SMS Gateway Python Client using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

## Why uv?

- **Fast**: 10-100x faster than pip
- **Reliable**: Consistent dependency resolution
- **Modern**: Built with Rust for performance
- **Compatible**: Drop-in replacement for pip

## Prerequisites

- Python 3.10 or higher
- Terminal/Command Prompt access

## Installation Steps

### 1. Install uv

#### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Verify Installation

```bash
uv --version
```

### 2. Create a New Project

Create a new Python project with uv:

```bash
# Create project with Python 3.13.1
uv init my-sms-project --app --python 3.13.1

# Navigate to project directory
cd my-sms-project
```

**What this does:**
- Creates a new directory `my-sms-project/`
- Sets up project structure with `pyproject.toml`
- Configures Python 3.13.1 as the project Python version
- `--app` flag indicates this is an application (not a library)

### 3. Create Virtual Environment

```bash
# Create virtual environment with seed packages
uv venv --python 3.13.1 --seed
```

**What this does:**
- Creates `.venv/` directory in your project
- Installs Python 3.13.1 in the virtual environment
- `--seed` ensures pip, setuptools, and wheel are installed

> **Note:** `uv init` typically creates `.venv/` automatically, but `--seed` explicitly ensures that standard tools are available.

### 4. Activate Virtual Environment

#### macOS/Linux

```bash
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)

```cmd
.venv\Scripts\activate.bat
```

**Verification:**
You should see `(.venv)` prefix in your terminal prompt:

```
(.venv) user@machine:~/my-sms-project$
```

### 5. Verify Environment

```bash
# Check Python version
python -V
# Output: Python 3.13.1

# List installed packages
uv pip list
# or
pip list

# Check uv pip works
uv pip --version
```

### 6. Install SMS Gateway Client

```bash
# Install the SMS Gateway client from PyPI
uv pip install puzzel-sms-gateway-client
```

**For development installation from source:**

```bash
# Clone the repository
git clone https://github.com/PuzzelSolutions/smsgw-client-python.git
cd smsgw-client-python/Generated/Python

# Install in editable mode
uv pip install -e .
```

### 7. Verify Installation

```bash
# List all installed packages
uv pip list

# You should see:
# - kiota-abstractions
# - kiota-http
# - kiota-serialization-json
# - kiota-serialization-text
# - kiota-serialization-form
# - kiota-serialization-multipart
# - httpx
# - and their dependencies
```

## Project Structure

After setup, your project should look like this:

```
my-sms-project/
├── .venv/                  # Virtual environment
├── .python-version         # Python version specification
├── pyproject.toml          # Project configuration
├── README.md               # Project README
└── src/                    # Your source code
    └── __init__.py
```

## Using uv in Your Project

### Installing Packages

```bash
# Install a package
uv pip install package-name

# Install multiple packages
uv pip install package1 package2 package3

# Install from requirements.txt
uv pip install -r requirements.txt

# Install in development mode
uv pip install -e .
```

### Managing Dependencies

```bash
# List installed packages
uv pip list

# Show package details
uv pip show package-name

# Freeze dependencies
uv pip freeze > requirements.txt

# Uninstall a package
uv pip uninstall package-name
```

### Syncing Dependencies

```bash
# Install all dependencies from pyproject.toml
uv pip sync

# Install with specific extras
uv pip install -e ".[dev]"
```

## Complete Example

Here's a complete example from start to finish:

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Create project
uv init sms-notification-service --app --python 3.13.1
cd sms-notification-service

# 3. Create and activate virtual environment
uv venv --python 3.13.1 --seed
source .venv/bin/activate

# 4. Verify setup
python -V
uv pip list

# 5. Install SMS Gateway client
uv pip install puzzel-sms-gateway-client

# 6. Create your first script
cat > send_sms.py << 'EOF'
import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message

async def main():
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = "https://your-gateway-server.com"
    
    client = MtHttpClient(request_adapter)
    
    request = GatewayRequest(
        service_id=12345,
        username="your_username",
        password="your_password",
        message=[Message(recipient="+47xxxxxxxxx", content="Hello from uv!")]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    print(f"Sent! Batch: {response.batch_reference}")

if __name__ == "__main__":
    asyncio.run(main())
EOF

# 7. Run your script
python send_sms.py
```

## Working with pyproject.toml

uv works seamlessly with `pyproject.toml`. Here's an example configuration:

```toml
[project]
name = "sms-notification-service"
version = "0.1.0"
description = "SMS notification service using Puzzel Gateway"
requires-python = ">=3.10"
dependencies = [
    "kiota-abstractions>=1.0.0",
    "kiota-http>=1.0.0",
    "kiota-serialization-json>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Install with dev dependencies:

```bash
uv pip install -e ".[dev]"
```

## Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

## Removing Virtual Environment

To completely remove the virtual environment:

```bash
# Make sure you're not in the virtual environment
deactivate

# Remove the directory
rm -rf .venv
```

## Common Commands Reference

| Task | Command |
|------|---------|
| Install uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Create project | `uv init <name> --app --python 3.13.1` |
| Create venv | `uv venv --python 3.13.1 --seed` |
| Activate (Unix) | `source .venv/bin/activate` |
| Activate (Windows) | `.venv\Scripts\activate` |
| Install package | `uv pip install <package>` |
| Install editable | `uv pip install -e .` |
| List packages | `uv pip list` |
| Freeze deps | `uv pip freeze > requirements.txt` |
| Uninstall | `uv pip uninstall <package>` |
| Deactivate | `deactivate` |

## Troubleshooting

### uv command not found

After installing uv, you may need to restart your terminal or reload your shell configuration:

```bash
# For bash
source ~/.bashrc

# For zsh
source ~/.zshrc

# Or just restart your terminal
```

### Permission denied during installation

Try running with appropriate permissions or install to user directory:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Python version not available

If the specified Python version isn't available:

```bash
# Check available Python versions
python3 --version
python3.13 --version

# Use available version
uv venv --python 3.12
```

### Virtual environment not activating

Make sure you're using the correct command for your OS and shell:

- **macOS/Linux (bash/zsh)**: `source .venv/bin/activate`
- **Windows PowerShell**: `.venv\Scripts\Activate.ps1`
- **Windows CMD**: `.venv\Scripts\activate.bat`

### Packages not found after installation

Make sure your virtual environment is activated:

```bash
# Check if activated (should show .venv path)
which python

# If not activated
source .venv/bin/activate
```

## Best Practices

1. **Always use virtual environments** - Isolate project dependencies
2. **Pin Python version** - Use specific version in `uv init`
3. **Use pyproject.toml** - Modern Python project configuration
4. **Commit .python-version** - Share Python version with team
5. **Don't commit .venv/** - Add to `.gitignore`
6. **Use requirements.txt or pyproject.toml** - Track dependencies
7. **Activate before working** - Always activate venv before coding

## Migrating from pip/Poetry

### From pip

```bash
# Old way
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# New way with uv
uv venv --seed
source .venv/bin/activate
uv pip install -r requirements.txt
```

### From Poetry

```bash
# Old way
poetry install
poetry shell

# New way with uv
uv venv --seed
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Additional Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [uv Installation Guide](https://github.com/astral-sh/uv#installation)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pyproject.toml Specification](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/)

## Next Steps

After setting up with uv:

1. Follow the [02 - Getting Started Guide](02-getting-started.md) to send your first SMS
2. Check out the [Example Files](examples/) for code samples
3. Review the [03 - Quick Reference](03-quick-reference.md) for common operations

---

**Need Help?**

- Check the [Main README](../README.md)
- Review the [Troubleshooting Guide](06-advanced.md#troubleshooting)
- Contact Puzzel support
