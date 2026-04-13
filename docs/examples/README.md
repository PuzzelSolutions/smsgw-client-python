# Example Code Files

This folder contains runnable example scripts demonstrating various features of the Puzzel SMS Gateway Python Client.

## Available Examples

### 1. example_basic.py
**Simple SMS sending example**

The most basic example showing how to send a single SMS message. Perfect starting point for new users.

```bash
python docs/examples/example_basic.py
```

Features demonstrated:
- Client setup and initialization
- Basic message sending
- Response handling

---

### 2. example_advanced.py
**Advanced configuration example**

Comprehensive example showing all available configuration options.

```bash
python docs/examples/example_advanced.py
```

Features demonstrated:
- Scheduled message delivery (send window)
- Custom originator (sender ID)
- Priority and validity settings
- Premium SMS with pricing
- GAS settings
- Custom parameters
- All message settings options

---

### 3. example_multiple_recipients.py
**Multiple recipients example**

Examples of sending SMS to multiple recipients in different ways.

```bash
python docs/examples/example_multiple_recipients.py
```

Features demonstrated:
- Sending same message to multiple recipients
- Sending personalized messages to different recipients
- Batch sending with rate limiting
- Bulk message handling

---

### 4. example_batch_management.py
**Batch management example**

Examples of managing message batches.

```bash
python docs/examples/example_batch_management.py
```

Features demonstrated:
- Listing all batches for a service
- Getting details of a specific batch
- Stopping a batch
- Monitoring batch status

---

## Running the Examples

### Prerequisites

1. Install the SMS Gateway client:
   ```bash
   # Using uv (recommended)
   uv pip install puzzel-sms-gateway-client
   
   # Or using pip
   pip install puzzel-sms-gateway-client
   ```

2. Configure your credentials in each example file:
   - `BASE_URL`: Your SMS Gateway server URL
   - `SERVICE_ID`: Your service ID
   - `USERNAME`: Your username
   - `PASSWORD`: Your password
   - `RECIPIENT`: A valid phone number for testing

### Running an Example

```bash
# Run an example from your project directory
python docs/examples/example_basic.py
```

## Customizing Examples

All examples are designed to be easily customizable:

1. Open the example file in your editor
2. Update the configuration variables at the top
3. Modify the message content or settings as needed
4. Run the script

## Example Structure

Each example follows a consistent structure:

```python
"""
Example description and features demonstrated
"""

import asyncio
# ... imports ...

async def main_function():
    """Main example function."""
    
    # Configuration
    BASE_URL = "..."
    SERVICE_ID = ...
    # ... etc ...
    
    # Setup client
    # ... client setup code ...
    
    # Example code
    # ... demonstration code ...
    
    # Error handling
    try:
        # ... API calls ...
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main_function())
```

## Tips

1. **Start Simple**: Begin with `example_basic.py` to verify your setup works
2. **Test Safely**: Use your own phone number for testing
3. **Read Comments**: Each example includes detailed comments explaining the code
4. **Check Output**: Examples print detailed information about the API responses
5. **Handle Errors**: All examples include error handling patterns

## Common Issues

### Import Errors

If you get import errors, make sure you've installed the client:
```bash
# Install from PyPI
pip install puzzel-sms-gateway-client
# or
uv pip install puzzel-sms-gateway-client
```

### Connection Errors

Check that:
- Your `BASE_URL` is correct
- You have network access to the SMS Gateway server
- The server is running and accessible

### Authentication Errors

Verify that:
- Your `SERVICE_ID`, `USERNAME`, and `PASSWORD` are correct
- Your account has permission to send SMS

### Phone Number Format

Phone numbers must:
- Include country code (e.g., `+47` for Norway)
- Be in format: `+[country code][number]`
- Example: `+47xxxxxxxxx`

## Next Steps

After running the examples:

1. Review the [04 - Complete Examples Documentation](../04-examples.md) for more use cases
2. Check the [05 - API Models Reference](../05-models.md) for detailed model information
3. Explore [06 - Advanced Topics](../06-advanced.md) for production patterns
4. Read the [03 - Quick Reference](../03-quick-reference.md) for common operations

## Need Help?

- Check the [02 - Getting Started Guide](../02-getting-started.md)
- Review the [Main README](../../README.md)
- Contact Puzzel support

## Contributing

If you create a useful example, consider:
1. Following the existing code style
2. Adding detailed comments
3. Including error handling
4. Documenting what the example demonstrates
