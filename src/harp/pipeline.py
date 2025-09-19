from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pysam
from tqdm import tqdm

from harp.harp_log import get_logger
from harp.harp_types import Variant, VariantKey
from harp.process import merge_results, process_chunk
from harp.writer import write_results

CHUNK_SIZE = 200_000  # Increase to reduce number of futures

logger = get_logger()


def pipeline(
    bam_path: Path, vcf_path: Path, out_path: Path, threads: int
) -> None:
    """Run HARP pipeline with multiprocessing and efficient merging."""

    logger.info("Starting HARP pipeline")
    logger.info(f"BAM file: {bam_path}")
    logger.info(f"VCF file: {vcf_path}")
    logger.info(f"Output file: {out_path}")
    logger.info(f"Threads: {threads}")

    global_variants: dict[VariantKey, Variant] = {}

    # Collect chromosome lengths
    with pysam.AlignmentFile(str(bam_path), "rb") as bamfile:
        chrom_lengths = {
            chrom: bamfile.get_reference_length(chrom)
            for chrom in bamfile.references
        }
    logger.info(f"Found {len(chrom_lengths)} chromosomes to process")

    # Submit jobs
    futures = []
    with ProcessPoolExecutor(max_workers=threads) as executor:
        for chrom, length in chrom_lengths.items():
            logger.info(f"Submitting chunks for {chrom} ({length:,} bp)")
            for start in range(0, length, CHUNK_SIZE):
                end = min(start + CHUNK_SIZE, length)
                futures.append(
                    executor.submit(
                        process_chunk, bam_path, vcf_path, chrom, start, end
                    )
                )

        # Merge as they complete
        for fut in tqdm(
            as_completed(futures), total=len(futures), desc="Processing chunks"
        ):
            chunk_result = fut.result()
            if chunk_result:
                merge_results(global_variants, chunk_result)

    logger.info("Merging complete")
    logger.info("Writing results...")

    # Write final results
    write_results(out_path, global_variants)

    logger.info("Pipeline finished successfully")
