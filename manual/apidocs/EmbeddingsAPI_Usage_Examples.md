# EmbeddingsAPI - Usage Examples

Complete guide with practical examples for all EmbeddingsAPI endpoints.

**Base URL**: `http://localhost:5000/iblink/v1`

**Purpose**: Generate text embeddings using local ONNX models with OpenAI API compatibility.

**OpenAI Compatibility**: Full compatibility with OpenAI Embeddings API specification

---

## Table of Contents

- [Embeddings Generation](#embeddings-generation)
  - [Single Text Embedding](#single-text-embedding)
  - [Batch Embeddings](#batch-embeddings)
  - [With Encoding Format](#with-encoding-format)
  - [Custom Dimensions](#custom-dimensions)
- [Model Management](#model-management)
  - [List Models](#get-models)
  - [Get Model Info](#get-modelmodelid)
- [Health and Monitoring](#health-and-monitoring)
  - [Health Check](#get-embeddingshealth)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Error Handling](#error-handling-examples)
- [Tips and Best Practices](#tips-and-best-practices)

---

## Embeddings Generation

### Single Text Embedding

Generate an embedding vector for a single text input.

**cURL:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "The quick brown fox jumps over the lazy dog",
    "model": "all-MiniLM-L6-v2"
  }'
```

**PowerShell:**
```powershell
$body = @{
    input = "The quick brown fox jumps over the lazy dog"
    model = "all-MiniLM-L6-v2"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        0.023064375,
        -0.009327292,
        0.015797347,
        ...
        0.012345678
      ],
      "index": 0
    }
  ],
  "model": "all-MiniLM-L6-v2",
  "usage": {
    "prompt_tokens": 12,
    "total_tokens": 12
  }
}
```

**Note:** The embedding array typically contains 384 or 768 dimensions depending on the model.

---

### Batch Embeddings

Generate embeddings for multiple texts in a single request.

**cURL:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      "The quick brown fox jumps over the lazy dog",
      "Machine learning is a subset of artificial intelligence",
      "Natural language processing enables computers to understand human language"
    ],
    "model": "all-MiniLM-L6-v2"
  }'
```

**PowerShell:**
```powershell
$body = @{
    input = @(
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Natural language processing enables computers to understand human language"
    )
    model = "all-MiniLM-L6-v2"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.023064375, -0.009327292, ...],
      "index": 0
    },
    {
      "object": "embedding",
      "embedding": [0.015234567, -0.012345678, ...],
      "index": 1
    },
    {
      "object": "embedding",
      "embedding": [0.018765432, -0.011234567, ...],
      "index": 2
    }
  ],
  "model": "all-MiniLM-L6-v2",
  "usage": {
    "prompt_tokens": 45,
    "total_tokens": 45
  }
}
```

---

### With Encoding Format

Specify the encoding format for the embeddings (float or base64).

**Float Format (Default):**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Sample text for embedding",
    "model": "all-MiniLM-L6-v2",
    "encoding_format": "float"
  }'
```

**PowerShell:**
```powershell
$body = @{
    input = "Sample text for embedding"
    model = "all-MiniLM-L6-v2"
    encoding_format = "float"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response (Float):**
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.023064375, -0.009327292, 0.015797347, ...],
      "index": 0
    }
  ],
  "model": "all-MiniLM-L6-v2",
  "usage": {
    "prompt_tokens": 6,
    "total_tokens": 6
  }
}
```

---

### Custom Dimensions

Request embeddings with specific dimensions (if supported by the model).

**cURL:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Sample text for embedding",
    "model": "all-MiniLM-L6-v2",
    "dimensions": 384
  }'
```

**PowerShell:**
```powershell
$body = @{
    input = "Sample text for embedding"
    model = "all-MiniLM-L6-v2"
    dimensions = 384
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Note:** The `dimensions` parameter may not be supported by all models. The actual output dimensions depend on the model architecture.

---

### Multi-Language Embeddings

Generate embeddings for text in different languages.

**English:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hello, how are you?",
    "model": "all-MiniLM-L6-v2"
  }'
```

**Japanese:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "こんにちは、お元気ですか？",
    "model": "all-MiniLM-L6-v2"
  }'
```

**Spanish:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hola, ¿cómo estás?",
    "model": "all-MiniLM-L6-v2"
  }'
```

**Chinese:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "你好，你好吗？",
    "model": "all-MiniLM-L6-v2"
  }'
```

**PowerShell:**
```powershell
$body = @{
    input = "こんにちは、お元気ですか？"
    model = "all-MiniLM-L6-v2"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

### Long Text Handling

The API automatically truncates text that exceeds the model's maximum sequence length.

**cURL:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "This is a very long text that exceeds the maximum sequence length...",
    "model": "all-MiniLM-L6-v2"
  }'
```

**Note:**
- Maximum sequence length is typically 512 tokens
- Text exceeding this limit will be truncated
- A warning will be logged but the request will succeed

---

## Model Management

### GET /models

List all available embedding models.

**cURL:**
```bash
curl http://localhost:5000/iblink/v1/models
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/models"
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "all-MiniLM-L6-v2",
      "object": "model",
      "created": 1705743600,
      "owned_by": "local"
    }
  ]
}
```

---

### GET /models/{modelId}

Get information about a specific model.

**cURL:**
```bash
curl http://localhost:5000/iblink/v1/models/all-MiniLM-L6-v2
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/models/all-MiniLM-L6-v2"
```

**Response:**
```json
{
  "id": "all-MiniLM-L6-v2",
  "object": "model",
  "created": 1705743600,
  "owned_by": "local"
}
```

**Error Response (Model Not Found):**
```json
{
  "error": {
    "message": "The model 'nonexistent-model' does not exist",
    "type": "invalid_request_error",
    "code": "model_not_found"
  }
}
```

---

## Health and Monitoring

### GET /embeddings/health

Check the health status of the Embeddings API.

**cURL:**
```bash
curl http://localhost:5000/iblink/v1/embeddings/health
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "service": "embeddings-api",
  "model": "all-MiniLM-L6-v2",
  "version": "1.0.0"
}
```

**Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "error": "ONNX model failed to load"
}
```

