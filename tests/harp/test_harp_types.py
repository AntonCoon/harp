import pytest

from harp.harp_types import Counts, Variant, VariantKey


def test_counts_iadd():
    c1 = Counts(h1_ref=1, h1_alt=2, h2_ref=3, h2_alt=4)
    c2 = Counts(h1_ref=10, h1_alt=20, h2_ref=30, h2_alt=40)
    c1 += c2
    assert c1.h1_ref == 11
    assert c1.h1_alt == 22
    assert c1.h2_ref == 33
    assert c1.h2_alt == 44


def test_variant_iadd_success():
    key = VariantKey("chr1", 100)
    v1 = Variant(key, "A", "T", Counts(1, 1, 1, 1))
    v2 = Variant(key, "A", "T", Counts(2, 2, 2, 2))
    v1 += v2
    assert v1.counts.h1_ref == 3
    assert v1.counts.h2_alt == 3


def test_variant_iadd_key_mismatch():
    v1 = Variant(VariantKey("chr1", 100), "A", "T", Counts())
    v2 = Variant(VariantKey("chr1", 101), "A", "T", Counts())
    with pytest.raises(ValueError):
        v1 += v2


def test_variant_iadd_allele_mismatch():
    key = VariantKey("chr1", 100)
    v1 = Variant(key, "A", "T", Counts())
    v2 = Variant(key, "G", "T", Counts())
    with pytest.raises(ValueError):
        v1 += v2
