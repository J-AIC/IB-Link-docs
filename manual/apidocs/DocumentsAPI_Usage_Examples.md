# DocumentsAPI - Usage Examples

Complete guide with practical examples for all DocumentsAPI endpoints.

**Base URL**: `http://localhost:8500/iblink/v1`

**Purpose**: Process documents, extract text, create embeddings, and manage document lifecycle with PostgreSQL storage.

---

## Table of Contents

- [Document Processing](#document-processing)
  - [Process Documents (Async)](#post-documentsprocess)
  - [Process with OCR](#process-with-ocr)
  - [Process Directories](#process-directories)
  - [Duplicate Handling Strategies](#duplicate-handling-strategies)
- [Status and Monitoring](#status-and-monitoring)
  - [Get Processing Status](#get-processing-status)
  - [Get Queue Status](#get-queue-status)
  - [Get Quota Status](#get-quota-status)
  - [Get Health Status](#get-health-status)
  - [Get Dependency Status](#get-dependency-status)
  - [List Jobs](#list-jobs)
  - [Get Active Jobs](#get-active-jobs)
  - [Cancel Job](#cancel-job)
  - [Cleanup Jobs](#cleanup-jobs)
- [Document Operations](#document-operations)
  - [Search Documents](#post-documentssearch)
  - [Extract Text](#post-documentsextract)
  - [List Documents](#post-documentslist)
  - [Delete Documents](#delete-documentsdelete)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Error Handling](#error-handling-examples)
- [Tips and Best Practices](#tips-and-best-practices)

---

## Document Processing

### POST /documents/process

Process documents asynchronously with status tracking, quota checking, and job queuing.

#### Basic Document Processing

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      "C:\\Documents\\report.pdf",
      "C:\\Documents\\meeting_notes.txt"
    ],
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

**PowerShell:**
```powershell
$body = @{
    files = @(
        "C:\Documents\report.pdf",
        "C:\Documents\meeting_notes.txt"
    )
    d_app_id = "my-app"
    project_id = "project-001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response (202 Accepted):**
```json
{
  "job_id": "my-app_project-001_20250120_103000",
  "status": "pending",
  "message": "Document processing job created",
  "status_url": "/iblink/v1/documents/status",
  "created_at": "2025-01-20T10:30:00Z"
}
```

---

### Process with OCR

Enable OCR for scanned documents or images.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      "C:\\Scans\\invoice.pdf",
      "C:\\Scans\\receipt.png"
    ],
    "d_app_id": "my-app",
    "project_id": "project-001",
    "enable_ocr": true
  }'
```

**PowerShell:**
```powershell
$body = @{
    files = @(
        "C:\Scans\invoice.pdf",
        "C:\Scans\receipt.png"
    )
    d_app_id = "my-app"
    project_id = "project-001"
    enable_ocr = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Per-File OCR Configuration:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {
        "file_path": "C:\\Scans\\invoice.pdf",
        "enable_ocr": true
      },
      {
        "file_path": "C:\\Documents\\report.pdf",
        "enable_ocr": false
      }
    ],
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

---

### Process Directories

Process all documents in a directory recursively.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "directories": [
      "C:\\Documents\\Project",
      "C:\\Data\\Reports"
    ],
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

**PowerShell:**
```powershell
$body = @{
    directories = @(
        "C:\Documents\Project",
        "C:\Data\Reports"
    )
    d_app_id = "my-app"
    project_id = "project-001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Mixed Files and Directories:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      "C:\\Important\\contract.pdf"
    ],
    "directories": [
      "C:\\Documents\\Archive"
    ],
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

---

### Duplicate Handling Strategies

Control how duplicates are handled during processing.

#### Skip Duplicates (Default)

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["C:\\Documents\\report.pdf"],
    "d_app_id": "my-app",
    "project_id": "project-001",
    "duplicate_strategy": "skip"
  }'
```

**PowerShell:**
```powershell
$body = @{
    files = @("C:\Documents\report.pdf")
    d_app_id = "my-app"
    project_id = "project-001"
    duplicate_strategy = "skip"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Update Existing Documents

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["C:\\Documents\\report.pdf"],
    "d_app_id": "my-app",
    "project_id": "project-001",
    "duplicate_strategy": "update"
  }'
```

#### Always Add (Allow Duplicates)

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["C:\\Documents\\report.pdf"],
    "d_app_id": "my-app",
    "project_id": "project-001",
    "duplicate_strategy": "add"
  }'
```

#### Sync Mode (Remove Orphaned)

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      "C:\\Documents\\current1.pdf",
      "C:\\Documents\\current2.pdf"
    ],
    "d_app_id": "my-app",
    "project_id": "project-001",
    "duplicate_strategy": "sync"
  }'
```

**Note:** Sync mode removes embeddings for documents not in the request.

---

### Custom Chunking Parameters

Control how documents are split into chunks.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["C:\\Documents\\large_document.pdf"],
    "d_app_id": "my-app",
    "project_id": "project-001",
    "chunk_size": 1000,
    "chunk_overlap": 200
  }'
```

**PowerShell:**
```powershell
$body = @{
    files = @("C:\Documents\large_document.pdf")
    d_app_id = "my-app"
    project_id = "project-001"
    chunk_size = 1000
    chunk_overlap = 200
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Parameters:**
- `chunk_size`: Number of characters per chunk (default: 500)
- `chunk_overlap`: Overlapping characters between chunks (default: 50)

---

## Status and Monitoring

### GET Processing Status

Check the status of a document processing job.

**By Job ID:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "processing",
    "job_id": "my-app_project-001_20250120_103000"
  }'
```

**By d_app_id and project_id (gets most recent job):**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "processing",
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "processing"
    job_id = "my-app_project-001_20250120_103000"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response (In Progress):**
```json
{
  "status_type": "processing",
  "timestamp": "2025-01-20T10:35:00Z",
  "processing_status": {
    "job_id": "my-app_project-001_20250120_103000",
    "status": "processing",
    "progress": {
      "percent_complete": 45.5,
      "processed_files": 5,
      "total_files": 11,
      "processed_embeddings": 125,
      "total_embeddings": 275
    },
    "current_file": "document_06.pdf",
    "request": {
      "d_app_id": "my-app",
      "project_id": "project-001"
    },
    "started_at": "2025-01-20T10:30:00Z",
    "estimated_completion": "2025-01-20T10:37:00Z"
  }
}
```

**Response (Completed):**
```json
{
  "status_type": "processing",
  "timestamp": "2025-01-20T10:40:00Z",
  "processing_status": {
    "job_id": "my-app_project-001_20250120_103000",
    "status": "completed",
    "progress": {
      "percent_complete": 100.0,
      "processed_files": 11,
      "total_files": 11,
      "processed_embeddings": 275,
      "total_embeddings": 275
    },
    "request": {
      "d_app_id": "my-app",
      "project_id": "project-001"
    },
    "started_at": "2025-01-20T10:30:00Z",
    "completed_at": "2025-01-20T10:38:45Z",
    "processing_summary": {
      "total_files": 11,
      "successful_files": 10,
      "failed_files": 1,
      "skipped_files": 0,
      "total_chunks": 275,
      "total_embeddings": 275,
      "total_size_bytes": 5242880,
      "processing_time_ms": 525000
    },
    "files": [
      {
        "file_name": "report.pdf",
        "file_path": "C:\\Documents\\report.pdf",
        "status": "completed",
        "chunks": 25,
        "embeddings": 25,
        "file_size_kb": 512.5,
        "processing_time_ms": 45000,
        "ocr_used": false
      }
    ]
  }
}
```

**With File Details:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "processing",
    "job_id": "my-app_project-001_20250120_103000",
    "include_files": true
  }'
```

---

### GET Queue Status

Check job queue status for concurrent job management.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "queue",
    "d_app_id": "my-app"
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "queue"
    d_app_id = "my-app"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status_type": "queue",
  "timestamp": "2025-01-20T10:35:00Z",
  "queue_status": {
    "active_jobs": 2,
    "max_concurrent_jobs": 5,
    "available_slots": 3,
    "queued_jobs": 0,
    "active_job_ids": [
      "my-app_project-001_20250120_103000",
      "my-app_project-002_20250120_103500"
    ]
  }
}
```

---

### GET Quota Status

Check resource quota usage for storage, documents, and embeddings.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "quota",
    "d_app_id": "my-app"
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "quota"
    d_app_id = "my-app"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status_type": "quota",
  "timestamp": "2025-01-20T10:35:00Z",
  "quota_status": {
    "storage": {
      "current_usage_bytes": 524288000,
      "current_usage_formatted": "500.0 MB",
      "max_quota_bytes": 10737418240,
      "max_quota_formatted": "10.0 GB",
      "usage_percent": 4.88,
      "available_bytes": 10213130240,
      "available_formatted": "9.5 GB"
    },
    "documents": {
      "current_usage": 1250,
      "max_quota": 10000,
      "usage_percent": 12.5,
      "available": 8750
    },
    "embeddings": {
      "current_usage": 12500,
      "max_quota": 100000,
      "usage_percent": 12.5,
      "available": 87500
    }
  }
}
```

---

### GET Health Status

Check API health and dependencies.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "health"
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "health"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Alternate Endpoint:**
```bash
curl http://localhost:8500/iblink/v1/documents/health
```

**Response:**
```json
{
  "status_type": "health",
  "timestamp": "2025-01-20T10:35:00Z",
  "health_status": {
    "status": "healthy",
    "version": "1.0.0",
    "uptime_seconds": 3600,
    "database": {
      "status": "healthy",
      "connection": "connected",
      "response_time_ms": 15
    },
    "embedding_api": {
      "status": "healthy",
      "url": "http://localhost:7500",
      "response_time_ms": 45
    },
    "active_jobs": 2,
    "total_documents": 1250,
    "total_embeddings": 12500
  }
}
```

---

### GET Dependency Status

Check status of all external dependencies.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "dependency"
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "dependency"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status_type": "dependency",
  "timestamp": "2025-01-20T10:35:00Z",
  "dependency_status": {
    "overall_status": "healthy",
    "dependencies": [
      {
        "name": "PostgreSQL Database",
        "type": "database",
        "status": "healthy",
        "url": "localhost:5432",
        "response_time_ms": 12,
        "last_checked": "2025-01-20T10:35:00Z"
      },
      {
        "name": "Embedding API",
        "type": "api",
        "status": "healthy",
        "url": "http://localhost:7500",
        "response_time_ms": 38,
        "last_checked": "2025-01-20T10:35:00Z"
      },
      {
        "name": "Retriever API",
        "type": "api",
        "status": "healthy",
        "url": "http://localhost:9100",
        "response_time_ms": 25,
        "last_checked": "2025-01-20T10:35:00Z"
      }
    ]
  }
}
```

---

### List Jobs

Get a list of all jobs for an application.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "jobs",
    "d_app_id": "my-app"
  }'
```

**With Limit:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "jobs",
    "d_app_id": "my-app",
    "limit": 10
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "jobs"
    d_app_id = "my-app"
    limit = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status_type": "jobs",
  "timestamp": "2025-01-20T10:35:00Z",
  "jobs": [
    {
      "job_id": "my-app_project-001_20250120_103000",
      "status": "completed",
      "d_app_id": "my-app",
      "project_id": "project-001",
      "started_at": "2025-01-20T10:30:00Z",
      "completed_at": "2025-01-20T10:38:45Z",
      "progress": {
        "percent_complete": 100.0,
        "processed_files": 11,
        "total_files": 11
      }
    },
    {
      "job_id": "my-app_project-002_20250120_103500",
      "status": "processing",
      "d_app_id": "my-app",
      "project_id": "project-002",
      "started_at": "2025-01-20T10:35:00Z",
      "progress": {
        "percent_complete": 25.0,
        "processed_files": 2,
        "total_files": 8
      }
    }
  ],
  "total_jobs": 2
}
```

---

### Get Active Jobs

Get only currently active (processing) jobs.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "active",
    "d_app_id": "my-app"
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "active"
    d_app_id = "my-app"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status_type": "active",
  "timestamp": "2025-01-20T10:35:00Z",
  "active_jobs": [
    {
      "job_id": "my-app_project-002_20250120_103500",
      "status": "processing",
      "current_file": "document_03.pdf",
      "progress": {
        "percent_complete": 25.0,
        "processed_files": 2,
        "total_files": 8
      },
      "started_at": "2025-01-20T10:35:00Z",
      "estimated_completion": "2025-01-20T10:42:00Z"
    }
  ],
  "total_active": 1
}
```

---

### Cancel Job

Cancel a running job.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "cancel",
    "job_id": "my-app_project-002_20250120_103500"
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "cancel"
    job_id = "my-app_project-002_20250120_103500"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status_type": "cancel",
  "timestamp": "2025-01-20T10:36:00Z",
  "message": "Job cancellation requested",
  "job_id": "my-app_project-002_20250120_103500",
  "previous_status": "processing"
}
```

---

### Cleanup Jobs

Remove completed, failed, or cancelled jobs from the database.

**Cleanup Old Jobs:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "cleanup",
    "d_app_id": "my-app",
    "older_than_hours": 24
  }'
```

**PowerShell:**
```powershell
$body = @{
    status_type = "cleanup"
    d_app_id = "my-app"
    older_than_hours = 24
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status_type": "cleanup",
  "timestamp": "2025-01-20T10:36:00Z",
  "message": "Cleanup completed",
  "jobs_removed": 15,
  "criteria": {
    "older_than_hours": 24,
    "statuses": ["completed", "failed", "cancelled"]
  }
}
```

**Cleanup Orphaned Jobs:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "cleanup_orphaned",
    "d_app_id": "my-app"
  }'
```

---

## Document Operations

### POST /documents/search

Search for documents by content or metadata.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "quarterly financial report",
    "d_app_id": "my-app",
    "project_id": "project-001",
    "top_k": 5
  }'
```

**PowerShell:**
```powershell
$body = @{
    query = "quarterly financial report"
    d_app_id = "my-app"
    project_id = "project-001"
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/search" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "results": [
    {
      "document_id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
      "file_name": "Q4_2024_Report.pdf",
      "file_path": "C:\\Documents\\Q4_2024_Report.pdf",
      "chunk_index": 3,
      "content": "The quarterly financial report for Q4 2024 shows...",
      "similarity_score": 0.92,
      "metadata": {
        "page": 5,
        "section": "Financial Summary"
      }
    },
    {
      "document_id": "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e",
      "file_name": "Annual_Review_2024.pdf",
      "file_path": "C:\\Documents\\Annual_Review_2024.pdf",
      "chunk_index": 12,
      "content": "Our quarterly reports demonstrate consistent growth...",
      "similarity_score": 0.85,
      "metadata": {
        "page": 18,
        "section": "Performance Analysis"
      }
    }
  ],
  "total_results": 2,
  "query": "quarterly financial report"
}
```

---

### POST /documents/extract

Extract text from documents without creating embeddings.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/extract \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "C:\\Documents\\contract.pdf"
  }'
```

**PowerShell:**
```powershell
$body = @{
    file_path = "C:\Documents\contract.pdf"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/extract" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "file_path": "C:\\Documents\\contract.pdf",
  "file_name": "contract.pdf",
  "text": "This Agreement is entered into as of January 1, 2025...",
  "page_count": 15,
  "character_count": 45230,
  "word_count": 8456,
  "extraction_time_ms": 1250,
  "metadata": {
    "title": "Service Agreement",
    "author": "Legal Department",
    "created_date": "2025-01-01",
    "modified_date": "2025-01-05"
  }
}
```

**With OCR:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/extract \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "C:\\Scans\\invoice.pdf",
    "enable_ocr": true
  }'
```

---

### POST /documents/list

List all documents for an application and project.

**cURL:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/list \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

**PowerShell:**
```powershell
$body = @{
    d_app_id = "my-app"
    project_id = "project-001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/list" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**With Pagination:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/list \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app",
    "project_id": "project-001",
    "page": 1,
    "page_size": 50
  }'
```

**Response:**
```json
{
  "documents": [
    {
      "document_id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
      "file_name": "report.pdf",
      "file_path": "C:\\Documents\\report.pdf",
      "file_hash": "sha256:abc123...",
      "file_size_bytes": 524288,
      "file_size_formatted": "512.0 KB",
      "chunk_count": 25,
      "embedding_count": 25,
      "created_at": "2025-01-20T10:30:00Z",
      "updated_at": "2025-01-20T10:30:00Z"
    },
    {
      "document_id": "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e",
      "file_name": "meeting_notes.txt",
      "file_path": "C:\\Documents\\meeting_notes.txt",
      "file_hash": "sha256:def456...",
      "file_size_bytes": 8192,
      "file_size_formatted": "8.0 KB",
      "chunk_count": 3,
      "embedding_count": 3,
      "created_at": "2025-01-20T10:32:00Z",
      "updated_at": "2025-01-20T10:32:00Z"
    }
  ],
  "total_documents": 2,
  "page": 1,
  "page_size": 50,
  "total_pages": 1
}
```

---

### DELETE /documents/delete

Delete documents and their embeddings.

**Delete Specific Documents:**
```bash
curl -X DELETE http://localhost:8500/iblink/v1/documents/delete \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app",
    "project_id": "project-001",
    "document_ids": [
      "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
      "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e"
    ]
  }'
```

**PowerShell:**
```powershell
$body = @{
    d_app_id = "my-app"
    project_id = "project-001"
    document_ids = @(
        "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
        "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e"
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/delete" `
    -Method DELETE `
    -Body $body `
    -ContentType "application/json"
```

**Response:**
```json
{
  "status": "success",
  "deleted_documents": 2,
  "deleted_embeddings": 28,
  "document_ids": [
    "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
    "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e"
  ]
}
```

**Delete All for Project:**
```bash
curl -X DELETE http://localhost:8500/iblink/v1/documents/delete \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app",
    "project_id": "project-001",
    "delete_all": true
  }'
```

**Response:**
```json
{
  "status": "success",
  "deleted_documents": 25,
  "deleted_embeddings": 345,
  "message": "All documents for project 'project-001' have been deleted"
}
```

---

## Complete Workflow Examples

### Workflow 1: Process Documents and Monitor

```bash
# 1. Start document processing
response=$(curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["C:\\Documents\\report.pdf"],
    "d_app_id": "my-app",
    "project_id": "project-001"
  }')

# Extract job_id from response
job_id=$(echo $response | jq -r '.job_id')
echo "Job ID: $job_id"

# 2. Poll status until complete
while true; do
  status=$(curl -X POST http://localhost:8500/iblink/v1/documents/status \
    -H "Content-Type: application/json" \
    -d "{
      \"status_type\": \"processing\",
      \"job_id\": \"$job_id\"
    }" | jq -r '.processing_status.status')

  echo "Status: $status"

  if [ "$status" == "completed" ] || [ "$status" == "failed" ]; then
    break
  fi

  sleep 5
done

# 3. Get final results
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d "{
    \"status_type\": \"processing\",
    \"job_id\": \"$job_id\",
    \"include_files\": true
  }"
```

### Workflow 2: Batch Processing with PowerShell

```powershell
# Process all PDFs in a directory
$directory = "C:\Documents\ToProcess"
$appId = "my-app"
$projectId = "batch-001"

# Start processing
$body = @{
    directories = @($directory)
    d_app_id = $appId
    project_id = $projectId
    enable_ocr = $false
    duplicate_strategy = "skip"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$jobId = $response.job_id
Write-Host "Started job: $jobId"

# Monitor progress
do {
    $statusBody = @{
        status_type = "processing"
        job_id = $jobId
    } | ConvertTo-Json

    $status = Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/status" `
        -Method POST `
        -Body $statusBody `
        -ContentType "application/json"

    $percent = $status.processing_status.progress.percent_complete
    $current = $status.processing_status.progress.processed_files
    $total = $status.processing_status.progress.total_files

    Write-Host "$percent% complete ($current/$total files)"

    Start-Sleep -Seconds 5

} while ($status.processing_status.status -eq "processing")

Write-Host "Processing $($status.processing_status.status)"
```

### Workflow 3: Search and Retrieve

```bash
# 1. Process documents
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "directories": ["C:\\Documents\\Knowledge"],
    "d_app_id": "my-app",
    "project_id": "kb-001"
  }'

# 2. Wait for processing to complete (or poll status)

# 3. Search for relevant documents
curl -X POST http://localhost:8500/iblink/v1/documents/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "product specifications",
    "d_app_id": "my-app",
    "project_id": "kb-001",
    "top_k": 10
  }' | jq '.results[] | {file_name, similarity_score, content}'
```

### Workflow 4: Update Documents with Sync

```bash
# Sync mode removes documents not in the list
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      "C:\\Current\\doc1.pdf",
      "C:\\Current\\doc2.pdf",
      "C:\\Current\\doc3.pdf"
    ],
    "d_app_id": "my-app",
    "project_id": "project-001",
    "duplicate_strategy": "sync"
  }'
```

### Workflow 5: Quota Management

```bash
# 1. Check current quota
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "quota",
    "d_app_id": "my-app"
  }' | jq '.quota_status'

# 2. List all documents
curl -X POST http://localhost:8500/iblink/v1/documents/list \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app",
    "project_id": "project-001"
  }' | jq '.total_documents'

# 3. Delete old documents if needed
curl -X DELETE http://localhost:8500/iblink/v1/documents/delete \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app",
    "project_id": "old-project",
    "delete_all": true
  }'

# 4. Check quota again
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "quota",
    "d_app_id": "my-app"
  }' | jq '.quota_status'
```

---

## Error Handling Examples

### Error Response Format

```json
{
  "error": "Error message description",
  "details": "Additional error context",
  "timestamp": "2025-01-20T10:35:00Z"
}
```

### Common Error Responses

#### Missing Required Parameters

```json
{
  "error": "Either 'files' or 'directories' must be provided"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

#### Storage Quota Exceeded

```json
{
  "error": "Storage quota exceeded",
  "current_usage": "9.8 GB",
  "max_quota": "10.0 GB",
  "requested": "500.0 MB"
}
```

**HTTP Status:** 507 Insufficient Storage

#### Document Quota Exceeded

```json
{
  "error": "Document quota exceeded",
  "current_usage": 9950,
  "max_quota": 10000,
  "requested": 100
}
```

**HTTP Status:** 507 Insufficient Storage

#### Job Queue Full

```json
{
  "error": "Job queue full",
  "message": "Maximum concurrent jobs reached. Job will be queued.",
  "queue_status": {
    "active_jobs": 5,
    "max_concurrent_jobs": 5,
    "queued_jobs": 3
  }
}
```

**HTTP Status:** 429 Too Many Requests

#### Job Not Found

```json
{
  "error": "Job not found",
  "d_app_id": "my-app",
  "project_id": "project-001"
}
```

**HTTP Status:** 404 Not Found

#### Invalid Status Type

```json
{
  "error": "Invalid status_type",
  "valid_types": ["processing", "queue", "quota", "health", "dependency", "jobs", "active", "cancel", "cleanup", "cleanup_orphaned"]
}
```

**HTTP Status:** 400 Bad Request

#### File Not Found

```json
{
  "error": "File not found",
  "file_path": "C:\\Documents\\missing.pdf"
}
```

**HTTP Status:** 404 Not Found

#### Unsupported File Type

```json
{
  "error": "Unsupported file type",
  "file_extension": ".exe",
  "supported_types": [".pdf", ".txt", ".md", ".docx", ".html", ".htm", ".rtf"]
}
```

**HTTP Status:** 400 Bad Request

---

## Tips and Best Practices

### 1. Use Async Processing for Large Jobs

```bash
# Always use async endpoint for multiple files
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "directories": ["C:\\Large\\Directory"],
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'

# Then poll status periodically
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "processing",
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

### 2. Monitor Quota Usage

```bash
# Check quota before large operations
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "quota",
    "d_app_id": "my-app"
  }' | jq '.quota_status.storage.usage_percent'
```

### 3. Use Appropriate Duplicate Strategy

```bash
# Skip duplicates (fastest, default)
duplicate_strategy="skip"

# Update existing documents
duplicate_strategy="update"

# Sync mode (removes orphaned documents)
duplicate_strategy="sync"

curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d "{
    \"files\": [...],
    \"d_app_id\": \"my-app\",
    \"project_id\": \"project-001\",
    \"duplicate_strategy\": \"$duplicate_strategy\"
  }"
