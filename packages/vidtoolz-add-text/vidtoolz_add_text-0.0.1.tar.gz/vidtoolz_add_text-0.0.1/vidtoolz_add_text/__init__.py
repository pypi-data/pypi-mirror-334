import vidtoolz
from vidtoolz_add_text.add_text import add_text_to_video, write_file


def create_parser(subparser):
    parser = subparser.add_parser("addtext", description="Add text to a video file")
    parser.add_argument("main_video", help="Path to the main video file.")
    parser.add_argument("text", help="Text to write")
    parser.add_argument(
        "-o",
        "--output",
        default="output.mp4",
        help="Output video file name (default: output.mp4)",
    )
    parser.add_argument(
        "-p",
        "--position",
        choices=[
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "center",
            "bottom",
        ],
        default="bottom",
        help="Position of the text (default: bottom)",
    )
    parser.add_argument(
        "-st",
        "--start-time",
        type=float,
        default=2,
        help="Start time when text should appear",
    )
    parser.add_argument(
        "-et",
        "--end-time",
        type=float,
        default=2,
        help="End time when text should disappear",
    )
    parser.add_argument(
        "-f", "--fontsize", type=int, default=50, help="Fontsize default:50"
    )

    return parser


class ViztoolzPlugin:
    """Add text to a video file"""

    __name__ = "addtext"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        clip , fps = add_text_to_video(
            args.main_video,
            args.text,
            args.start_time,
            args.end_time,
            args.position,
            args.fontsize,
        )
        write_file(clip, args.output, fps)

    def hello(self, args):
        # this routine will be called when "vidtoolz "addtext is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


addtext_plugin = ViztoolzPlugin()
