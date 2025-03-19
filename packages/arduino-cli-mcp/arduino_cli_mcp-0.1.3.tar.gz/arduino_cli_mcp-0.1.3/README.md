# Arduino CLI MCP

Arduino CLI MCP is a server that provides Arduino CLI integration for VSCode and Claude, allowing you to compile and upload Arduino sketches through the Arduino CLI.

## Overview

Arduino CLI MCP provides a wrapper for Arduino CLI that simplifies workflows through features such as auto-approval of repetitive operations. This tool is particularly useful for developers and educators who frequently work with Arduino projects.

## Introduction to Model Context Protocol (MCP)

Model Context Protocol (MCP) is an open protocol specifically designed to enable Large Language Models (LLMs) to seamlessly integrate with external data sources and tools. Whether you're developing an AI IDE, enhancing chat interfaces, or building automated AI workflows, MCP provides a standardized way to connect LLMs with the context they need. Through MCP, the Arduino CLI MCP server can interact with various AI models, handling Arduino-related operations and commands.

## Installation

```bash
pip install arduino-cli-mcp
```

After installation, you can run it with the following command:

```bash
python -m arduino_cli_mcp
```

## Prerequisites

- Arduino CLI installed and available in PATH
- Python 3.11+
- Working directory with appropriate file permissions

## Configuration

The tool can be configured using JSON format as follows:

```json
"github.com/arduino-cli-mcp": {
  "command": "python",
  "args": [
    "/Users/oliver/code/mcp/arduino-cli-mcp/main.py",
    "--workdir",
    "/Users/oliver/Documents/Cline/MCP/arduino-cli-mcp"
  ],
  "disabled": false,
  "autoApprove": [
    "upload",
    "compile",
    "install_board"
  ]
}
```

### Configuration Options

- `command`: The command to execute (Python in this case)
- `args`: List of arguments passed to the command
  - First argument is the path to the main script
  - `--workdir` specifies the working directory for Arduino CLI operations
- `disabled`: Enable/disable the tool (set to `false` to enable)
- `autoApprove`: List of Arduino CLI operations that can be auto-approved without user confirmation
  - Supported operations: `upload`, `compile`, `install_board`

### Configuration for Claude.app

Add the following to your Claude settings:

```json
"mcpServers": {
  "arduino": {
    "command": "python",
    "args": ["-m", "arduino_cli_mcp"]
  }
}
```

### Configuration for Zed

Add the following to your Zed settings.json file:

```json
"context_servers": {
  "arduino-cli-mcp": {
    "command": "python",
    "args": ["-m", "arduino_cli_mcp"]
  }
},
```

### Custom Configuration - Arduino CLI Path

By default, the server looks for Arduino CLI in the system PATH. You can specify a custom path by adding the `--arduino-cli-path` parameter to the `args` list in your configuration.

Example:

```json
{
  "command": "python",
  "args": ["-m", "arduino_cli_mcp", "--arduino-cli-path=/path/to/arduino-cli"]
}
```

## Usage

Start the MCP server:

```bash
arduino-cli-mcp --workdir /path/to/your/arduino/projects
```

Once configured, the tool will automatically handle Arduino CLI commands, with special handling for operations listed in the `autoApprove` section.

## Arduino CLI MCP Server

This is a Model Context Protocol server that provides Arduino CLI functionality. The server enables large language models to interact with Arduino boards through natural language commands, compile sketches, upload firmware, and manage libraries.

### Available Tools

- `list_boards` - Lists all connected Arduino boards.

  - No parameters required

- `compile_sketch` - Compiles an Arduino sketch.

  - Required parameters:
    - `sketch_path` (string): Path to the sketch file
    - `board_fqbn` (string): Fully qualified board name (e.g., 'arduino:avr:uno')

- `upload_sketch` - Uploads a compiled sketch to a board.

  - Required parameters:
    - `sketch_path` (string): Path to the sketch file
    - `board_fqbn` (string): Fully qualified board name
    - `port` (string): Upload port (e.g., '/dev/ttyACM0', 'COM3')

- `search_library` - Searches for Arduino libraries.

  - Required parameters:
    - `query` (string): Search term

- `install_library` - Installs an Arduino library.

  - Required parameters:
    - `library_name` (string): Name of the library to install

## Interaction Examples

1. Listing connected boards:

```json
{
  "name": "list_boards",
  "arguments": {}
}
```

Response:

```json
{
  "boards": [
    {
      "port": "COM3",
      "fqbn": "arduino:avr:uno",
      "name": "Arduino Uno"
    },
    {
      "port": "COM4",
      "fqbn": "arduino:avr:nano",
      "name": "Arduino Nano"
    }
  ]
}
```

2. Compiling a sketch:

```json
{
  "name": "compile_sketch",
  "arguments": {
    "sketch_path": "/path/to/Blink.ino",
    "board_fqbn": "arduino:avr:uno"
  }
}
```

Response:

```json
{
  "success": true,
  "output": "Sketch uses 924 bytes (2%) of program storage space. Maximum is 32256 bytes.",
  "binary_path": "/path/to/build/arduino.avr.uno/Blink.ino.hex"
}
```

3. Error response example:

```json
{
  "error": true,
  "message": "Compilation failed: Syntax error on line 5",
  "details": "Missing semicolon at the end of statement"
}
```

## Debugging

You can use the MCP inspector tool to debug the server:

```bash
npx @modelcontextprotocol/inspector python -m arduino_cli_mcp
```

## Example Questions for Claude

1. "What Arduino boards are currently connected to my computer?"
2. "Compile my Blink sketch for Arduino Uno"
3. "Upload my LED project to the Arduino Mega on COM5 port"
4. "Can you search for libraries related to OLED displays?"
5. "Install the Servo library for Arduino"

## Features

- Compile Arduino sketches
- Upload sketches to Arduino boards
- Install Arduino platforms
- List available boards and platforms
- Create and manage Arduino projects
- Search and install libraries

## Contributing

We encourage you to contribute to arduino-cli-mcp to help expand and improve it. Whether you want to add new Arduino-related tools, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see:
https://github.com/modelcontextprotocol/servers

Pull requests are welcome! Feel free to contribute new ideas, bug fixes, or improvements to make arduino-cli-mcp more powerful and useful.

## Related Links

- [Arduino CLI Documentation](https://arduino.github.io/arduino-cli/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

_For the Chinese version, please refer to [README.zh-tw.md](README.zh-tw.md)_
