from pathlib import Path

from harp.harp_types import Counts, Variant, VariantKey
from harp.process import merge_results, process_chunk


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


def make_variant(
    chrom: str, pos: int, h1_REF=0, h1_ALT=0, h2_REF=0, h2_ALT=0
) -> Variant:
    return Variant(
        key=VariantKey(chrom, pos),
        ref="A",
        alt="T",
        counts=Counts(h1_REF, h1_ALT, h2_REF, h2_ALT),
    )


def test_merge_results_add_new():
    global_variants = {}
    chunk_result = {VariantKey("chr1", 10): make_variant("chr1", 10, h1_REF=1)}

    merge_results(global_variants, chunk_result)

    assert VariantKey("chr1", 10) in global_variants
    var = global_variants[VariantKey("chr1", 10)]
    assert var.counts.h1_REF == 1
    assert var.counts.h1_ALT == 0
    assert var.counts.h2_REF == 0
    assert var.counts.h2_ALT == 0


def test_merge_results_merge_existing():
    v1 = make_variant("chr1", 10, h1_REF=1, h2_ALT=2)
    v2 = make_variant("chr1", 10, h1_REF=3, h2_ALT=1)

    global_variants = {v1.key: v1}
    chunk_result = {v2.key: v2}

    merge_results(global_variants, chunk_result)
    var = global_variants[v1.key]

    # Counts should be summed
    assert var.counts.h1_REF == 4
    assert var.counts.h1_ALT == 0
    assert var.counts.h2_REF == 0
    assert var.counts.h2_ALT == 3
