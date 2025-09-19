"""
I/O functions for reading variants in genomic intervals.
"""

from pathlib import Path
from typing import Iterator

import pysam

from harp.harp_errors import VCFParsingError
from harp.harp_types import Counts, Variant, VariantKey


def load_variants_chunk(
    vcf_path: Path, chrom: str, start: int, end: int
) -> dict[VariantKey, Variant]:
    """
    Load variants from a VCF only within a specified genomic interval.

    Args:
        vcf_path (Path): Path to VCF file (gzipped/indexed or plain).
        chrom (str): Chromosome name.
        start (int): 0-based start position (inclusive).
        end (int): 0-based end position (exclusive).

    Returns:
        dict[VariantKey, Variant]: Dictionary of variants within the interval.
    """
    try:
        vcffile = pysam.VariantFile(str(vcf_path))
    except Exception as e:
        raise VCFParsingError(f"Failed to open VCF: {vcf_path}") from e

    variants: dict[VariantKey, Variant] = {}

    for record in vcffile.fetch(chrom, start, end):
        # Only simple bi-allelic SNVs
        if (
            len(record.alts) != 1
            or len(record.ref) != 1
            or len(record.alts[0]) != 1
        ):
            continue

        key = VariantKey(chrom=chrom, pos=record.pos - 1)
        variants[key] = Variant(
            key=key,
            ref=record.ref,
            alt=record.alts[0],
            counts=Counts(),
        )

    return variants


def open_bam_iterator(
    bam_path: Path, chrom: str, start: int, end: int
) -> Iterator[pysam.AlignedSegment]:
    """
    Open a BAM file, check it exists, and return an
    iterator over reads for the given region.
    """
    if not bam_path.exists():
        raise FileNotFoundError(f"BAM file not found: {bam_path}")

    bamfile = pysam.AlignmentFile(str(bam_path), "rb")
    return bamfile.fetch(chrom, start, end)
