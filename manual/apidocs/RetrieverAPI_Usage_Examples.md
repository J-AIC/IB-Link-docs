# RetrieverAPI - Usage Examples

Complete guide with practical examples for the IB-Link Retriever API - a standalone semantic search and document retrieval service.

**Base URL**: `http://localhost:6500/iblink/v1/retriever`

---

## Table of Contents

- [Overview](#overview)
- [Semantic Search](#semantic-search)
  - [Basic Vector Search](#basic-vector-search)
  - [Filtered Search by Directories](#filtered-search-by-directories)
  - [Filtered Search by File Paths](#filtered-search-by-file-paths)
  - [Filtered Search by Document IDs](#filtered-search-by-document-ids)
  - [Hybrid Search](#hybrid-search)
  - [Hybrid RRF Search](#hybrid-rrf-search)
  - [Custom Weights for Hybrid Search](#custom-weights-for-hybrid-search)
- [API Information](#api-information)
  - [Get API Info](#get-api-info)
  - [Health Check](#health-check)
  - [Test Endpoint](#test-endpoint)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Error Handling](#error-handling-examples)
- [Tips and Best Practices](#tips-and-best-practices)

---

## Overview

The RetrieverAPI provides semantic search capabilities for document retrieval using:
- **Vector Search**: Semantic similarity using embeddings
- **Hybrid Search**: Combination of vector and full-text search with weighted scoring
- **Hybrid RRF**: Reciprocal Rank Fusion for optimal result ranking

**Key Features**:
- Multi-mode search (vector, hybrid, hybrid_rrf)
- Advanced filtering (directories, files, documents, projects)
- Customizable relevance scoring
- PDF page-level precision
- Chunk-based retrieval with metadata

**Default Port**: 6500

---

## Semantic Search

### Basic Vector Search

Perform semantic search using vector embeddings (default mode).

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning algorithms",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "machine learning algorithms"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "query": "machine learning algorithms",
  "project_id": "project-alpha",
  "d_app_id": "my-app-001",
  "total_results": 10,
  "total_unfiltered_results": 10,
  "filtered_directories": null,
  "filtered_file_paths": null,
  "results": [
    {
      "id": "doc-123-chunk-5",
      "text": "Machine learning algorithms such as neural networks, decision trees, and support vector machines are fundamental to modern AI applications...",
      "score": 0.92,
      "metadata": {
        "source": "ai_guide.pdf",
        "directory": "C:\\Documents\\AI",
        "file_path": "C:\\Documents\\AI\\ai_guide.pdf",
        "chunk_index": 5,
        "chunk_category": "PDF",
        "page_range": "12-14",
        "start_page": 12,
        "end_page": 14,
        "document_id": "550e8400-e29b-41d4-a716-446655440000"
      }
    },
    {
      "id": "doc-456-chunk-2",
      "text": "Various algorithms in machine learning include supervised, unsupervised, and reinforcement learning approaches...",
      "score": 0.87,
      "metadata": {
        "source": "ml_basics.txt",
        "directory": "C:\\Documents\\ML",
        "file_path": "C:\\Documents\\ML\\ml_basics.txt",
        "chunk_index": 2,
        "chunk_category": "TEXT",
        "document_id": "660e8400-e29b-41d4-a716-446655440001"
      }
    }
  ]
}
```

---

### Filtered Search by Directories

Search within specific directories only.

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "quantum computing principles",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 5,
    "files_directories": [
      "C:\\Research\\Quantum",
      "C:\\Research\\Physics"
    ]
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "quantum computing principles"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 5
    files_directories = @(
        "C:\Research\Quantum",
        "C:\Research\Physics"
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "query": "quantum computing principles",
  "project_id": "project-alpha",
  "d_app_id": "my-app-001",
  "total_results": 5,
  "total_unfiltered_results": 15,
  "filtered_directories": [
    "C:\\Research\\Quantum",
    "C:\\Research\\Physics"
  ],
  "filtered_file_paths": null,
  "results": [
    {
      "id": "doc-789-chunk-0",
      "text": "Quantum computing leverages principles of quantum mechanics such as superposition and entanglement...",
      "score": 0.94,
      "metadata": {
        "source": "quantum_intro.pdf",
        "directory": "C:\\Research\\Quantum",
        "file_path": "C:\\Research\\Quantum\\quantum_intro.pdf",
        "chunk_index": 0,
        "page_range": "1-3",
        "start_page": 1,
        "end_page": 3
      }
    }
  ]
}
```

---

### Filtered Search by File Paths

Search within specific files only.

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "neural network architecture",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10,
    "file_paths": [
      "C:\\Documents\\AI\\deep_learning.pdf",
      "C:\\Documents\\AI\\cnn_guide.pdf"
    ]
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "neural network architecture"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 10
    file_paths = @(
        "C:\Documents\AI\deep_learning.pdf",
        "C:\Documents\AI\cnn_guide.pdf"
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "query": "neural network architecture",
  "project_id": "project-alpha",
  "d_app_id": "my-app-001",
  "total_results": 8,
  "total_unfiltered_results": 25,
  "filtered_directories": null,
  "filtered_file_paths": [
    "C:\\Documents\\AI\\deep_learning.pdf",
    "C:\\Documents\\AI\\cnn_guide.pdf"
  ],
  "results": [
    {
      "id": "doc-234-chunk-10",
      "text": "Convolutional neural network architectures consist of multiple layers including convolutional, pooling, and fully connected layers...",
      "score": 0.91,
      "metadata": {
        "source": "cnn_guide.pdf",
        "directory": "C:\\Documents\\AI",
        "file_path": "C:\\Documents\\AI\\cnn_guide.pdf",
        "chunk_index": 10,
        "page_range": "25-27",
        "start_page": 25,
        "end_page": 27
      }
    }
  ]
}
```

---

### Filtered Search by Document IDs

Search within specific documents using their unique identifiers. This takes precedence over directory and file path filters.

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "data preprocessing techniques",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 5,
    "documents_id": [
      "550e8400-e29b-41d4-a716-446655440000",
      "660e8400-e29b-41d4-a716-446655440001"
    ]
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "data preprocessing techniques"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 5
    documents_id = @(
        "550e8400-e29b-41d4-a716-446655440000",
        "660e8400-e29b-41d4-a716-446655440001"
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "query": "data preprocessing techniques",
  "project_id": "project-alpha",
  "d_app_id": "my-app-001",
  "total_results": 5,
  "total_unfiltered_results": 5,
  "filtered_directories": null,
  "filtered_file_paths": null,
  "results": [
    {
      "id": "doc-550e-chunk-3",
      "text": "Data preprocessing techniques include normalization, standardization, handling missing values, and feature encoding...",
      "score": 0.89,
      "metadata": {
        "source": "data_science.pdf",
        "directory": "C:\\Documents\\DS",
        "file_path": "C:\\Documents\\DS\\data_science.pdf",
        "chunk_index": 3,
        "document_id": "550e8400-e29b-41d4-a716-446655440000",
        "page_range": "45-47",
        "start_page": 45,
        "end_page": 47
      }
    }
  ]
}
```

---

### Hybrid Search

Combine vector similarity and full-text search for improved relevance using weighted scoring.

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "supervised learning classification",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10,
    "search_mode": "hybrid",
    "vector_weight": 0.7,
    "text_weight": 0.3,
    "enable_phrase_matching": true
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "supervised learning classification"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 10
    search_mode = "hybrid"
    vector_weight = 0.7
    text_weight = 0.3
    enable_phrase_matching = $true
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "query": "supervised learning classification",
  "project_id": "project-alpha",
  "d_app_id": "my-app-001",
  "total_results": 10,
  "total_unfiltered_results": 10,
  "filtered_directories": null,
  "filtered_file_paths": null,
  "results": [
    {
      "id": "doc-345-chunk-7",
      "text": "Supervised learning classification algorithms are trained on labeled datasets to predict categorical outcomes...",
      "score": 0.93,
      "metadata": {
        "source": "ml_classification.pdf",
        "directory": "C:\\Documents\\ML",
        "file_path": "C:\\Documents\\ML\\ml_classification.pdf",
        "chunk_index": 7,
        "chunk_category": "PDF",
        "page_range": "15-17",
        "start_page": 15,
        "end_page": 17,
        "vector_score": 0.91,
        "text_score": 0.88,
        "text_rank": 2.5,
        "document_id": "770e8400-e29b-41d4-a716-446655440002"
      }
    }
  ]
}
```

---

### Hybrid RRF Search

Use Reciprocal Rank Fusion (RRF) to combine vector and text search results for optimal ranking.

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "deep learning frameworks tensorflow pytorch",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 15,
    "search_mode": "hybrid_rrf",
    "rrf_k": 60,
    "enable_phrase_matching": true
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "deep learning frameworks tensorflow pytorch"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 15
    search_mode = "hybrid_rrf"
    rrf_k = 60
    enable_phrase_matching = $true
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "query": "deep learning frameworks tensorflow pytorch",
  "project_id": "project-alpha",
  "d_app_id": "my-app-001",
  "total_results": 15,
  "total_unfiltered_results": 15,
  "filtered_directories": null,
  "filtered_file_paths": null,
  "results": [
    {
      "id": "doc-678-chunk-12",
      "text": "Popular deep learning frameworks include TensorFlow and PyTorch, both offering extensive libraries for building neural networks...",
      "score": 0.95,
      "metadata": {
        "source": "dl_frameworks.pdf",
        "directory": "C:\\Documents\\DL",
        "file_path": "C:\\Documents\\DL\\dl_frameworks.pdf",
        "chunk_index": 12,
        "chunk_category": "PDF",
        "page_range": "30-32",
        "start_page": 30,
        "end_page": 32,
        "vector_score": 0.89,
        "text_score": 0.92,
        "text_rank": 1.0,
        "document_id": "880e8400-e29b-41d4-a716-446655440003"
      }
    }
  ]
}
```

---

### Custom Weights for Hybrid Search

Adjust the balance between semantic similarity and keyword matching.

#### Favor Vector Similarity (90% vector, 10% text)

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "transformer attention mechanism",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10,
    "search_mode": "hybrid",
    "vector_weight": 0.9,
    "text_weight": 0.1
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "transformer attention mechanism"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 10
    search_mode = "hybrid"
    vector_weight = 0.9
    text_weight = 0.1
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Favor Text Search (30% vector, 70% text)

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "specific technical term XYZ-123",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10,
    "search_mode": "hybrid",
    "vector_weight": 0.3,
    "text_weight": 0.7,
    "enable_phrase_matching": true
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "specific technical term XYZ-123"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 10
    search_mode = "hybrid"
    vector_weight = 0.3
    text_weight = 0.7
    enable_phrase_matching = $true
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Balanced Search (50% vector, 50% text)

**cURL:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "natural language processing applications",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10,
    "search_mode": "hybrid",
    "vector_weight": 0.5,
    "text_weight": 0.5
  }'
```

**PowerShell:**
```powershell
$body = @{
    text = "natural language processing applications"
    d_app_id = "my-app-001"
    project_id = "project-alpha"
    limit = 10
    search_mode = "hybrid"
    vector_weight = 0.5
    text_weight = 0.5
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

## API Information

### Get API Info

Get detailed information about the RetrieverAPI configuration and available endpoints.

**cURL:**
```bash
curl http://localhost:6500/iblink/v1/retriever/info
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever/info"
```

**Response:**
```json
{
  "service": "IB-Link Retriever API",
  "version": "1.0.0",
  "description": "Standalone semantic search and document retrieval API",
  "endpoints": [
    {
      "method": "POST",
      "path": "/iblink/v1/retriever",
      "description": "Perform semantic search on documents"
    },
    {
      "method": "GET",
      "path": "/iblink/v1/retriever/health",
      "description": "Health check endpoint"
    },
    {
      "method": "GET",
      "path": "/iblink/v1/retriever/info",
      "description": "API information"
    }
  ],
  "configuration": {
    "port": 6500,
    "embeddingApiUrl": "http://localhost:6004",
    "embeddingModel": "all-MiniLM-L6-v2",
    "defaultTopK": 10,
    "maxTopK": 100
  }
}
```

---

### Health Check

Check the health status of RetrieverAPI and its dependencies.

**cURL:**
```bash
curl http://localhost:6500/iblink/v1/retriever/health
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever/health"
```

**Response (Healthy):**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "service": "retriever-api",
  "version": "1.0.0",
  "port": 6500,
  "dependencies": {
    "database": {
      "status": "healthy",
      "message": "Database connection healthy"
    },
    "embeddingApi": {
      "status": "healthy",
      "message": "Embedding API available",
      "url": "http://localhost:6004"
    }
  }
}
```

**Response (Degraded - Database Issues):**
```json
{
  "status": "degraded",
  "timestamp": "2025-01-20T10:30:00Z",
  "service": "retriever-api",
  "version": "1.0.0",
  "port": 6500,
  "dependencies": {
    "database": {
      "status": "unhealthy",
      "message": "Cannot connect to database"
    },
    "embeddingApi": {
      "status": "healthy",
      "message": "Embedding API available",
      "url": "http://localhost:6004"
    }
  }
}
```

**Response (Unhealthy - All Dependencies Down):**
```json
{
  "status": "unhealthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "service": "retriever-api",
  "version": "1.0.0",
  "port": 6500,
  "dependencies": {
    "database": {
      "status": "unhealthy",
      "message": "Database check failed: Connection timeout"
    },
    "embeddingApi": {
      "status": "unhealthy",
      "message": "Embedding API unreachable",
      "url": "http://localhost:6004"
    }
  }
}
```

---

### Test Endpoint

Simple test endpoint to verify the API is running.

**cURL:**
```bash
curl http://localhost:6500/iblink/v1/retriever/test
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:6500/iblink/v1/retriever/test"
```

**Response:**
```json
{
  "message": "Test successful",
  "timestamp": "2025-01-20T10:30:00.123Z"
}
```

---

## Complete Workflow Examples

### Workflow 1: Basic Document Search

```bash
# 1. Check API health
curl http://localhost:6500/iblink/v1/retriever/health

# 2. Get API information and configuration
curl http://localhost:6500/iblink/v1/retriever/info

# 3. Perform a basic search
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "database optimization techniques",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10
  }'

# 4. Narrow down search to specific directory
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "database optimization techniques",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 5,
    "files_directories": ["C:\\Documents\\Database"]
  }'
```

### Workflow 2: Advanced Hybrid Search with Filtering

```bash
# 1. Check dependencies are healthy
curl http://localhost:6500/iblink/v1/retriever/health

# 2. Start with hybrid RRF search for best results
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "RESTful API design best practices",
    "d_app_id": "dev-app-002",
    "project_id": "project-beta",
    "limit": 20,
    "search_mode": "hybrid_rrf",
    "rrf_k": 60,
    "enable_phrase_matching": true
  }'

# 3. Refine with specific files if needed
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "RESTful API design best practices",
    "d_app_id": "dev-app-002",
    "project_id": "project-beta",
    "limit": 10,
    "search_mode": "hybrid_rrf",
    "file_paths": [
      "C:\\Docs\\API\\rest_guide.pdf",
      "C:\\Docs\\API\\web_services.pdf"
    ]
  }'
```

### Workflow 3: Multi-Project Search Strategy

```bash
# 1. Search across project A
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "authentication methods",
    "d_app_id": "security-app",
    "project_id": "project-a",
    "limit": 10,
    "search_mode": "hybrid",
    "vector_weight": 0.7,
    "text_weight": 0.3
  }'

# 2. Search across project B
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "authentication methods",
    "d_app_id": "security-app",
    "project_id": "project-b",
    "limit": 10,
    "search_mode": "hybrid",
    "vector_weight": 0.7,
    "text_weight": 0.3
  }'

# 3. Compare results and analyze differences
```

### Workflow 4: Iterative Search Refinement

```bash
# 1. Start with broad vector search
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "cloud computing",
    "d_app_id": "research-app",
    "project_id": "cloud-project",
    "limit": 50
  }'

# 2. Switch to hybrid mode for better precision
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "cloud computing infrastructure AWS",
    "d_app_id": "research-app",
    "project_id": "cloud-project",
    "limit": 20,
    "search_mode": "hybrid",
    "vector_weight": 0.6,
    "text_weight": 0.4
  }'

# 3. Use document IDs from best results for focused search
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "AWS EC2 deployment strategies",
    "d_app_id": "research-app",
    "project_id": "cloud-project",
    "limit": 10,
    "search_mode": "hybrid_rrf",
    "documents_id": [
      "550e8400-e29b-41d4-a716-446655440000",
      "660e8400-e29b-41d4-a716-446655440001"
    ]
  }'
```

### Workflow 5: Monitoring and Health Checks

```bash
# 1. Perform health check before operations
HEALTH_STATUS=$(curl -s http://localhost:6500/iblink/v1/retriever/health | jq -r '.status')

if [ "$HEALTH_STATUS" == "healthy" ]; then
  echo "API is healthy, proceeding with search"

  # 2. Execute search
  curl -X POST http://localhost:6500/iblink/v1/retriever \
    -H "Content-Type: application/json" \
    -d '{
      "text": "your search query",
      "d_app_id": "monitoring-app",
      "project_id": "monitoring-project",
      "limit": 10
    }'
else
  echo "API is not healthy: $HEALTH_STATUS"
  echo "Check dependencies and try again"
fi

# 3. Verify embedding API is available
curl http://localhost:6004/health
```

---

## Error Handling Examples

### Error Response Format

All errors follow this standard format:

```json
{
  "error": {
    "message": "Human-readable error message",
    "type": "error_type",
    "code": "error_code"
  }
}
```

### Common Error Responses

#### Missing Required Parameter (400)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Missing required parameter 'text'",
    "type": "invalid_request_error",
    "code": "missing_parameter"
  }
}
```

#### Missing d_app_id (400)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "project_id": "project-alpha",
    "limit": 10
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Missing required parameter 'd_app_id'",
    "type": "invalid_request_error",
    "code": "missing_parameter"
  }
}
```

#### Missing project_id (400)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "d_app_id": "my-app-001",
    "limit": 10
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Missing required parameter 'project_id'",
    "type": "invalid_request_error",
    "code": "missing_parameter"
  }
}
```

