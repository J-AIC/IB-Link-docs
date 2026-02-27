# LlamaServerAPI - Usage Examples

Complete guide with practical examples for all LlamaServerAPI endpoints.

**Base URL**: `http://localhost:9000/iblink/v1/llama-server`

---

## Table of Contents

- [Server Management](#server-management)
  - [Start Server](#post-start)
  - [Stop Server](#post-stop)
  - [Get Status](#get-status)
  - [Switch Model](#post-switch-model)
- [Model Management](#model-management)
  - [List Models](#get-models)
  - [Delete Model](#delete-models)
- [Model Download](#model-download)
  - [Search Models](#post-modelssearch)
  - [Get Model Info](#get-modelsinfo)
  - [Download Model](#post-modelsdownload)
  - [Download Model with Progress](#post-modelsdownload-stream)
- [Binary Management](#binary-management)
  - [List Binaries](#get-binaries)
  - [Get Binary Info](#get-binariesinfo)
  - [Set Active Binary](#post-binariesset)
- [Configuration](#configuration)
  - [Get API Info](#get-info)
  - [Update Configuration](#post-config)
- [Monitoring](#monitoring)
  - [Get Logs](#get-logs)
  - [Stream Logs](#get-logsstream)
  - [Health Check](#get-health)

---

## Server Management

### POST /start

Start llama-server with a specified model.

#### Basic Start

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\Qwen3-0.6B-Q4_K_M.gguf",
    "port": 8080
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_path = "C:\Models\Qwen3-0.6B-Q4_K_M.gguf"
    port = 8080
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/start" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully started llama-server with Qwen3-0.6B-Q4_K_M.gguf",
  "port": 8080,
  "model": "Qwen3-0.6B-Q4_K_M.gguf",
  "endpoint": "http://localhost:8080/v1"
}
```

#### Start with Specific Binary

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\model.gguf",
    "binary_path": "C:\\llama-cpp\\x64\\llama-server.exe",
    "port": 8080
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_path = "C:\Models\model.gguf"
    binary_path = "C:\llama-cpp\x64\llama-server.exe"
    port = 8080
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/start" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Start with Custom Options

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\model.gguf",
    "port": 8080,
    "options": {
      "n_gpu_layers": 99,
      "ctx_size": 4096,
      "n_threads": 8,
      "batch_size": 512
    }
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_path = "C:\Models\model.gguf"
    port = 8080
    options = @{
        n_gpu_layers = 99
        ctx_size = 4096
        n_threads = 8
        batch_size = 512
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/start" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully started llama-server with model.gguf",
  "port": 8080,
  "model": "model.gguf",
  "endpoint": "http://localhost:8080/v1"
}
```

---

### POST /stop

Stop the running llama-server instance.

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/stop
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/stop" `
    -Method POST
```

**Response:**
```json
{
  "success": true,
  "message": "Server stopped successfully"
}
```

---

### GET /status

Get current server status and health information.

**cURL:**
```bash
curl http://localhost:9000/iblink/v1/llama-server/status
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/status"
```

**Response (Server Running):**
```json
{
  "is_running": true,
  "status": "running",
  "current_model": "Qwen3-0.6B-Q4_K_M.gguf",
  "port": 8080,
  "health": {
    "is_healthy": true,
    "response_time_ms": 45,
    "endpoint": "http://localhost:8080/health",
    "last_check": "2025-01-20T10:30:00Z"
  },
  "last_updated": "2025-01-20T10:30:00Z"
}
```

**Response (Server Stopped):**
```json
{
  "is_running": false,
  "status": "stopped",
  "current_model": null,
  "port": null,
  "health": null,
  "last_updated": "2025-01-20T10:30:00Z"
}
```

---

### POST /switch-model

Switch to a different model (stops current, starts new).

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\Different-Model-Q4_K_M.gguf",
    "binary_path": "C:\\llama-cpp\\x64\\llama-server.exe"
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_path = "C:\Models\Different-Model-Q4_K_M.gguf"
    binary_path = "C:\llama-cpp\x64\llama-server.exe"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/switch-model" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**With Custom Options:**

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\Large-Model-Q6_K.gguf",
    "binary_path": "C:\\llama-cpp\\x64\\llama-server.exe",
    "options": {
      "n_gpu_layers": 99,
      "ctx_size": 8192,
      "n_threads": 8
    }
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_path = "C:\Models\Large-Model-Q6_K.gguf"
    binary_path = "C:\llama-cpp\x64\llama-server.exe"
    options = @{
        n_gpu_layers = 99
        ctx_size = 8192
        n_threads = 8
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/switch-model" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully switched to Different-Model-Q4_K_M.gguf",
  "port": 8080,
  "model": "Different-Model-Q4_K_M.gguf",
  "endpoint": "http://localhost:8080/v1"
}
```

---

## Model Management

### GET /models

List all available GGUF models in the configured directory.

### DELETE /models

Delete a downloaded GGUF model file.

**cURL:**
```bash
curl -X DELETE "http://localhost:9000/iblink/v1/llama-server/models?modelPath=C:\\Models\\model-to-delete.gguf"
```

**PowerShell:**
```powershell
$modelPath = "C:\Models\model-to-delete.gguf"
$encodedPath = [System.Web.HttpUtility]::UrlEncode($modelPath)
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models?modelPath=$encodedPath" -Method DELETE
```

**Response:**
```json
{
  "success": true,
  "message": "Model deleted successfully",
  "deleted_file": "C:\\Models\\model-to-delete.gguf"
}
```

**Error Response (Model in use):**
```json
{
  "error": {
    "message": "Cannot delete model that is currently loaded",
    "type": "conflict_error",
    "code": "model_in_use",
    "details": "Stop the server before deleting the active model"
  }
}
```

---

**cURL:**
```bash
curl http://localhost:9000/iblink/v1/llama-server/models
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models"
```

**Response:**
```json
{
  "models": [
    {
      "name": "Qwen3-0.6B-Q4_K_M",
      "path": "C:\\Models\\Qwen3-0.6B-Q4_K_M.gguf",
      "size_bytes": 487654321,
      "size_formatted": "464.8 MB",
      "is_available": true,
      "metadata": {
        "architecture": "qwen3",
        "quantization": "Q4_K_M",
        "context_length": 40960,
        "embedding_length": 1024,
        "parameters": "596M"
      }
    },
    {
      "name": "Gemma-2-2B-Q4_K_M",
      "path": "C:\\Models\\Gemma-2-2B-Q4_K_M.gguf",
      "size_bytes": 1573424896,
      "size_formatted": "1.47 GB",
      "is_available": true,
      "metadata": {
        "architecture": "gemma2",
        "quantization": "Q4_K_M",
        "context_length": 8192,
        "embedding_length": 2048,
        "parameters": "2.6B"
      }
    }
  ],
  "total_count": 2,
  "models_directory": "C:\\Models"
}
```

---

## Model Download

### POST /models/search

Search for GGUF models on HuggingFace.

#### Search for Gemma Models

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/search \
  -H "Content-Type: application/json" \
  -d '{"query": "gemma gguf"}'
```

**PowerShell:**
```powershell
$body = @{
    query = "gemma gguf"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/search" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Search for Llama Models

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/search \
  -H "Content-Type: application/json" \
  -d '{"query": "llama gguf"}'
```

**PowerShell:**
```powershell
$body = @{
    query = "llama gguf"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/search" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Search for Qwen Models

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/search \
  -H "Content-Type: application/json" \
  -d '{"query": "qwen gguf"}'
```

**PowerShell:**
```powershell
$body = @{
    query = "qwen gguf"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/search" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "models": [
    {
      "id": "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF",
      "name": "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF",
      "author": "ggml-org",
      "downloads": 12345,
      "likes": 89,
      "tags": ["gguf", "gemma", "text-generation"]
    },
    {
      "id": "bartowski/gemma-3-4b-it-GGUF",
      "name": "bartowski/gemma-3-4b-it-GGUF",
      "author": "bartowski",
      "downloads": 8765,
      "likes": 56,
      "tags": ["gguf", "gemma", "instruction-tuned"]
    }
  ],
  "total_count": 2
}
```

---

### GET /models/info

Get detailed information about a HuggingFace model repository.

#### Get Info for Single File Model

**cURL:**
```bash
curl "http://localhost:9000/iblink/v1/llama-server/models/info?repository=ggml-org/gemma-2-2b-it-Q4_K_M-GGUF"
```

**PowerShell:**
```powershell
$repository = "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF"
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/info?repository=$repository"
```

**Response:**
```json
{
  "id": "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF",
  "name": "gemma-2-2b-it-Q4_K_M-GGUF",
  "files": [
    {
      "file_name": "gemma-2-2b-it-Q4_K_M.gguf",
      "file_path": "gemma-2-2b-it-Q4_K_M.gguf",
      "size_bytes": 1573424896,
      "size_formatted": "1.47 GB",
      "is_gguf": true,
      "is_split_part": false
    },
    {
      "file_name": "README.md",
      "file_path": "README.md",
      "size_bytes": 2048,
      "size_formatted": "2.0 KB",
      "is_gguf": false,
      "is_split_part": false
    }
  ],
  "is_split_model": false,
  "split_groups": null,
  "total_size_bytes": 1573426944,
  "total_size_formatted": "1.47 GB"
}
```

#### Get Info for Split Model

**cURL:**
```bash
curl "http://localhost:9000/iblink/v1/llama-server/models/info?repository=TheBloke/Llama-2-70B-GGUF"
```

**PowerShell:**
```powershell
$repository = "TheBloke/Llama-2-70B-GGUF"
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/info?repository=$repository"
```

**Response:**
```json
{
  "id": "TheBloke/Llama-2-70B-GGUF",
  "name": "Llama-2-70B-GGUF",
  "files": [
    {
      "file_name": "llama-2-70b.Q4_K_M-00001-of-00003.gguf",
      "file_path": "llama-2-70b.Q4_K_M-00001-of-00003.gguf",
      "size_bytes": 13404954624,
      "size_formatted": "12.5 GB",
      "is_gguf": true,
      "is_split_part": true
    },
    {
      "file_name": "llama-2-70b.Q4_K_M-00002-of-00003.gguf",
      "file_path": "llama-2-70b.Q4_K_M-00002-of-00003.gguf",
      "size_bytes": 13404954624,
      "size_formatted": "12.5 GB",
      "is_gguf": true,
      "is_split_part": true
    },
    {
      "file_name": "llama-2-70b.Q4_K_M-00003-of-00003.gguf",
      "file_path": "llama-2-70b.Q4_K_M-00003-of-00003.gguf",
      "size_bytes": 13400091136,
      "size_formatted": "12.5 GB",
      "is_gguf": true,
      "is_split_part": true
    }
  ],
  "is_split_model": true,
  "split_groups": [
    {
      "base_name": "llama-2-70b.Q4_K_M",
      "total_parts": 3,
      "total_size_bytes": 40210000384,
      "total_size_formatted": "37.5 GB"
    }
  ],
  "total_size_bytes": 40210000384,
  "total_size_formatted": "37.5 GB"
}
```

---

### POST /models/download

Download one or more GGUF model files from HuggingFace.

#### Download Specific Files

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF",
    "files": ["gemma-2-2b-it-Q4_K_M.gguf"]
  }'
```

**PowerShell:**
```powershell
$body = @{
    repository = "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF"
    files = @("gemma-2-2b-it-Q4_K_M.gguf")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/download" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Download Split Model Parts

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "TheBloke/Llama-2-70B-GGUF",
    "files": [
      "llama-2-70b.Q4_K_M-00001-of-00003.gguf",
      "llama-2-70b.Q4_K_M-00002-of-00003.gguf",
      "llama-2-70b.Q4_K_M-00003-of-00003.gguf"
    ]
  }'
```

**PowerShell:**
```powershell
$body = @{
    repository = "TheBloke/Llama-2-70B-GGUF"
    files = @(
        "llama-2-70b.Q4_K_M-00001-of-00003.gguf",
        "llama-2-70b.Q4_K_M-00002-of-00003.gguf",
        "llama-2-70b.Q4_K_M-00003-of-00003.gguf"
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/download" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Download All GGUF Files

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "unsloth/Qwen3-4B-Instruct-2507-GGUF",
    "download_all_gguf": true
  }'
```

**PowerShell:**
```powershell
$body = @{
    repository = "unsloth/Qwen3-4B-Instruct-2507-GGUF"
    download_all_gguf = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/models/download" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully downloaded 1 files",
  "downloaded_files": [
    {
      "file_name": "gemma-2-2b-it-Q4_K_M.gguf",
      "file_path": "C:\\Users\\user\\.iblink\\Models\\gemma-2-2b-it-Q4_K_M.gguf",
      "size_bytes": 1573424896,
      "is_split_part": false,
      "split_index": null,
      "split_total": null
    }
  ],
  "total_size_bytes": 1573424896,
  "failed_files": []
}
```

---

### POST /models/download-stream

Download model files with real-time progress updates via Server-Sent Events.

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download-stream \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF",
    "files": ["gemma-2-2b-it-Q4_K_M.gguf"]
  }' \
  -N
```

**PowerShell:**
```powershell
$body = @{
    repository = "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF"
    files = @("gemma-2-2b-it-Q4_K_M.gguf")
} | ConvertTo-Json

# Note: PowerShell doesn't handle SSE natively well
# For better experience, use a dedicated SSE client or browser
Invoke-WebRequest -Uri "http://localhost:9000/iblink/v1/llama-server/models/download-stream" `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -TimeoutSec 3600
```

**Response (SSE stream):**
```
data: {"type":"progress","message":"Starting download from repository: ggml-org/gemma-2-2b-it-Q4_K_M-GGUF"}

data: {"type":"progress","message":"Files to download: 1"}

data: {"type":"progress","message":"Total size: 1.47 GB"}

data: {"type":"progress","message":"[1/1] gemma-2-2b-it-Q4_K_M.gguf: 5.2% (Overall: 5.2%) - 12.3 MB/s"}

data: {"type":"progress","message":"[1/1] gemma-2-2b-it-Q4_K_M.gguf: 15.8% (Overall: 15.8%) - 14.7 MB/s"}

data: {"type":"progress","message":"[1/1] gemma-2-2b-it-Q4_K_M.gguf: 52.1% (Overall: 52.1%) - 13.9 MB/s"}

data: {"type":"progress","message":"[1/1] gemma-2-2b-it-Q4_K_M.gguf: 89.3% (Overall: 89.3%) - 12.8 MB/s"}

data: {"type":"progress","message":"[1/1] gemma-2-2b-it-Q4_K_M.gguf: 100.0% (Overall: 100.0%) - 13.5 MB/s"}

data: {"type":"success","message":"Successfully downloaded 1 files","data":{"downloaded_files":[...]}}
```

---

## Binary Management

### GET /binaries

List all available llama-server.exe binaries in the system.

**cURL:**
```bash
curl http://localhost:9000/iblink/v1/llama-server/binaries
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/binaries"
```

**Response:**
```json
{
  "binaries": [
    {
      "name": "llama-server.exe",
      "path": "C:\\llama-cpp\\x64\\llama-server.exe",
      "platform": "Windows",
      "architecture": "x64",
      "size_bytes": 12345678,
      "size_formatted": "11.77 MB",
      "last_modified": "2025-01-20T10:30:00Z",
      "is_executable": true,
      "is_compatible": true,
      "version": "b5502",
      "build_info": "llama.cpp build 5502"
    },
    {
      "name": "llama-server.exe",
      "path": "C:\\llama-cpp\\arm64\\llama-server.exe",
      "platform": "Windows",
      "architecture": "ARM64",
      "size_bytes": 11234567,
      "size_formatted": "10.71 MB",
      "last_modified": "2025-01-20T09:15:00Z",
      "is_executable": true,
      "is_compatible": false,
      "version": "b5502",
      "build_info": "llama.cpp build 5502"
    }
  ],
  "total_count": 2,
  "current_binary": "C:\\llama-cpp\\x64\\llama-server.exe",
  "binaries_directory": "C:\\llama-cpp"
}
```

---

### GET /binaries/info

Get detailed information about a specific binary.

**cURL:**
```bash
curl "http://localhost:9000/iblink/v1/llama-server/binaries/info?binaryPath=C:\\llama-cpp\\x64\\llama-server.exe"
```

**PowerShell:**
```powershell
$binaryPath = "C:\llama-cpp\x64\llama-server.exe"
$encodedPath = [System.Web.HttpUtility]::UrlEncode($binaryPath)
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/binaries/info?binaryPath=$encodedPath"
```

**Response:**
```json
{
  "name": "llama-server.exe",
  "path": "C:\\llama-cpp\\x64\\llama-server.exe",
  "platform": "Windows",
  "architecture": "x64",
  "size_bytes": 12345678,
  "size_formatted": "11.77 MB",
  "last_modified": "2025-01-20T10:30:00Z",
  "is_executable": true,
  "is_compatible": true,
  "version": "b5502",
  "build_info": "llama.cpp build 5502",
  "detailed_info": {
    "supports_gpu": true,
    "supports_cuda": false,
    "supports_metal": false,
    "supports_vulkan": true
  }
}
```

---

### POST /binaries/set

Set the active llama-server binary for future operations.

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/binaries/set \
  -H "Content-Type: application/json" \
  -d '{"binary_path": "C:\\llama-cpp\\x64\\llama-server.exe"}'
```

**PowerShell:**
```powershell
$body = @{
    binary_path = "C:\llama-cpp\x64\llama-server.exe"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/binaries/set" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "message": "Binary configuration updated successfully",
  "binary_path": "C:\\llama-cpp\\x64\\llama-server.exe",
  "platform": "Windows",
  "architecture": "x64",
  "version": "b5502",
  "saved_to": "C:\\Users\\user\\.iblink\\server_settings.json"
}
```

---

## Configuration

### GET /info

Get API configuration and capabilities.

**cURL:**
```bash
curl http://localhost:9000/iblink/v1/llama-server/info
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/info"
```

**Response:**
```json
{
  "server_type": "LlamaServer",
  "version": "1.0.0",
  "configuration": {
    "llama_server_path": "C:\\llama-cpp\\x64\\llama-server.exe",
    "models_directory": "C:\\Users\\user\\.iblink\\Models",
    "default_arguments": "-ngl 99 -c 4096 -t 4 -b 512",
    "default_port": 8080
  },
  "capabilities": [
    "start_server",
    "stop_server",
    "switch_model",
    "health_check",
    "model_discovery",
    "model_download",
    "model_search",
    "log_streaming",
    "conflict_resolution",
    "binary_management"
  ],
  "supported_architectures": ["x64", "ARM64"],
  "supported_quantizations": ["Q4_K_M", "Q4_K_S", "Q5_K_M", "Q6_K", "Q8_0"]
}
```

---

### POST /config

Update server configuration dynamically.

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/config \
  -H "Content-Type: application/json" \
  -d '{
    "llama_server_path": "C:\\llama-cpp\\llama-server.exe",
    "models_directory": "D:\\AI\\Models",
    "default_arguments": "-ngl 99 -c 8192 -t 8 -b 1024"
  }'
```

**PowerShell:**
```powershell
$body = @{
    llama_server_path = "C:\llama-cpp\llama-server.exe"
    models_directory = "D:\AI\Models"
    default_arguments = "-ngl 99 -c 8192 -t 8 -b 1024"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/config" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Partial Update:**

**cURL:**
```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/config \
  -H "Content-Type: application/json" \
  -d '{
    "models_directory": "D:\\AI\\Models"
  }'
```

**PowerShell:**
```powershell
$body = @{
    models_directory = "D:\AI\Models"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/config" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "updated_configuration": {
    "llama_server_path": "C:\\llama-cpp\\llama-server.exe",
    "models_directory": "D:\\AI\\Models",
    "default_arguments": "-ngl 99 -c 8192 -t 8 -b 1024"
  }
}
```

---

## Monitoring

### GET /logs

Get recent server logs (last N entries).

#### Get Last 50 Lines

**cURL:**
```bash
curl "http://localhost:9000/iblink/v1/llama-server/logs?lines=50"
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/logs?lines=50"
```

#### Get Last 100 Lines (Default)

**cURL:**
```bash
curl http://localhost:9000/iblink/v1/llama-server/logs
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/logs"
```

#### Filter by Log Level

**cURL:**
```bash
curl "http://localhost:9000/iblink/v1/llama-server/logs?lines=50&level=error"
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/iblink/v1/llama-server/logs?lines=50&level=error"
```

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-01-20T10:30:00Z",
      "level": "info",
      "message": "Server started successfully"
    },
    {
      "timestamp": "2025-01-20T10:30:01Z",
      "level": "info",
      "message": "Loading model: Qwen3-0.6B-Q4_K_M.gguf"
    },
    {
      "timestamp": "2025-01-20T10:30:15Z",
      "level": "info",
      "message": "Model loaded successfully"
    },
    {
      "timestamp": "2025-01-20T10:30:16Z",
      "level": "info",
      "message": "Server is listening on http://0.0.0.0:8080"
    }
  ],
  "total_lines": 4,
  "server_running": true,
  "current_model": "Qwen3-0.6B-Q4_K_M.gguf"
}
```

---

### GET /logs/stream

Stream logs in real-time using Server-Sent Events.

**cURL:**
```bash
curl -N http://localhost:9000/iblink/v1/llama-server/logs/stream
```

**PowerShell:**
```powershell
# Note: PowerShell doesn't handle SSE well natively
# Consider using a dedicated SSE client or browser
Invoke-WebRequest -Uri "http://localhost:9000/iblink/v1/llama-server/logs/stream"
```

**JavaScript Example (Browser):**
```javascript
const eventSource = new EventSource('http://localhost:9000/iblink/v1/llama-server/logs/stream');

eventSource.onmessage = (event) => {
  const log = JSON.parse(event.data);
  console.log(`[${log.timestamp}] ${log.level}: ${log.message}`);
};

eventSource.onerror = (error) => {
  console.error('SSE Error:', error);
  eventSource.close();
};
```

**Response (SSE format):**
```
data: {"timestamp":"2025-01-20T10:30:00Z","level":"info","message":"Server started"}

data: {"timestamp":"2025-01-20T10:30:01Z","level":"debug","message":"Processing request"}

data: {"timestamp":"2025-01-20T10:30:02Z","level":"info","message":"eval time = 1263.80 ms / 119 tokens"}
```

---

### GET /health

API health check endpoint.

**cURL:**
```bash
curl http://localhost:9000/health
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9000/health"
```

**Response (Healthy):**
```json
{
  "status": "healthy",
  "service": "llamaserver-api",
  "timestamp": "2025-01-20T10:30:00Z",
  "version": "1.0.0",
  "uptime_seconds": 3600
}
```

**Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "service": "llamaserver-api",
  "timestamp": "2025-01-20T10:30:00Z",
  "version": "1.0.0",
  "error": "Database connection failed"
}
```

---

## Complete Workflow Examples

### Workflow 1: First Time Setup and Start

```bash
# 1. Check API health
curl http://localhost:9000/health

# 2. List available binaries
curl http://localhost:9000/iblink/v1/llama-server/binaries

# 3. Set compatible binary
curl -X POST http://localhost:9000/iblink/v1/llama-server/binaries/set \
  -H "Content-Type: application/json" \
  -d '{"binary_path": "C:\\llama-cpp\\x64\\llama-server.exe"}'

# 4. List available models
curl http://localhost:9000/iblink/v1/llama-server/models

# 5. Start server with a model
curl -X POST http://localhost:9000/iblink/v1/llama-server/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\Qwen3-0.6B-Q4_K_M.gguf",
    "port": 8080
  }'

# 6. Check status
curl http://localhost:9000/iblink/v1/llama-server/status

# 7. View logs
curl "http://localhost:9000/iblink/v1/llama-server/logs?lines=20"
```

### Workflow 2: Download and Run a New Model

```bash
# 1. Search for models
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/search \
  -H "Content-Type: application/json" \
  -d '{"query": "gemma gguf"}'

# 2. Get model info
curl "http://localhost:9000/iblink/v1/llama-server/models/info?repository=ggml-org/gemma-2-2b-it-Q4_K_M-GGUF"

# 3. Download model with progress
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download-stream \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "ggml-org/gemma-2-2b-it-Q4_K_M-GGUF",
    "files": ["gemma-2-2b-it-Q4_K_M.gguf"]
  }' \
  -N

# 4. Verify download
curl http://localhost:9000/iblink/v1/llama-server/models

# 5. Start with new model
curl -X POST http://localhost:9000/iblink/v1/llama-server/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Users\\user\\.iblink\\Models\\gemma-2-2b-it-Q4_K_M.gguf",
    "port": 8080
  }'
```

### Workflow 3: Switch Between Models

```bash
# 1. Check current status
curl http://localhost:9000/iblink/v1/llama-server/status

# 2. Switch to different model
curl -X POST http://localhost:9000/iblink/v1/llama-server/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\Different-Model.gguf"
  }'

# 3. Verify switch
curl http://localhost:9000/iblink/v1/llama-server/status
```

---

## Error Handling Examples

### Error Response Format

All errors follow this format:

```json
{
  "error": {
    "message": "Detailed error message",
    "type": "error_type",
    "code": "error_code",
    "details": "Additional context if available"
  }
}
```

### Common Error Responses

#### Binary Architecture Mismatch

```json
{
  "error": {
    "message": "The specified executable is not a valid application for this OS platform",
    "type": "server_error",
    "code": "binary_incompatible",
    "details": "ARM64 binary cannot run on x64 system. Use /binaries endpoint to find compatible binary."
  }
}
```

#### Model Not Found

```json
{
  "error": {
    "message": "Model file not found",
    "type": "not_found_error",
    "code": "model_not_found",
    "details": "C:\\Models\\nonexistent.gguf does not exist"
  }
}
```

#### Port Already in Use

```json
{
  "error": {
    "message": "Port 8080 is already in use",
    "type": "conflict_error",
    "code": "port_conflict",
    "details": "Another process (PID: 1234) is using port 8080"
  }
}
```

#### Server Not Running

```json
{
  "error": {
    "message": "Server is not running",
    "type": "server_error",
    "code": "server_not_running",
    "details": "Cannot stop server that is not running"
  }
}
```

---

## Tips and Best Practices

### 1. Always Set Binary First
```bash
# Recommended: Set binary before starting
curl -X POST http://localhost:9000/iblink/v1/llama-server/binaries/set \
  -d '{"binary_path": "C:\\compatible\\llama-server.exe"}'

# Then start without specifying binary
curl -X POST http://localhost:9000/iblink/v1/llama-server/start \
  -d '{"model_path": "C:\\Models\\model.gguf"}'
```

### 2. Check Status Before Operations
```bash
# Always check status before starting/switching
curl http://localhost:9000/iblink/v1/llama-server/status
```

### 3. Use download-stream for Large Models
```bash
# Prefer streaming download for better progress tracking
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download-stream \
  -d '{"repository": "repo/model", "files": ["large-model.gguf"]}' \
  -N
```

### 4. Monitor Logs During Operations
```bash
# Open log stream in separate terminal
curl -N http://localhost:9000/iblink/v1/llama-server/logs/stream
```

### 5. Graceful Shutdown
```bash
# Always stop server before application exit
curl -X POST http://localhost:9000/iblink/v1/llama-server/stop
```

---

**Last Updated**: 2025-11-14
**API Version**: 1.0.0
**Documentation**: `src/IB-Link.LlamaServerAPI/README.md`
