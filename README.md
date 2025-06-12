# strands-tutorial-log-opentelemetry

A Python project built with the Strands Agents framework for creating an AI agent with custom tools and logging capabilities.

## Overview

This project demonstrates how to create an AI agent using the Strands Agents framework. The agent is equipped with several tools including a calculator, current time retriever, Python REPL, and a custom letter counter tool. It also includes comprehensive logging of agent interactions and debug information.

## Features

- AI agent with multiple tools
- Custom tool implementation (letter counter)
- Comprehensive logging system
- Composite callback handler for both console output and file logging

## Project Structure

- `agent.py` - Main agent implementation
- `composite_callback_handler.py` - Custom logging handler with OpenTelemetry integration
- `telemetry_config.py` - OpenTelemetry configuration for S3 logging
- `requirements.txt` - Project dependencies
- `agent_interactions.log` - Log of agent interactions
- `agent_debug.log` - Debug information log
- S3 bucket - Remote storage for logs via OpenTelemetry

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the agent with:

```bash
python agent.py
```

The agent can:
1. Tell the current time
2. Perform calculations
3. Count specific letters in words
4. Execute Python code through a REPL

## Custom Tools

### Letter Counter
Counts occurrences of a specific letter in a word:

```python
letter_counter("strawberry", "r")  # Returns 2
```

## Logging

The project implements a comprehensive logging system with multiple components:

### Logging Architecture
- **CompositeCallbackHandler**: Combines console output, file logging, and S3 logging
  - Uses the standard `PrintingCallbackHandler` for user-facing output
  - Implements custom `FileLoggingHandler` for detailed logging to files
  - Integrates with OpenTelemetry for shipping logs to S3

### Log Files
- `agent_interactions.log` - Records all agent interactions including:
  - Tool invocations with inputs and sequence numbers
  - Agent reasoning text
  - Complete interaction data
  - Timestamps for all events

- `agent_debug.log` - Contains detailed debug information:
  - Strands framework internal logs
  - Debug-level information for troubleshooting
  - Formatted with timestamp, level, logger name, and message

- **S3 Logs** - Stored in the configured S3 bucket:
  - Organized with timestamps and prefixes
  - Contains the same information as local logs
  - Enables centralized log storage and analysis

### OpenTelemetry Integration
- Uses OpenTelemetry for distributed tracing and logging
- Creates spans for agent interactions and tool usage
- Provides context for understanding agent behavior
- Enables integration with other observability tools

### Implementation Details
- Uses Python's built-in `logging` module
- Custom S3LogHandler for direct S3 uploads
- Buffered logging to reduce API calls
- Tool usage tracking with sequential numbering
- Separate handlers for different log destinations

## Dependencies

- strands-agents >= 0.1.0
- strands-agents-tools >= 0.1.0
- opentelemetry-api >= 1.18.0
- opentelemetry-sdk >= 1.18.0
- opentelemetry-exporter-otlp >= 1.18.0
- boto3 >= 1.28.0

## AWS Configuration

To use the S3 logging functionality:

1. Ensure AWS credentials are properly configured:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=your_region
   ```

2. Create an S3 bucket for logs:
   ```bash
   aws s3api create-bucket --bucket your-s3-bucket-name --region your-region
   ```

3. Update the bucket name in `agent.py`:
   ```python
   CompositeCallbackHandler("agent_interactions.log", "your-s3-bucket-name")
   ```