---

## Complete Workflow Examples

### Workflow 1: Basic Embedding Generation

```bash
# 1. Check API health
curl http://localhost:5000/iblink/v1/embeddings/health

# 2. List available models
curl http://localhost:5000/iblink/v1/models

# 3. Generate embedding for single text
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Machine learning is transforming technology",
    "model": "all-MiniLM-L6-v2"
  }' | jq '.data[0].embedding | length'

# Output: 384 (dimension size)
```

### Workflow 2: Batch Processing with PowerShell

```powershell
# Check health
$health = Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings/health"
Write-Host "API Status: $($health.status)"

# Prepare batch of texts
$texts = @(
    "The first document about machine learning",
    "The second document about neural networks",
    "The third document about deep learning",
    "The fourth document about AI applications"
)

# Generate embeddings in batch
$body = @{
    input = $texts
    model = "all-MiniLM-L6-v2"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Display results
Write-Host "Generated $($response.data.Count) embeddings"
Write-Host "Token usage: $($response.usage.total_tokens)"

# Save embeddings to file
$response | ConvertTo-Json -Depth 10 | Out-File "embeddings_output.json"
```

### Workflow 3: Similarity Search Preparation

```bash
# Generate embeddings for a corpus of documents
documents=(
  "Document 1: Introduction to machine learning"
  "Document 2: Deep learning fundamentals"
  "Document 3: Natural language processing basics"
  "Document 4: Computer vision applications"
)

# Create JSON array
json_input=$(printf '%s\n' "${documents[@]}" | jq -R . | jq -s .)

# Generate embeddings
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d "{
    \"input\": $json_input,
    \"model\": \"all-MiniLM-L6-v2\"
  }" > document_embeddings.json

# Generate query embedding
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is deep learning?",
    "model": "all-MiniLM-L6-v2"
  }' > query_embedding.json

# Now use these embeddings for cosine similarity calculation
```

### Workflow 4: Integration with Python

