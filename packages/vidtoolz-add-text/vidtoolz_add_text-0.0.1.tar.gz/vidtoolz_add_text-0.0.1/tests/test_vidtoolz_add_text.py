import pytest
import vidtoolz_add_text as w

from argparse import ArgumentParser
from vidtoolz_add_text.add_text import add_text_to_video, write_file
import os


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(
        ["video.mp4", "hello", "-st", "3", "-et", "7", "-f", "100"]
    )
    assert result.main_video == "video.mp4"
    assert result.text == "hello"
    assert result.start_time == 3
    assert result.end_time == 7
    assert result.fontsize == 100
    assert result.position == "bottom"
    assert result.output == "output.mp4"


def test_plugin(capsys):
    w.addtext_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


HERE = os.path.dirname(__file__)
# Define a test video file path
TEST_VIDEO_FILE = os.path.join(HERE, "test_video.mp4")

# Define a temporary output video file path
TEMP_OUTPUT_VIDEO_FILE = os.path.join(HERE, "temp_output.mp4")


def test_add_text_to_video():
    # Test adding text to a video
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    assert video_with_text is not None
    assert fps > 0


def test_add_text_to_video_invalid_position():
    # Test adding text to a video with an invalid position
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "invalid-position"
    )
    assert video_with_text is not None
    assert fps > 0


def test_write_file():
    # Test writing the video to a file
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 2, 5, "center"
    )
    write_file(video_with_text, TEMP_OUTPUT_VIDEO_FILE, fps)
    assert os.path.exists(TEMP_OUTPUT_VIDEO_FILE)


def test_write_file_invalid_output_path():
    # Test writing the video to an invalid output path
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    with pytest.raises(SystemExit):
        write_file(video_with_text, "/invalid/output/path", fps)


def test_add_text_to_video_invalid_video_file():
    # Test adding text to an invalid video file
    with pytest.raises(SystemExit):
        add_text_to_video("invalid_video_file.mp4", "Test text", 0, 5, "center")


def test_add_text_to_video_invalid_text():
    # Test adding invalid text to a video
    with pytest.raises(SystemExit):
        add_text_to_video(TEST_VIDEO_FILE, None, 0, 5, "center")


def test_add_text_to_video_invalid_fontsize():
    # Test adding text to a video with an invalid font size
    with pytest.raises(SystemExit):
        add_text_to_video(
            TEST_VIDEO_FILE, "Test text", 0, 5, "center", fontsize="invalid"
        )


def test_add_text_to_video_invalid_start_time():
    # Test adding text to a video with an invalid start time
    with pytest.raises(SystemExit):
        add_text_to_video(TEST_VIDEO_FILE, "Test text", "invalid", 5, "center")


def test_add_text_to_video_invalid_end_time():
    # Test adding text to a video with an invalid end time
    with pytest.raises(SystemExit):
        add_text_to_video(TEST_VIDEO_FILE, "Test text", 0, "invalid", "center")


def test_write_file_invalid_video_with_text():
    # Test writing an invalid video to a file
    with pytest.raises(SystemExit):
        write_file(None, TEMP_OUTPUT_VIDEO_FILE, 30)


def test_write_file_invalid_output_video_path():
    # Test writing a video to an invalid output path
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    with pytest.raises(SystemExit):
        write_file(video_with_text, "/invalid/output/path", fps)


def test_write_file_invalid_fps():
    # Test writing a video with an invalid FPS to a file
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    with pytest.raises(SystemExit):
        write_file(video_with_text, TEMP_OUTPUT_VIDEO_FILE, "invalid")


def teardown_module():
    # Remove the temporary output video file
    if os.path.exists(TEMP_OUTPUT_VIDEO_FILE):
        os.remove(TEMP_OUTPUT_VIDEO_FILE)
