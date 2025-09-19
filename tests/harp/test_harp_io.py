from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harp.harp_errors import VCFParsingError
from harp.harp_io import load_variants_chunk
from harp.harp_types import Counts, Variant, VariantKey


def test_load_variants_chunk_invalid_file(tmp_path: Path):
    """Test that loading an invalid file raises VCFParsingError."""
    bad_file = tmp_path / "bad.vcf"
    bad_file.write_text("not a VCF")
    with pytest.raises(VCFParsingError):
        load_variants_chunk(bad_file, "chr1", 0, 10)


@patch("harp.harp_io.pysam.VariantFile")
def test_load_variants_chunk_basic(mock_variantfile, tmp_path: Path):
    """Test that load_variants_chunk creates Variant objects
    from mocked VCF records."""
    # Mock one record
    mock_record = MagicMock()
    mock_record.chrom = "chr1"
    mock_record.pos = 5
    mock_record.ref = "A"
    mock_record.alts = ["T"]

    # Configure fetch to return the mocked record
    mock_vcf = MagicMock()
    mock_vcf.fetch.return_value = [mock_record]
    mock_variantfile.return_value = mock_vcf

    vcf_file = tmp_path / "dummy.vcf"
    vcf_file.write_text("")  # content not used due to mocking

    variants = load_variants_chunk(vcf_file, "chr1", 0, 10)
    key = VariantKey("chr1", 4)  # 0-based

    assert key in variants
    var = variants[key]
    assert isinstance(var, Variant)
    assert var.ref == "A"
    assert var.alt == "T"
    assert isinstance(var.counts, Counts)

    # Ensure fetch was called with the correct parameters
    mock_vcf.fetch.assert_called_once_with("chr1", 0, 10)


@patch("harp.harp_io.pysam.VariantFile")
def test_load_variants_chunk_filters(mock_variantfile, tmp_path: Path):
    """Test that non-SNVs are skipped."""
    mock_record = MagicMock()
    mock_record.chrom = "chr1"
    mock_record.pos = 5
    mock_record.ref = "AT"  # not a SNV
    mock_record.alts = ["T"]

    mock_vcf = MagicMock()
    mock_vcf.fetch.return_value = [mock_record]
    mock_variantfile.return_value = mock_vcf

    vcf_file = tmp_path / "dummy.vcf"
    vcf_file.write_text("")

    variants = load_variants_chunk(vcf_file, "chr1", 0, 10)
    assert variants == {}  # non-SNV skipped
