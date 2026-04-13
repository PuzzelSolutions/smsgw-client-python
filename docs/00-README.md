# Documentation Index

Welcome to the Puzzel SMS Gateway Python Client (Kiota) documentation.

## Getting Started

Start here if you're new to the client:

1. **[Main README](../README.md)** - Overview, installation, and quick start guide
2. **[01 - uv Setup Guide](01-uv-setup.md)** - Complete guide for setting up with uv (recommended)
3. **[02 - Getting Started Guide](02-getting-started.md)** - Step-by-step guide for beginners
4. **[03 - Quick Reference](03-quick-reference.md)** - Cheat sheet for common operations
5. **[Basic Example](examples/example_basic.py)** - Simple SMS sending example

## Documentation

### Setup and Installation

- **[01 - uv Setup Guide](01-uv-setup.md)** - Complete guide for setting up with uv (recommended)
  - Installation and project creation
  - Virtual environment management
  - Common commands and best practices
  - Troubleshooting

- **[02 - Getting Started Guide](02-getting-started.md)** - Step-by-step guide for beginners
  - Send your first SMS in 5 minutes
  - Common issues and troubleshooting
  - Complete working examples

### Quick References

- **[03 - Quick Reference Guide](03-quick-reference.md)** - Quick lookup for common operations
  - Common code snippets
  - Status codes
  - Model hierarchy
  - Best practices

### Core Documentation

- **[04 - Usage Examples](04-examples.md)** - Comprehensive code examples covering all features
  - Basic message sending
  - Message settings and configuration
  - Batch operations
  - Advanced use cases
  - Error handling
  - Production patterns

- **[05 - API Models Reference](05-models.md)** - Detailed documentation of all data models
  - Request and response models
  - Message models
  - Settings models
  - Batch models
  - Error models
  - Enums

- **[06 - Advanced Topics](06-advanced.md)** - Deep dive into advanced features
  - Architecture overview
  - Request adapters
  - Authentication
  - Middleware
  - Timeout and retry configuration
  - Performance optimization
  - Security best practices
  - Monitoring and observability
  - Troubleshooting

- **[07 - Testing Guide](07-testing.md)** - Running and writing tests
  - Running the test suite with uv
  - Coverage reporting
  - Test structure overview
  - What is tested (client, models, request builders)
  - Shared fixtures reference
  - Writing sync, async, and parametrized tests

- **[08 - Publishing Guide](08-publishing.md)** - Publishing the package to PyPI with uv
  - Bumping the version
  - Building wheel and sdist with `uv build`
  - Publishing to TestPyPI for validation
  - Publishing to PyPI with `uv publish`
  - Storing credentials securely

## Example Files

Practical examples you can run directly (located in `docs/examples/`):

- **[example_basic.py](examples/example_basic.py)** - Send a simple SMS
- **[example_advanced.py](examples/example_advanced.py)** - Send SMS with all configuration options
- **[example_multiple_recipients.py](examples/example_multiple_recipients.py)** - Send to multiple recipients
- **[example_batch_management.py](examples/example_batch_management.py)** - Manage message batches

## Documentation Structure

```
Python/
├── README.md                          # Main documentation
├── docs/
│   ├── 00-README.md                   # This file - Documentation index
│   ├── 01-uv-setup.md                 # uv setup guide
│   ├── 02-getting-started.md          # Getting started guide
│   ├── 03-quick-reference.md          # Quick reference guide
│   ├── 04-examples.md                 # Comprehensive examples
│   ├── 05-models.md                   # API models reference
│   ├── 06-advanced.md                 # Advanced topics
│   ├── 07-testing.md                  # Testing guide
│   ├── 08-publishing.md               # Publishing guide
│   └── examples/                      # Example code files
│       ├── README.md                  # Examples guide
│       ├── example_basic.py           # Basic example
│       ├── example_advanced.py        # Advanced example
│       ├── example_multiple_recipients.py  # Multiple recipients
│       └── example_batch_management.py     # Batch management
└── src/                               # Generated Kiota client code
    ├── mt_http_client.py              # Main client
    ├── models/                        # Data models
    ├── gw/                            # Gateway endpoints
    ├── management/                    # Management endpoints
    └── ...
```

## Common Tasks

### Sending Messages