```python
import requests
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# API endpoint
api_url = "http://localhost:5000/iblink/v1/embeddings"

# Generate embeddings
def get_embedding(text):
    response = requests.post(
        api_url,
        json={
            "input": text,
            "model": "all-MiniLM-L6-v2"
        }
    )
    return response.json()["data"][0]["embedding"]

# Example texts
texts = [
    "Machine learning is a branch of AI",
    "Neural networks are used in deep learning",
    "Python is a popular programming language"
]

# Generate embeddings
embeddings = [get_embedding(text) for text in texts]

# Calculate similarity matrix
similarity_matrix = cosine_similarity(embeddings)
print("Similarity matrix:")
print(similarity_matrix)
```

### Workflow 5: Batch Processing Large Dataset

```bash
# Process large dataset in batches
input_file="documents.txt"
batch_size=10
output_file="embeddings.jsonl"

# Read file and process in batches
while IFS= read -r line; do
    batch+=("$line")

    if [ ${#batch[@]} -eq $batch_size ]; then
        # Create JSON array
        json_input=$(printf '%s\n' "${batch[@]}" | jq -R . | jq -s .)

        # Generate embeddings
        curl -X POST http://localhost:5000/iblink/v1/embeddings \
          -H "Content-Type: application/json" \
          -d "{
            \"input\": $json_input,
            \"model\": \"all-MiniLM-L6-v2\"
          }" >> "$output_file"

        # Clear batch
        batch=()
    fi
done < "$input_file"

# Process remaining items
if [ ${#batch[@]} -gt 0 ]; then
    json_input=$(printf '%s\n' "${batch[@]}" | jq -R . | jq -s .)
    curl -X POST http://localhost:5000/iblink/v1/embeddings \
      -H "Content-Type: application/json" \
      -d "{
        \"input\": $json_input,
        \"model\": \"all-MiniLM-L6-v2\"
      }" >> "$output_file"
fi
```

---

## Error Handling Examples

### Error Response Format

```json
{
  "error": {
    "message": "Error description",
    "type": "error_type",
    "code": "error_code"
  }
}
```

### Common Error Responses

#### Missing Input Parameter

```json
{
  "error": {
    "message": "Missing required parameter 'input'",
    "type": "invalid_request_error",
    "code": "missing_parameter"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "all-MiniLM-L6-v2"
  }'
```

#### Empty Input

```json
{
  "error": {
    "message": "Input cannot be empty",
    "type": "invalid_request_error",
    "code": "invalid_input"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "",
    "model": "all-MiniLM-L6-v2"
  }'
```

#### Model Not Found

```json
{
  "error": {
    "message": "The model 'invalid-model' does not exist",
    "type": "invalid_request_error",
    "code": "model_not_found"
  }
}
```

**Example Request:**
```bash
curl http://localhost:5000/iblink/v1/models/invalid-model
```

#### Internal Server Error

```json
{
  "error": {
    "message": "Internal server error occurred while processing embeddings",
    "type": "api_error"
  }
}
```

**HTTP Status:** 500

---

## Tips and Best Practices

### 1. Use Batch Requests for Multiple Texts

```bash
# Efficient: Single request for multiple texts
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": ["text1", "text2", "text3"],
    "model": "all-MiniLM-L6-v2"
  }'

# Inefficient: Multiple requests
for text in "text1" "text2" "text3"; do
  curl -X POST http://localhost:5000/iblink/v1/embeddings \
    -H "Content-Type: application/json" \
    -d "{\"input\": \"$text\", \"model\": \"all-MiniLM-L6-v2\"}"
done
```

### 2. Handle Text Truncation

```bash
# Pre-process long texts before sending
max_chars=2000  # Approximate max (512 tokens ≈ 2000 chars)

if [ ${#text} -gt $max_chars ]; then
    text="${text:0:$max_chars}"
fi

curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d "{
    \"input\": \"$text\",
    \"model\": \"all-MiniLM-L6-v2\"
  }"
```

### 3. Optimize Batch Size

```bash
# Optimal batch size for local processing
optimal_batch_size=20

# Too large may cause memory issues
# Too small doesn't utilize batching benefits
```

