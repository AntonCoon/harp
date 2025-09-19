from pathlib import Path

from harp.harp_io import load_variants_chunk, open_bam_iterator
from harp.harp_types import Variant, VariantKey


def process_chunk(
    bam_path: Path,
    vcf_path: Path,
    chrom: str,
    start: int,
    end: int,
) -> dict[VariantKey, Variant]:
    variants = load_variants_chunk(vcf_path, chrom, start, end)
    if not variants:
        return {}

    for read in open_bam_iterator(bam_path, chrom, start, end):
        if read.is_secondary or read.is_supplementary:
            continue
        if not read.has_tag("HP"):
            continue

        hap = read.get_tag("HP")
        if hap not in (1, 2):
            continue

        for read_idx, ref_idx in read.get_aligned_pairs(matches_only=True):
            if ref_idx is None or VariantKey(chrom, ref_idx) not in variants:
                continue

            key = VariantKey(chrom, ref_idx)
            var: Variant = variants[key]

            base = read.query_sequence[read_idx]
            if base == var.ref:
                var.counts[f"h{hap}_REF"] += 1
            elif base == var.alt:
                var.counts[f"h{hap}_ALT"] += 1

    return variants
