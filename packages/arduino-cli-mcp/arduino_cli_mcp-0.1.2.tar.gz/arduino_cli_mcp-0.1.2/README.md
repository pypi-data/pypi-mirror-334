# Arduino CLI MCP

Arduino CLI MCP 是一個為 VSCode 和 Claude 提供 Arduino CLI 整合的服務器，可讓您通過 Arduino CLI 編譯和上傳 Arduino 草圖。

## 概述

Arduino CLI MCP 為 Arduino CLI 提供了一個包裝器，通過自動批准重複操作等功能來簡化工作流程。這個工具對於經常使用 Arduino 項目的開發人員和教育工作者特別有用。

## 模型上下文協議 (MCP) 簡介

模型上下文協議 (MCP) 是一種開放協議，專門用於使大型語言模型 (LLM) 能夠與外部數據源和工具無縫集成。無論您是在開發 AI IDE，增強聊天界面，還是構建自動化 AI 工作流程，MCP 都提供了一種標準化的方式來連接 LLM 與它們所需的上下文。通過 MCP，Arduino CLI MCP 服務器可以與各種 AI 模型交互，處理與 Arduino 相關的操作和命令。

## 安裝

```bash
pip install arduino-cli-mcp
```

安裝後，您可以使用以下命令運行：

```bash
python -m arduino_cli_mcp
```

## 先決條件

- Arduino CLI 已安裝並可在 PATH 中使用
- Python 3.11+
- 工作目錄具有適當的文件權限

## 配置

該工具可以使用 JSON 格式配置，如下所示：

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

### 配置選項

- `command`: 要執行的命令（本例中為 Python）
- `args`: 傳遞給命令的參數列表
  - 第一個參數是主腳本的路徑
  - `--workdir` 指定 Arduino CLI 操作的工作目錄
- `disabled`: 啟用/禁用工具（設為 `false` 以啟用）
- `autoApprove`: 可以自動批准而無需用戶確認的 Arduino CLI 操作列表
  - 支持的操作：`upload`, `compile`, `install_board`

### Claude.app 的配置

將以下內容添加到您的 Claude 設置中：

```json
"mcpServers": {
  "arduino": {
    "command": "python",
    "args": ["-m", "arduino_cli_mcp"]
  }
}
```

### Zed 的配置

將以下內容添加到您的 Zed settings.json 文件中：

```json
"context_servers": {
  "arduino-cli-mcp": {
    "command": "python",
    "args": ["-m", "arduino_cli_mcp"]
  }
},
```

### 自定義配置 - Arduino CLI 路徑

默認情況下，服務器在系統 PATH 中查找 Arduino CLI。您可以通過在配置中的 `args` 列表中添加 `--arduino-cli-path` 參數來指定自定義路徑。

示例：

```json
{
  "command": "python",
  "args": ["-m", "arduino_cli_mcp", "--arduino-cli-path=/path/to/arduino-cli"]
}
```

## 使用方法

啟動 MCP 服務器：

```bash
arduino-cli-mcp --workdir /path/to/your/arduino/projects
```

配置完成後，該工具將自動處理 Arduino CLI 命令，並對 `autoApprove` 部分中列出的操作進行特殊處理。

## Arduino CLI MCP 服務器

這是一個提供 Arduino CLI 功能的模型上下文協議服務器。該服務器使大型語言模型能夠通過自然語言命令與 Arduino 板交互，編譯草圖，上傳固件，並管理庫。

### 可用工具

- `list_boards` - 列出所有連接的 Arduino 板。

  - 不需要參數

- `compile_sketch` - 編譯 Arduino 草圖。

  - 必需參數：
    - `sketch_path` (字符串): 草圖文件的路徑
    - `board_fqbn` (字符串): 完全限定板名稱（例如 'arduino:avr:uno'）

- `upload_sketch` - 將編譯好的草圖上傳到板上。

  - 必需參數：
    - `sketch_path` (字符串): 草圖文件的路徑
    - `board_fqbn` (字符串): 完全限定板名稱
    - `port` (字符串): 上傳端口（例如 '/dev/ttyACM0'，'COM3'）

- `search_library` - 搜索 Arduino 庫。

  - 必需參數：
    - `query` (字符串): 搜索詞

- `install_library` - 安裝 Arduino 庫。

  - 必需參數：
    - `library_name` (字符串): 要安裝的庫的名稱

## 交互示例

1. 列出連接的板：

```json
{
  "name": "list_boards",
  "arguments": {}
}
```

回應：

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

2. 編譯草圖：

```json
{
  "name": "compile_sketch",
  "arguments": {
    "sketch_path": "/path/to/Blink.ino",
    "board_fqbn": "arduino:avr:uno"
  }
}
```

回應：

```json
{
  "success": true,
  "output": "Sketch uses 924 bytes (2%) of program storage space. Maximum is 32256 bytes.",
  "binary_path": "/path/to/build/arduino.avr.uno/Blink.ino.hex"
}
```

3. 錯誤回應示例：

```json
{
  "error": true,
  "message": "Compilation failed: Syntax error on line 5",
  "details": "Missing semicolon at the end of statement"
}
```

## 調試

您可以使用 MCP inspector 工具來調試服務器：

```bash
npx @modelcontextprotocol/inspector python -m arduino_cli_mcp
```

## Claude 的示例問題

1. "目前有哪些 Arduino 板連接到我的電腦？"
2. "為 Arduino Uno 編譯我的 Blink 草圖"
3. "將我的 LED 項目上傳到 COM5 端口上的 Arduino Mega"
4. "您能搜索與 OLED 顯示相關的庫嗎？"
5. "為 Arduino 安裝 Servo 庫"

## 功能

- 編譯 Arduino 草圖
- 上傳草圖到 Arduino 板
- 安裝 Arduino 平台
- 列出可用的板和平台
- 創建和管理 Arduino 項目
- 搜索和安裝庫

## 貢獻

我們鼓勵您為 arduino-cli-mcp 做出貢獻，以幫助擴展和改進它。無論您是想添加新的 Arduino 相關工具，增強現有功能，還是改進文檔，您的投入都是有價值的。

有關其他 MCP 服務器和實現模式的示例，請參見：
https://github.com/modelcontextprotocol/servers

歡迎提交拉取請求！隨時貢獻新想法，錯誤修復或改進，使 arduino-cli-mcp 更強大和有用。

## 相關鏈接

- [Arduino CLI 文檔](https://arduino.github.io/arduino-cli/)

## 許可證

此項目根據 MIT 許可證授權 - 詳情請參見 LICENSE 文件。

---

_對於英文版本，請參考 [README.md](README.md)_