**PowerShell:**
```powershell
$optimalBatchSize = 20
$allTexts = @(...) # Your full dataset

# Process in optimal batches
for ($i = 0; $i -lt $allTexts.Count; $i += $optimalBatchSize) {
    $batch = $allTexts[$i..([Math]::Min($i + $optimalBatchSize - 1, $allTexts.Count - 1))]

    $body = @{
        input = $batch
        model = "all-MiniLM-L6-v2"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"

    # Process response...
}
```

### 4. Cache Embeddings

```bash
# Calculate hash of text
text_hash=$(echo -n "$text" | sha256sum | cut -d' ' -f1)
cache_file="cache/${text_hash}.json"

# Check if cached
if [ -f "$cache_file" ]; then
    embedding=$(cat "$cache_file")
else
    # Generate and cache
    embedding=$(curl -X POST http://localhost:5000/iblink/v1/embeddings \
      -H "Content-Type: application/json" \
      -d "{\"input\": \"$text\", \"model\": \"all-MiniLM-L6-v2\"}")

    echo "$embedding" > "$cache_file"
fi
```

### 5. Error Handling in Scripts

**PowerShell:**
```powershell
try {
    $body = @{
        input = "Sample text"
        model = "all-MiniLM-L6-v2"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"

    Write-Host "Successfully generated embedding with $($response.data[0].embedding.Count) dimensions"
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json

    Write-Host "Error ($statusCode): $($errorBody.error.message)" -ForegroundColor Red

    if ($errorBody.error.code -eq "missing_parameter") {
        Write-Host "Ensure 'input' parameter is provided"
    }
    elseif ($errorBody.error.code -eq "model_not_found") {
        Write-Host "Check available models with GET /iblink/v1/models"
    }
}
```

**Bash:**
```bash
response=$(curl -w "\n%{http_code}" -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Sample text",
    "model": "all-MiniLM-L6-v2"
  }')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ $http_code -eq 200 ]; then
    echo "Success: Generated embedding"
    echo "$body" | jq '.data[0].embedding | length'
else
    echo "Error (HTTP $http_code):"
    echo "$body" | jq '.error.message'
fi
```

### 6. Monitor Token Usage

```bash
# Track token usage for cost estimation
total_tokens=0

response=$(curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": ["text1", "text2", "text3"],
    "model": "all-MiniLM-L6-v2"
  }')

tokens=$(echo "$response" | jq '.usage.total_tokens')
total_tokens=$((total_tokens + tokens))

echo "Total tokens used: $total_tokens"
```

### 7. Use Consistent Model Names

```bash
# Define model as environment variable
export EMBEDDING_MODEL="all-MiniLM-L6-v2"

# Use in all requests
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d "{
    \"input\": \"$text\",
    \"model\": \"$EMBEDDING_MODEL\"
  }"
```

### 8. Validate API Availability

```bash
# Check health before processing
health_status=$(curl -s http://localhost:5000/iblink/v1/embeddings/health | jq -r '.status')

if [ "$health_status" == "healthy" ]; then
    echo "API is healthy, proceeding with embedding generation"
    # Process embeddings...
else
    echo "API is unhealthy, aborting"
    exit 1
fi
```

### 9. Normalize Embeddings for Similarity

```python
import numpy as np

def normalize_embedding(embedding):
    """Normalize embedding to unit length for cosine similarity"""
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding

# Get embedding from API
response = requests.post(
    "http://localhost:5000/iblink/v1/embeddings",
    json={"input": "Sample text", "model": "all-MiniLM-L6-v2"}
)

embedding = np.array(response.json()["data"][0]["embedding"])
normalized_embedding = normalize_embedding(embedding)
```

### 10. Handle Rate Limiting

```bash
# Add delay between requests to avoid overwhelming the API
for text in "${texts[@]}"; do
    curl -X POST http://localhost:5000/iblink/v1/embeddings \
      -H "Content-Type: application/json" \
      -d "{\"input\": \"$text\", \"model\": \"all-MiniLM-L6-v2\"}"

    sleep 0.1  # 100ms delay
done
```

