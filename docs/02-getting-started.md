# Getting Started with Puzzel SMS Gateway Python Client

A step-by-step guide to send your first SMS in 5 minutes.

## Prerequisites

Before you begin, make sure you have:

1. **Python 3.10 or higher** installed
2. **Puzzel SMS Gateway credentials**:
   - Service ID
   - Username
   - Password
   - Gateway server URL
3. **A valid phone number** to send test messages to

## Step 1: Install the Client

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

#### Option A: Create a New Project with uv

If you're starting a new project, use this approach:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new project
uv init my-sms-project --app --python 3.13.1
cd my-sms-project

# Create virtual environment with seed packages
uv venv --python 3.13.1 --seed

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Verify installation
python -V
uv pip list

# Install the SMS Gateway client from PyPI
uv pip install puzzel-sms-gateway-client
```

> **Note:** `uv init` typically creates `.venv/` automatically, but `--seed` explicitly ensures that pip, setuptools, and wheel are installed in the virtual environment.

#### Option B: Install into Existing Project

If you already have a project:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to your project directory
cd /path/to/your/project

# Install the client from PyPI
uv pip install puzzel-sms-gateway-client
```

### Using pip

```bash
# Install from PyPI
pip install puzzel-sms-gateway-client
```

This will install the client and all its dependencies.

### Development Installation

If you want to install from source for development purposes:

```bash
# Clone the repository
git clone https://github.com/PuzzelSolutions/smsgw-client-python.git
cd smsgw-client-python/Generated/Python

# Install in editable mode
pip install -e .
# or with uv
uv pip install -e .
```

### Verify Your Environment

After installation, verify that everything is set up correctly:

```bash
# Check Python version (should be 3.10 or higher)
python -V

# List installed packages
uv pip list
# or
pip list

# You should see packages like:
# - kiota-abstractions
# - kiota-http
# - kiota-serialization-json
# - httpx
# - and others...
```

## Step 2: Set Up Your Credentials

Create a file called `config.py` in your project:

```python
# config.py
BASE_URL = "https://your-gateway-server.com"
SERVICE_ID = 12345  # Your service ID
USERNAME = "your_username"
PASSWORD = "your_password"
```

**Important**: Never commit credentials to version control. Consider using environment variables instead:

```python
# config.py
import os

BASE_URL = os.getenv("SMS_GATEWAY_URL", "https://your-gateway-server.com")
SERVICE_ID = int(os.getenv("SMS_SERVICE_ID", "0"))
USERNAME = os.getenv("SMS_USERNAME", "")
PASSWORD = os.getenv("SMS_PASSWORD", "")
```

## Step 3: Send Your First SMS

Create a file called `send_first_sms.py`:

```python
# send_first_sms.py
import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message

# Import your configuration
from config import BASE_URL, SERVICE_ID, USERNAME, PASSWORD


async def send_first_sms():
    """Send your first SMS."""
    
    # 1. Create the client
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = BASE_URL
    client = MtHttpClient(request_adapter)
    
    # 2. Create your message
    request = GatewayRequest(
        service_id=SERVICE_ID,
        username=USERNAME,
        password=PASSWORD,
        message=[
            Message(
                recipient="+47xxxxxxxxx",  # Replace with your phone number
                content="Hello! This is my first SMS from Puzzel Gateway."
            )
        ]
    )
    
    # 3. Send the message
    try:
        response = await client.gw.rs.send_messages.post(request)
        
        print("✓ SMS sent successfully!")
        print(f"Batch Reference: {response.batch_reference}")
        
        for status in response.message_status:
            print(f"\nMessage Details:")
            print(f"  Recipient: {status.recipient}")
            print(f"  Message ID: {status.message_id}")
            print(f"  Status: {status.status_message}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    # Run the async function
    asyncio.run(send_first_sms())
```

## Step 4: Run Your Script

```bash
python send_first_sms.py
```

You should see output like:

```
✓ SMS sent successfully!
Batch Reference: 60908fdd-6da7-4658-b0f7-5685e513c19f

Message Details:
  Recipient: +47xxxxxxxxx
  Message ID: 7a04egxihb00
  Status: Message enqueued for sending
```

## Step 5: Check Your Phone

Within a few seconds, you should receive the SMS on your phone!

## What's Next?

### Send to Multiple Recipients

```python
request = GatewayRequest(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    message=[
        Message(recipient="+47xxxxxxxx1", content="Hello Alice!"),
        Message(recipient="+47xxxxxxxx2", content="Hello Bob!"),
        Message(recipient="+47xxxxxxxx3", content="Hello Charlie!"),
    ]
)
```

### Schedule a Message