```

### 4. Enable OCR Only When Needed

```bash
# OCR is slower and more resource-intensive
# Only enable for scanned documents
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {"file_path": "C:\\Scans\\invoice.pdf", "enable_ocr": true},
      {"file_path": "C:\\Documents\\text.pdf", "enable_ocr": false}
    ],
    "d_app_id": "my-app",
    "project_id": "project-001"
  }'
```

### 5. Optimize Chunk Size

```bash
# Smaller chunks for precise search (default: 500)
chunk_size=300
chunk_overlap=50

# Larger chunks for context retention
chunk_size=1000
chunk_overlap=200

curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d "{
    \"files\": [...],
    \"d_app_id\": \"my-app\",
    \"project_id\": \"project-001\",
    \"chunk_size\": $chunk_size,
    \"chunk_overlap\": $chunk_overlap
  }"
```

### 6. Handle Errors Gracefully

**PowerShell:**
```powershell
try {
    $body = @{
        files = @("C:\Documents\report.pdf")
        d_app_id = "my-app"
        project_id = "project-001"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8500/iblink/v1/documents/process" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"

    Write-Host "Job started: $($response.job_id)"
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json

    if ($statusCode -eq 507) {
        Write-Host "Quota exceeded: $($errorBody.error)" -ForegroundColor Red
    }
    elseif ($statusCode -eq 429) {
        Write-Host "Too many concurrent jobs" -ForegroundColor Yellow
    }
    else {
        Write-Host "Error: $($errorBody.error)" -ForegroundColor Red
    }
}
```

### 7. Clean Up Old Jobs

```bash
# Periodically clean up completed jobs
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "cleanup",
    "d_app_id": "my-app",
    "older_than_hours": 72
  }'
