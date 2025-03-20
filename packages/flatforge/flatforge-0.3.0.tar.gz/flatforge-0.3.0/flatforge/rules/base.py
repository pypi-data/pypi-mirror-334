"""
Base rule classes for FlatForge.

This module contains the abstract base classes for rules in the FlatForge library.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from flatforge.core import ValidationError, FieldValue, ParsedRecord


class Rule(ABC):
    """
    Abstract base class for all rules.
    
    A rule is a check that is applied to an individual field of the parser input file.
    Rules can either validate or transform field values.
    """
    
    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None):
        """
        Initialize a rule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        self.name = name
        self.params = params or {}
    
    @abstractmethod
    def apply(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Apply the rule to a field value.
        
        Args:
            field_value: The field value to apply the rule to
            record: The record containing the field value
            
        Raises:
            ValidationError: If the rule fails
        """
        pass


class ValidationRule(Rule):
    """
    Abstract base class for validation rules.
    
    A validation rule performs validation on an input field against predefined
    validation rules and throws a graceful exception with specific error code
    which tells what rule has been violated.
    """
    
    @abstractmethod
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate a field value.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If validation fails
        """
        pass
    
    def apply(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Apply the validation rule to a field value.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
        """
        try:
            self.validate(field_value, record)
        except ValidationError as e:
            field_value.errors.append(e)
            record.is_valid = False


class TransformerRule(Rule):
    """
    Abstract base class for transformer rules.
    
    A transformer rule converts an input field to an output field based on
    predefined transformation rules.
    """
    
    @abstractmethod
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> Any:
        """
        Transform a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The transformed value
            
        Raises:
            TransformationError: If transformation fails
        """
        pass
    
    def apply(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Apply the transformer rule to a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
        """
        try:
            field_value.transformed_value = self.transform(field_value, record)
        except Exception as e:
            error = ValidationError(
                f"Transformation failed: {str(e)}",
                field_name=field_value.field.name,
                rule_name=self.name,
                section_name=record.section.name,
                record_number=record.record_number,
                field_value=field_value.value
            )
            field_value.errors.append(error)
            record.is_valid = False


class GlobalRule(ABC):
    """
    Abstract base class for global rules.
    
    A global rule is applied across all rows of the input flat file.
    
    Attributes:
        name: The name of the rule
        params: Parameters for the rule
        state: State dictionary for storing rule-specific state
    """
    
    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None):
        """
        Initialize a global rule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        self.name = name
        self.params = params or {}
        self.state: Dict[str, Any] = {}
    
    @abstractmethod
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        This method is called for each record in the file.
        
        Args:
            record: The record to process
        """
        pass
    
    @abstractmethod
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        This method is called after all records have been processed.
        
        Returns:
            A list of validation errors, if any
        """
        pass
        
    def calculate_value(self) -> Any:
        """
        Calculate the value for this global rule.
        
        This method is called after all records have been processed to calculate
        the final value for the rule (e.g., sum, count, checksum).
        
        Returns:
            The calculated value
        """
        return None
        
    def should_insert_value(self) -> bool:
        """
        Determine if this rule should insert its calculated value.
        
        Returns:
            True if the rule should insert its calculated value, False otherwise
        """
        return self.params.get("insert_value", False)
        
    def get_target_field(self) -> Optional[str]:
        """
        Get the target field for inserting the calculated value.
        
        Returns:
            The target field in the format "section.field", or None if not specified
        """
        return self.params.get("target_field") 