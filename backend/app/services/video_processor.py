"""
Video processing service using FFmpeg
Handles all video manipulation operations
"""

import subprocess
import logging
import json
import re
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Video processing using FFmpeg"""
    
    def __init__(self):
        self.ffmpeg_cmd = "ffmpeg"
        self.ffprobe_cmd = "ffprobe"
        self.verify_ffmpeg()
    
    def verify_ffmpeg(self):
        """Verify FFmpeg is installed"""
        try:
            subprocess.run(
                [self.ffmpeg_cmd, "-version"],
                capture_output=True,
                timeout=5
            )
            logger.info("✓ FFmpeg is available")
        except FileNotFoundError:
            logger.warning("⚠ FFmpeg not found in PATH. Install with: pip install ffmpeg-python or brew install ffmpeg")
    
    def get_metadata(self, video_path: str) -> Dict[str, Any]:
        """
        Extract video metadata using FFprobe
        
        Args:
            video_path: Path to video file
        
        Returns:
            Dictionary with video metadata
        """
        try:
            cmd = [
                self.ffprobe_cmd,
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "format=duration,size:stream=width,height,r_frame_rate,codec_name",
                "-of", "json",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                # Extract information
                format_info = data.get("format", {})
                stream_info = data.get("streams", [{}])[0]
                
                duration = float(format_info.get("duration", 0))
                size = int(format_info.get("size", 0))
                width = stream_info.get("width", 0)
                height = stream_info.get("height", 0)
                fps = stream_info.get("r_frame_rate", "30/1")
                codec = stream_info.get("codec_name", "unknown")
                
                # Parse FPS
                if "/" in str(fps):
                    parts = str(fps).split("/")
                    fps_value = float(parts[0]) / float(parts[1]) if parts[1] != "0" else 30
                else:
                    fps_value = float(fps)
                
                return {
                    "duration_seconds": round(duration, 2),
                    "file_size_mb": round(size / (1024 * 1024), 2),
                    "width": width,
                    "height": height,
                    "fps": round(fps_value, 2),
                    "codec": codec,
                    "resolution": f"{width}x{height}"
                }
            else:
                logger.error(f"FFprobe error: {result.stderr}")
                return {"error": result.stderr}
        
        except Exception as e:
            logger.error(f"Error getting metadata: {str(e)}")
            return {"error": str(e)}
    
    def extract_frames(self, video_path: str, output_dir: str, fps: int = 1) -> int:
        """
        Extract frames from video
        
        Args:
            video_path: Path to input video
            output_dir: Directory to save frames
            fps: Frames per second to extract
        
        Returns:
            Number of frames extracted
        """
        try:
            output_pattern = f"{output_dir}/frame_%04d.jpg"
            
            cmd = [
                self.ffmpeg_cmd,
                "-i", video_path,
                "-vf", f"fps={fps}",
                output_pattern
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                frames = list(Path(output_dir).glob("frame_*.jpg"))
                logger.info(f"✓ Extracted {len(frames)} frames")
                return len(frames)
            else:
                logger.error(f"Frame extraction error: {result.stderr}")
                return 0
        
        except Exception as e:
            logger.error(f"Error extracting frames: {str(e)}")
            return 0
    
    def add_text_overlay(
        self,
        video_path: str,
        output_path: str,
        text: str,
        x: int = 50,
        y: int = 50,
        fontsize: int = 24,
        fontcolor: str = "white"
    ) -> bool:
        """
        Add text overlay to video
        
        Args:
            video_path: Input video path
            output_path: Output video path
            text: Text to add
            x: X position
            y: Y position
            fontsize: Font size
            fontcolor: Font color
        
        Returns:
            True if successful
        """
        try:
            # Escape special characters in text
            text = text.replace("'", "\\'").replace(":", "\\:")
            
            cmd = [
                self.ffmpeg_cmd,
                "-i", video_path,
                "-vf", f"drawtext=text='{text}':x={x}:y={y}:fontsize={fontsize}:fontcolor={fontcolor}",
                "-c:v", "libx264",
                "-preset", "fast",
                "-c:a", "aac",
                output_path,
                "-y"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info(f"✓ Text overlay added: {output_path}")
                return True
            else:
                logger.error(f"Text overlay error: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error adding text overlay: {str(e)}")
            return False
    
    def resize_video(
        self,
        video_path: str,
        output_path: str,
        width: int = 1280,
        height: int = 720
    ) -> bool:
        """
        Resize video
        
        Args:
            video_path: Input video path
            output_path: Output video path
            width: Target width
            height: Target height
        
        Returns:
            True if successful
        """
        try:
            cmd = [
                self.ffmpeg_cmd,
                "-i", video_path,
                "-vf", f"scale={width}:{height}",
                "-c:v", "libx264",
                "-preset", "fast",
                "-c:a", "aac",
                output_path,
                "-y"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info(f"✓ Video resized: {output_path}")
                return True
            else:
                logger.error(f"Resize error: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error resizing video: {str(e)}")
            return False
    
    def merge_videos(self, video_list: List[str], output_path: str) -> bool:
        """
        Merge multiple videos
        
        Args:
            video_list: List of video paths
            output_path: Output video path
        
        Returns:
            True if successful
        """
        try:
            # Create concat file
            concat_file = "/tmp/concat.txt"
            with open(concat_file, "w") as f:
                for video in video_list:
                    f.write(f"file '{video}'\n")
            
            cmd = [
                self.ffmpeg_cmd,
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c", "copy",
                output_path,
                "-y"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info(f"✓ Videos merged: {output_path}")
                return True
            else:
                logger.error(f"Merge error: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error merging videos: {str(e)}")
            return False
