"""
Configuration parser module for FlatForge.

This module contains the classes for parsing configuration files.
"""
import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union

import yaml

from flatforge.core import (
    ConfigError, Field, Record, Section, FileFormat, FileType, SectionType
)


class ConfigParser(ABC):
    """
    Abstract base class for config parsers.
    
    A config parser parses a configuration file that describes the structure
    of a flat file and the rules to apply to each field.
    """
    
    @classmethod
    def from_file(cls, file_path: str) -> 'ConfigParser':
        """
        Create a config parser from a file.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            A config parser instance
            
        Raises:
            ConfigError: If the file cannot be parsed
        """
        if not os.path.exists(file_path):
            raise ConfigError(f"Configuration file not found: {file_path}")
            
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.json':
            return JsonConfigParser(file_path)
        elif file_ext in ('.yaml', '.yml'):
            return YamlConfigParser(file_path)
        else:
            raise ConfigError(f"Unsupported configuration file format: {file_ext}")
    
    def __init__(self, file_path: str):
        """
        Initialize a config parser.
        
        Args:
            file_path: Path to the configuration file
        """
        self.file_path = file_path
        self.config: Dict[str, Any] = {}
    
    @abstractmethod
    def parse(self) -> FileFormat:
        """
        Parse the configuration file.
        
        Returns:
            A FileFormat object representing the parsed configuration
            
        Raises:
            ConfigError: If the configuration is invalid
        """
        pass
    
    def _parse_field(self, field_config: Dict[str, Any]) -> Field:
        """
        Parse a field configuration.
        
        Args:
            field_config: Field configuration dictionary
            
        Returns:
            A Field object
            
        Raises:
            ConfigError: If the field configuration is invalid
        """
        if 'name' not in field_config:
            raise ConfigError("Field must have a name")
        if 'position' not in field_config:
            raise ConfigError(f"Field {field_config['name']} must have a position")
            
        return Field(
            name=field_config['name'],
            position=field_config['position'],
            length=field_config.get('length'),
            rules=field_config.get('rules', []),
            description=field_config.get('description')
        )
    
    def _parse_record(self, record_config: Dict[str, Any]) -> Record:
        """
        Parse a record configuration.
        
        Args:
            record_config: Record configuration dictionary
            
        Returns:
            A Record object
            
        Raises:
            ConfigError: If the record configuration is invalid
        """
        if 'name' not in record_config:
            raise ConfigError("Record must have a name")
        if 'fields' not in record_config:
            raise ConfigError(f"Record {record_config['name']} must have fields")
            
        fields = [self._parse_field(field) for field in record_config['fields']]
        
        # Sort fields by position
        fields.sort(key=lambda f: f.position)
        
        return Record(
            name=record_config['name'],
            fields=fields,
            description=record_config.get('description')
        )
    
    def _parse_section(self, section_config: Dict[str, Any]) -> Section:
        """
        Parse a section configuration.
        
        Args:
            section_config: Section configuration dictionary
            
        Returns:
            A Section object
            
        Raises:
            ConfigError: If the section configuration is invalid
            
        Notes:
            The 'identifier' field is optional. If not provided, the section will be identified
            based on its position in the file:
            - For 2-section files (header + body): header is 1 record, body is the rest
            - For 3-section files (header + body + footer): header is 1 record, 
              body is everything except the last record, footer is the last record
        """
        if 'name' not in section_config:
            raise ConfigError("Section must have a name")
        if 'type' not in section_config:
            raise ConfigError(f"Section {section_config['name']} must have a type")
        if 'record' not in section_config:
            raise ConfigError(f"Section {section_config['name']} must have a record")
            
        try:
            section_type = SectionType(section_config['type'])
        except ValueError:
            raise ConfigError(f"Invalid section type: {section_config['type']}")
            
        record = self._parse_record(section_config['record'])
        
        return Section(
            name=section_config['name'],
            type=section_type,
            record=record,
            min_records=section_config.get('min_records', 1),
            max_records=section_config.get('max_records'),
            identifier=section_config.get('identifier'),
            description=section_config.get('description')
        )
    
    def _parse_file_format(self, config: Dict[str, Any]) -> FileFormat:
        """
        Parse a file format configuration.
        
        Args:
            config: File format configuration dictionary
            
        Returns:
            A FileFormat object
            
        Raises:
            ConfigError: If the file format configuration is invalid
        """
        if 'name' not in config:
            raise ConfigError("File format must have a name")
        if 'type' not in config:
            raise ConfigError(f"File format {config['name']} must have a type")
        if 'sections' not in config:
            raise ConfigError(f"File format {config['name']} must have sections")
            
        try:
            file_type = FileType(config['type'])
        except ValueError:
            raise ConfigError(f"Invalid file type: {config['type']}")
            
        sections = [self._parse_section(section) for section in config['sections']]
        
        # Validate that there is at most one header and one footer
        header_count = sum(1 for s in sections if s.type == SectionType.HEADER)
        if header_count > 1:
            raise ConfigError("File format can have at most one header section")
            
        footer_count = sum(1 for s in sections if s.type == SectionType.FOOTER)
        if footer_count > 1:
            raise ConfigError("File format can have at most one footer section")
            
        # Validate that there is at least one body section
        body_count = sum(1 for s in sections if s.type == SectionType.BODY)
        if body_count == 0:
            raise ConfigError("File format must have at least one body section")
            
        return FileFormat(
            name=config['name'],
            type=file_type,
            sections=sections,
            delimiter=config.get('delimiter'),
            quote_char=config.get('quote_char'),
            escape_char=config.get('escape_char'),
            newline=config.get('newline', '\n'),
            encoding=config.get('encoding', 'utf-8'),
            skip_blank_lines=config.get('skip_blank_lines', True),
            exit_on_first_error=config.get('exit_on_first_error', False),
            description=config.get('description')
        )


class JsonConfigParser(ConfigParser):
    """Config parser for JSON configuration files."""
    
    def parse(self) -> FileFormat:
        """
        Parse a JSON configuration file.
        
        Returns:
            A FileFormat object representing the parsed configuration
            
        Raises:
            ConfigError: If the configuration is invalid
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in configuration file: {str(e)}")
        except Exception as e:
            raise ConfigError(f"Error reading configuration file: {str(e)}")
            
        return self._parse_file_format(self.config)


class YamlConfigParser(ConfigParser):
    """Config parser for YAML configuration files."""
    
    def parse(self) -> FileFormat:
        """
        Parse a YAML configuration file.
        
        Returns:
            A FileFormat object representing the parsed configuration
            
        Raises:
            ConfigError: If the configuration is invalid
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigError(f"Invalid YAML in configuration file: {str(e)}")
        except Exception as e:
            raise ConfigError(f"Error reading configuration file: {str(e)}")
            
        return self._parse_file_format(self.config) 