#### Invalid Limit Parameter (400)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 150
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Parameter 'limit' must be between 1 and 100",
    "type": "invalid_request_error",
    "code": "invalid_parameter"
  }
}
```

#### Invalid Search Mode (400)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10,
    "search_mode": "fuzzy"
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Invalid search_mode. Must be one of: vector, hybrid, hybrid_rrf",
    "type": "invalid_request_error",
    "code": "invalid_parameter"
  }
}
```

#### Invalid Weights for Hybrid Search (400)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10,
    "search_mode": "hybrid",
    "vector_weight": 1.5,
    "text_weight": 0.3
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Weights must be between 0.0 and 1.0",
    "type": "invalid_request_error",
    "code": "invalid_parameter"
  }
}
```

#### Embedding API Unavailable (503)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Embedding API is currently unavailable. Please ensure the service is running at http://localhost:6004",
    "type": "service_unavailable",
    "code": "embedding_api_unavailable"
  }
}
```

#### Database Unavailable (503)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10
  }'
```

**Response:**
```json
{
  "error": {
    "message": "Database connection failed. Please check database configuration and connectivity.",
    "type": "service_unavailable",
    "code": "database_unavailable"
  }
}
```

#### Internal Server Error (500)

**Request:**
```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning",
    "d_app_id": "my-app-001",
    "project_id": "project-alpha",
    "limit": 10
  }'
