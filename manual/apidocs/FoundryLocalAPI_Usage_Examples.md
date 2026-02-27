# FoundryLocalAPI - Usage Examples

Complete guide with practical examples for all FoundryLocalAPI endpoints.

**Base URL**: `http://localhost:9500/iblink/v1/foundry-local`

**Purpose**: Manage FoundryLocal servers for running local AI models with streaming, chat, and completion capabilities.

**OpenAI Compatibility**: Partial compatibility through FoundryLocal proxy server

---

## Table of Contents

- [Server Management](#server-management)
  - [Start Server](#post-start)
  - [Start Server with Streaming](#post-start-stream)
  - [Stop Server](#post-stop)
  - [Get Server Status](#get-status)
  - [Switch Model](#post-switch-model)
- [Model Management](#model-management)
  - [List Available Models](#get-models)
  - [List Downloaded Models](#get-modelsdownloaded)
  - [List Loaded Models](#get-modelsloaded)
  - [Unload All Models](#post-modelsunload-all)
  - [Download Model](#post-modelsmodelnamedownload)
  - [Download Model with Streaming](#post-modelsmodelnamedownload-stream)
  - [Delete Model](#delete-modelsmodelname)
- [Configuration and Info](#configuration-and-info)
  - [Get Server Info](#get-info)
  - [Update Configuration](#post-config)
- [Logging](#logging)
  - [Get Recent Logs](#get-logs)
  - [Stream Live Logs](#get-logsstream)
- [Health and Monitoring](#health-and-monitoring)
  - [Health Check](#get-health)
- [OpenAI Compatibility](#openai-compatibility)
  - [List Models (OpenAI Format)](#get-v1models)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Error Handling](#error-handling-examples)
- [Tips and Best Practices](#tips-and-best-practices)

---

## Server Management

### POST /start

Start FoundryLocal server with a specified model.

**cURL:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_name = "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/start" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "success": true,
  "message": "Server started successfully",
  "port": 1234,
  "model": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
  "loaded_model_id": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
  "endpoint": "http://127.0.0.1:1234/v1",
  "api_key": "fl-YourApiKey123"
}
```

**With Custom Port:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
    "port": 1235
  }'
```

**With Options:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
    "options": {
      "auto_download": true,
      "timeout_seconds": 300,
      "health_check_interval_seconds": 2
    }
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_name = "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
    options = @{
        auto_download = $true
        timeout_seconds = 300
        health_check_interval_seconds = 2
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/start" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

### POST /start-stream

Start FoundryLocal server with real-time progress updates via Server-Sent Events.

**cURL:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start-stream \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
  }' \
  -N
```

**PowerShell:**
```powershell
$body = @{
    model_name = "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
} | ConvertTo-Json

# Note: PowerShell doesn't handle SSE natively well
Invoke-WebRequest -Uri "http://localhost:9500/iblink/v1/foundry-local/start-stream" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**JavaScript Example:**
```javascript
const response = await fetch('http://localhost:9500/iblink/v1/foundry-local/start-stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model_name: 'Qwen2.5-0.5B-Instruct-Q8_0-GGUF'
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const text = decoder.decode(value);
  const lines = text.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.substring(6));
      console.log(`[${data.type}] ${data.message}`);
    }
  }
}
```

**Response Stream:**
```
data: {"type":"progress","message":"Checking if model is downloaded..."}

data: {"type":"progress","message":"Model found locally"}

data: {"type":"progress","message":"Starting FoundryLocal server..."}

data: {"type":"progress","message":"Waiting for server to be ready..."}

data: {"type":"progress","message":"Server health check passed"}

data: {"type":"success","message":"Server started successfully","data":{"success":true,"port":1234,"model":"Qwen2.5-0.5B-Instruct-Q8_0-GGUF","endpoint":"http://127.0.0.1:1234/v1"}}
```

---

### POST /stop

Stop the currently running FoundryLocal server.

**cURL:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/stop
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/stop" `
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

Get the current status of the FoundryLocal server.

**cURL:**
```bash
curl http://localhost:9500/iblink/v1/foundry-local/status
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/status"
```

**Response (Server Running):**
```json
{
  "is_running": true,
  "status": "running",
  "current_model": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
  "loaded_model_id": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
  "port": 1234,
  "health": {
    "is_healthy": true,
    "response_time_ms": 45,
    "endpoint": "http://127.0.0.1:1234/v1",
    "last_check": "2025-01-20T10:30:00Z",
    "api_key": "fl-YourApiKey123"
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
  "loaded_model_id": null,
  "port": null,
  "health": {
    "is_healthy": false,
    "response_time_ms": 0,
    "endpoint": null,
    "last_check": "2025-01-20T10:30:00Z"
  },
  "last_updated": "2025-01-20T10:30:00Z"
}
```

---

### POST /switch-model

Stop the current server and start with a different model.

**cURL:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
  }'
```

**PowerShell:**
```powershell
$body = @{
    model_name = "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/switch-model" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**With Options:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Llama-3.2-1B-Instruct-Q8_0-GGUF",
    "options": {
      "auto_download": true,
      "timeout_seconds": 240
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Server started successfully",
  "port": 1234,
  "model": "Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
  "loaded_model_id": "Qwen/Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
  "endpoint": "http://127.0.0.1:1234/v1",
  "api_key": "fl-YourApiKey123"
}
```

---

## Model Management

### GET /models

List all available FoundryLocal models (from FoundryLocal's model registry).

**cURL:**
```bash
curl http://localhost:9500/iblink/v1/foundry-local/models
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/models"
```

**Response:**
```json
{
  "models": [
    {
      "model_id": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
      "simple_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
      "size": "0.5B",
      "quantization": "Q8_0",
      "is_downloaded": true,
      "is_loaded": false,
      "file_size_bytes": 524288000,
      "file_size_formatted": "500.0 MB"
    },
    {
      "model_id": "Qwen/Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
      "simple_name": "Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
      "size": "3B",
      "quantization": "Q4_K_M",
      "is_downloaded": false,
      "is_loaded": false,
      "file_size_bytes": 2147483648,
      "file_size_formatted": "2.0 GB"
    }
  ],
  "total_count": 2
}
```

---

### GET /models/downloaded

List only the models that have been downloaded locally.

**cURL:**
```bash
curl http://localhost:9500/iblink/v1/foundry-local/models/downloaded
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/models/downloaded"
```

**Response:**
```json
{
  "models": [
    {
      "model_id": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
      "simple_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
      "size": "0.5B",
      "quantization": "Q8_0",
      "is_downloaded": true,
      "is_loaded": false,
      "file_size_bytes": 524288000,
      "file_size_formatted": "500.0 MB",
      "download_date": "2025-01-15T14:30:00Z"
    }
  ],
  "total_count": 1
}
```

---

### GET /models/loaded

List currently loaded models in the FoundryLocal server.

**cURL:**
```bash
curl http://localhost:9500/iblink/v1/foundry-local/models/loaded
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/models/loaded"
```

**Response:**
```json
{
  "models": [
    {
      "model_id": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
      "simple_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
      "size": "0.5B",
      "quantization": "Q8_0",
      "is_downloaded": true,
      "is_loaded": true,
      "loaded_at": "2025-01-20T10:30:00Z"
    }
  ],
  "total_count": 1
}
```

---

### POST /models/unload-all

Unload all currently loaded models.

**cURL:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/models/unload-all
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/models/unload-all" `
    -Method POST
```

**Response:**
```json
{
  "success": true,
  "message": "All models unloaded successfully"
}
```

---

### POST /models/{modelName}/download

Download a specific model.

**cURL:**
```bash
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-3B-Instruct-Q4_K_M-GGUF/download"
```

**PowerShell:**
```powershell
$modelName = "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/models/$modelName/download" `
    -Method POST
```

**Response:**
```json
{
  "success": true,
  "message": "Model downloaded successfully",
  "model_name": "Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
  "actual_model_id": "Qwen/Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
  "file_size_bytes": 2147483648,
  "download_time_seconds": 125
}
```

---

### POST /models/{modelName}/download-stream

Download a model with real-time progress updates via Server-Sent Events.

**cURL:**
```bash
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-3B-Instruct-Q4_K_M-GGUF/download-stream" -N
```

**PowerShell:**
```powershell
$modelName = "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
Invoke-WebRequest -Uri "http://localhost:9500/iblink/v1/foundry-local/models/$modelName/download-stream" `
    -Method POST
```

**JavaScript Example:**
```javascript
const modelName = 'Qwen2.5-3B-Instruct-Q4_K_M-GGUF';
const response = await fetch(
  `http://localhost:9500/iblink/v1/foundry-local/models/${modelName}/download-stream`,
  { method: 'POST' }
);

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const text = decoder.decode(value);
  const lines = text.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.substring(6));

      if (data.type === 'progress') {
        console.log(`Progress: ${data.message}`);
      } else if (data.type === 'success') {
        console.log('Download complete!');
      } else if (data.type === 'error') {
        console.error(`Error: ${data.message}`);
      }
    }
  }
}
```

**Response Stream:**
```
data: {"type":"progress","message":"Starting download: Qwen2.5-3B-Instruct-Q4_K_M-GGUF"}

data: {"type":"progress","message":"Downloaded: 5.2% (105 MB / 2048 MB) - 12.5 MB/s"}

data: {"type":"progress","message":"Downloaded: 25.8% (528 MB / 2048 MB) - 14.2 MB/s"}

data: {"type":"progress","message":"Downloaded: 50.1% (1025 MB / 2048 MB) - 13.8 MB/s"}

data: {"type":"progress","message":"Downloaded: 75.5% (1546 MB / 2048 MB) - 14.0 MB/s"}

data: {"type":"progress","message":"Downloaded: 100.0% (2048 MB / 2048 MB) - 13.9 MB/s"}

data: {"type":"success","message":"Download completed successfully","data":{"success":true,"model_name":"Qwen2.5-3B-Instruct-Q4_K_M-GGUF"}}
```

---

### DELETE /models/{modelName}

Delete a downloaded model from the local cache.

**cURL:**
```bash
curl -X DELETE "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
```

**PowerShell:**
```powershell
$modelName = "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/models/$modelName" `
    -Method DELETE
```

**Response:**
```json
{
  "success": true,
  "message": "Model deleted successfully",
  "model_name": "Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
  "freed_space_bytes": 2147483648,
  "freed_space_formatted": "2.0 GB"
}
```

---

## Configuration and Info

### GET /info

Get server configuration and capabilities.

**cURL:**
```bash
curl http://localhost:9500/iblink/v1/foundry-local/info
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/info"
```

**Response:**
```json
{
  "service": "FoundryLocal API",
  "version": "2.0.0",
  "foundry_local_version": "0.5.0",
  "capabilities": [
    "model_management",
    "server_control",
    "streaming_download",
    "health_monitoring",
    "log_streaming"
  ],
  "configuration": {
    "default_port": 1234,
    "cache_dir": "C:\\Users\\user\\.cache\\foundrylocal",
    "default_log_level": "INFO"
  },
  "model_registry": {
    "total_models": 45,
    "downloaded_models": 3,
    "loaded_models": 1
  }
}
```

---

### POST /config

Update server configuration.

**cURL:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/config \
  -H "Content-Type: application/json" \
  -d '{
    "port": 1235,
    "cache_dir": "D:\\AI\\Models",
    "default_log_level": "DEBUG"
  }'
```

**PowerShell:**
```powershell
$body = @{
    port = 1235
    cache_dir = "D:\AI\Models"
    default_log_level = "DEBUG"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/config" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Partial Update:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/config \
  -H "Content-Type: application/json" \
  -d '{
    "default_log_level": "INFO"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "port": 1235,
  "cachedir": "D:\\AI\\Models",
  "default_log_level": "DEBUG"
}
```

**Reset to Defaults:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/config \
  -H "Content-Type: application/json" \
  -d '{
    "defaults": true
  }'
```

---

## Logging

### GET /logs

Get recent log entries.

**cURL:**
```bash
curl "http://localhost:9500/iblink/v1/foundry-local/logs?count=50"
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/logs?count=50"
```

**Default (Last 100 entries):**
```bash
curl http://localhost:9500/iblink/v1/foundry-local/logs
```

**Response:**
```json
[
  {
    "timestamp": "2025-01-20T10:30:00Z",
    "level": "INFO",
    "message": "Server started successfully",
    "source": "FoundryLocalApiService"
  },
  {
    "timestamp": "2025-01-20T10:30:01Z",
    "level": "INFO",
    "message": "Model loaded: Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
    "source": "FoundryLocalService"
  },
  {
    "timestamp": "2025-01-20T10:30:15Z",
    "level": "DEBUG",
    "message": "Health check passed - response time: 45ms",
    "source": "HealthMonitor"
  }
]
```

---

### GET /logs/stream

Stream live logs using Server-Sent Events.

**cURL:**
```bash
curl -N http://localhost:9500/iblink/v1/foundry-local/logs/stream
```

**PowerShell:**
```powershell
# Note: PowerShell doesn't handle SSE well natively
Invoke-WebRequest -Uri "http://localhost:9500/iblink/v1/foundry-local/logs/stream"
```

**JavaScript Example:**
```javascript
const eventSource = new EventSource('http://localhost:9500/iblink/v1/foundry-local/logs/stream');

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
data: {"timestamp":"2025-01-20T10:30:00Z","level":"INFO","message":"Server started","source":"FoundryLocalApiService"}

data: {"timestamp":"2025-01-20T10:30:01Z","level":"DEBUG","message":"Processing request","source":"API"}

data: {"timestamp":"2025-01-20T10:30:02Z","level":"INFO","message":"Model loaded successfully","source":"FoundryLocalService"}
```

---

## Health and Monitoring

### GET /health

Check the health of the FoundryLocal API and the underlying FoundryLocal server.

**cURL:**
```bash
curl http://localhost:9500/iblink/v1/foundry-local/health
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/health"
```

**Response (Healthy with Running Server):**
```json
{
  "status": "healthy",
  "service": "foundry-local-api",
  "version": "2.0.0",
  "timestamp": "2025-01-20T10:30:00Z",
  "foundry_local": {
    "is_running": true,
    "status": "running",
    "port": 1234,
    "model": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
  }
}
```

**Response (Healthy with Stopped Server):**
```json
{
  "status": "healthy",
  "service": "foundry-local-api",
  "version": "2.0.0",
  "timestamp": "2025-01-20T10:30:00Z",
  "foundry_local": {
    "is_running": false,
    "status": "stopped",
    "port": null,
    "model": null
  }
}
```

---

## OpenAI Compatibility

### GET /v1/models

List models in OpenAI-compatible format.

**cURL:**
```bash
curl http://localhost:9500/v1/models
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:9500/v1/models"
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
      "object": "model",
      "created": 1705743600,
      "owned_by": "foundry-local"
    },
    {
      "id": "Qwen/Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
      "object": "model",
      "created": 1705743600,
      "owned_by": "foundry-local"
    }
  ]
}
```

**Note:** This endpoint only lists downloaded models to match OpenAI's behavior of listing available models.

---

## Complete Workflow Examples

### Workflow 1: First Time Setup

```bash
# 1. Check API health
curl http://localhost:9500/iblink/v1/foundry-local/health

# 2. Get server info
curl http://localhost:9500/iblink/v1/foundry-local/info

# 3. List available models
curl http://localhost:9500/iblink/v1/foundry-local/models | jq '.models[] | {simple_name, size, is_downloaded}'

# 4. Download a small model
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-0.5B-Instruct-Q8_0-GGUF/download"

# 5. Start server with the downloaded model
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
  }'

# 6. Check server status
curl http://localhost:9500/iblink/v1/foundry-local/status

# 7. Use the model (via FoundryLocal proxy)
# Note: Use the endpoint and API key from the start response
curl -X POST http://127.0.0.1:1234/v1/chat/completions \
  -H "Authorization: Bearer fl-YourApiKey123" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Workflow 2: Download Model with Progress

```bash
# Start streaming download
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-3B-Instruct-Q4_K_M-GGUF/download-stream" -N

# Monitor in real-time:
# data: {"type":"progress","message":"Starting download..."}
# data: {"type":"progress","message":"Downloaded: 25.0%..."}
# data: {"type":"progress","message":"Downloaded: 50.0%..."}
# data: {"type":"success","message":"Download completed"}
```

**PowerShell with Progress:**
```powershell
$modelName = "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"
$uri = "http://localhost:9500/iblink/v1/foundry-local/models/$modelName/download-stream"

$client = New-Object System.Net.Http.HttpClient
$response = $client.PostAsync($uri, $null).Result
$stream = $response.Content.ReadAsStreamAsync().Result
$reader = New-Object System.IO.StreamReader($stream)

while ($null -ne ($line = $reader.ReadLine())) {
    if ($line.StartsWith("data: ")) {
        $data = $line.Substring(6) | ConvertFrom-Json
        Write-Host "[$($data.type)] $($data.message)"
    }
}

$reader.Close()
$client.Dispose()
```

### Workflow 3: Switch Between Models

```bash
# Check current status
curl http://localhost:9500/iblink/v1/foundry-local/status | jq '.current_model'

# Switch to a different model
curl -X POST http://localhost:9500/iblink/v1/foundry-local/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
    "options": {
      "auto_download": true
    }
  }'

# Verify switch
curl http://localhost:9500/iblink/v1/foundry-local/status | jq '.current_model'
```

### Workflow 4: Model Management

```bash
# List all available models
curl http://localhost:9500/iblink/v1/foundry-local/models \
  | jq '.models[] | select(.is_downloaded == false) | .simple_name'

# Download multiple models
for model in "Qwen2.5-0.5B-Instruct-Q8_0-GGUF" "Qwen2.5-3B-Instruct-Q4_K_M-GGUF"; do
  echo "Downloading $model..."
  curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/$model/download"
done

# List downloaded models
curl http://localhost:9500/iblink/v1/foundry-local/models/downloaded

# Delete an unused model
curl -X DELETE "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
```

### Workflow 5: Monitoring and Debugging

```bash
# Stream logs in one terminal
curl -N http://localhost:9500/iblink/v1/foundry-local/logs/stream

# In another terminal, perform operations
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{"model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"}'

# Check recent logs for errors
curl "http://localhost:9500/iblink/v1/foundry-local/logs?count=20" \
  | jq '.[] | select(.level == "ERROR")'

# Get server info
curl http://localhost:9500/iblink/v1/foundry-local/info | jq
```

---

## Error Handling Examples

### Error Response Format

```json
{
  "error": {
    "message": "Error description",
    "type": "error_type",
    "code": "error_code",
    "details": "Additional information"
  }
}
```

### Common Error Responses

#### Missing Model Name

```json
{
  "error": {
    "message": "Model name is required",
    "type": "invalid_request_error",
    "code": "missing_model_name"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Model Not Found

```json
{
  "error": {
    "message": "Model 'nonexistent-model' not found in registry",
    "type": "not_found_error",
    "code": "model_not_found"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "nonexistent-model"
  }'
```

#### Model Not Downloaded

```json
{
  "error": {
    "message": "Model must be downloaded before starting server",
    "type": "precondition_failed",
    "code": "model_not_downloaded",
    "details": "Use auto_download option or download manually first"
  }
}
```

#### Server Already Running

```json
{
  "error": {
    "message": "FoundryLocal server is already running with model 'Qwen2.5-0.5B-Instruct-Q8_0-GGUF'",
    "type": "conflict_error",
    "code": "server_already_running",
    "details": "Stop the current server first or use switch-model endpoint"
  }
}
```

#### Server Start Timeout

```json
{
  "error": {
    "message": "Server failed to start within timeout period",
    "type": "timeout_error",
    "code": "server_start_timeout",
    "details": "Timeout: 180 seconds. Try increasing timeout_seconds option."
  }
}
```

#### Download Failed

```json
{
  "error": {
    "message": "Failed to download model",
    "type": "download_error",
    "code": "download_failed",
    "details": "Network connection error or model not available"
  }
}
```

#### Configuration Update Failed

```json
{
  "error": {
    "message": "Failed to update configuration. Check logs for details.",
    "type": "configuration_error",
    "code": "update_failed"
  }
}
```

---

## Tips and Best Practices

### 1. Use Auto-Download for Convenience

```bash
# Auto-download enabled (default)
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
    "options": {
      "auto_download": true
    }
  }'

# Or download explicitly first for better control
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-0.5B-Instruct-Q8_0-GGUF/download-stream" -N
```

### 2. Monitor Downloads with Streaming

```bash
# Use streaming endpoints for long-running operations
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-3B-Instruct-Q4_K_M-GGUF/download-stream" -N

# Instead of non-streaming which gives no progress feedback
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-3B-Instruct-Q4_K_M-GGUF/download"
```

### 3. Check Status Before Operations

```bash
# Always check status before starting
status=$(curl -s http://localhost:9500/iblink/v1/foundry-local/status | jq -r '.is_running')

if [ "$status" == "true" ]; then
  echo "Server is running, stopping first..."
  curl -X POST http://localhost:9500/iblink/v1/foundry-local/stop
fi

# Now start with new model
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
  }'
```

### 4. Use Switch-Model for Convenience

```bash
# Instead of manually stopping and starting
curl -X POST http://localhost:9500/iblink/v1/foundry-local/stop
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{"model_name": "new-model"}'

# Use switch-model (does both automatically)
curl -X POST http://localhost:9500/iblink/v1/foundry-local/switch-model \
  -H "Content-Type: application/json" \
  -d '{"model_name": "new-model"}'
```

### 5. List Downloaded Models First

```bash
# Check what's already downloaded before starting
curl http://localhost:9500/iblink/v1/foundry-local/models/downloaded \
  | jq '.models[] | .simple_name'

# Then use one of the downloaded models
```

### 6. Increase Timeout for Large Models

```bash
# Large models may need more time to load
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Llama-3.2-3B-Instruct-Q8_0-GGUF",
    "options": {
      "timeout_seconds": 300,
      "auto_download": true
    }
  }'
```

### 7. Configure Custom Cache Directory

```bash
# Set custom cache directory for models
curl -X POST http://localhost:9500/iblink/v1/foundry-local/config \
  -H "Content-Type: application/json" \
  -d '{
    "cache_dir": "D:\\AI\\Models"
  }'

# Verify configuration
curl http://localhost:9500/iblink/v1/foundry-local/info | jq '.configuration.cache_dir'
```

### 8. Handle Errors Gracefully

**PowerShell:**
```powershell
try {
    $body = @{
        model_name = "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/start" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"

    Write-Host "Server started on port $($response.port)"
}
catch {
    $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json

    if ($errorBody.error.code -eq "server_already_running") {
        Write-Host "Server already running - switching model instead"
        Invoke-RestMethod -Uri "http://localhost:9500/iblink/v1/foundry-local/switch-model" `
            -Method POST `
            -Body $body `
            -ContentType "application/json"
    }
    else {
        Write-Host "Error: $($errorBody.error.message)" -ForegroundColor Red
    }
}
```

### 9. Clean Up Unused Models

```bash
# List all downloaded models with sizes
curl http://localhost:9500/iblink/v1/foundry-local/models/downloaded \
  | jq '.models[] | {name: .simple_name, size: .file_size_formatted}'

# Delete unused models to free space
curl -X DELETE "http://localhost:9500/iblink/v1/foundry-local/models/old-model-name"
```

### 10. Monitor Server Health

```bash
# Periodic health check script
while true; do
  health=$(curl -s http://localhost:9500/iblink/v1/foundry-local/health | jq -r '.foundry_local.is_healthy')

  if [ "$health" == "true" ]; then
    echo "$(date): Server healthy"
  else
    echo "$(date): Server unhealthy - restarting..."
    curl -X POST http://localhost:9500/iblink/v1/foundry-local/stop
    sleep 2
    curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
      -H "Content-Type: application/json" \
      -d '{"model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"}'
  fi

  sleep 30
done
```

---

## Model Recommendations

### Small Models (500MB - 1GB)
- **Qwen2.5-0.5B-Instruct-Q8_0-GGUF**: Fastest, good for simple tasks
- **Llama-3.2-1B-Instruct-Q8_0-GGUF**: Balanced speed and capability

### Medium Models (1GB - 3GB)
- **Qwen2.5-3B-Instruct-Q4_K_M-GGUF**: Best balance for general use
- **Llama-3.2-3B-Instruct-Q4_K_M-GGUF**: Strong reasoning capabilities

### Large Models (5GB+)
- **Qwen2.5-7B-Instruct-Q4_K_M-GGUF**: Advanced reasoning
- **Llama-3.1-8B-Instruct-Q4_K_M-GGUF**: High quality responses

---

## FoundryLocal Server Usage

After starting the server via the API, you can interact with it using the OpenAI-compatible endpoints:

```bash
# Get the endpoint and API key from the start response
ENDPOINT="http://127.0.0.1:1234/v1"
API_KEY="fl-YourApiKey123"

# Chat completion
curl -X POST "$ENDPOINT/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
    "messages": [
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'

# Streaming chat
curl -X POST "$ENDPOINT/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
    "messages": [
      {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true
  }' \
  -N
```

---

**Last Updated**: 2025-01-20
**API Version**: 2.0.0
**Default Port**: 9500
**Documentation**: `src/IB-Link.FoundryLocalAPI/README.md`

---

## Additional Resources

- [FoundryLocal GitHub](https://github.com/FoundryAI/foundry-local)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [GGUF Model Format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)

---

## Quick Reference

### Common Operations

```bash
# Start server
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{"model_name": "Qwen2.5-0.5B-Instruct-Q8_0-GGUF"}'

# Stop server
curl -X POST http://localhost:9500/iblink/v1/foundry-local/stop

# Get status
curl http://localhost:9500/iblink/v1/foundry-local/status

# Switch model
curl -X POST http://localhost:9500/iblink/v1/foundry-local/switch-model \
  -H "Content-Type: application/json" \
  -d '{"model_name": "model-name"}'

# List models
curl http://localhost:9500/iblink/v1/foundry-local/models

# Download model
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/model-name/download"

# Health check
curl http://localhost:9500/iblink/v1/foundry-local/health
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Model or resource not found
- `409 Conflict` - Server already running
- `408 Request Timeout` - Operation timeout
- `500 Internal Server Error` - Server error
