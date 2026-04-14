import torch
import colorsys
import numpy as np


class HSLRangeToMask:
    """
    ComfyUI custom node: HSL Color Range → Mask
    Converts pixels within a given HSL range into a white mask, rest is black.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                # Hue: 0–360
                "start_hue":        ("FLOAT", {"default": 0.0,   "min": 0.0,   "max": 360.0, "step": 0.1}),
                "end_hue":          ("FLOAT", {"default": 360.0, "min": 0.0,   "max": 360.0, "step": 0.1}),
                # Saturation: 0–100 %
                "start_saturation": ("FLOAT", {"default": 0.0,   "min": 0.0,   "max": 100.0, "step": 0.1}),
                "end_saturation":   ("FLOAT", {"default": 100.0, "min": 0.0,   "max": 100.0, "step": 0.1}),
                # Lightness: 0–100 %
                "start_lightness":  ("FLOAT", {"default": 0.0,   "min": 0.0,   "max": 100.0, "step": 0.1}),
                "end_lightness":    ("FLOAT", {"default": 100.0, "min": 0.0,   "max": 100.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "generate_mask"
    CATEGORY = "image/masking"

    def generate_mask(
        self,
        image,
        start_hue, end_hue,
        start_saturation, end_saturation,
        start_lightness, end_lightness,
    ):
        # image shape: (batch, H, W, 3)  float32  0‒1
        batch_masks = []

        for img in image:
            np_img = img.cpu().numpy()          # (H, W, 3)  float32  0‒1

            # --- RGB → HLS via colorsys (vectorised with numpy) ---
            # colorsys.rgb_to_hls works per-pixel; vectorise with np.vectorize
            r, g, b = np_img[..., 0], np_img[..., 1], np_img[..., 2]

            vfunc = np.vectorize(colorsys.rgb_to_hls)
            h_raw, l_raw, s_raw = vfunc(r, g, b)
            # h_raw: 0‒1  (multiply × 360 for degrees)
            # l_raw: 0‒1  (multiply × 100 for percent)
            # s_raw: 0‒1  (multiply × 100 for percent)

            h = h_raw * 360.0
            s = s_raw * 100.0
            l = l_raw * 100.0

            # --- Build boolean masks for each channel ---
            # Hue wraps around 360°, handle crossing the 0/360 boundary
            if start_hue <= end_hue:
                hue_mask = (h >= start_hue) & (h <= end_hue)
            else:
                # e.g. start=340, end=20 → reds that wrap around
                hue_mask = (h >= start_hue) | (h <= end_hue)

            sat_mask = (s >= start_saturation) & (s <= end_saturation)
            lit_mask = (l >= start_lightness)  & (l <= end_lightness)

            combined = (hue_mask & sat_mask & lit_mask).astype(np.float32)

            batch_masks.append(torch.from_numpy(combined))

        # Stack → (batch, H, W)
        mask_tensor = torch.stack(batch_masks, dim=0)
        return (mask_tensor,)


# ── Node registration ────────────────────────────────────────────────────────
NODE_CLASS_MAPPINGS = {
    "HSLRangeToMask": HSLRangeToMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HSLRangeToMask": "HSL Range → Mask",
}
