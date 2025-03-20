import pytest
import moviepy as mpy
from vidtoolz_apply_fadein_fadeout.applyfadeinfadeout import apply_fade_effect
import vidtoolz_apply_fadein_fadeout as w

from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["test.mp4", "fadein"])
    assert result.video == "test.mp4"
    assert result.fade_type == "fadein"
    assert result.duration == 1
    assert result.output == "output_video.mp4"


def test_plugin(capsys):
    w.fadeinout_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


@pytest.fixture
def sample_clip():
    """Create a short test video clip."""
    return mpy.ColorClip(size=(640, 480), color=(255, 0, 0), duration=5).with_fps(
        30
    )  # Red video


@pytest.mark.parametrize("fade_type", ["fadein", "fadeout", "both"])
def test_apply_fade_effect_with_clip(sample_clip, fade_type):
    """Test fade effects using a VideoFileClip."""
    duration = 1  # 1-second fade duration
    processed_clip, fps = apply_fade_effect(sample_clip, fade_type, duration)

    assert isinstance(processed_clip, mpy.VideoClip), "Output should be a VideoClip"
    assert (
        processed_clip.duration == sample_clip.duration
    ), "Clip duration should remain unchanged"
    assert fps == sample_clip.fps, "FPS should be preserved"

    sample_clip.close()
    processed_clip.close()


@pytest.mark.parametrize("fade_type", ["fadein", "fadeout", "both"])
def test_apply_fade_effect_with_path(tmp_path, fade_type):
    """Test fade effects using a file path."""
    test_video_path = str(tmp_path / "test.mp4")
    sample_clip = mpy.ColorClip(
        size=(640, 480), color=(255, 0, 0), duration=5
    ).with_fps(30)
    sample_clip.write_videofile(test_video_path, codec="libx264", fps=30, audio=False)

    duration = 1  # 1-second fade duration
    processed_clip, fps = apply_fade_effect(test_video_path, fade_type, duration)

    assert isinstance(processed_clip, mpy.VideoClip), "Output should be a VideoClip"
    assert (
        processed_clip.duration == sample_clip.duration
    ), "Clip duration should remain unchanged"
    assert fps == sample_clip.fps, "FPS should be preserved"

    sample_clip.close()
    processed_clip.close()


def test_invalid_fade_type(sample_clip):
    """Test with an invalid fade type."""
    with pytest.raises(ValueError, match="Invalid fade type"):
        apply_fade_effect(sample_clip, "invalid_type", 1)