```

### 8. Cancel Long-Running Jobs

```bash
# Cancel a stuck job
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "cancel",
    "job_id": "my-app_project-001_20250120_103000"
  }'
```

### 9. Use Project IDs for Organization

```bash
# Organize documents by project
projects=("project-2024-q1" "project-2024-q2" "project-2024-q3")

for project in "${projects[@]}"; do
  curl -X POST http://localhost:8500/iblink/v1/documents/process \
    -H "Content-Type: application/json" \
    -d "{
      \"directories\": [\"C:\\\\Projects\\\\$project\"],
      \"d_app_id\": \"my-app\",
      \"project_id\": \"$project\"
    }"
done
```

### 10. Monitor Dependencies

```bash
# Check dependency health before processing
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{
    "status_type": "dependency"
  }' | jq '.dependency_status.overall_status'

# If healthy, proceed with processing
if [ "$(curl -s http://localhost:8500/iblink/v1/documents/health | jq -r '.status')" == "healthy" ]; then
  curl -X POST http://localhost:8500/iblink/v1/documents/process \
    -H "Content-Type: application/json" \
    -d '{...}'
fi
```

---

## Supported File Types

- **PDF** (.pdf) - with OCR support
- **Text** (.txt)
- **Markdown** (.md)
- **Word** (.docx)
- **HTML** (.html, .htm)
- **Rich Text** (.rtf)

---

## Performance Considerations

### Processing Times

| File Type | Size | With OCR | Without OCR |
|-----------|------|----------|-------------|
| PDF (text) | 1MB | 2-3s | 1-2s |
| PDF (scanned) | 1MB | 10-15s | N/A |
| DOCX | 500KB | 1-2s | 0.5-1s |
| TXT | 100KB | 0.2-0.5s | 0.2-0.5s |

### Concurrent Jobs

- Default: 5 concurrent jobs per d_app_id
- Configurable via application settings
- Queue management prevents overload

### Quota Limits (Default)

- Storage: 10 GB per d_app_id
- Documents: 10,000 per d_app_id
- Embeddings: 100,000 per d_app_id

---

**Last Updated**: 2025-01-20
**API Version**: 1.0.0
**Default Port**: 8500
**Documentation**: `src/IB-Link.DocumentsAPI/README.md`

---

## Additional Resources

- [DocumentsAPI Architecture](../../ARCHITECTURE_UPDATE.md)
- [Database Schema Documentation](../Database/README.md)
- [Embedding API Documentation](./EmbeddingAPI_Usage_Examples.md)
- [Retriever API Documentation](./RetrieverAPI_Usage_Examples.md)

---

## Quick Reference

### Common Operations

```bash
# Process documents
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{"files": [...], "d_app_id": "app", "project_id": "proj"}'

# Check status
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{"status_type": "processing", "job_id": "..."}'

# Search documents
curl -X POST http://localhost:8500/iblink/v1/documents/search \
  -H "Content-Type: application/json" \
  -d '{"query": "...", "d_app_id": "app", "project_id": "proj"}'

# List documents
curl -X POST http://localhost:8500/iblink/v1/documents/list \
  -H "Content-Type: application/json" \
  -d '{"d_app_id": "app", "project_id": "proj"}'

# Delete documents
curl -X DELETE http://localhost:8500/iblink/v1/documents/delete \
  -H "Content-Type: application/json" \
  -d '{"d_app_id": "app", "project_id": "proj", "document_ids": [...]}'

# Health check
curl http://localhost:8500/iblink/v1/documents/health
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `202 Accepted` - Job created (async processing)
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Job or document not found
- `429 Too Many Requests` - Queue full or rate limited
- `500 Internal Server Error` - Server error
- `507 Insufficient Storage` - Quota exceeded