```python
from src.models.settings import Settings
from src.models.send_window import SendWindow

message = Message(
    recipient="+47xxxxxxxxx",
    content="This message will be sent tomorrow at 9 AM",
    settings=Settings(
        send_window=SendWindow(
            start_date="2026-03-21",
            start_time="09:00:00"
        )
    )
)
```

### Use a Custom Sender ID

```python
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType

message = Message(
    recipient="+47xxxxxxxxx",
    content="Message from MyCompany",
    settings=Settings(
        originator_settings=OriginatorSettings(
            originator="MyCompany",
            originator_type=OriginatorType.Alphanumeric
        )
    )
)
```

## Common Issues

### Issue: "Connection refused" or "Connection timeout"

**Solution**: Check that your `BASE_URL` is correct (`https://smsgw.puzzel.com`) and that you have network access to the SMS Gateway server. 

**Important**: The base URL should be just the domain (`https://smsgw.puzzel.com`), not including the path (`/gw/rs`). The client automatically adds the correct path.

### Issue: "401 Unauthorized"

**Solution**: Verify your credentials (`SERVICE_ID`, `USERNAME`, `PASSWORD`) are correct.

### Issue: "Invalid phone number"

**Solution**: Make sure your phone number includes the country code (e.g., `+47` for Norway) and is in the correct format.

### Issue: "Module not found"

**Solution**: Make sure you installed the client with `pip install puzzel-sms-gateway-client` or `uv pip install puzzel-sms-gateway-client`. Also verify that your virtual environment is activated.

### Issue: "uv: command not found"

**Solution**: Install uv first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc depending on your shell
```

### Issue: Virtual environment not activating

**Solution**: Make sure you're using the correct activation command for your OS:
- macOS/Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

You should see `(.venv)` in your terminal prompt when activated.

## Learn More

Now that you've sent your first SMS, explore more features:

- **[Main README](../README.md)** - Complete documentation
- **[03 - Quick Reference](03-quick-reference.md)** - Common operations cheat sheet
- **[04 - Examples](04-examples.md)** - Comprehensive usage examples
- **[Example Files](examples/)** - More runnable examples

## Need Help?

- Check the [Troubleshooting Guide](06-advanced.md#troubleshooting)
- Review the [FAQ](../README.md)
- Contact Puzzel support

## Best Practices

1. **Always use async/await** - The client is fully asynchronous
2. **Store credentials securely** - Use environment variables
3. **Validate phone numbers** - Check format before sending
4. **Handle errors** - Always use try/except blocks
5. **Check status codes** - Verify the response status

## Quick Tips

- Phone numbers must include country code (e.g., `+47xxxxxxxxx`)
- Standard SMS can be up to 160 characters (70 for Unicode)
- Status code `1` means success
- Use batch references to track your messages
- Test with your own phone number first

## Example: Complete Working Script

Here's a complete, production-ready example:

```python
import asyncio
import os
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message


async def send_sms(recipient: str, content: str):
    """Send an SMS message."""
    
    # Get configuration from environment
    base_url = os.getenv("SMS_GATEWAY_URL")
    service_id = int(os.getenv("SMS_SERVICE_ID"))
    username = os.getenv("SMS_USERNAME")
    password = os.getenv("SMS_PASSWORD")
    
    # Validate configuration
    if not all([base_url, service_id, username, password]):
        raise ValueError("Missing required configuration")
    
    # Create client
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = base_url
    client = MtHttpClient(request_adapter)
    
    # Create request
    request = GatewayRequest(
        service_id=service_id,
        username=username,
        password=password,
        message=[Message(recipient=recipient, content=content)]
    )
    
    # Send message
    try:
        response = await client.gw.rs.send_messages.post(request)
        
        if response.message_status and response.message_status[0].status_code == 1:
            print(f"✓ SMS sent to {recipient}")
            return True
        else:
            print(f"✗ Failed to send SMS: {response.message_status[0].status_message}")
            return False
            
    except Exception as e:
        print(f"✗ Error sending SMS: {e}")
        return False


if __name__ == "__main__":
    # Set environment variables (or use .env file)
    os.environ["SMS_GATEWAY_URL"] = "https://your-gateway-server.com"
    os.environ["SMS_SERVICE_ID"] = "12345"
    os.environ["SMS_USERNAME"] = "your_username"
    os.environ["SMS_PASSWORD"] = "your_password"
    
    # Send SMS
    success = asyncio.run(send_sms(
        recipient="+47xxxxxxxxx",
        content="Hello from Puzzel SMS Gateway!"
    ))
    
    if success:
        print("Done!")
    else:
        print("Failed!")
```

## Congratulations!

You've successfully sent your first SMS using the Puzzel SMS Gateway Python Client. 🎉

Continue exploring the documentation to learn about advanced features like scheduled messages, batch operations, and more.

Happy coding!
