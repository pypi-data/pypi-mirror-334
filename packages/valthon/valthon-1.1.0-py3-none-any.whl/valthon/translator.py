#! /usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from valthon import VAL2PY_MAPPINGS, VERSION_NUMBER
from valthon.logger import Logger


def ends_in_py(word: str) -> bool:
    """Return True if word ends in .py, else False.

    Returns:
        boolean: Whether 'word' ends with 'py' or not

    """
    return word[-3:] == ".py"


def change_file_name(name: str, outputname: str | None = None) -> str:
    """Change *.py filenames to *.vln filenames.

    If filename does not end in .py, add .vln to the end.

    Returns:
        str: Resulting filename with *.vln at the end (unless 'outputname' is
        specified, then that is returned).

    """
    # If outputname is specified, return that
    if outputname is not None:
        return outputname

    # Otherwise, create a new name
    if ends_in_py(name):
        return name[:-3] + ".vln"
    return name + ".vln"


def translate_dictionary(definition_string: str) -> str:
    """Translate one specific dictionary definition from using {} to using dict().

    Returns:
        str: An equivalent definition (including '='), but using the
        dict()-contructor instead of { and }

    """
    # Remove = before definition
    definition_string = re.sub(r"\s*=\s*", "", definition_string)

    # Remove { and }
    definition_string = re.sub(r"[{}]", "", definition_string)

    # Remove newlines
    definition_string = re.sub(r"\s*\n\s*", "", definition_string)

    # Find all pairs
    pairs = re.split(r"\s*,\s*", definition_string)

    # Convert each pair to a tuple definition
    result_inner = ""
    for pair in pairs:
        if pair.strip() == "":
            continue
        key, value = re.split(r"\s*:\s*", pair)

        if result_inner == "":
            result_inner = f"({key}, {value})"

        else:
            result_inner += f", ({key}, {value})"

    if result_inner == "":
        return "= dict()"
    return f"= dict([{result_inner}])"


def pre_reverse_parse(infile_string: str) -> str:
    """Perform some necessary changes to the file before reverse parsing can ensue.

    This includes changing dict definitions to use dict() constructor.

    Returns:
        str: The source with changes to dictionary definitions

    """
    dictionaries = re.findall(
        r"=\s*{\s*(?:.+\s*:\s*.+(?:\s*,\s*)?)*\s*}",
        infile_string,
    )

    for dictionary in dictionaries:
        infile_string = re.sub(
            dictionary,
            translate_dictionary(dictionary),
            infile_string,
        )

    return infile_string


def safe_substitute(value: str, deescaped_key: str, line: str) -> str:
    """Perform Python token substitution on a valthon line, ignoring tokens in strings.

    Returns:
        Code line with safe Python token substitutions

    """
    string_pattern = r"""
        (?P<string>(['"])(?:\\.|(?!\2).)*\2)  # Match single or double-quoted strings
    """

    def replace_callback(match) -> str:
        if match.group("string"):
            return match.group(0)
        return re.sub(
            rf'(?<!["\'#])\b{re.escape(value)}\b(?!["\'])',
            f"{deescaped_key}_is_not_valid_python",
            match.group(0),
        )

    return re.sub(string_pattern, replace_callback, line)


def reverse_parse(filename: str, outputname: str) -> None:
    """Change a Python file to a valthon file.

    All semantically significant whitespace resulting in a change
    in indentation levels will have a matching opening or closing
    curly-brace.
    """
    # Open a file as bytes
    inlines = []
    with Path(filename).open(encoding="utf-8") as infile:
        inlines = infile.readlines()

    # Read file to string
    infile_str_raw = ""
    for line in inlines:
        infile_str_raw += line

    # Fix indentation
    infile_str_indented = ""
    for line in infile_str_raw.split("\n"):
        # Search for comments, and remove for now. Re-add them before writing to
        # result string
        m = re.search(r"[ \t]*(#.*$)", line)

        # Make sure # sign is not inside quotations. Delete match object if it is
        if m is not None:
            m2 = re.search(r"[\"'].*#.*[\"']", m.group(0))
            if m2 is not None:
                m = None

        if m is not None:
            add_comment = m.group(0)
            line = re.sub(r"[ \t]*(#.*$)", "", line)
        else:
            add_comment = ""

        # skip empty lines:
        if line.strip() in {"\n", "\r\n", ""}:
            infile_str_indented += add_comment + "\n"
            continue

        # disallow valthon in original Python file
        # replace anything in mappings.keys() with its value but opposite
        for value, key in VAL2PY_MAPPINGS.items():
            if "\\s" in value:
                value = value.replace("\\s+", " ")
            line = safe_substitute(value, key, line)
            line = re.sub(
                rf'(?<!["\'#])\b{re.escape(key)}\b(?!["\'])',
                value,
                line,
            )

        infile_str_indented += line + add_comment + "\n"

    # Save the file
    with Path(outputname).open("w", encoding="utf-8") as outfile:
        outfile.write(infile_str_indented)


def main() -> None:
    """Translate python to valthon.

    Command line utility and Python module for translating python code
    to valthon code.
    """
    argparser = argparse.ArgumentParser(
        "py2vln",
        description="py2vln translates python to valthon",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    argparser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"v{VERSION_NUMBER}",
    )
    argparser.add_argument(
        "-o",
        "--output",
        type=str,
        help="specify name of output file",
        nargs=1,
    )
    argparser.add_argument("input", type=str, help="python file to translate", nargs=1)

    cmd_args = argparser.parse_args()

    logger = Logger()

    try:
        outputname = (
            cmd_args.output[0]
            if cmd_args.output is not None
            else change_file_name(cmd_args.input[0], None)
        )
        with Path(cmd_args.input[0]).open(encoding="utf-8") as infile:
            infile_string = "".join(infile.readlines())

        temp_path = Path(cmd_args.input[0] + ".py2vlntemp")
        with temp_path.open("w", encoding="utf-8") as tempoutfile:
            tempoutfile.write(infile_string)

        reverse_parse(cmd_args.input[0] + ".py2vlntemp", outputname)
        Path(cmd_args.input[0] + ".py2vlntemp").unlink()

    except FileNotFoundError:
        logger.log_error(f"No file named {cmd_args.input[0]}")

    except Exception as e:
        logger.log_error(f"Unexpected error: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    main()
