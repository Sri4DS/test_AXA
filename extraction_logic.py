import fitz  # PyMuPDF
import re
from typing import Dict, List, Optional, Tuple
import time
from dataclasses import dataclass
from data_model import DataElement, ExtractionResult, DocumentMetadata
import yaml
from datetime import datetime

@dataclass
class ExtractionConfig:
    data_elements: List[DataElement]

class PDFExtractor:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        
    def load_config(self, config_path: str) -> ExtractionConfig:
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            return ExtractionConfig(
                data_elements=[DataElement(**elem) for elem in config_data['data_elements']]
            )
        except Exception as e:
            raise Exception(f"Failed to load config: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract all text from PDF content"""
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_data_element(self, text: str, element: DataElement) -> Optional[str]:
        """Extract specific data element using pattern matching"""
        try:
            lines = text.split('\n')
            
            for pattern in element.patterns:
                for i, line in enumerate(lines):
                    if pattern.lower() in line.lower():
                        # Look for value in current or next line
                        value_line = line
                        if ':' in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                value_line = parts[1].strip()
                        elif i + 1 < len(lines) and lines[i + 1].strip():
                            value_line = lines[i + 1].strip()
                        
                        if value_line and not any(p.lower() in value_line.lower() for p in element.patterns):
                            # Clean up the extracted value
                            value = self.clean_extracted_value(value_line)
                            if value:
                                return value
            return None
        except Exception:
            return None
    
    def clean_extracted_value(self, value: str) -> str:
        """Clean and validate extracted values"""
        try:
            value = value.strip()
            
            # Remove common prefixes/suffixes and clean up
            value = re.sub(r'^[:\-\s\._]+|[:\-\s\._]+$', '', value)
            value = re.sub(r'\s+', ' ', value)
            
            return value if value else None
        except Exception:
            return None
    
    def extract_all_data(self, pdf_content: bytes, filename: str) -> ExtractionResult:
        """Extract all configured data elements from PDF"""
        start_time = time.time()
        
        try:
            text = self.extract_text_from_pdf(pdf_content)
            extracted_data = {}
            successful_extractions = 0
            
            for element in self.config.data_elements:
                value = self.extract_data_element(text, element)
                if value:
                    extracted_data[element.name] = value
                    successful_extractions += 1
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            confidence_score = successful_extractions / len(self.config.data_elements) if self.config.data_elements else 0
            
            return ExtractionResult(
                document_name=filename,
                extracted_data=extracted_data,
                confidence_score=round(confidence_score, 2),
                extraction_timestamp=datetime.now(),
                processing_time_ms=processing_time_ms
            )
            
        except Exception as e:
            raise Exception(f"Extraction failed: {str(e)}")
    
    def get_document_metadata(self, pdf_content: bytes, filename: str) -> DocumentMetadata:
        """Get metadata about the uploaded document"""
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            metadata = DocumentMetadata(
                filename=filename,
                upload_time=datetime.now(),
                page_count=len(doc),
                file_size_kb=len(pdf_content) / 1024
            )
            doc.close()
            return metadata
        except Exception as e:
            raise Exception(f"Failed to get document metadata: {str(e)}")