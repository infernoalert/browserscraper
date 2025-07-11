"""
File utilities for browser scraper
"""

import os
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from .logger import ScraperLogger
from .exceptions import OutputException


class FileHandler:
    """Handles file operations for scraped data"""
    
    def __init__(self, output_dir: str = "output", logger: Optional[ScraperLogger] = None):
        self.output_dir = Path(output_dir)
        self.logger = logger
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            if self.logger:
                self.logger.info(f"Output directory ensured: {self.output_dir}")
        except Exception as e:
            raise OutputException(f"Failed to create output directory: {str(e)}")
    
    def generate_filename(self, prefix: str, extension: str, include_timestamp: bool = True) -> str:
        """Generate filename with optional timestamp"""
        if include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{prefix}_{timestamp}.{extension}"
        return f"{prefix}.{extension}"
    
    def save_json(self, data: Any, filename: str, indent: int = 2) -> str:
        """Save data as JSON file"""
        try:
            file_path = self.output_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            
            if self.logger:
                self.logger.info(f"JSON file saved: {file_path}")
            return str(file_path)
        except Exception as e:
            raise OutputException(f"Failed to save JSON file: {str(e)}")
    
    def save_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Save data as CSV file"""
        try:
            if not data:
                raise OutputException("No data to save")
            
            file_path = self.output_dir / filename
            
            # Get headers from first row
            headers = list(data[0].keys())
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            
            if self.logger:
                self.logger.info(f"CSV file saved: {file_path}")
            return str(file_path)
        except Exception as e:
            raise OutputException(f"Failed to save CSV file: {str(e)}")
    
    def save_xml(self, data: Any, filename: str, root_element: str = "data") -> str:
        """Save data as XML file"""
        try:
            file_path = self.output_dir / filename
            
            # Create root element
            root = ET.Element(root_element)
            
            # Convert data to XML
            if isinstance(data, list):
                for i, item in enumerate(data):
                    item_elem = ET.SubElement(root, "item", {"id": str(i)})
                    self._dict_to_xml(item, item_elem)
            elif isinstance(data, dict):
                self._dict_to_xml(data, root)
            else:
                root.text = str(data)
            
            # Write to file
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            
            if self.logger:
                self.logger.info(f"XML file saved: {file_path}")
            return str(file_path)
        except Exception as e:
            raise OutputException(f"Failed to save XML file: {str(e)}")
    
    def _dict_to_xml(self, data: Dict[str, Any], parent: ET.Element):
        """Convert dictionary to XML elements"""
        for key, value in data.items():
            # Clean key name for XML
            clean_key = str(key).replace(' ', '_').replace('-', '_')
            
            if isinstance(value, dict):
                elem = ET.SubElement(parent, clean_key)
                self._dict_to_xml(value, elem)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    elem = ET.SubElement(parent, clean_key, {"index": str(i)})
                    if isinstance(item, dict):
                        self._dict_to_xml(item, elem)
                    else:
                        elem.text = str(item)
            else:
                elem = ET.SubElement(parent, clean_key)
                elem.text = str(value)
    
    def save_text(self, data: str, filename: str) -> str:
        """Save data as text file"""
        try:
            file_path = self.output_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
            
            if self.logger:
                self.logger.info(f"Text file saved: {file_path}")
            return str(file_path)
        except Exception as e:
            raise OutputException(f"Failed to save text file: {str(e)}")
    
    def create_backup(self, file_path: str) -> str:
        """Create backup of existing file"""
        try:
            original_path = Path(file_path)
            if original_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = original_path.with_suffix(f".backup_{timestamp}{original_path.suffix}")
                
                # Copy file
                import shutil
                shutil.copy2(original_path, backup_path)
                
                if self.logger:
                    self.logger.info(f"Backup created: {backup_path}")
                return str(backup_path)
            else:
                if self.logger:
                    self.logger.warning(f"Original file not found for backup: {file_path}")
                return ""
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to create backup: {str(e)}")
            return ""
    
    def load_json(self, filename: str) -> Any:
        """Load data from JSON file"""
        try:
            file_path = self.output_dir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise OutputException(f"Failed to load JSON file: {str(e)}")
    
    def load_csv(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from CSV file"""
        try:
            file_path = self.output_dir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            raise OutputException(f"Failed to load CSV file: {str(e)}")
    
    def file_exists(self, filename: str) -> bool:
        """Check if file exists"""
        file_path = self.output_dir / filename
        return file_path.exists()
    
    def get_file_size(self, filename: str) -> int:
        """Get file size in bytes"""
        try:
            file_path = self.output_dir / filename
            return file_path.stat().st_size
        except Exception as e:
            raise OutputException(f"Failed to get file size: {str(e)}")
    
    def list_files(self, extension: Optional[str] = None) -> List[str]:
        """List files in output directory"""
        try:
            files = []
            for file_path in self.output_dir.iterdir():
                if file_path.is_file():
                    if extension is None or file_path.suffix.lower() == f".{extension.lower()}":
                        files.append(file_path.name)
            return sorted(files)
        except Exception as e:
            raise OutputException(f"Failed to list files: {str(e)}")
    
    def delete_file(self, filename: str) -> bool:
        """Delete file"""
        try:
            file_path = self.output_dir / filename
            if file_path.exists():
                file_path.unlink()
                if self.logger:
                    self.logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to delete file: {str(e)}")
            return False


class DataExporter:
    """Exports scraped data in various formats"""
    
    def __init__(self, file_handler: FileHandler, logger: Optional[ScraperLogger] = None):
        self.file_handler = file_handler
        self.logger = logger
    
    def export_data(self, data: Any, format_type: str, filename_prefix: str = "scraped_data", 
                   include_timestamp: bool = True, create_backup: bool = False) -> str:
        """Export data in specified format"""
        try:
            # Generate filename
            filename = self.file_handler.generate_filename(
                filename_prefix, format_type, include_timestamp
            )
            
            # Create backup if requested
            if create_backup and self.file_handler.file_exists(filename):
                self.file_handler.create_backup(str(self.file_handler.output_dir / filename))
            
            # Export based on format
            if format_type.lower() == 'json':
                return self.file_handler.save_json(data, filename)
            elif format_type.lower() == 'csv':
                if not isinstance(data, list):
                    data = [data] if isinstance(data, dict) else [{"data": data}]
                return self.file_handler.save_csv(data, filename)
            elif format_type.lower() == 'xml':
                return self.file_handler.save_xml(data, filename)
            elif format_type.lower() == 'txt':
                text_data = json.dumps(data, indent=2) if not isinstance(data, str) else data
                return self.file_handler.save_text(text_data, filename)
            else:
                raise OutputException(f"Unsupported format: {format_type}")
        
        except Exception as e:
            raise OutputException(f"Failed to export data: {str(e)}")
    
    def export_summary(self, data: Any, stats: Dict[str, Any], filename_prefix: str = "summary") -> str:
        """Export data summary with statistics"""
        try:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "statistics": stats,
                "sample_data": data[:5] if isinstance(data, list) and len(data) > 5 else data
            }
            
            filename = self.file_handler.generate_filename(filename_prefix, "json", True)
            return self.file_handler.save_json(summary, filename)
        
        except Exception as e:
            raise OutputException(f"Failed to export summary: {str(e)}") 