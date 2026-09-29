"""
Export API endpoints.

Requirements covered:
- REQ-EXP-005: Acknowledge within 2 seconds
- REQ-EXP-008: Prevent duplicate exports
- REQ-EXP-019: Handle expired links
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timedelta
import time

app = FastAPI()


class ExportRequest(BaseModel):
    """REQ-EXP-001, REQ-EXP-002: Supported formats"""
    format: str = Field(..., pattern="^(csv|json)$")
    filters: dict = Field(default_factory=dict)


class ExportCreatedResponse(BaseModel):
    """REQ-EXP-005: Return export ID"""
    export_id: str
    status: str
    status_url: str


class ExportStatusResponse(BaseModel):
    """REQ-EXP-009: Progress tracking"""
    export_id: str
    status: str
    progress_percent: int
    download_url: Optional[str] = None
    file_size: Optional[int] = None
    expires_at: Optional[datetime] = None
    error_message: Optional[str] = None


@app.post("/api/exports", response_model=ExportCreatedResponse, status_code=202)
async def create_export(
    request: ExportRequest,
    user_id: UUID = Depends(get_current_user)
) -> ExportCreatedResponse:
    """
    REQ-EXP-005: When a user requests export, the system shall acknowledge 
    the request within 2 seconds and return an export ID
    
    REQ-EXP-008: When a user requests export while another is in progress,
    the system shall reject the request
    """
    start_time = time.time()
    
    # REQ-EXP-008: Check for existing active export
    active_export = await get_active_export(user_id)
    if active_export:
        raise HTTPException(
            status_code=409,
            detail="Export already in progress"
        )
    
    # Create export record
    export_id = uuid4()
    await create_export_record(
        export_id=export_id,
        user_id=user_id,
        format=request.format,
        filters=request.filters
    )
    
    # Enqueue task (async, non-blocking)
    await enqueue_export_task(
        export_id=str(export_id),
        user_id=str(user_id),
        format=request.format,
        filters=request.filters
    )
    
    # REQ-EXP-005: Verify response time < 2 seconds
    elapsed = time.time() - start_time
    assert elapsed < 2.0, f"Response took {elapsed}s"
    
    return ExportCreatedResponse(
        export_id=str(export_id),
        status="pending",
        status_url=f"/api/exports/{export_id}"
    )


@app.get("/api/exports/{export_id}", response_model=ExportStatusResponse)
async def get_export_status(
    export_id: UUID,
    user_id: UUID = Depends(get_current_user)
) -> ExportStatusResponse:
    """
    REQ-EXP-009: While export is in progress, display progress
    """
    export = await get_export_record(export_id)
    
    if not export:
        raise HTTPException(status_code=404, detail="Export not found")
    
    if export.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # REQ-EXP-019: Check if download link expired
    download_url = None
    if export.status == "completed":
        if export.completed_at + timedelta(days=7) < datetime.now():
            raise HTTPException(status_code=410, detail="Link expired")
        download_url = f"/api/exports/{export_id}/download"
    
    return ExportStatusResponse(
        export_id=str(export_id),
        status=export.status,
        progress_percent=export.progress_percent,
        download_url=download_url,
        file_size=export.file_size,
        expires_at=export.completed_at + timedelta(days=7) if export.completed_at else None,
        error_message=export.error_message
    )


# Helper functions (implementation details)
async def get_current_user() -> UUID:
    """Extract user from JWT token"""
    ...

async def get_active_export(user_id: UUID):
    """Check if user has active export"""
    ...

async def create_export_record(**kwargs):
    """Create export in database"""
    ...

async def enqueue_export_task(**kwargs):
    """Enqueue Celery task"""
    ...

async def get_export_record(export_id: UUID):
    """Get export from database"""
    ...