```

**Response:**
```json
{
  "error": {
    "message": "An unexpected error occurred while processing your search request. Please try again later.",
    "type": "api_error",
    "code": "internal_error"
  }
}
```

---

## Tips and Best Practices

### 1. Choose the Right Search Mode

**Vector Search** - Best for:
- Semantic/conceptual queries
- Finding similar concepts with different wording
- Exploratory research
- When exact keyword matching is not critical

```bash
# Good use case: finding conceptually similar content
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{
    "text": "ways to improve code performance",
    "search_mode": "vector"
  }'
```

**Hybrid Search** - Best for:
- Balanced semantic and keyword matching
- Technical documentation search
- When you need both concepts and specific terms
- Customizable relevance weighting

```bash
# Good use case: technical queries with specific terms
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{
    "text": "Python asyncio event loop optimization",
    "search_mode": "hybrid",
    "vector_weight": 0.6,
    "text_weight": 0.4
  }'
```

**Hybrid RRF** - Best for:
- Optimal result ranking
- Complex multi-term queries
- When you want the best of both approaches
- Production search systems

```bash
# Good use case: complex queries requiring best ranking
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{
    "text": "microservices architecture patterns kubernetes docker",
    "search_mode": "hybrid_rrf",
    "rrf_k": 60
  }'
