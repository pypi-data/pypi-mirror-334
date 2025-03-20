#! /usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path

from valthon import VERSION_NUMBER, parser
from valthon.logger import Logger


def main() -> None:
    # Setup argument parser
    argparser = argparse.ArgumentParser(
        "valthon",
        description=(
            "Valthon is a python preprosessor that translates valthon files to python."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    argparser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"v{VERSION_NUMBER}",
    )
    argparser.add_argument(
        "--verbose",
        help="print progress",
        action="store_true",
    )
    argparser.add_argument(
        "-c",
        "--compile",
        help="translate to python only (don't run files)",
        action="store_true",
    )
    argparser.add_argument(
        "-k",
        "--keep",
        help="keep generated python files",
        action="store_true",
    )
    argparser.add_argument(
        "--python2",
        help="use python2 instead of python3 (default)",
        action="store_true",
    )
    argparser.add_argument(
        "-o",
        "--output",
        type=str,
        help="specify name of output file (if -c is present)",
        nargs=1,
    )
    argparser.add_argument("input", type=str, help="valthon files to process", nargs=1)
    argparser.add_argument(
        "args",
        type=str,
        help="arguments to script",
        nargs=argparse.REMAINDER,
    )

    # Parse arguments
    cmd_args = argparser.parse_args()

    # Create logger
    logger = Logger(cmd_args.verbose)

    # Check for invalid combination of flags
    if cmd_args.output is not None and cmd_args.compile is False:
        logger.log_error("Cannot specify output when valthon is not in compile mode")
        sys.exit(1)

    # Where to output files
    if cmd_args.compile or cmd_args.keep:
        # No path prefix
        path_prefix = ""
        logger.log_info("Placing files in this directory")

    else:
        # Prefix with . to hide, also to avoid name conflicts.
        path_prefix = "python_"
        logger.log_info(
            "Placing files in this directory, but prefixing them with python_*",
        )

    # List of all files to translate from valthon to python
    parse_que = []

    # Add all files from cmd line
    parse_que.append(cmd_args.input[0])
    if cmd_args.compile:
        for arg in cmd_args.args:
            parse_que.append(arg)

    # Add all files from imports, and recursivelly (ish) add all imports from
    # the imports (and so on..)
    logger.log_info("Scanning for imports")
    i = 0
    while i < len(parse_que):
        try:
            import_files = parser.parse_imports(parse_que[i])

        except FileNotFoundError:
            logger.log_error(f"No file named '{parse_que[i]}'")
            sys.exit(1)

        for import_file in import_files:
            if Path(import_file).is_file() and import_file not in parse_que:
                logger.log_info(f"Adding '{import_file}' to parse que")
                parse_que.append(import_file)

        i += 1

    if not path_prefix:
        import_translations = {}
        for file in parse_que:
            import_translations[file[:-3]] = path_prefix + file[:-3]

    else:
        import_translations = None

    # Parsing
    current_file_name = None
    try:
        for file in parse_que:
            current_file_name = file
            logger.log_info(f"Parsing '{file}'")

            if cmd_args.output is None:
                outputname = None
            elif Path(cmd_args.output[0]).is_dir():
                new_file_name = parser._change_file_name(os.path.split(file)[1])
                outputname = os.path.join(cmd_args.output[0], new_file_name)
            else:
                outputname = cmd_args.output[0]

            parser.parse_file(
                file,
                path_prefix,
                outputname,
                import_translations,
            )
    except (TypeError, FileNotFoundError) as e:
        logger.log_error(f"Error while parsing '{current_file_name}'.\n{e!s}")
        # Cleanup
        try:
            for file in parse_que:
                Path(path_prefix + parser._change_file_name(file, None)).unlink()
        except Exception as e:
            logger.log_error(f"Failed to delete file: {e}")
            raise e
        sys.exit(1)

    # Stop if we were only asked to translate
    if cmd_args.compile:
        return

    # Run file
    if cmd_args.python2:
        python_commands = ["python2", "py -2", sys.executable]
    else:
        python_commands = ["python3", "python", "py", sys.executable]
        if os.name == "nt":
            python_commands.pop(0)

    filename = Path(cmd_args.input[0]).name
    py_file = path_prefix + parser._change_file_name(filename, None)
    args_str = " ".join(arg for arg in cmd_args.args)

    try:
        logger.log_info("Running")
        logger.program_header()

        # Try different Python commands until one works
        success = False
        for cmd in python_commands:
            try:
                if os.name == "nt":
                    result = subprocess.run(
                        f"{cmd} {py_file} {args_str}",
                        shell=True,
                        check=False,
                    )
                else:
                    result = subprocess.run([cmd, py_file, *cmd_args.args], check=False)

                if result.returncode == 0:
                    success = True
                    break
            except:
                continue

        if not success:
            logger.log_error("Could not find a working Python interpreter")

        logger.program_footer()

    except Exception as e:
        logger.log_error("Unexpected error while running Python")
        logger.log_info(f"Reported error message: {e!s}")

    # Delete file if requested
    try:
        if not cmd_args.keep:
            logger.log_info("Deleting files")
            for file in parse_que:
                filename = Path(file).name
                Path(path_prefix + parser._change_file_name(filename, None)).unlink()
    except:
        logger.log_error(
            "Could not delete created python files.\nSome garbage may remain in ~/.valthontemp/",
        )


if __name__ == "__main__":
    main()