**PowerShell:**
```powershell
foreach ($text in $texts) {
    $body = @{
        input = $text
        model = "all-MiniLM-L6-v2"
    } | ConvertTo-Json

    Invoke-RestMethod -Uri "http://localhost:5000/iblink/v1/embeddings" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"

    Start-Sleep -Milliseconds 100
}
```

---

## OpenAI API Compatibility

### Drop-in Replacement

The EmbeddingsAPI is fully compatible with OpenAI's Embeddings API:

**OpenAI API:**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")
response = client.embeddings.create(
    input="Sample text",
    model="text-embedding-ada-002"
)
```

**EmbeddingsAPI (Compatible):**
```python
from openai import OpenAI

client = OpenAI(
    api_key="not-needed",  # No API key required
    base_url="http://localhost:5000/iblink/v1"
)
response = client.embeddings.create(
    input="Sample text",
    model="all-MiniLM-L6-v2"
)
```

### Supported Parameters

| Parameter | OpenAI | EmbeddingsAPI | Notes |
|-----------|--------|---------------|-------|
| input | ✓ | ✓ | String or array of strings |
| model | ✓ | ✓ | Use local model name |
| encoding_format | ✓ | ✓ | float (base64 planned) |
| dimensions | ✓ | ✓ | Model-dependent |
| user | ✓ | ✓ | Optional tracking |

---

## Performance Considerations

### Typical Processing Times

| Input Type | Size | Processing Time | Throughput |
|------------|------|-----------------|------------|
| Single text | 50 words | 20-50ms | 20-50 req/s |
| Batch (10 texts) | 50 words each | 100-200ms | 50-100 texts/s |
| Batch (50 texts) | 50 words each | 400-800ms | 60-125 texts/s |
| Long text | 500 words | 80-150ms | 6-12 req/s |

**Note:** Times measured on typical desktop CPU (Intel i7/AMD Ryzen 5). ONNX runtime provides efficient inference.

### Model Specifications

**all-MiniLM-L6-v2:**
- Dimensions: 384
- Max sequence length: 512 tokens (≈2000 characters)
- Parameters: 22.7M
- Model size: ~90MB
- Recommended for: General-purpose embeddings

---

## Common Use Cases

### 1. Semantic Search

Generate embeddings for documents and queries to enable semantic search.

### 2. Document Clustering

Create embeddings for documents to group similar content.

### 3. Recommendation Systems

Generate user and item embeddings for similarity-based recommendations.

### 4. Duplicate Detection

Compare embeddings to find duplicate or near-duplicate content.

### 5. Text Classification

Use embeddings as features for machine learning models.

---

**Last Updated**: 2025-01-20
**API Version**: 1.0.0
**Default Port**: 5000
**OpenAI Compatibility**: Full Embeddings API v1

---

## Additional Resources

- [OpenAI Embeddings API Reference](https://platform.openai.com/docs/api-reference/embeddings)
- [ONNX Runtime Documentation](https://onnxruntime.ai/)
- [Sentence Transformers Models](https://www.sbert.net/)
- [DocumentsAPI Integration](./DocumentsAPI_Usage_Examples.md)

---

## Quick Reference

### Common Operations

```bash
# Generate single embedding
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"input": "text", "model": "all-MiniLM-L6-v2"}'

# Generate batch embeddings
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"input": ["text1", "text2"], "model": "all-MiniLM-L6-v2"}'

# List models
curl http://localhost:5000/iblink/v1/models

# Get model info
curl http://localhost:5000/iblink/v1/models/all-MiniLM-L6-v2

# Health check
curl http://localhost:5000/iblink/v1/embeddings/health
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `400 Bad Request` - Invalid parameters or empty input
- `404 Not Found` - Model not found
- `500 Internal Server Error` - Server error during processing

### Model Information

- **Model Name**: all-MiniLM-L6-v2
- **Embedding Dimensions**: 384
- **Max Tokens**: 512
- **Architecture**: BERT-based
- **Use Case**: General-purpose semantic similarity
