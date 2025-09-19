from pathlib import Path

from harp.harp_types import Variant, VariantKey


def write_results(
    out_path: Path, global_variants: dict[VariantKey, Variant]
) -> None:
    """
    Write the global variant counts to a TSV file.

    Args:
        out_path (Path): Path to the output TSV file.
        global_variants (dict[VariantKey, Variant]): Merged variant counts.
    """
    with open(out_path, "w") as outfile:
        outfile.write("chrom\tpos\th1_REF\th1_ALT\th2_REF\th2_ALT\n")
        for key in sorted(
            global_variants.keys(), key=lambda k: (k.chrom, k.pos)
        ):
            var = global_variants[key]
            c = var.counts
            outfile.write(
                f"{key.chrom}\t{key.pos}\t"
                f"{c.h1_ref}\t{c.h1_alt}\t"
                f"{c.h2_ref}\t{c.h2_alt}\n"
            )
