import pytest

from harp.harp_errors import VCFParsingError
from harp.io import load_variants


def test_load_variants_success(tmp_path):
    vcf_content = (
        "##fileformat=VCFv4.2\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
        "chr1\t10\t.\tA\tT\t.\t.\t.\n"
        "chr1\t20\t.\tG\tC\t.\t.\t.\n"
    )
    vcf_file = tmp_path / "test.vcf"
    vcf_file.write_text(vcf_content)

    variants = load_variants(str(vcf_file))
    assert "chr1" in variants
    assert 9 in variants["chr1"]  # 0-based
    assert 19 in variants["chr1"]


def test_load_variants_invalid_file(tmp_path):
    bad_file = tmp_path / "bad.vcf"
    bad_file.write_text("not a vcf")
    with pytest.raises(VCFParsingError):
        load_variants(str(bad_file))