```

### 2. Always Check Health Before Batch Operations

```bash
# Check health before starting large batch operations
HEALTH=$(curl -s http://localhost:6500/iblink/v1/retriever/health | jq -r '.status')

if [ "$HEALTH" == "healthy" ]; then
  # Proceed with batch searches
  for query in "${queries[@]}"; do
    curl -X POST http://localhost:6500/iblink/v1/retriever -d "$query"
  done
else
  echo "API not healthy, aborting batch operation"
fi
```

### 3. Use Appropriate Limit Values

```bash
# Small limit for quick previews
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{"text": "query", "limit": 5}'

# Medium limit for regular searches
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{"text": "query", "limit": 20}'

# Maximum limit for comprehensive results
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{"text": "query", "limit": 100}'
```

### 4. Leverage Filtering for Precision

```bash
# Combine multiple filters for precise results
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "security best practices",
    "d_app_id": "my-app",
    "project_id": "security-project",
    "limit": 15,
    "files_directories": ["C:\\Security\\Guidelines"],
    "search_mode": "hybrid_rrf"
  }'
```

### 5. Optimize Weights Based on Query Type

```bash
# For semantic queries - favor vector similarity
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{
    "text": "what causes software bugs",
    "search_mode": "hybrid",
    "vector_weight": 0.8,
    "text_weight": 0.2
  }'

