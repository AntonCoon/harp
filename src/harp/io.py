"""
I/O functions for reading variants and alignments.
"""

import pysam

from harp.harp_errors import VCFParsingError
from harp.harp_types import Counts, Variant, VariantKey


def load_variants(vcf_path: str) -> dict[str, dict[int, Variant]]:
    """
    Load variants from a VCF into a nested dictionary.

    The structure is:
        chrom -> { pos0: Variant }

    Only bi-allelic SNVs (single nucleotide variants) are included.

    Args:
        vcf_path (str): Path to a VCF file (optionally gzipped and indexed).

    Returns:
        dict[str, dict[int, Variant]]: Dictionary of variants grouped by
        chromosome and position.

    Raises:
        VCFParsingError: If the VCF cannot be opened or parsed.
    """
    try:
        vcffile = pysam.VariantFile(vcf_path)
    except Exception as e:
        raise VCFParsingError(f"Failed to open VCF: {vcf_path}") from e

    variants_by_chrom: dict[str, dict[int, Variant]] = {}

    for record in vcffile.fetch():
        # Only keep simple bi-allelic SNVs
        if (
            len(record.alts) != 1
            or len(record.ref) != 1
            or len(record.alts[0]) != 1
        ):
            continue

        chrom = record.chrom
        pos0 = record.pos - 1  # convert to 0-based

        key = VariantKey(chrom=chrom, pos=pos0)
        variant = Variant(
            key=key,
            ref=record.ref,
            alt=record.alts[0],
            counts=Counts(),
        )

        variants_by_chrom.setdefault(chrom, {})[pos0] = variant

    return variants_by_chrom
