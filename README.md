# HSL Range → Mask  —  ComfyUI Custom Node

Pick a range of colours by **Hue / Saturation / Lightness** and get back a clean **mask** where every matching pixel is white and everything else is black.

---

## Installation

1. Copy the **`hsl_mask_node`** folder into:
   ```
   ComfyUI/custom_nodes/hsl_mask_node/
   ```
   The folder must contain both files:
   ```
   custom_nodes/
   └── hsl_mask_node/
       ├── __init__.py
       └── hsl_mask_node.py
   ```

2. Restart ComfyUI.

3. The node appears in the node browser under:
   **`image → masking → HSL Range → Mask`**

---

## Inputs

| Input | Type | Range | Description |
|---|---|---|---|
| `image` | IMAGE | — | Any image from the pipeline |
| `start_hue` | FLOAT | 0 – 360 | Start of the hue range (degrees) |
| `end_hue` | FLOAT | 0 – 360 | End of the hue range (degrees) |
| `start_saturation` | FLOAT | 0 – 100 | Minimum saturation (%) |
| `end_saturation` | FLOAT | 0 – 100 | Maximum saturation (%) |
| `start_lightness` | FLOAT | 0 – 100 | Minimum lightness (%) |
| `end_lightness` | FLOAT | 0 – 100 | Maximum lightness (%) |

## Output

| Output | Type | Description |
|---|---|---|
| `mask` | MASK | White where colour matches, black elsewhere |

---

## Tips

- **Isolate reds that cross the 0°/360° boundary**: set `start_hue = 340`, `end_hue = 20`. The node handles the wrap-around automatically.
- Pipe the mask into a **MaskToImage**, **InvertMask**, or use it with **VAE Encode (inpaint)** for targeted inpainting.
- Combine multiple HSL masks with a **MaskComposite** node to select several colour families at once.

---

## Requirements

- ComfyUI (any recent version)
- Python standard library only (`colorsys`, `numpy`) — no extra `pip install` needed.