# For exact term queries - favor text search
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{
    "text": "ERROR-CODE-5023",
    "search_mode": "hybrid",
    "vector_weight": 0.2,
    "text_weight": 0.8,
    "enable_phrase_matching": true
  }'
```

### 6. Use Document IDs for Follow-up Searches

```bash
# 1. Initial broad search
RESPONSE=$(curl -s -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{"text": "API documentation", "limit": 20}')

# 2. Extract relevant document IDs
RELEVANT_DOCS=$(echo $RESPONSE | jq -r '.results[0:3].metadata.document_id')

# 3. Search within those documents
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d "{
    \"text\": \"authentication endpoints\",
    \"documents_id\": $RELEVANT_DOCS
  }"
```

### 7. Enable Phrase Matching for Exact Terms

```bash
# For queries with specific phrases or technical terms
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{
    "text": "null pointer exception",
    "search_mode": "hybrid",
    "enable_phrase_matching": true,
    "text_weight": 0.5
  }'
```

### 8. Handle Pagination for Large Result Sets

```bash
# First batch - top 20 results
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{"text": "query", "limit": 20}'

# If you need more, adjust your search strategy instead of pagination
# Use more specific queries or filters
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{
    "text": "more specific query",
    "limit": 20,
    "files_directories": ["C:\\Specific\\Path"]
  }'
