import vidtoolz
from vidtoolz_apply_fadein_fadeout.applyfadeinfadeout import (
    apply_fade_effect,
    write_clip,
)


def create_parser(subparser):
    parser = subparser.add_parser(
        "fadeinout", description="Apply fadein-fadeout effects on videos "
    )
    # Add subprser arguments here.
    parser.add_argument("video", help="Path to the input video file.")
    parser.add_argument(
        "fade_type",
        choices=["fadein", "fadeout", "both"],
        help="Type of fade effect to apply.",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        default=1,
        help="Duration of the fade effect in seconds. (Default 1)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output_video.mp4",
        help="Path for the output video file. Defaults to 'output_video.mp4'.",
    )

    return parser


class ViztoolzPlugin:
    """Apply fadein-fadeout effects on videos"""

    __name__ = "fadeinout"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        clip, fps = apply_fade_effect(args.video, args.fade_type, args.duration)
        write_clip(clip, fps, args.output)
        print(f"{args.output} written.")

    def hello(self, args):
        # this routine will be called when "vidtoolz "fadeinout is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


fadeinout_plugin = ViztoolzPlugin()
