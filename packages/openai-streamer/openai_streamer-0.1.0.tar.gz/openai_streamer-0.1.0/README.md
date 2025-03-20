# OpenAI Streamer

A Python package for streaming text completion using OpenAI's Responses API.

## Installation

You can install the package directly from the source:

```bash
# Activate your conda environment
conda activate OpenRAPI

# Install the package in development mode
pip install -e .
```

Or you can build and install the package:

```bash
# Activate your conda environment
conda activate OpenRAPI

# Build the package
python setup.py sdist bdist_wheel

# Install the package
pip install dist/openai_streamer-0.1.0-py3-none-any.whl
```

## Usage

### Basic Usage

```python
from openai_streamer.streamer import stream_completion

# Simple example
prompt = "Write a short poem about artificial intelligence."
instructions = "You are a creative poet with a technical background."

response = stream_completion(prompt, instructions=instructions)
```

### Using the Class

```python
from openai_streamer.streamer import OpenAIStreamer

# Create an instance
streamer = OpenAIStreamer()

# Generate a completion
prompt = "Explain quantum computing in simple terms."
instructions = "You are a science educator explaining complex topics to beginners."

response = streamer.stream_completion(prompt, instructions=instructions)
```

## Configuration

The package uses environment variables for configuration. Create a `.env` file in your project root with:

```
OPENAI_API_KEY=your_api_key_here
```

## Requirements

- Python 3.8+
- openai>=1.0.0
- python-dotenv>=0.19.0

## License

MIT
