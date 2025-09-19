# HARP

HARP — **Haplotype Allele Read Profiler**.  
A Python tool for counting **haplotype-specific read support** for SNVs from a haplotagged BAM file and a phased VCF file.

---

## Features

- Computes allele counts per haplotype (h1 and h2) for SNVs.
- Supports parallel processing of BAM files for faster execution.
- Handles indexed BAM and bgzipped VCF files.
- Produces a simple TSV output suitable for downstream analysis.

---

## Installation

Using [Poetry](https://python-poetry.org/):

```bash
git clone https://github.com/yourusername/harp.git
cd harp
poetry install
```

## Usage

Run HARP via CLI:
```bash
poetry run harp run --bam PATH_TO_BAM --vcf PATH_TO_VCF --out OUTPUT_TSV [--threads N]
```

Example
```bash
poetry run harp run \
    --bam specification/test_data/giab_2023.05.hg002.haplotagged.chr16_28000000_29000000.processed.30x.bam \
    --vcf specification/test_data/giab_2023.05.hg002.wf_snp.chr16_28000000_29000000.vcf.gz \
    --out result.tsv \
    --threads 4
```

CLI options:

- bam FILE — Input BAM file (indexed) [required]
- vcf FILE — Input phased VCF file [required]
- out FILE — Output TSV file [required]
- threads INTEGER — Number of parallel threads to use (default: 4)

## Output Format

The output is a tab-separated file with the following columns:
- `chrom` — Chromosome name
pos — 0-based genomic position of the variant
- `h1_REF` — Number of reads supporting the reference allele on haplotype 1
- `h1_ALT` — Number of reads supporting the alternate allele on haplotype 1
- `h2_REF` — Number of reads supporting the reference allele on haplotype 2
- `h2_ALT` — Number of reads supporting the alternate allele on haplotype 2

Example output:
```python-repl
chrom	pos	    h1_REF	h1_ALT	h2_REF	h2_ALT
chr16	28001380	11	    4	    3	    12
chr16	28002343	11	    5	    3	    12
chr16	28003017	12	    4	    3	    13
chr16	28003087	12	    4	    3	    11
chr16	28004800	13	    4	    3	    9
...
```

## Notes

- HARP assumes that the BAM file is **haplotagged** (`HP` tag present).
- The BAM file must be **coordinate-sorted** and indexed (`.bai` present). Unsorted BAMs will lead to incorrect counts or skipped reads.
- Only **bi-allelic SNVs** are counted.
- Chunk size and threading can be tuned for performance.
