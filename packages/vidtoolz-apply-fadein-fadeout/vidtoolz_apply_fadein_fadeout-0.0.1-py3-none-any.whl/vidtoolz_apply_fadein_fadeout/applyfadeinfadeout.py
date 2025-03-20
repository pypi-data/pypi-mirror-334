import argparse
from moviepy import VideoFileClip
from moviepy import vfx


def apply_fade_effect(video_path, fade_type, duration):
    """
    Apply fadein or fadeout effect to a video and write the result to an output file.

    Parameters:
        video_path     : Path to the input video file or clip
        fade_type (str): "fadein" or "fadeout" or "both".
        duration (float): Duration of the fade effect in seconds.
    """
    # Load video clip
    clip = VideoFileClip(video_path) if isinstance(video_path, str) else video_path
    fps = clip.fps
    # Apply fade effects
    if fade_type.lower() == "fadein":
        processed_clip = clip.with_effects([vfx.FadeIn(duration)])
    elif fade_type.lower() == "fadeout":
        processed_clip = clip.with_effects([vfx.FadeOut(duration)])
    elif fade_type.lower() == "both":
        processed_clip = clip.with_effects(
            [vfx.FadeIn(duration), vfx.FadeOut(duration)]
        )
    else:
        raise ValueError("Invalid fade type. Choose 'fadein', 'fadeout', or 'both'.")

    return processed_clip, fps


def write_clip(processed_clip, fps, output_path):
    """
    output_path (str): Path to save the output video.
    """
    # Write the result to the output file. Using the same codec as input.
    has_audio = processed_clip.audio is not None
    processed_clip.write_videofile(
        output_path, codec="libx264",  fps=fps,  audio_codec="aac" if has_audio else None,
    )
    # Close the clips to free up resources
    processed_clip.close()
