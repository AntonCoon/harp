import click


@click.group()
@click.version_option(prog_name="HARP")
def cli():
    """HARP — Haplotype Allele Read Profiler"""
    pass


@cli.command()
@click.option(
    "--bam", type=click.Path(exists=True), help="Input BAM file (indexed)"
)
@click.option(
    "--vcf", type=click.Path(exists=True), help="Input phased VCF file"
)
@click.option("--out", type=click.Path(), help="Output TSV file")
def run(bam, vcf, out):
    """Compute haplotype-specific allele counts for SNVs."""
    click.echo(f"BAM: {bam}")
    click.echo(f"VCF: {vcf}")
    click.echo(f"Output TSV: {out}")
    click.echo("HARP CLI skeleton ready for future implementation.")


if __name__ == "__main__":
    cli()
