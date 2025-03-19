import sys,os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, vfx

POSITION_MAP = {
    "top-left": ("left", "top"),
    "top-right": ("right", "top"),
    "bottom-left": ("left", "bottom"),
    "bottom-right": ("right", "bottom"),
    "center": ("center", "center"),
    "bottom": ("center", "bottom"),
}


def add_text_to_video(
    input_video_path, text, start_time, end_time, position, fontsize=50
):
    try:
        # Load the original video
        video = VideoFileClip(input_video_path)
    except Exception as e:
        sys.exit("Error loading video file: " + str(e))

    try:
        here = os.path.dirname(__file__)
        font=os.path.join(here, "fonts", "SEASRN.ttf")
        # Create a text clip using a common system font.
        txt_clip = TextClip(
            font=font,
            text=text,
            font_size=fontsize,
            # bg_color=color,
            # size=(wid + 5, text_hight + 10),
            # method="caption",
            stroke_width=2,
            stroke_color="black",
            color="white",
        )
        # text, fontsize=fontsize, color='white', font='Arial')
    except Exception as e:
        sys.exit("Error creating text clip: " + str(e))

    # Convert position string to a tuple
    pos_tuple = POSITION_MAP.get(position, ("center", "bottom"))
    try:
        # Set duration and starting time, and position the text
        txt_clip = (
            txt_clip.with_position(pos_tuple)
            .with_duration(end_time - start_time)
            .with_start(start_time)
        )
    except Exception as e:
        sys.exit("Error setting properties on text clip: " + str(e))

    txt_clip = txt_clip.with_effects([vfx.CrossFadeIn(0.5), vfx.CrossFadeOut(0.5)])

    try:
        # Overlay the text clip on the video
        video_with_text = CompositeVideoClip([video, txt_clip])
    except Exception as e:
        sys.exit("Error combining clips: " + str(e))

    return video_with_text, video.fps


def write_file(video_with_text, output_video_path, fps):
    try:
        # Write the result to a file
        video_with_text.write_videofile(
            output_video_path,
            codec="libx264",
            fps=fps,
            audio_codec="aac",
            temp_audiofile="temp_audio.m4a",
            remove_temp=True,
        )
    except Exception as e:
        sys.exit("Error writing video file: " + str(e))
    video_with_text.close()
