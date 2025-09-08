# Create a small fit for purpose data model / tables to store relevant data required 
# for the application to function & outputs.

from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class DataElement:
    name: str
    description: str
    patterns: List[str]


@dataclass
class ExtractionConfig:
    data_elements: List[DataElement]


@dataclass
class DocumentMetadata:
    filename: str
    upload_time: datetime = field(default_factory=datetime.now)
    page_count: int = 0
    file_size_kb: float = 0.0
    
    def to_dict(self):
        """Convert metadata to dictionary"""
        return {
            "filename": self.filename,
            "upload_time": self.upload_time.isoformat(),
            "page_count": self.page_count,
            "file_size_kb": self.file_size_kb
        }

@dataclass
class ExtractionResult:
    document_name: str
    extracted_data: Dict[str, Any]
    confidence_score: float = 0.0
    extraction_timestamp: datetime = field(default_factory=datetime.now)
    processing_time_ms: int = 0
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "document_name": self.document_name,
            "extracted_data": self.extracted_data,
            "confidence_score": self.confidence_score,
            "extraction_timestamp": self.extraction_timestamp.isoformat(),
            "processing_time_ms": self.processing_time_ms
        }



