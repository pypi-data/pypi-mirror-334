"""
Rules module for FlatForge.

This module contains the rule classes for validating and transforming flat files.
"""

from flatforge.rules.base import Rule, ValidationRule, TransformerRule, GlobalRule
from flatforge.rules.validation import (
    RequiredRule, NumericRule, StringLengthRule, RegexRule, DateRule, ChoiceRule
)
from flatforge.rules.transformation import (
    TrimRule, CaseRule, PadRule, DateFormatRule, SubstringRule, ReplaceRule
)
from flatforge.rules.global_rules import CountRule, SumRule, ChecksumRule, UniquenessRule

# Register validation rules
VALIDATION_RULES = {
    'required': RequiredRule,
    'numeric': NumericRule,
    'string_length': StringLengthRule,
    'regex': RegexRule,
    'date': DateRule,
    'choice': ChoiceRule
}

# Register transformation rules
TRANSFORMER_RULES = {
    'trim': TrimRule,
    'case': CaseRule,
    'pad': PadRule,
    'date_format': DateFormatRule,
    'substring': SubstringRule,
    'replace': ReplaceRule
}

# Register global rules
GLOBAL_RULES = {
    'count': CountRule,
    'sum': SumRule,
    'checksum': ChecksumRule,
    'uniqueness': UniquenessRule
}

__all__ = [
    'Rule', 'ValidationRule', 'TransformerRule', 'GlobalRule',
    'RequiredRule', 'NumericRule', 'StringLengthRule', 'RegexRule', 'DateRule', 'ChoiceRule',
    'TrimRule', 'CaseRule', 'PadRule', 'DateFormatRule', 'SubstringRule', 'ReplaceRule',
    'CountRule', 'SumRule', 'ChecksumRule', 'UniquenessRule',
    'VALIDATION_RULES', 'TRANSFORMER_RULES', 'GLOBAL_RULES'
] 