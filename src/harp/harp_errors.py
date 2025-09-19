"""
Custom exceptions for HARP.
"""


class HarpError(Exception):
    """Base class for all HARP-specific errors."""


class VCFParsingError(HarpError):
    """Raised when a VCF file cannot be opened or parsed."""


class BAMProcessingError(HarpError):
    """Raised when a BAM file cannot be processed."""


class InvalidVariantError(HarpError):
    """Raised when variant data is malformed or inconsistent."""