- [Send a simple SMS](04-examples.md#send-a-single-sms)
- [Send to multiple recipients](04-examples.md#send-multiple-sms-messages)
- [Send personalized messages](04-examples.md#send-personalized-messages)
- [Schedule messages](04-examples.md#scheduled-messages-with-send-window)
- [Set custom sender ID](04-examples.md#custom-originator)
- [Send premium SMS](04-examples.md#premium-sms-with-gas-settings)

### Batch Management

- [List all batches](04-examples.md#list-all-batches)
- [Get batch details](04-examples.md#get-batch-details)
- [Stop a batch](04-examples.md#stop-a-batch)
- [Monitor batch status](04-examples.md#monitor-batch-status)

### Configuration

- [Client setup](06-advanced.md#request-adapters)
- [Authentication](06-advanced.md#authentication)
- [Timeout configuration](06-advanced.md#timeout-and-retry-configuration)
- [Custom headers](06-advanced.md#custom-headers-and-configuration)

### Error Handling

- [Basic error handling](04-examples.md#comprehensive-error-handling)
- [Retry logic](04-examples.md#retry-logic-with-exponential-backoff)
- [Input validation](04-examples.md#validation-before-sending)

### Testing

- [Running the test suite](07-testing.md#running-tests)
- [Test structure](07-testing.md#test-structure)
- [Available fixtures](07-testing.md#fixtures)
- [Writing new tests](07-testing.md#writing-new-tests)

### Production

- [Performance optimization](06-advanced.md#performance-optimization)
- [Security best practices](06-advanced.md#security-best-practices)
- [Monitoring](06-advanced.md#monitoring-and-observability)
- [Troubleshooting](06-advanced.md#troubleshooting)

## API Reference

### Main Components

- **MtHttpClient** - Main entry point for the SDK
- **GatewayRequest** - Request object for sending messages
- **Message** - Individual SMS message
- **Settings** - Message configuration options
- **GatewayResponse** - Response from send operations

### Endpoints

- `client.gw.rs.send_messages` - Send messages
- `client.management` - Batch management operations

For detailed API reference, see [05 - API Models Reference](05-models.md).

## Migration Guide

If you're migrating from the previous version (v2.x), see the [Migration Guide](../README.md#migration-from-v2x) in the main README.

Key differences:
- Fully asynchronous (requires async/await)
- Credentials in request instead of client
- Fluent, path-based API
- Type-safe dataclass models

## Support and Resources

- **Main Documentation**: [README.md](../README.md)
- **Puzzel Website**: [www.puzzel.com](https://www.puzzel.com)
- **SMS Gateway Documentation**: Contact Puzzel support

## Quick Links

### For Beginners

1. [01 - uv Setup Guide](01-uv-setup.md) - Set up your development environment
2. [Installation](../README.md#installation) - Install the client
3. [02 - Getting Started Guide](02-getting-started.md) - Send your first SMS
4. [Quick Start](../README.md#quick-start) - Quick code example
5. [Basic Example](examples/example_basic.py) - Runnable example
6. [03 - Quick Reference](03-quick-reference.md) - Common operations cheat sheet

### For Developers

1. [04 - Usage Examples](04-examples.md)
2. [05 - API Models](05-models.md)
3. [06 - Advanced Topics](06-advanced.md)
4. [07 - Testing Guide](07-testing.md)
5. [08 - Publishing Guide](08-publishing.md)

### For Production

1. [Security Best Practices](06-advanced.md#security-best-practices)
2. [Performance Optimization](06-advanced.md#performance-optimization)
3. [Monitoring](06-advanced.md#monitoring-and-observability)
4. [Troubleshooting](06-advanced.md#troubleshooting)

## Maintenance

### Keeping Documentation Updated

When the API changes:

1. Update [05-models.md](05-models.md) with new or changed models
2. Add examples to [04-examples.md](04-examples.md)
3. Update [03-quick-reference.md](03-quick-reference.md) snippets
4. Add migration notes to [README.md](../README.md) if needed

### Adding New Examples

New examples should:

1. Be placed in [docs/examples/](examples/) as `example_*.py`
2. Be referenced in this index under [Example Files](#example-files)
3. Include detailed comments
4. Follow the existing style

## Contributing

For issues, questions, or contributions, please contact Puzzel support.

## License

Released under the MIT license. See [LICENSE](../LICENSE) for details.

---

**Last Updated**: March 2026  
**Version**: 3.0 (Kiota-generated)
