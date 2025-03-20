# Commit Message CLI

A command-line tool to generate commit messages using AI.

## Prerequisites

This tool requires an active smoothdev.io subscription to use. When you first run the tool, it will initiate a device flow authentication process:

1. The tool will display a URL and a device code
2. Visit the URL in your browser
3. Sign in to your smoothdev.io account
4. Enter the device code to authenticate
5. The tool will save the authentication token for future use

If you don't have a smoothdev.io account:

1. Visit [app.smoothdev.io](https://app.smoothdev.io) to create an account
2. Subscribe to a plan that includes the commit message generator
3. Once your subscription is active, you can use this CLI tool

## Installation

### Using pip

```bash
pip install commit-message-cli
```

### Using Homebrew

```bash
brew install commit-message-cli
```

## Configuration

The tool can be configured in two ways:

### 1. Environment Variables

Set the following environment variables to configure the tool:

```bash
export SMOOTHDEV_AUTH0_DOMAIN="your-domain"
export SMOOTHDEV_AUTH0_CLIENT_ID="your-client-id"
export SMOOTHDEV_AUTH0_AUDIENCE="your-audience"
export SMOOTHDEV_REDIRECT_URI="your-redirect-uri"
```

### 2. Configuration File

You can create a configuration file at `~/.smoothdevio/config.json`. A template is provided in `config.template.json`:

1. Create your configuration directory:

```bash
mkdir -p ~/.smoothdevio
```

2. Copy the template:

```bash
cp config.template.json ~/.smoothdevio/config.json
```

3. Edit the configuration file with your settings:

```json
{
  "aws_profile": "default",
  "aws_region": "us-east-1",
  "auth0_domain": "your-domain",
  "auth0_audience": "your-audience",
  "redirect_uri": "your-redirect-uri"
}
```

Note: Environment variables take precedence over the configuration file.

## Usage

```bash
generate-commit-message [options]
```

For more details on usage and options, run:

```bash
generate-commit-message --help
```