```

### 9. Monitor Performance with Metadata

```bash
# Analyze score distributions to optimize search mode
RESPONSE=$(curl -s -X POST http://localhost:6500/iblink/v1/retriever \
  -d '{"text": "query", "limit": 20}')

# Check average scores
echo $RESPONSE | jq '.results[].score' | \
  awk '{sum+=$1; count+=1} END {print "Avg score:", sum/count}'

# Check vector vs text score balance in hybrid mode
echo $RESPONSE | jq '.results[].metadata | select(.vector_score) |
  {vector_score, text_score}'
```

### 10. Structured Error Handling

```bash
# Robust error handling in scripts
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  http://localhost:6500/iblink/v1/retriever \
  -d '{"text": "query", "d_app_id": "app", "project_id": "proj"}')

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

case $HTTP_CODE in
  200)
    echo "Success: $(echo $BODY | jq -r '.total_results') results found"
    ;;
  400)
    echo "Bad request: $(echo $BODY | jq -r '.error.message')"
    ;;
  503)
    echo "Service unavailable: $(echo $BODY | jq -r '.error.code')"
    ;;
  500)
    echo "Server error - please retry later"
    ;;
  *)
    echo "Unexpected status: $HTTP_CODE"
    ;;
esac
```

### 11. Use Environment Variables for Configuration

```bash
# Set up environment variables for reusable configurations
export RETRIEVER_URL="http://localhost:6500/iblink/v1/retriever"
export D_APP_ID="my-application"
export PROJECT_ID="my-project"

