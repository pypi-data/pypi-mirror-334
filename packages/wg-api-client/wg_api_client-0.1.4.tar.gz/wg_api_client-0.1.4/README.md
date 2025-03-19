# WireGuard Configuration API Client

A comprehensive client library and CLI tool for interacting with the WireGuard Configuration Distribution API.

[![CI](https://github.com/tiiuae/wg-api-client-lib/actions/workflows/ci.yml/badge.svg)](https://github.com/tiiuae/wg-api-client-lib/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/wg-api-client.svg)](https://pypi.org/project/wg-api-client/)

## Features

- Complete API client for the WireGuard Configuration Distribution API
- Command-line interface for all API operations
- Automatic token authentication and renewal
- Configuration file support
- WireGuard keypair generation
- WireGuard configuration file creation
- Hardware-based device ID generation for reliable device identification

## Installation

### From PyPI (Recommended)

```bash
pip install wg-api-client
```

### From Source

```bash
git clone https://github.com/tiiuae/wg-api-client-lib.git
cd wg-api-client-lib
pip install -e .
```

### Prerequisites for Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-pip wireguard-tools
```

## Usage

### As a Command-Line Tool

The package installs a `wg-api-client` command that can be used to interact with the API:

```bash
# Show help
wg-api-client --help

# Authenticate with the API
wg-api-client auth

# Get a WireGuard configuration (device ID is automatically generated from hardware information)
wg-api-client get-config --output mydevice.conf
```

### As a Library

```python
from wg_api_client import WireGuardAPI, WireGuardHelper
from wg_api_client.unique_id import get_unique_device_id

# Initialize the API client
api = WireGuardAPI(
    api_url="http://20.46.55.161:8080/api/v1",
    hashed_credential="your-hashed-credential"
)

# Authenticate
success, _ = api.authenticate()
if success:
    # Generate a device ID based on hardware information
    device_id = get_unique_device_id()
    
    # Generate a keypair
    private_key, public_key = WireGuardHelper.generate_keypair()
    
    # Request a configuration
    success, config_data = api.request_wireguard_config(
        device_id=device_id,
        role="drone",
        public_key=public_key
    )
    
    if success:
        # Create a configuration file
        WireGuardHelper.create_client_config(config_data, "device.conf")
```

## Configuration

The tool stores configuration in `~/.wg_api_config` by default. You can specify a different location with the `--config-file` parameter.

## Available Commands

### Global Parameters

These parameters can be used with any command:

- `--api-url`: Base URL for the API (default: http://20.46.55.161:8080/api/v1)
- `--hashed-credential`: Hashed credential for authentication
- `--config-file`: Path to configuration file (default: ~/.wg_api_config)

### Authentication

```bash
wg-api-client auth
```

This will:
- Authenticate with the API using the hashed credential
- Store the JWT token in the configuration file
- Store the refresh token for automatic token renewal

### Device Configuration Management

#### Get WireGuard Configuration

```bash
wg-api-client get-config [--role {drone|fmo}] [--public-key KEY] [--output FILE]
```

Parameters:
- `--role`: Device role - either "drone" or "fmo" (default: "drone")
- `--public-key`: WireGuard public key (if not provided, a new keypair will be generated)
- `--output`: Output configuration file (default: "wg.conf")

Examples:

```bash
# Generate a new keypair and configuration with hardware-based device ID
wg-api-client get-config

# Set role to FMO and use an existing public key
wg-api-client get-config --role fmo --public-key "AbCdEf123..." --output fmo.conf
```

#### List All Devices (Admin only)

```bash
wg-api-client list-devices
```

This will display detailed information about all devices, including:
- Device ID
- Role
- IP address
- Public key
- Creation and update timestamps

#### Get Device Information (Admin only)

```bash
wg-api-client get-device DEVICE_ID
```

#### Delete a Device (Admin only)

```bash
wg-api-client delete-device DEVICE_ID
```

#### Delete All Devices (Admin only)

```bash
wg-api-client delete-all-devices [--confirm]
```

Use the `--confirm` flag to bypass the confirmation prompt.

### FMO-specific Operations

#### Get FMO Device Information (Admin only)

```bash
wg-api-client get-fmo
```

#### Remove FMO Role (Admin only)

```bash
wg-api-client delete-fmo
```

### Credential Management (Admin only)

#### Add a New Credential

```bash
wg-api-client add-credential --hashed-credential HASH [--role {user|admin}]
```

Parameters:
- `--hashed-credential`: Hashed credential to add (required)
- `--role`: Role for the credential - either "user" or "admin" (default: "user")

## Examples of Common Workflows

### Setting Up a New Drone Device

```bash
# Authenticate with the API
wg-api-client auth

# Generate a WireGuard configuration with hardware-based device ID
wg-api-client get-config --output drone.conf

# Transfer the generated configuration file to the device and apply it using the WireGuard tools
```

### Setting Up an FMO Device

```bash
# Authenticate with the API
wg-api-client auth

# Check if there's already an FMO device
wg-api-client get-fmo

# If needed, remove the current FMO role
wg-api-client delete-fmo

# Generate a WireGuard configuration for the new FMO device
wg-api-client get-config --role fmo --output fmo.conf
```

### Administrator Tasks

```bash
# Check all registered devices
wg-api-client list-devices

# Add a new admin credential
wg-api-client add-credential --hashed-credential "your-hashed-credential" --role admin

# Clean up old devices
wg-api-client delete-device old-device-id
```

## Device ID Generation

The client generates a unique device ID based on hardware information. The ID generation follows this priority:

1. eth0 MAC address (on Linux systems)
2. Primary network interface MAC address
3. Any available physical network interface MAC address
4. MAC address from uuid.getnode()
5. Machine UUID from OS-specific sources
6. Fallback to machine-specific information

This ensures each device gets a stable, unique identifier that persists across reboots and reinstallations of the software.

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/tiiuae/wg-api-client-lib.git
cd wg-api-client-lib

# Install development dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

### Run Tests

```bash
pytest
```

### Run Linters

```bash
# Format code with Black
black .

# Sort imports
isort .

# Check with pylint
pylint wg_api_client

# Check with mypy
mypy wg_api_client

# Security check with bandit
bandit -r wg_api_client
```

## Publishing

This package is available on PyPI and can be automatically published through GitHub releases.

### Automatic Publishing

1. Update version numbers in:
   - `wg_api_client/__init__.py` (`__version__` variable)
   - `setup.py` (`version` parameter)

2. Create a new GitHub release:
   - Go to the GitHub repository
   - Click "Releases" → "Create a new release"
   - Tag version should be in format `v{version}` (e.g., `v0.1.2`)
   - The GitHub Action will automatically build and publish to PyPI

### Manual Publishing

For detailed instructions on manual publishing, see [PUBLISHING.md](PUBLISHING.md).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.