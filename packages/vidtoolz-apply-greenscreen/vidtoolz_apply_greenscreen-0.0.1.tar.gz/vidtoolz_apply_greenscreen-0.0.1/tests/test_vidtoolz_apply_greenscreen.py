import pytest
from unittest.mock import Mock, patch
from moviepy import ColorClip, CompositeVideoClip
import os

from vidtoolz_apply_greenscreen.apply_greenscreen import overlay_greenscreen, write_clip
import vidtoolz_apply_greenscreen as w

from argparse import ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["test.mp4", "hello.mp4"])
    assert result.main_video == "test.mp4"
    assert result.greenscreen_video == "hello.mp4"
    assert result.position == "bottom"
    assert result.output == "output.mp4"
    assert result.start_time == 1


def test_plugin(capsys):
    w.greenscreen_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


@pytest.fixture
def sample_clips(tmp_path):
    """Creates temporary sample video clips for testing."""
    here = os.path.dirname(__file__)
    main_video = os.path.join(here, "test_video.mp4")
    greenscreen_video = os.path.join(here, "subscribe.mp4")
    return main_video, greenscreen_video


def test_overlay_with_file(sample_clips):
    """Main test."""
    main_video, greenscreen_video = sample_clips

    composite, fps = overlay_greenscreen(main_video, greenscreen_video, "bottom")

    assert isinstance(composite, CompositeVideoClip)
    assert fps == 59.98
    assert len(composite.clips) == 2
