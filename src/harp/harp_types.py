"""
Custom data types used throughout HARP.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VariantKey:
    """
    Represents a genomic variant key uniquely identified by chromosome
    and position.

    Attributes:
        chrom (str): Chromosome name.
        pos (int): 0-based genomic position.
    """

    chrom: str
    pos: int


@dataclass
class Counts:
    """
    Stores allele counts for haplotypes 1 and 2.

    Attributes:
        h1_ref (int): Number of reads supporting REF allele on haplotype 1.
        h1_alt (int): Number of reads supporting ALT allele on haplotype 1.
        h2_ref (int): Number of reads supporting REF allele on haplotype 2.
        h2_alt (int): Number of reads supporting ALT allele on haplotype 2.
    """

    h1_ref: int = 0
    h1_alt: int = 0
    h2_ref: int = 0
    h2_alt: int = 0

    def __iadd__(self, other: "Counts") -> "Counts":
        """In-place addition of counts from another `Counts` object."""
        self.h1_ref += other.h1_ref
        self.h1_alt += other.h1_alt
        self.h2_ref += other.h2_ref
        self.h2_alt += other.h2_alt
        return self


@dataclass
class Variant:
    """
    Represents a single SNV with reference/alternate alleles and counts.

    Attributes:
        key (VariantKey): Genomic location of the variant.
        ref (str): Reference allele.
        alt (str): Alternate allele.
        counts (Counts): Read support counts for each haplotype/allele.
    """

    key: VariantKey
    ref: str
    alt: str
    counts: Counts

    def __iadd__(self, other: "Variant") -> "Variant":
        """
        In-place addition of counts from another Variant.

        Raises:
            ValueError: if ref/alt alleles or key do not match.
        """
        if self.key != other.key:
            raise ValueError(
                f"Cannot merge variants with different keys: "
                f"{self.key} != {other.key}"
            )
        if self.ref != other.ref or self.alt != other.alt:
            raise ValueError(
                f"Cannot merge variants with different alleles: "
                f"{self.ref}/{self.alt} != {other.ref}/{other.alt}"
            )

        self.counts += other.counts
        return self
