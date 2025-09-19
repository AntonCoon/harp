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
    """
    Process a genomic interval from a BAM and VCF file,
    counting allele support per haplotype.

    Args:
        bam_path (Path): Path to the haplotagged BAM file.
        vcf_path (Path): Path to the VCF file containing variants.
        chrom (str): Chromosome name.
        start (int): Start position of the interval (0-based, inclusive).
        end (int): End position of the interval (0-based, exclusive).

    Returns:
        dict[VariantKey, Variant]: Dictionary mapping VariantKey to
        Variant with updated counts.
    """
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
                if hap == 1:
                    var.counts.h1_ref += 1
                else:
                    var.counts.h2_ref += 1
            elif base == var.alt:
                if hap == 1:
                    var.counts.h1_alt += 1
                else:
                    var.counts.h2_alt += 1

    return variants


def merge_results(
    global_variants: dict[VariantKey, Variant],
    chunk_result: dict[VariantKey, Variant],
):
    """
    Merge counts from a single chunk into the global variants dictionary.

    Args:
        global_variants (dict[VariantKey, Variant]): Dictionary storing
        cumulative Variant counts.
        chunk_result (dict[VariantKey, Variant]): Dictionary with Variant
        counts from one chunk.

    Modifies:
        global_variants in-place by summing counts with chunk_result.
    """
    for key, var in chunk_result.items():
        if key not in global_variants:
            global_variants[key] = var
        else:
            global_variants[key] += var
