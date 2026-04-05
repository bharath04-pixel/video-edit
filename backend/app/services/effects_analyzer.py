"""
Effects Analysis Service
Analyzes videos to detect and report effects used
"""

import cv2
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class EffectsAnalyzer:
    """Analyze video for effects applied"""
    
    def __init__(self):
        self.effects_detected = []
    
    def analyze_video(self, video_path: str) -> dict:
        """
        Analyze video file for effects
        
        Args:
            video_path: Path to video file
            
        Returns:
            {
                "effects": ["effect1", "effect2", ...],
                "color_grade": {...},
                "filters": [...],
                "transitions": [...],
                "adjustments": {...},
                "confidence": 0.85
            }
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            effects = {
                "effects": [],
                "color_grading": {},
                "brightness_adjustments": [],
                "contrast_adjustments": [],
                "saturation_adjustments": [],
                "blur_effects": [],
                "transitions": [],
                "filters": [],
                "speed_changes": [],
                "audio_effects": [],
                "confidence": 0.0
            }
            
            # Sample frames
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            if frame_count == 0:
                return effects
            
            frames_to_sample = min(30, frame_count)
            sample_indices = np.linspace(0, frame_count - 1, frames_to_sample, dtype=int)
            
            sampled_frames = []
            for idx in sample_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    sampled_frames.append(frame)
            
            cap.release()
            
            if not sampled_frames:
                return effects
            
            # Analyze frames
            # 1. Detect brightness changes
            brightness_data = self._analyze_brightness(sampled_frames)
            if brightness_data["detected"]:
                effects["brightness_adjustments"].append(brightness_data)
                effects["effects"].append("Brightness Adjustment")
            
            # 2. Detect contrast changes
            contrast_data = self._analyze_contrast(sampled_frames)
            if contrast_data["detected"]:
                effects["contrast_adjustments"].append(contrast_data)
                effects["effects"].append("Contrast Adjustment")
            
            # 3. Detect saturation changes
            saturation_data = self._analyze_saturation(sampled_frames)
            if saturation_data["detected"]:
                effects["saturation_adjustments"].append(saturation_data)
                effects["effects"].append("Saturation Adjustment")
            
            # 4. Detect blur effects
            blur_data = self._analyze_blur(sampled_frames)
            if blur_data["detected"]:
                effects["blur_effects"].append(blur_data)
                effects["effects"].append("Blur Effect")
            
            # 5. Detect color grading
            color_data = self._analyze_color_grading(sampled_frames)
            if color_data["detected"]:
                effects["color_grading"] = color_data
                effects["effects"].append("Color Grading")
            
            # 6. Detect transitions (frame changes)
            transition_data = self._analyze_transitions(sampled_frames)
            if transition_data["detected"]:
                effects["transitions"].append(transition_data)
                effects["effects"].append("Transitions")
            
            # Calculate confidence
            effects["confidence"] = min(0.95, len(effects["effects"]) * 0.15 + 0.5)
            
            logger.info(f"✓ Effects analyzed: {effects['effects']}")
            return effects
            
        except Exception as e:
            logger.error(f"Error analyzing effects: {str(e)}")
            return {
                "effects": [],
                "error": str(e),
                "confidence": 0.0
            }
    
    def _analyze_brightness(self, frames: list) -> dict:
        """Detect brightness adjustments"""
        try:
            brightness_values = []
            for frame in frames:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = np.mean(gray)
                brightness_values.append(brightness)
            
            # Check for significant variations
            brightness_array = np.array(brightness_values)
            std_dev = np.std(brightness_array)
            mean_brightness = np.mean(brightness_array)
            
            detected = std_dev > 15  # Threshold for brightness variation
            
            return {
                "detected": detected,
                "mean_brightness": float(mean_brightness),
                "variation": float(std_dev),
                "range": [float(min(brightness_values)), float(max(brightness_values))]
            }
        except:
            return {"detected": False}
    
    def _analyze_contrast(self, frames: list) -> dict:
        """Detect contrast adjustments"""
        try:
            contrast_values = []
            for frame in frames:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                contrast = np.std(gray)
                contrast_values.append(contrast)
            
            contrast_array = np.array(contrast_values)
            mean_contrast = np.mean(contrast_array)
            
            detected = mean_contrast > 30  # Higher contrast threshold
            
            return {
                "detected": detected,
                "mean_contrast": float(mean_contrast),
                "range": [float(min(contrast_values)), float(max(contrast_values))]
            }
        except:
            return {"detected": False}
    
    def _analyze_saturation(self, frames: list) -> dict:
        """Detect saturation adjustments"""
        try:
            saturation_values = []
            for frame in frames:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                s_channel = hsv[:, :, 1]  # Saturation
                avg_saturation = np.mean(s_channel)
                saturation_values.append(avg_saturation)
            
            saturation_array = np.array(saturation_values)
            mean_saturation = np.mean(saturation_array)
            
            detected = mean_saturation > 100  # Saturation threshold
            
            return {
                "detected": detected,
                "mean_saturation": float(mean_saturation),
                "range": [float(min(saturation_values)), float(max(saturation_values))]
            }
        except:
            return {"detected": False}
    
    def _analyze_blur(self, frames: list) -> dict:
        """Detect blur effects"""
        try:
            blur_scores = []
            for frame in frames:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Laplacian variance detects blur
                laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                blur_scores.append(laplacian_var)
            
            blur_array = np.array(blur_scores)
            avg_blur = np.mean(blur_array)
            
            # Low variance = more blur
            detected = avg_blur < 100
            
            return {
                "detected": detected,
                "blur_score": float(avg_blur),
                "intensity": "High" if avg_blur < 50 else "Medium" if avg_blur < 100 else "Low"
            }
        except:
            return {"detected": False}
    
    def _analyze_color_grading(self, frames: list) -> dict:
        """Detect color grading"""
        try:
            color_profiles = []
            for frame in frames:
                # Analyze color distribution
                b, g, r = cv2.split(frame)
                color_profiles.append({
                    "r": float(np.mean(r)),
                    "g": float(np.mean(g)),
                    "b": float(np.mean(b))
                })
            
            avg_r = np.mean([p["r"] for p in color_profiles])
            avg_g = np.mean([p["g"] for p in color_profiles])
            avg_b = np.mean([p["b"] for p in color_profiles])
            
            # Detect color cast
            total = avg_r + avg_g + avg_b
            r_ratio = avg_r / total if total > 0 else 0.33
            g_ratio = avg_g / total if total > 0 else 0.33
            b_ratio = avg_b / total if total > 0 else 0.33
            
            # If ratios deviate from neutral (0.33, 0.33, 0.33), color grading detected
            deviation = abs(r_ratio - 0.33) + abs(g_ratio - 0.33) + abs(b_ratio - 0.33)
            detected = deviation > 0.1
            
            # Determine color tone
            if avg_r > avg_b and avg_r > avg_g:
                tone = "Warm (Reddish)"
            elif avg_b > avg_r and avg_b > avg_g:
                tone = "Cool (Bluish)"
            elif avg_g > avg_r and avg_g > avg_b:
                tone = "Green tinted"
            else:
                tone = "Neutral"
            
            return {
                "detected": detected,
                "tone": tone,
                "rgb_balance": {"r": avg_r, "g": avg_g, "b": avg_b},
                "deviation": float(deviation)
            }
        except:
            return {"detected": False}
    
    def _analyze_transitions(self, frames: list) -> dict:
        """Detect scene transitions (cuts, fades, etc)"""
        try:
            if len(frames) < 2:
                return {"detected": False}
            
            transitions = []
            for i in range(1, len(frames)):
                # Compute difference between consecutive frames
                diff = cv2.absdiff(frames[i-1], frames[i])
                mean_diff = np.mean(diff)
                
                # High difference = scene cut or transition
                if mean_diff > 50:
                    transitions.append({
                        "type": "Cut/Fade",
                        "intensity": float(mean_diff)
                    })
            
            detected = len(transitions) > 0
            
            return {
                "detected": detected,
                "count": len(transitions),
                "transitions": transitions[:5]  # Return first 5
            }
        except:
            return {"detected": False}
