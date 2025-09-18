from click.testing import CliRunner

from harp.harp import cli


def test_run_command_with_invalid_paths():
    """CLI should exit with code 2 if BAM/VCF paths do not exist."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "run",
            "--bam",
            "nonexistent.bam",
            "--vcf",
            "nonexistent.vcf",
            "--out",
            "out.tsv",
        ],
    )
    assert result.exit_code == 2
    assert (
        "Error" in result.output
        or "No such file or directory" in result.output
    )


def test_run_command_with_valid_paths(tmp_path):
    """CLI should run successfully when BAM/VCF exist (even as empty files)."""
    bam = tmp_path / "dummy.bam"
    bam.touch()
    vcf = tmp_path / "dummy.vcf"
    vcf.touch()
    out = tmp_path / "out.tsv"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["run", "--bam", str(bam), "--vcf", str(vcf), "--out", str(out)],
    )
    assert result.exit_code == 0
    assert f"BAM: {bam}" in result.output
    assert f"VCF: {vcf}" in result.output
    assert f"Output TSV: {out}" in result.output
    assert (
        "HARP CLI skeleton ready for future implementation." in result.output
    )


def test_help_shows_commands():
    """Test that --help shows available commands."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "run" in result.output
