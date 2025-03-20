# Chat Agent CLI

A personal chat agent that interfaces with Together AI through the AirTrain module. This CLI application allows you to have conversations with AI models and stores your chat history locally.

## Features

- Interactive chat with AI powered by Together AI
- Local storage of chat history
- Easy-to-use command-line interface
- Session management (start new chats, continue previous ones)

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/your-repo/airtrain.git
cd airtrain/examples/apps/cli/trmx_agent

# Install the package
pip install -e .
```

### From PyPI

```bash
pip install trmx
```

## Usage

After installation, you can use the chat agent with the following commands:

```bash
# Start a new chat session
trmx

# List previous chat sessions
trmx --list

# Continue a previous session (multiple ways):
trmx 92f31c          # Using a partial session ID directly
trmx 92              # Even just a few characters will work
trmx --continue 92   # Using the --continue or -c flag
trmx -c 92           # Short form

# Show storage info
trmx --info

# Show help
trmx --help

# Show version
trmx --version

# List available providers
trmx --list-providers

# List available models for the current provider
trmx --list-models

# List models for a specific provider
trmx --list-models --provider openai

# Set a specific provider and model for a single chat session
trmx --provider fireworks --model fireworks/deepseek-r1

# Configure a new provider/model as the default
trmx --add --provider openai --model gpt-4
```

## Configuration

The chat agent can be configured using environment variables:

- `TRMX_DIR`: Path to store chat history, credentials, and configuration (default: `~/.trmx`)
- Various API keys like `TOGETHER_API_KEY`, `OPENAI_API_KEY`, etc. for the providers you want to use

You can set these in your shell or create a `.env` file in your working directory.

Credentials are loaded in the following order:
1. From environment variables
2. From the credentials files in `~/.trmx/credentials/`
3. If not found, the CLI will prompt you to enter your API key and offer to save it

## Requirements

- Python 3.8 or higher
- airtrain package
- Internet connection for AI model access 