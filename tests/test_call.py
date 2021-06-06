from catplist import catplist
from click.testing import CliRunner


class TestCatPlist:
    def test_integer(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["./test/integers.plist"]
        )
        assert "{'integer1': 1, 'integer2': 100000}" in result.output
        assert result.exit_code == 0

    def test_strings(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["./test/strings.plist"]
        )
        assert "{'stringdict': {'chinese': '他没喝啤酒', 'japanese': '日本語もできる', 'python': '🐍'}}" in result.output
        assert result.exit_code == 0

    # make sure the current help is also in the markdown
    def test_help_in_markdown(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["--help"]
        )
        with open("README.md", "r", encoding="utf-8") as fh:
            long_description = fh.read()

            #print(result.output)
            #print(long_description)
            assert result.output in long_description
