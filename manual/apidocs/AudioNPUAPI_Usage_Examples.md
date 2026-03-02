# AudioNPUAPI - Usage Examples

Complete guide with practical examples for the AudioNPUAPI system and the Whisper Server it manages.

**System Architecture**: AudioNPUAPI is a C# manager service that controls a Python-based Whisper Server optimized for Snapdragon NPU acceleration.

**Default Whisper Server URL**: `http://localhost:8000`

**OpenAI Compatibility**: Full compatibility with OpenAI Whisper API v1 specification

---

## Table of Contents

- [System Overview](#system-overview)
- [Server Management](#server-management)
  - [Starting the AudioNPUAPI Manager](#starting-the-audionpuapi-manager)
  - [Stopping the Server](#stopping-the-server)
  - [Server Configuration](#server-configuration)
- [Whisper Server API Endpoints](#whisper-server-api-endpoints)
  - [Health Check](#get-health)
  - [Server Status](#get-status)
  - [Audio Transcription](#post-v1audiotranscriptions)
  - [Audio Translation](#post-v1audiotranslations)
- [Real-time Transcription](#real-time-transcription)
  - [WebSocket Streaming](#websocket-streaming)
  - [Real-time Microphone](#real-time-microphone)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Error Handling](#error-handling-examples)
- [Tips and Best Practices](#tips-and-best-practices)

---

## System Overview

### Architecture

```
┌─────────────────────────────────────────────┐
│        IB-Link.AudioNPUAPI (C#)             │
│         Manager/Controller Layer            │
│                                             │
│  • Lifecycle Management                    │
│  • Configuration                           │
│  • Log Monitoring                          │
└──────────────┬──────────────────────────────┘
               │ Controls via PowerShell
               ▼
┌─────────────────────────────────────────────┐
│      Whisper Server (Python/FastAPI)        │
│          OpenAI-Compatible API              │
│                                             │
│  • Transcription Endpoints                 │
│  • Translation Endpoints                   │
│  • WebSocket Streaming                     │
│  • NPU/CPU Inference                       │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│    Hardware Acceleration Layer              │
│                                             │
│  • Qualcomm NPU (QNN) - Snapdragon X Elite │
│  • CPU Fallback - Universal Support        │
└─────────────────────────────────────────────┘
```

### Components

1. **AudioNPUAPI Manager (C#)**:
   - Console application that manages Python whisper-server lifecycle
   - Handles bootstrap, start, stop, restart, status operations
   - Monitors Python server logs
   - Configured via `appsettings.json`

2. **Whisper Server (Python)**:
   - FastAPI-based HTTP server with WebSocket support
   - OpenAI-compatible transcription API
   - NPU-accelerated inference with CPU fallback
   - Configured via `config.yaml` and `.env`

---

## Server Management

### Starting the AudioNPUAPI Manager

The AudioNPUAPI manager automatically starts and manages the Python whisper-server.

**Basic Start:**
```bash
# Navigate to the AudioNPUAPI directory
cd src\IB-Link.AudioNPUAPI

# Run the manager
dotnet run
```

**Output:**
```
═══════════════════════════════════════════════════════════════════
  IB-Link Audio NPU Manager - Whisper Server Controller
═══════════════════════════════════════════════════════════════════

Checking whisper server status...
Starting whisper server on 127.0.0.1:8000...
✓ Whisper server started successfully at http://127.0.0.1:8000

═══════════════════════════════════════════════════════════════════
  Whisper Server Information:
  • API URL: http://127.0.0.1:8000
  • Swagger UI: http://127.0.0.1:8000/docs
  • Health Check: http://127.0.0.1:8000/health
  • WebSocket: ws://127.0.0.1:8000/v1/audio/realtime
═══════════════════════════════════════════════════════════════════

Press Ctrl+C to stop the server and exit
```

### Stopping the Server

**Using Ctrl+C:**
```
Press Ctrl+C in the running AudioNPUAPI console
```

**Output:**
```
[SHUTDOWN] Stopping whisper server...
✓ Whisper server stopped successfully

AudioNPUAPI manager stopped.
```

### Server Configuration

**appsettings.json** (AudioNPUAPI Manager):
```json
{
  "AudioNPUApi": {
    "WhisperServerPath": "..\\..\\whisper-server",
    "DefaultPort": 8000,
    "DefaultHost": "127.0.0.1",
    "DefaultModel": "whisper_large_v3_turbo",
    "StartupTimeout": 60,
    "HealthCheckInterval": 30,
    "ShowPythonOutput": true
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  }
}
```

**Configuration Parameters:**
- `WhisperServerPath`: Path to whisper-server directory
- `DefaultPort`: Server port (default: 8000)
- `DefaultHost`: Server host (default: 127.0.0.1)
- `DefaultModel`: Whisper model to use
- `StartupTimeout`: Timeout for server startup (seconds)
- `HealthCheckInterval`: Health check frequency (seconds)
- `ShowPythonOutput`: Show Python server logs in console

---

## Whisper Server API Endpoints

Once the AudioNPUAPI manager starts the Whisper Server, you can interact with these endpoints.

### GET /health

Check if the whisper server is running and healthy.

**cURL:**
```bash
curl http://localhost:8000/health
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z"
}
```

---

### GET /status

Get detailed server status, configuration, and performance metrics.

**cURL:**
```bash
curl http://localhost:8000/status
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/status"
```

**Response:**
```json
{
  "status": "running",
  "uptime": 3600,
  "total_requests": 150,
  "active_connections": 2,
  "config": {
    "model": "whisper-large-v3-turbo",
    "npu_enabled": true,
    "target_runtime": "qnn_dlc",
    "precision": "w8a8"
  },
  "hardware": {
    "device": "Snapdragon X Elite",
    "npu_available": true,
    "cpu_fallback": true
  },
  "performance": {
    "average_inference_time_ms": 250,
    "total_audio_processed_seconds": 7200
  }
}
```

---

### POST /v1/audio/transcriptions

Transcribe audio files into text using the Whisper model.

#### Basic Transcription

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo"
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "text": "This is the transcribed text from the audio file."
}
```

#### Transcription with Language Specification

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@japanese_audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "language=ja"
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\japanese_audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    language = "ja"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Supported Languages:**
- `en` - English
- `ja` - Japanese
- `zh` - Chinese
- `es` - Spanish
- `fr` - French
- `de` - German
- `ko` - Korean
- `auto` - Auto-detect (default)

**Response:**
```json
{
  "text": "これは日本語の音声ファイルから文字起こしされたテキストです。"
}
```

#### Verbose JSON Output

Get detailed transcription with segments and metadata.

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json"
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    response_format = "verbose_json"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "task": "transcribe",
  "language": "en",
  "duration": 30.0,
  "text": "This is the complete transcribed text.",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 5.0,
      "text": "This is the first segment.",
      "tokens": [50364, 1668, 307, 264, 1489, 9469, 13],
      "temperature": 0.0,
      "avg_logprob": -0.25,
      "compression_ratio": 1.2,
      "no_speech_prob": 0.01
    },
    {
      "id": 1,
      "seek": 500,
      "start": 5.0,
      "end": 10.0,
      "text": "This is the second segment.",
      "tokens": [50364, 1668, 307, 264, 1489, 9469, 13],
      "temperature": 0.0,
      "avg_logprob": -0.22,
      "compression_ratio": 1.3,
      "no_speech_prob": 0.005
    }
  ]
}
```

#### Text-Only Output

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=text"
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    response_format = "text"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```
This is the transcribed text from the audio file.
```

#### SRT Subtitle Format

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@video_audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=srt" \
  -o subtitles.srt
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\video_audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    response_format = "srt"
}

$result = Invoke-RestMethod -Uri $uri -Method Post -Form $form
$result | Out-File -FilePath "C:\Output\subtitles.srt" -Encoding UTF8
```

**Response:**
```srt
1
00:00:00,000 --> 00:00:05,000
This is the first subtitle.

2
00:00:05,000 --> 00:00:10,000
This is the second subtitle.
```

#### VTT Subtitle Format

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@video_audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=vtt" \
  -o subtitles.vtt
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\video_audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    response_format = "vtt"
}

$result = Invoke-RestMethod -Uri $uri -Method Post -Form $form
$result | Out-File -FilePath "C:\Output\subtitles.vtt" -Encoding UTF8
```

**Response:**
```vtt
WEBVTT

00:00:00.000 --> 00:00:05.000
This is the first subtitle.

00:00:05.000 --> 00:00:10.000
This is the second subtitle.
```

#### Transcription with Prompt

Use a prompt to guide the model's transcription style.

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@interview.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "language=en" \
  -F "prompt=This is an interview between Dr. Smith and a reporter about climate change."
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\interview.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    language = "en"
    prompt = "This is an interview between Dr. Smith and a reporter about climate change."
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

#### Transcription with Temperature

Control randomness/creativity in transcription.

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "temperature=0.2"
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    temperature = "0.2"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Temperature Values:**
- `0.0` - Most deterministic (recommended for accuracy)
- `0.2` - Slightly creative
- `0.5` - Balanced
- `1.0` - Most creative/random

---

### POST /v1/audio/translations

Translate audio from any language to English.

**cURL:**
```bash
curl -X POST http://localhost:8000/v1/audio/translations \
  -F "file=@spanish_audio.wav" \
  -F "model=whisper-large-v3-turbo"
```

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/translations"
$filePath = "C:\Audio\spanish_audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "text": "This is the English translation of the Spanish audio."
}
```

**Note:** The translation endpoint always outputs English text, regardless of the input language.

---

## Real-time Transcription

### WebSocket Streaming

Stream audio chunks for real-time transcription via WebSocket.

**JavaScript Example:**
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/v1/audio/stream');

ws.onopen = () => {
  console.log('Connected to Whisper Server');

  // Send configuration
  ws.send(JSON.stringify({
    model: 'whisper-large-v3-turbo',
    language: 'auto',
    response_format: 'json'
  }));

  // Start streaming audio chunks
  // Audio should be raw PCM (16kHz, 16-bit, mono)
  streamAudioChunks(ws);
};

ws.onmessage = (event) => {
  const result = JSON.parse(event.data);

  if (result.type === 'partial') {
    console.log('Partial:', result.text);
  } else if (result.type === 'final') {
    console.log('Final:', result.text);
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from Whisper Server');
};

// Function to stream audio chunks
function streamAudioChunks(ws) {
  // Get audio from microphone or file
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      const mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
          // Send audio chunk as binary
          ws.send(event.data);
        }
      };

      // Record in 1-second chunks
      mediaRecorder.start(1000);
    })
    .catch(err => console.error('Microphone error:', err));
}
```

**Python Example:**
```python
import asyncio
import websockets
import json

async def transcribe_stream():
    uri = "ws://localhost:8000/v1/audio/stream"

    async with websockets.connect(uri) as websocket:
        # Send configuration
        config = {
            "model": "whisper-large-v3-turbo",
            "language": "auto",
            "response_format": "json"
        }
        await websocket.send(json.dumps(config))

        # Stream audio chunks
        with open("audio.wav", "rb") as f:
            chunk_size = 16000  # 1 second at 16kHz
            while True:
                chunk = f.read(chunk_size * 2)  # 2 bytes per sample
                if not chunk:
                    break
                await websocket.send(chunk)

                # Receive transcription
                result = await websocket.recv()
                data = json.loads(result)
                print(f"{data['type']}: {data['text']}")

asyncio.run(transcribe_stream())
```

**Message Types:**
- `partial` - Partial transcription (interim results)
- `final` - Final transcription for segment

---

### Real-time Microphone

Real-time transcription directly from microphone input.

**HTML/JavaScript Example:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Real-time Whisper Transcription</title>
</head>
<body>
    <h1>Real-time Transcription</h1>
    <button id="startBtn">Start Transcription</button>
    <button id="stopBtn" disabled>Stop Transcription</button>
    <div id="status">Status: Disconnected</div>
    <div id="transcription"></div>

    <script>
        let ws = null;
        let mediaRecorder = null;

        document.getElementById('startBtn').addEventListener('click', startTranscription);
        document.getElementById('stopBtn').addEventListener('click', stopTranscription);

        async function startTranscription() {
            // Connect to WebSocket
            ws = new WebSocket('ws://localhost:8000/v1/audio/realtime');

            ws.onopen = () => {
                document.getElementById('status').textContent = 'Status: Connected';
                document.getElementById('startBtn').disabled = true;
                document.getElementById('stopBtn').disabled = false;

                // Send start command with configuration
                ws.send(JSON.stringify({
                    action: 'start',
                    config: {
                        language: 'auto',
                        vad_enabled: true,
                        energy_threshold: 1000
                    }
                }));
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.type === 'transcription') {
                    const text = data.text;
                    const isFinal = data.is_final;
                    const confidence = data.confidence;

                    const transcriptionDiv = document.getElementById('transcription');
                    const color = isFinal ? 'black' : 'gray';
                    const weight = isFinal ? 'bold' : 'normal';

                    transcriptionDiv.innerHTML += `<p style="color: ${color}; font-weight: ${weight}">${text} (${(confidence * 100).toFixed(1)}%)</p>`;
                    transcriptionDiv.scrollTop = transcriptionDiv.scrollHeight;
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                document.getElementById('status').textContent = 'Status: Error';
            };

            ws.onclose = () => {
                document.getElementById('status').textContent = 'Status: Disconnected';
                document.getElementById('startBtn').disabled = false;
                document.getElementById('stopBtn').disabled = true;
            };

            // Start capturing microphone
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0 && ws && ws.readyState === WebSocket.OPEN) {
                        ws.send(event.data);
                    }
                };

                mediaRecorder.start(500); // Send chunks every 500ms
            } catch (err) {
                console.error('Microphone access error:', err);
                alert('Could not access microphone: ' + err.message);
            }
        }

        function stopTranscription() {
            if (ws) {
                ws.send(JSON.stringify({ action: 'stop' }));
                ws.close();
                ws = null;
            }

            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
                mediaRecorder = null;
            }
        }
    </script>
</body>
</html>
```

**Control Commands:**
```json
{"action": "start", "config": {...}}  // Start transcription
{"action": "pause"}                   // Pause transcription
{"action": "resume"}                  // Resume transcription
{"action": "stop"}                    // Stop transcription
```

---

## Complete Workflow Examples

### Workflow 1: Basic Setup and Transcription

```bash
# 1. Start the AudioNPUAPI manager
cd src\IB-Link.AudioNPUAPI
dotnet run

# 2. Wait for server to start, then in a new terminal:

# 3. Check health
curl http://localhost:8000/health

# 4. Check status
curl http://localhost:8000/status

# 5. Transcribe an audio file
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@recording.wav" \
  -F "model=whisper-large-v3-turbo"

# 6. Stop the server (in the AudioNPUAPI terminal)
# Press Ctrl+C
```

### Workflow 2: Multi-Language Processing

```bash
# 1. Transcribe English audio
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@english.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "language=en" \
  -F "response_format=json" \
  -o english_result.json

# 2. Transcribe Japanese audio
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@japanese.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "language=ja" \
  -F "response_format=verbose_json" \
  -o japanese_result.json

# 3. Translate Spanish to English
curl -X POST http://localhost:8000/v1/audio/translations \
  -F "file=@spanish.wav" \
  -F "model=whisper-large-v3-turbo" \
  -o spanish_translation.json
```

### Workflow 3: Video Subtitle Generation

```bash
# 1. Extract audio from video using ffmpeg
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# 2. Generate SRT subtitles
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=srt" \
  -o subtitles.srt

# 3. Generate VTT subtitles for web
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=vtt" \
  -o subtitles.vtt

# 4. Embed subtitles into video
ffmpeg -i video.mp4 -i subtitles.srt -c copy -c:s mov_text output_with_subs.mp4
```

### Workflow 4: Batch Processing with PowerShell

```powershell
# Process all WAV files in a directory
$audioDir = "C:\Audio\ToProcess"
$outputDir = "C:\Audio\Results"
$uri = "http://localhost:8000/v1/audio/transcriptions"

Get-ChildItem -Path $audioDir -Filter "*.wav" | ForEach-Object {
    Write-Host "Processing $($_.Name)..."

    $form = @{
        file = Get-Item -Path $_.FullName
        model = "whisper-large-v3-turbo"
        language = "auto"
        response_format = "verbose_json"
    }

    try {
        $result = Invoke-RestMethod -Uri $uri -Method Post -Form $form

        $outputFile = Join-Path $outputDir "$($_.BaseName)_transcription.json"
        $result | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile

        Write-Host "✓ Completed: $($_.Name)" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed: $($_.Name) - $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

### Workflow 5: Real-time Meeting Transcription

```html
<!-- Save as meeting_transcription.html and open in browser -->
<!DOCTYPE html>
<html>
<head>
    <title>Meeting Transcription</title>
    <style>
        #transcription {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            font-family: monospace;
        }
        .final { font-weight: bold; color: black; }
        .partial { color: gray; }
    </style>
</head>
<body>
    <h1>Real-time Meeting Transcription</h1>
    <button id="startBtn">Start Recording</button>
    <button id="pauseBtn" disabled>Pause</button>
    <button id="stopBtn" disabled>Stop</button>
    <div id="status">Not connected</div>
    <hr>
    <h2>Transcription:</h2>
    <div id="transcription"></div>

    <script src="meeting_transcription.js"></script>
</body>
</html>
```

---

## Error Handling Examples

### Error Response Format

```json
{
  "error": {
    "message": "Error description",
    "type": "error_type",
    "code": "ERROR_CODE"
  }
}
```

### Common Error Responses

#### Invalid Audio File

```json
{
  "error": {
    "message": "Invalid or corrupted audio file",
    "type": "validation_error",
    "code": "INVALID_AUDIO"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@corrupted.wav" \
  -F "model=whisper-large-v3-turbo"
```

#### File Too Large

```json
{
  "error": {
    "message": "File size exceeds maximum limit of 100MB",
    "type": "validation_error",
    "code": "FILE_TOO_LARGE"
  }
}
```

#### Unsupported Format

```json
{
  "error": {
    "message": "Unsupported audio format. Supported formats: WAV, MP3, M4A, FLAC, OGG",
    "type": "validation_error",
    "code": "UNSUPPORTED_FORMAT"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@document.pdf" \
  -F "model=whisper-large-v3-turbo"
```

#### Model Not Found

```json
{
  "error": {
    "message": "Requested model 'whisper-small' not found",
    "type": "not_found_error",
    "code": "MODEL_NOT_FOUND"
  }
}
```

#### NPU Processing Error

```json
{
  "error": {
    "message": "NPU processing failed, falling back to CPU",
    "type": "server_error",
    "code": "NPU_ERROR",
    "details": {
      "fallback_used": true,
      "original_error": "QNN context initialization failed"
    }
  }
}
```

#### Server Not Running

```bash
curl http://localhost:8000/health
```

**Output:**
```
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

**Solution:** Start the AudioNPUAPI manager first.

---

## Tips and Best Practices

### 1. Server Management

```bash
# Always check server status before making requests
curl http://localhost:8000/health

# Monitor the AudioNPUAPI console for Python server logs
# Look for "[PYTHON]" prefixed messages

# For production, consider running as Windows Service
# (See whisper-server documentation)
```

### 2. Audio Format Optimization

```bash
# Convert audio to optimal format using ffmpeg
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav

# Reduce file size while maintaining quality
ffmpeg -i large_audio.wav -acodec libmp3lame -b:a 128k smaller_audio.mp3

# Extract specific time range
ffmpeg -i long_audio.wav -ss 00:01:30 -t 00:00:30 -c copy segment.wav
```

### 3. Language Detection

```bash
# Let the model auto-detect language
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@unknown_language.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "language=auto"

# Specify language for better accuracy
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@japanese.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "language=ja"
```

### 4. Use Appropriate Response Format

```bash
# For simple applications - use text
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=text"

# For detailed analysis - use verbose_json
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json"

# For video subtitles - use srt or vtt
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=srt"
```

### 5. Performance Optimization

```bash
# Chunk long audio files (>30 seconds) for better performance
ffmpeg -i long_audio.wav -f segment -segment_time 30 -c copy chunk%03d.wav

# Use NPU acceleration when available (automatic on Snapdragon X Elite)
# Check status to verify NPU is enabled
curl http://localhost:8000/status | grep npu_enabled

# Monitor performance metrics
curl http://localhost:8000/status | grep average_inference_time
```

### 6. Error Handling in Scripts

**PowerShell:**
```powershell
try {
    $uri = "http://localhost:8000/v1/audio/transcriptions"
    $form = @{
        file = Get-Item -Path "C:\Audio\audio.wav"
        model = "whisper-large-v3-turbo"
    }

    $result = Invoke-RestMethod -Uri $uri -Method Post -Form $form
    Write-Host "Success: $($result.text)"
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json

    Write-Host "Error ($statusCode): $($errorBody.error.message)" -ForegroundColor Red
    Write-Host "Code: $($errorBody.error.code)"
}
```

**Bash:**
```bash
response=$(curl -w "\n%{http_code}" -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ $http_code -eq 200 ]; then
    echo "Success: $body"
else
    echo "Error (HTTP $http_code): $body"
fi
```

### 7. Real-time Transcription Best Practices

```javascript
// Use proper audio format for WebSocket streaming
const audioContext = new AudioContext({
    sampleRate: 16000  // 16kHz required
});

// Enable VAD to reduce unnecessary processing
const config = {
    model: 'whisper-large-v3-turbo',
    language: 'auto',
    vad_enabled: true,
    energy_threshold: 1000
};

// Handle connection errors gracefully
ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    // Implement reconnection logic
    setTimeout(() => reconnect(), 5000);
};
```

### 8. Save Transcriptions with Metadata

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\interview.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
    language = "en"
    response_format = "verbose_json"
}

$result = Invoke-RestMethod -Uri $uri -Method Post -Form $form

# Create enriched output with metadata
$output = @{
    source_file = $filePath
    transcription = $result
    processed_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    model_used = "whisper-large-v3-turbo"
}

$output | ConvertTo-Json -Depth 10 | Out-File "C:\Output\interview_complete.json"
```

### 9. Monitor Server Health

```bash
# Create a health check script
while true; do
    response=$(curl -s http://localhost:8000/health)
    status=$(echo $response | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

    if [ "$status" == "healthy" ]; then
        echo "[$(date)] Server is healthy"
    else
        echo "[$(date)] Server is unhealthy!"
        # Send alert or restart server
    fi

    sleep 30
done
```

### 10. Use Timeouts for Long Files

**PowerShell:**
```powershell
$uri = "http://localhost:8000/v1/audio/transcriptions"
$filePath = "C:\Audio\long_audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-large-v3-turbo"
}

# Set timeout to 10 minutes for long files
Invoke-RestMethod -Uri $uri -Method Post -Form $form -TimeoutSec 600
```

---

## OpenAI API Compatibility

### Drop-in Replacement

The Whisper Server provides full OpenAI Whisper API compatibility:

**OpenAI API:**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
```

**AudioNPUAPI Whisper Server (Compatible):**
```python
from openai import OpenAI

client = OpenAI(
    api_key="not-needed",  # No API key required
    base_url="http://localhost:8000/v1"
)
transcription = client.audio.transcriptions.create(
    model="whisper-large-v3-turbo",
    file=audio_file
)
```

### Supported Parameters

| Parameter | OpenAI | AudioNPUAPI | Notes |
|-----------|--------|-------------|-------|
| file | ✓ | ✓ | Audio file to transcribe |
| model | ✓ | ✓ | Use "whisper-large-v3-turbo" |
| language | ✓ | ✓ | ISO-639-1 code or "auto" |
| prompt | ✓ | ✓ | Guidance text |
| response_format | ✓ | ✓ | json, text, srt, vtt, verbose_json |
| temperature | ✓ | ✓ | 0.0-1.0 |

---

## Performance Benchmarks

### Typical Processing Times

| Hardware | Model | Audio Duration | Processing Time | RTF |
|----------|-------|----------------|----------------|-----|
| Snapdragon X Elite (NPU) | large-v3-turbo | 30s | 1.5s | 0.05x |
| Snapdragon X Elite (NPU) | large-v3-turbo | 60s | 3.0s | 0.05x |
| Intel i7-12700K (CPU) | large-v3-turbo | 30s | 25s | 0.83x |
| Intel i7-12700K (CPU) | large-v3-turbo | 60s | 50s | 0.83x |

**RTF (Real-Time Factor)**: Lower is better. RTF < 1.0 means faster than real-time.

### Supported Audio Formats

- **WAV** - Recommended for best quality
- **MP3** - Good compression
- **M4A** - Apple audio format
- **FLAC** - Lossless compression
- **OGG** - Open format
- **WebM** - Web audio

### File Size Limits

- Maximum file size: 100MB (configurable)
- Recommended chunk size for streaming: 30 seconds
- Optimal sample rate: 16kHz

---

**Last Updated**: 2025-01-20
**AudioNPUAPI Version**: 1.0.0
**Whisper Server Version**: 2.0.0
**OpenAI Compatibility**: Full v1 Audio API

---

## Additional Resources

- [Whisper Server API Documentation](../../whisper-server-qnn/server/docs/API.md)
- [Whisper Server Setup Guide](../../whisper-server-qnn/server/docs/SETUP.md)
- [OpenAI Whisper API Reference](https://platform.openai.com/docs/api-reference/audio)
- [Qualcomm AI Hub Models](https://aihub.qualcomm.com/)

---

## Quick Reference

### Common Operations

```bash
# Start manager
cd src\IB-Link.AudioNPUAPI && dotnet run

# Check health
curl http://localhost:8000/health

# Basic transcription
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" -F "model=whisper-large-v3-turbo"

# With language
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" -F "model=whisper-large-v3-turbo" -F "language=ja"

# Verbose output
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" -F "model=whisper-large-v3-turbo" -F "response_format=verbose_json"

# Translation to English
curl -X POST http://localhost:8000/v1/audio/translations \
  -F "file=@audio.wav" -F "model=whisper-large-v3-turbo"

# Generate subtitles
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" -F "model=whisper-large-v3-turbo" -F "response_format=srt"
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `400 Bad Request` - Invalid parameters or audio format
- `404 Not Found` - Model not found
- `408 Request Timeout` - Processing timeout
- `413 Payload Too Large` - File exceeds size limit
- `415 Unsupported Media Type` - Unsupported audio format
- `500 Internal Server Error` - Server error (NPU error with fallback)
