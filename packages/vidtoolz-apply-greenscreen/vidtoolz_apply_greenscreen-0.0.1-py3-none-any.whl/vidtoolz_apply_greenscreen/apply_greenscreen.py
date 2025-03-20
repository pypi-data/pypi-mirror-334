import moviepy as mpy
import argparse
import numpy as np


POSITION_MAP = {
    "top-left": ("left", "top"),
    "top-right": ("right", "top"),
    "bottom-left": ("left", "bottom"),
    "bottom-right": ("right", "bottom"),
    "center": ("center", "center"),
    "bottom": ("center", "bottom"),
}


def overlay_greenscreen(main_video, greenscreen_video, position, start_time=1):

    # Load main video only if it's a file path
    final_clip = (
        mpy.VideoFileClip(main_video) if isinstance(main_video, str) else main_video
    )

    # Load green screen video
    youtube_animation = mpy.VideoFileClip(greenscreen_video)

    # Manual frame-by-frame mask creation
    def modify_frame(get_frame, t):
        # Get the original frame
        frame = get_frame(t)

        # Create mask where green pixels become transparent
        green_channel = frame[:, :, 1]
        red_channel = frame[:, :, 0]
        blue_channel = frame[:, :, 2]

        # Where green is high and red/blue are lower (create alpha channel)
        alpha = np.where(
            (green_channel > 180) & (red_channel < 120) & (blue_channel < 120), 0, 255
        ).astype("uint8")

        # Create RGBA frame
        h, w = frame.shape[:2]
        rgba = np.zeros((h, w, 4), dtype="uint8")
        rgba[:, :, :3] = frame
        rgba[:, :, 3] = alpha

        return rgba

    # Create a new clip with the modified frames
    new_clip = mpy.VideoClip(
        lambda t: modify_frame(youtube_animation.get_frame, t),
        duration=youtube_animation.duration,
    )
    new_clip.audio = youtube_animation.audio

    # Convert position string to a tuple
    pos_tuple = POSITION_MAP.get(position, ("center", "bottom"))

    # Position the clip
    positioned_clip = new_clip.with_position(pos_tuple).with_start(start_time)

    # Overlay the clip onto the main video
    final_composite = mpy.CompositeVideoClip([final_clip, positioned_clip])

    return final_composite, final_clip.fps


def overlay_greenscreen2(main_video, greenscreen_video, position, start_time=1):
    # Load main video only if it's a file path
    final_clip = (
        mpy.VideoFileClip(main_video) if isinstance(main_video, str) else main_video
    )

    # Load green screen video
    youtube_animation = mpy.VideoFileClip(greenscreen_video).subclipped(4)
    mask_effect = mpy.vfx.MaskColor(color=[100, 225, 35], threshold=255, stiffness=5)
    mask = mask_effect.apply(youtube_animation).to_mask()
    masked_clip = youtube_animation.with_mask(mask)

    # Convert position string to a tuple
    pos_tuple = POSITION_MAP.get(position, ("center", "bottom"))

    # Position the masked clip
    masked_clip = masked_clip.with_position(pos_tuple).with_start(start_time)

    # Overlay the masked clip onto the main video
    final_composite = mpy.CompositeVideoClip([final_clip, masked_clip])

    return final_composite, final_clip.fps


def write_clip(final_composite, output_video, fps):
    # Write the output file
    final_composite.write_videofile(
        output_video, codec="libx264", fps=fps, audio_codec="aac"
    )
