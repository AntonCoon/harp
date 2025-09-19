from pathlib import Path

import click

from harp.pipeline import pipeline


@click.group()
@click.version_option(prog_name="HARP")
def cli():
    """HARP — Haplotype Allele Read Profiler"""
    pass


@cli.command()
@click.option(
    "--bam",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Input BAM file (indexed)",
)
@click.option(
    "--vcf",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Input phased VCF file",
)
@click.option(
    "--out",
    type=click.Path(dir_okay=False, path_type=Path),
    required=True,
    help="Output TSV file",
)
@click.option(
    "--threads",
    type=int,
    default=4,
    show_default=True,
    help="Number of parallel threads to use",
)
def run(bam: Path, vcf: Path, out: Path, threads: int):
    """Compute haplotype-specific allele counts for SNVs."""
    click.echo(
        f"Running HARP on:\n  BAM: {bam}\n  VCF: {vcf}\n  Output: {out}"
    )
    pipeline(bam_path=bam, vcf_path=vcf, out_path=out, threads=threads)
    click.echo("HARP finished successfully.")


if __name__ == "__main__":
    cli()
