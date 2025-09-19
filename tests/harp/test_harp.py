from click.testing import CliRunner

from harp.harp import cli


def test_run_command_with_invalid_paths():
    """CLI should exit with code != 0 if BAM/VCF paths do not exist."""
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
    assert result.exit_code != 0
    assert (
        "No such file or directory" in result.output
        or "Error" in result.output
    )


def test_help_shows_commands():
    """Test that --help shows available commands."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "run" in result.output
