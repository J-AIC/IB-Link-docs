# AudioAPI - Usage Examples

Complete guide with practical examples for all AudioAPI endpoints.

**Base URL**: `http://localhost:7000/iblink/v1`

**OpenAI Compatibility**: Full compatibility with OpenAI Audio API v1 specification

---

## Table of Contents

- [Audio Transcription](#audio-transcription)
  - [Basic Transcription](#basic-transcription)
  - [Transcription with Language](#transcription-with-language)
  - [Verbose JSON Output](#verbose-json-output)
  - [Text-Only Output](#text-only-output)
  - [SRT Subtitle Format](#srt-subtitle-format)
  - [VTT Subtitle Format](#vtt-subtitle-format)
  - [Enhanced Transcription](#enhanced-transcription-ib-link-extension)
  - [Force Specific Provider](#force-specific-provider)
  - [Batch Processing](#batch-processing-ib-link-extension)
  - [Performance Benchmark](#performance-benchmark-ib-link-extension)
- [Health and Monitoring](#health-and-monitoring)
  - [Health Check](#get-health)
  - [System Information](#get-system-info)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Error Handling](#error-handling-examples)
- [Tips and Best Practices](#tips-and-best-practices)

---

## Audio Transcription

### Basic Transcription

Transcribe an audio file using the default JSON response format.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.mp3" \
  -F "model=whisper-1"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.mp3"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "text": "This is the transcribed text from the audio file."
}
```

---

### Transcription with Language

Specify the input language to improve accuracy and latency.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-1" \
  -F "language=en"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    language = "en"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Supported Languages:**
- `en` - English
- `ja` - Japanese
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh` - Chinese
- And many more (ISO-639-1 format)

**Response:**
```json
{
  "text": "This is the transcribed text in English."
}
```

---

### Verbose JSON Output

Get detailed transcription information including segments and metadata.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=verbose_json"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.mp3"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    response_format = "verbose_json"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "task": "transcribe",
  "language": "en",
  "duration": 10.5,
  "text": "This is the complete transcribed text.",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 10.5,
      "text": "This is the complete transcribed text.",
      "tokens": [],
      "temperature": 0.0,
      "avg_logprob": -0.5,
      "compression_ratio": 1.0,
      "no_speech_prob": 0.0
    }
  ]
}
```

---

### Text-Only Output

Get plain text output without JSON formatting.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-1" \
  -F "response_format=text"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    response_format = "text"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```
This is the transcribed text from the audio file.
```

---

### SRT Subtitle Format

Generate SRT (SubRip) subtitle format for video applications.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@video_audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=srt"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\video_audio.mp3"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    response_format = "srt"
}

$result = Invoke-RestMethod -Uri $uri -Method Post -Form $form
$result | Out-File -FilePath "C:\Output\subtitles.srt" -Encoding UTF8
```

**Response:**
```
1
00:00:00,000 --> 00:00:10,500
This is the transcribed text from the audio file.

```

---

### VTT Subtitle Format

Generate WebVTT subtitle format for web video players.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@video_audio.wav" \
  -F "model=whisper-1" \
  -F "response_format=vtt"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\video_audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    response_format = "vtt"
}

$result = Invoke-RestMethod -Uri $uri -Method Post -Form $form
$result | Out-File -FilePath "C:\Output\subtitles.vtt" -Encoding UTF8
```

**Response:**
```
WEBVTT

00:00:00.000 --> 00:00:10.500
This is the transcribed text from the audio file.

```

---

### Enhanced Transcription (IB-Link Extension)

Get transcription with hardware acceleration details and performance metrics.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "_enhanced=true"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.mp3"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    _enhanced = "true"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "text": "This is the transcribed text.",
  "_enhanced": {
    "language": "en",
    "duration": 10.5,
    "processing_time_ms": 525.3,
    "real_time_factor": 0.05,
    "provider": "QNN",
    "hardware_info": {
      "hasQNNProvider": true,
      "hasDirectML": false,
      "hasCUDA": false,
      "isSnapdragonXElite": true,
      "recommendedProvider": "QNN",
      "availableProviders": ["QNN", "CPU"],
      "systemInfo": "Windows 11 ARM64",
      "cpuInfo": "Snapdragon(R) X Elite - X1E80100",
      "npuInfo": "Qualcomm Hexagon NPU"
    },
    "performance_metrics": {
      "sessionId": "session_12345",
      "provider": "QNN",
      "totalProcessingTimeMs": 525.3,
      "modelLoadTimeMs": 120.5,
      "inferenceTimeMs": 404.8,
      "audioDurationSeconds": 10.5,
      "realTimeFactor": 0.05,
      "memoryUsageMB": 245.6
    }
  }
}
```

---

### Force Specific Provider

Force the use of a specific hardware acceleration provider.

**Available Providers:**
- `auto` - Automatic selection (default)
- `qnn` - Qualcomm Neural Network (NPU)
- `directml` - DirectML GPU acceleration
- `cpu` - CPU-only processing
- `legacy` - Legacy service implementation

**cURL (Force QNN):**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-1" \
  -F "_provider=qnn" \
  -F "_enhanced=true"
```

**cURL (Force CPU):**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-1" \
  -F "_provider=cpu"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    _provider = "qnn"
    _enhanced = "true"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "text": "Transcribed using QNN provider.",
  "_enhanced": {
    "provider": "QNN",
    "real_time_factor": 0.05,
    "hardware_info": {
      "hasQNNProvider": true,
      "isSnapdragonXElite": true
    }
  }
}
```

---

### Batch Processing (IB-Link Extension)

Process multiple audio files in a single request for improved efficiency.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "files=@audio1.mp3" \
  -F "files=@audio2.wav" \
  -F "files=@audio3.m4a" \
  -F "model=whisper-1" \
  -F "_batch=true"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"

# Create multipart form data manually
$boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"

$bodyLines = @(
    "--$boundary",
    "Content-Disposition: form-data; name=`"files`"; filename=`"audio1.mp3`"",
    "Content-Type: audio/mpeg$LF",
    [System.IO.File]::ReadAllBytes("C:\Audio\audio1.mp3"),
    "--$boundary",
    "Content-Disposition: form-data; name=`"files`"; filename=`"audio2.wav`"",
    "Content-Type: audio/wav$LF",
    [System.IO.File]::ReadAllBytes("C:\Audio\audio2.wav"),
    "--$boundary",
    "Content-Disposition: form-data; name=`"model`"$LF",
    "whisper-1",
    "--$boundary",
    "Content-Disposition: form-data; name=`"_batch`"$LF",
    "true",
    "--$boundary--$LF"
)

Invoke-RestMethod -Uri $uri -Method Post -ContentType "multipart/form-data; boundary=$boundary" -Body $bodyLines
```

**Response:**
```json
{
  "batch_results": [
    {
      "file": "audio1.mp3",
      "text": "Transcription of first file.",
      "language": "en",
      "success": true
    },
    {
      "file": "audio2.wav",
      "text": "Transcription of second file.",
      "language": "en",
      "success": true
    },
    {
      "file": "audio3.m4a",
      "text": "Transcription of third file.",
      "language": "ja",
      "success": true
    }
  ],
  "total_files": 3,
  "successful_files": 3
}
```

---

### Performance Benchmark (IB-Link Extension)

Run performance benchmarks to test transcription speed and consistency.

**cURL:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@benchmark_audio.wav" \
  -F "model=whisper-1" \
  -F "_benchmark=10" \
  -F "_provider=qnn"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$filePath = "C:\Audio\benchmark_audio.wav"

$form = @{
    file = Get-Item -Path $filePath
    model = "whisper-1"
    _benchmark = "10"
    _provider = "qnn"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response:**
```json
{
  "benchmark_results": {
    "iterations": 10,
    "average_rtf": 0.052,
    "min_rtf": 0.048,
    "max_rtf": 0.061,
    "results": [0.051, 0.048, 0.053, 0.052, 0.049, 0.055, 0.050, 0.061, 0.049, 0.052]
  },
  "provider": "QNN",
  "audio_duration": 10.5
}
```

**RTF (Real-Time Factor) Interpretation:**
- **RTF < 1.0**: Faster than real-time (can process audio faster than playback)
- **RTF = 1.0**: Real-time processing (processes at playback speed)
- **RTF > 1.0**: Slower than real-time (takes longer to process than audio duration)

---

## Health and Monitoring

### GET /health

Check API health status with hardware capabilities and performance information.

**cURL:**
```bash
curl http://localhost:7000/iblink/v1/audio/health
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:7000/iblink/v1/audio/health"
```

**Response (Snapdragon X Elite with QNN):**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "service": "IB-Link Audio API",
  "version": "2.0.0",
  "openai_compatibility": "Full",
  "whisperService": "available",
  "hardware": {
    "hasQNNProvider": true,
    "hasDirectML": false,
    "hasCUDA": false,
    "isSnapdragonXElite": true,
    "recommendedProvider": "QNN",
    "availableProviders": ["QNN", "CPU"],
    "systemInfo": "Windows 11 ARM64",
    "cpuInfo": "Snapdragon(R) X Elite - X1E80100",
    "npuInfo": "Qualcomm Hexagon NPU",
    "socInfo": "Snapdragon X Elite"
  },
  "isInitialized": true,
  "activeProvider": "QNN",
  "performanceMetrics": {
    "sessionId": "main_session",
    "provider": "QNN",
    "totalCalls": 156,
    "successCount": 155,
    "failureCount": 1,
    "averageLatency": 52.3,
    "totalDuration": "01:45:23",
    "peakMemoryUsage": 512.8
  },
  "recommendations": {
    "optimalProvider": "QNN",
    "supportsQNN": true,
    "message": "🚀 Snapdragon X Elite detected with QNN support - optimal performance available!"
  }
}
```

**Response (x64 with DirectML):**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "service": "IB-Link Audio API",
  "version": "2.0.0",
  "openai_compatibility": "Full",
  "whisperService": "available",
  "hardware": {
    "hasQNNProvider": false,
    "hasDirectML": true,
    "hasCUDA": false,
    "isSnapdragonXElite": false,
    "recommendedProvider": "DirectML",
    "availableProviders": ["DirectML", "CPU"],
    "systemInfo": "Windows 11 x64",
    "cpuInfo": "Intel(R) Core(TM) i7-12700K",
    "gpuInfo": "NVIDIA GeForce RTX 3060"
  },
  "isInitialized": true,
  "activeProvider": "DirectML",
  "performanceMetrics": {
    "averageLatency": 125.6,
    "successCount": 89
  },
  "recommendations": {
    "optimalProvider": "DirectML",
    "supportsQNN": false,
    "message": "DirectML GPU acceleration available"
  }
}
```

**Response (CPU-only):**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "service": "IB-Link Audio API",
  "version": "2.0.0",
  "openai_compatibility": "Full",
  "whisperService": "available",
  "hardware": {
    "hasQNNProvider": false,
    "hasDirectML": false,
    "hasCUDA": false,
    "isSnapdragonXElite": false,
    "recommendedProvider": "CPU",
    "availableProviders": ["CPU"],
    "systemInfo": "Windows 11 x64",
    "cpuInfo": "AMD Ryzen 5 5600X"
  },
  "isInitialized": true,
  "activeProvider": "CPU",
  "recommendations": {
    "message": "CPU-only mode - consider hardware acceleration"
  }
}
```

---

### GET /system/info

Get detailed system information and optimization recommendations.

**cURL:**
```bash
curl http://localhost:7000/iblink/v1/audio/system/info
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:7000/iblink/v1/audio/system/info"
```

**Response:**
```json
{
  "service": "IB-Link Audio API",
  "version": "2.0.0",
  "openai_compatibility": "Full",
  "timestamp": "2025-01-20T10:30:00Z",
  "hardware_capabilities": {
    "hasQNNProvider": true,
    "hasDirectML": false,
    "hasCUDA": false,
    "isSnapdragonXElite": true,
    "recommendedProvider": "QNN",
    "availableProviders": ["QNN", "CPU"],
    "systemInfo": "Windows 11 ARM64",
    "cpuInfo": "Snapdragon(R) X Elite - X1E80100",
    "npuInfo": "Qualcomm Hexagon NPU"
  },
  "performance_metrics": {
    "sessionId": "main_session",
    "provider": "QNN",
    "averageLatency": 52.3,
    "realTimeFactor": 0.05,
    "memoryUsageMB": 245.6
  },
  "active_provider": "QNN",
  "optimization_tips": {
    "tips": [
      "🚀 Snapdragon X Elite with QNN detected - optimal NPU acceleration active",
      "💡 Using EP Context models for instant loading"
    ],
    "performance_category": "Optimal (NPU)"
  }
}
```

---

## Complete Workflow Examples

### Workflow 1: Basic Transcription Workflow

```bash
# 1. Check API health
curl http://localhost:7000/iblink/v1/audio/health

# 2. Transcribe a simple audio file
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@meeting_recording.mp3" \
  -F "model=whisper-1" \
  -F "language=en" \
  -F "response_format=json"

# 3. Save transcription to file
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@meeting_recording.mp3" \
  -F "model=whisper-1" \
  -F "response_format=text" \
  -o transcription.txt
```

### Workflow 2: Video Subtitle Generation

```bash
# 1. Extract audio from video (using ffmpeg)
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# 2. Generate SRT subtitles
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-1" \
  -F "language=en" \
  -F "response_format=srt" \
  -o subtitles.srt

# 3. Generate VTT subtitles for web
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-1" \
  -F "language=en" \
  -F "response_format=vtt" \
  -o subtitles.vtt

# 4. Merge subtitles back to video (using ffmpeg)
ffmpeg -i video.mp4 -i subtitles.srt -c copy -c:s mov_text output_with_subs.mp4
```

### Workflow 3: Batch Processing Multiple Files

```bash
# 1. Check system capabilities
curl http://localhost:7000/iblink/v1/audio/system/info

# 2. Process all files in batch
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "files=@lecture_part1.mp3" \
  -F "files=@lecture_part2.mp3" \
  -F "files=@lecture_part3.mp3" \
  -F "files=@lecture_part4.mp3" \
  -F "model=whisper-1" \
  -F "language=en" \
  -F "_batch=true" \
  -o batch_results.json

# 3. Process results and create individual files
# (Use jq or PowerShell to parse JSON and save individual transcriptions)
```

### Workflow 4: Performance Testing and Optimization

```bash
# 1. Test with CPU provider
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@test_audio.wav" \
  -F "model=whisper-1" \
  -F "_provider=cpu" \
  -F "_benchmark=5" \
  -o benchmark_cpu.json

# 2. Test with QNN provider (if available)
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@test_audio.wav" \
  -F "model=whisper-1" \
  -F "_provider=qnn" \
  -F "_benchmark=5" \
  -o benchmark_qnn.json

# 3. Test with DirectML provider (if available)
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@test_audio.wav" \
  -F "model=whisper-1" \
  -F "_provider=directml" \
  -F "_benchmark=5" \
  -o benchmark_directml.json

# 4. Compare results
# (Parse JSON files to compare average_rtf values)
```

### Workflow 5: Multi-Language Transcription

```bash
# 1. Auto-detect language
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@multilingual.mp3" \
  -F "model=whisper-1" \
  -F "response_format=verbose_json" \
  -o auto_detected.json

# 2. Transcribe English audio
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@english_audio.mp3" \
  -F "model=whisper-1" \
  -F "language=en"

# 3. Transcribe Japanese audio
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@japanese_audio.wav" \
  -F "model=whisper-1" \
  -F "language=ja"

# 4. Transcribe Spanish audio
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@spanish_audio.m4a" \
  -F "model=whisper-1" \
  -F "language=es"
```

---

## Error Handling Examples

### Error Response Format

All errors follow this format:

```json
{
  "error": {
    "message": "Human-readable error message",
    "type": "error_type",
    "param": "parameter_name",
    "code": "error_code"
  }
}
```

### Common Error Responses

#### Missing Required Parameter

```json
{
  "error": {
    "message": "Missing required parameter: 'file'",
    "type": "invalid_request_error",
    "param": "file",
    "code": "missing_required_parameter"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "model=whisper-1"
```

#### Invalid Response Format

```json
{
  "error": {
    "message": "Invalid value for 'response_format': xml. Must be one of: json, text, srt, verbose_json, vtt",
    "type": "invalid_request_error",
    "param": "response_format",
    "code": "invalid_parameter_value"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=xml"
```

#### Invalid Temperature Value

```json
{
  "error": {
    "message": "Invalid value for 'temperature': must be between 0 and 1",
    "type": "invalid_request_error",
    "param": "temperature",
    "code": "invalid_parameter_value"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "temperature=1.5"
```

#### Invalid Audio Format

```json
{
  "error": {
    "message": "Invalid audio file format: Unsupported file type",
    "type": "invalid_request_error",
    "code": "invalid_file_format"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@document.pdf" \
  -F "model=whisper-1"
```

#### No Speech Detected

```json
{
  "error": {
    "message": "No speech detected in audio file",
    "type": "invalid_request_error",
    "code": "no_speech_detected"
  }
}
```

#### Service Unavailable

```json
{
  "error": {
    "message": "The engine is currently overloaded, please try again later",
    "type": "server_error",
    "code": "engine_overloaded"
  }
}
```

#### Request Cancelled

```json
{
  "error": {
    "message": "Request was cancelled",
    "type": "request_cancelled"
  }
}
```

#### Internal Server Error

```json
{
  "error": {
    "message": "Internal server error",
    "type": "server_error",
    "code": "internal_error"
  }
}
```

---

## Tips and Best Practices

### 1. Choose the Right Response Format

```bash
# For programmatic processing - use JSON
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=json"

# For detailed analysis - use verbose_json
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=verbose_json"

# For simple text output - use text
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=text"

# For video subtitles - use srt or vtt
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=srt"
```

### 2. Specify Language When Known

```bash
# Improves accuracy and reduces latency
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@english_audio.mp3" \
  -F "model=whisper-1" \
  -F "language=en"

# Let the model auto-detect when uncertain
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@unknown_language.mp3" \
  -F "model=whisper-1"
```

### 3. Use Batch Processing for Multiple Files

```bash
# More efficient than individual requests
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "files=@file1.mp3" \
  -F "files=@file2.mp3" \
  -F "files=@file3.mp3" \
  -F "model=whisper-1" \
  -F "_batch=true"
```

### 4. Monitor Performance with Enhanced Mode

```bash
# Get detailed performance metrics
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "_enhanced=true"
```

### 5. Use Appropriate Provider for Hardware

```bash
# On Snapdragon X Elite - use QNN for best performance
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "_provider=qnn"

# On x64 with GPU - use DirectML
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "_provider=directml"

# For compatibility - use auto
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "_provider=auto"
```

### 6. Audio File Preparation

```bash
# Convert to optimal format using ffmpeg
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav

# Extract audio from video
ffmpeg -i video.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3

# Reduce file size while maintaining quality
ffmpeg -i large_audio.wav -acodec libmp3lame -b:a 128k smaller_audio.mp3
```

### 7. Handle Large Files

```bash
# For files longer than 30 seconds, the API automatically uses
# DecodeEntireFile method for better results

# Split very long files into chunks if needed
ffmpeg -i long_audio.mp3 -f segment -segment_time 300 -c copy output%03d.mp3

# Then process as batch
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "files=@output000.mp3" \
  -F "files=@output001.mp3" \
  -F "files=@output002.mp3" \
  -F "model=whisper-1" \
  -F "_batch=true"
```

### 8. Error Handling in Scripts

```bash
# Capture HTTP status code
response=$(curl -w "\n%{http_code}" -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ $http_code -eq 200 ]; then
    echo "Success: $body"
else
    echo "Error (HTTP $http_code): $body"
fi
```

**PowerShell Error Handling:**
```powershell
try {
    $uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
    $form = @{
        file = Get-Item -Path "C:\Audio\audio.mp3"
        model = "whisper-1"
    }

    $result = Invoke-RestMethod -Uri $uri -Method Post -Form $form
    Write-Host "Success: $($result.text)"
}
catch {
    $errorDetails = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "Error: $($errorDetails.error.message)"
    Write-Host "Code: $($errorDetails.error.code)"
}
```

### 9. Save Output to File

```bash
# Save JSON response
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=json" \
  -o transcription.json

# Save text response
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=text" \
  -o transcription.txt

# Save SRT subtitles
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=srt" \
  -o subtitles.srt
```

### 10. Use Timeouts for Long Audio

```bash
# Set appropriate timeout for long files
curl --max-time 600 -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@long_audio.mp3" \
  -F "model=whisper-1"
```

**PowerShell:**
```powershell
$uri = "http://localhost:7000/iblink/v1/audio/transcriptions"
$form = @{
    file = Get-Item -Path "C:\Audio\long_audio.mp3"
    model = "whisper-1"
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form -TimeoutSec 600
```

---

## OpenAI Compatibility Notes

### Fully Compatible Parameters

These parameters work exactly as in OpenAI's Audio API:

- `file` - Audio file to transcribe
- `model` - Model ID (use "whisper-1")
- `language` - ISO-639-1 language code
- `prompt` - Optional text to guide transcription
- `response_format` - Output format (json, text, srt, verbose_json, vtt)
- `temperature` - Sampling temperature (0-1)

### IB-Link Extensions

These additional parameters are specific to IB-Link Audio API:

- `_provider` - Force specific hardware acceleration provider
- `_enhanced` - Include hardware and performance information
- `_batch` - Enable batch processing mode
- `_benchmark` - Run performance benchmarks
- `files` - Multiple files for batch processing

### Drop-in Replacement

You can use this API as a drop-in replacement for OpenAI's Audio API:

```bash
# OpenAI API call
curl -X POST https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "file=@audio.mp3" \
  -F "model=whisper-1"

# IB-Link API call (identical parameters)
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1"
```

---

## Performance Benchmarks

### Typical Real-Time Factors (RTF)

| Provider | Hardware | Typical RTF | Performance |
|----------|----------|-------------|-------------|
| QNN | Snapdragon X Elite | 0.05-0.10 | Excellent |
| DirectML | NVIDIA RTX 3060 | 0.20-0.40 | Very Good |
| DirectML | AMD RX 6800 | 0.25-0.50 | Good |
| CPU | Intel i7-12700K | 0.80-1.50 | Moderate |
| CPU | AMD Ryzen 5 5600X | 0.90-1.60 | Moderate |

**Note:** Lower RTF is better. RTF < 1.0 means faster than real-time processing.

### Supported Audio Formats

- **WAV** - Recommended for best quality
- **MP3** - Good balance of size and quality
- **M4A** - Apple audio format
- **FLAC** - Lossless compression
- **WebM** - Web audio format
- **OGG** - Open format
- **MP4/MPEG/MPGA** - Video audio tracks

---

**Last Updated**: 2025-01-20
**API Version**: 2.0.0
**Documentation**: `src/IB-Link.AudioAPI/README.md`
**OpenAI Compatibility**: Full v1 Audio API

---

## Additional Resources

- [AudioAPI Technical Documentation](../IB-Link.AudioAPI/AudioAPI_Documentation.md)
- [OpenAI Audio API Reference](https://platform.openai.com/docs/api-reference/audio)
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)
- [Whisper Model Information](https://github.com/openai/whisper)

---

## Quick Reference

### Common cURL Patterns

```bash
# Basic transcription
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" -F "model=whisper-1"

# With language
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" -F "model=whisper-1" -F "language=en"

# Enhanced mode
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" -F "model=whisper-1" -F "_enhanced=true"

# Batch processing
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "files=@file1.mp3" -F "files=@file2.mp3" -F "model=whisper-1" -F "_batch=true"

# Benchmark
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" -F "model=whisper-1" -F "_benchmark=10"

# Health check
curl http://localhost:7000/iblink/v1/audio/health
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `400 Bad Request` - Invalid parameters or audio format
- `499 Client Closed Request` - Request was cancelled
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service overloaded or unavailable
