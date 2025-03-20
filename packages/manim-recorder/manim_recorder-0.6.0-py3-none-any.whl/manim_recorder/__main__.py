import argparse
import pathlib
import sys
from manim import logger


def launch_recorder():
    """Launch the GUI recorder."""
    from manim_recorder.service.gui_recorder import Recorder
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    recorder = Recorder()
    recorder.show()
    sys.exit(app.exec())


def generate_subtitles(json_file_path, transcript):
    """Generate subtitles from the provided JSON file."""
    from manim_recorder.generate_subcaption import Generate_Subcaption

    if json_file_path.suffix != ".json":
        logger.warning("The provided file is not a JSON file: %s", json_file_path)
        return

    subtitle_generator = Generate_Subcaption(json_file_path.absolute(), cache=True)
    subtitle_generator.subtitle_write(transcript=transcript)


def main():
    """Main function to parse arguments and execute commands."""
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Manim Recorder and Caption Generator")

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for the recorder command
    subparsers.add_parser(
        "rec", aliases=["recorder", "recording"], help="Launch the GUI recorder"
    )

    # Subparser for the caption command
    caption_parser = subparsers.add_parser(
        "caption",
        aliases=["subtitle", "srt"],
        help="Generate subtitles from a JSON file",
    )
    caption_parser.add_argument(
        "json_file", type=str, help="Path to the JSON file containing subtitles"
    )
    caption_parser.add_argument(
        "--transcript", action="store_true", help="Include transcript in subtitles"
    )
    caption_parser.add_argument(
        "--trx", action="store_true", help="Alias for --transcript"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if args.command in ["rec", "recorder", "recording"]:
        launch_recorder()
    elif args.command in ["caption", "subtitle", "srt"]:
        json_file_path = pathlib.Path(args.json_file)
        if json_file_path.exists():
            generate_subtitles(json_file_path, args.transcript or args.trx)
        else:
            logger.warning("The file does not exist: %s", json_file_path)


if __name__ == "__main__":
    main()
