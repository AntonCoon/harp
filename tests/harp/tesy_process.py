from pathlib import Path

from harp.harp_types import Counts, Variant, VariantKey
from harp.process import process_chunk


def test_process_chunk_minimal(tmp_path: Path):
    # Use dummy paths; we just want to make sure the function runs
    bam_path = tmp_path / "dummy.bam"
    vcf_path = tmp_path / "dummy.vcf"

    # Create empty files so function doesn't crash opening them
    bam_path.write_bytes(b"")
    vcf_path.write_text("")

    result = process_chunk(bam_path, vcf_path, "chr1", 0, 10)
    # Should return a dict (empty in this minimal case)
    assert isinstance(result, dict)


def test_process_chunk_return_type(tmp_path: Path):
    # Dummy files again
    bam_path = tmp_path / "dummy.bam"
    vcf_path = tmp_path / "dummy.vcf"

    bam_path.write_bytes(b"")
    vcf_path.write_text("")

    result = process_chunk(bam_path, vcf_path, "chr1", 0, 10)
    # Keys (if any) should be VariantKey
    for key, var in result.items():
        assert isinstance(key, VariantKey)
        assert isinstance(var, Variant)
        assert isinstance(var.counts, Counts)