# Use in searches
curl -X POST $RETRIEVER_URL \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"search query\",
    \"d_app_id\": \"$D_APP_ID\",
    \"project_id\": \"$PROJECT_ID\",
    \"limit\": 10
  }"
```

### 12. Cache Frequently Accessed Results

```bash
# Cache search results for frequently used queries
CACHE_FILE="search_cache_$(echo -n "$QUERY" | md5sum | cut -d' ' -f1).json"

if [ -f "$CACHE_FILE" ] && [ $(find "$CACHE_FILE" -mmin -30) ]; then
  # Use cached results (less than 30 minutes old)
  cat "$CACHE_FILE"
else
  # Fetch new results and cache
  curl -X POST http://localhost:6500/iblink/v1/retriever \
    -d "{\"text\": \"$QUERY\"}" | tee "$CACHE_FILE"
fi
```

---

## Search Mode Comparison

| Feature | Vector | Hybrid | Hybrid RRF |
|---------|--------|--------|------------|
| **Semantic Understanding** | ✓✓✓ | ✓✓ | ✓✓ |
| **Keyword Matching** | ✗ | ✓✓ | ✓✓ |
| **Phrase Matching** | ✗ | ✓✓ | ✓✓ |
| **Custom Weighting** | ✗ | ✓✓✓ | ✗ |
| **Optimal Ranking** | ✓ | ✓✓ | ✓✓✓ |
| **Speed** | ✓✓✓ | ✓✓ | ✓ |
| **Best For** | Conceptual | Balanced | Production |

---

## Parameter Reference

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | string | Search query text |
| `d_app_id` | string | Client application identifier |
| `project_id` | string | Project scope identifier |

### Optional Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `limit` | integer | 10 | 1-100 | Maximum number of results |
| `search_mode` | string | "vector" | vector, hybrid, hybrid_rrf | Search algorithm mode |
| `vector_weight` | float | 0.7 | 0.0-1.0 | Weight for vector similarity (hybrid mode) |
| `text_weight` | float | 0.3 | 0.0-1.0 | Weight for text search (hybrid mode) |
| `rrf_k` | integer | 60 | 1-1000 | RRF constant (hybrid_rrf mode) |
| `enable_phrase_matching` | boolean | true | - | Enable exact phrase matching |
| `files_directories` | array | null | - | Filter by directory paths |
| `file_paths` | array | null | - | Filter by specific file paths |
| `documents_id` | array | null | - | Filter by document UUIDs |

---

**Last Updated**: 2025-01-20
**API Version**: 1.0.0
**Default Port**: 6500
**Documentation**: `docs/API/RetrieverAPI_Usage_Examples.md`

---

## Additional Resources

- [EmbeddingsAPI Documentation](./EmbeddingsAPI_Usage_Examples.md) - Generate embeddings for custom applications
- [DocumentsAPI Documentation](./DocumentsAPI_Usage_Examples.md) - Document processing and management
- [IB-Link Architecture Guide](../Architecture/System_Overview.md) - System architecture and components
- [Database Schema](../Database/Schema_Documentation.md) - Database structure and relationships

---

## Quick Reference

### Common cURL Commands

```bash
# Basic search
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{"text":"query","d_app_id":"app","project_id":"proj","limit":10}'

# Hybrid RRF search with filters
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{"text":"query","d_app_id":"app","project_id":"proj","search_mode":"hybrid_rrf","files_directories":["C:\\Docs"],"limit":20}'

# Health check
curl http://localhost:6500/iblink/v1/retriever/health

# API info
curl http://localhost:6500/iblink/v1/retriever/info
```

### HTTP Status Codes

- `200 OK` - Search completed successfully
- `400 Bad Request` - Invalid parameters or missing required fields
- `500 Internal Server Error` - Unexpected server error
- `503 Service Unavailable` - Dependencies (database or embedding API) unavailable
