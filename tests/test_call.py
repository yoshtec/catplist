from catplist import catplist
from click.testing import CliRunner


class TestCatPlist:
    def test_integer(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["./tests/integers.plist"]
        )
        assert "{'integer1': 1, 'integer2': 100000}" in result.output
        assert result.exit_code == 0

    def test_strings(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["./tests/strings.plist"]
        )
        assert "{'stringdict': {'chinese': '他没喝啤酒', 'japanese': '日本語もできる', 'python': '🐍'}}" in result.output
        assert result.exit_code == 0

    def test_strings_yaml(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["--format", "yaml", "./tests/strings.plist"]
        )
        expected_result = """stringdict:
  chinese: 他没喝啤酒
  japanese: 日本語もできる
  python: 🐍"""
        assert expected_result in result.output
        assert result.exit_code == 0

    # make sure the current help is also in the markdown
    def test_help_in_markdown(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["--help"]
        )
        with open("README.md", "r", encoding="utf-8") as fh:
            long_description = fh.read()

            print(result.output)
            print(long_description)
            assert result.output in long_description

    def test_uuid(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["./tests/uuid.plist"]
        )
        assert "{'storeUUID': UUID('3c6a9bac-1e61-4db3-ba70-470fce89729b')}" == result

    def test_uuid_json(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["--format", "json", "./tests/uuid.plist"]
        )
        assert "" == result


    def test_uuid_yaml(self):
        runner = CliRunner()
        result = runner.invoke(
            catplist.catplist, ["--format", "yaml", "./tests/uuid.plist"]
        )
        assert "" == result
