# Surreal Athlete & Sand Cheetah — Concept Art Specification

A high-octane cinematic concept art brief: a male athlete sprinting across desert dunes, pursued by a colossal sand-formed cheetah entity. Designed for sports brand advertising campaigns (Nike, Adidas, Puma).

## Files

| File | Description |
|------|-------------|
| `scene.json` | Full scene specification — subject, environment, lighting, camera, and brand customization fields |
| `prompt_generator.py` | Python script that converts the spec into ready-to-use prompts for Midjourney, Stable Diffusion, and DALL-E 3 |

## Quick Start

```bash
python prompt_generator.py
```

Outputs formatted prompts for all three supported brands (Nike / Adidas / Puma) across all three AI image platforms.

## Custom Brand

```python
from prompt_generator import load_scene, BrandConfig, format_for_midjourney

scene = load_scene()
brand = BrandConfig(
    brand="Puma",
    product="Nitro Running Collection",
    clothing_color="black",
    shoe_accent="neon yellow"
)
print(format_for_midjourney(scene, brand))
```

## Scene Summary

| Element | Detail |
|---------|--------|
| Subject | Lean male athlete, late 20s, mid-stride sprint |
| Creature | Kaiju-scale cheetah composed of swirling sand and dust |
| Environment | Vast Sahara desert dunes, partly cloudy blue sky |
| Camera | 24mm wide angle, low angle, f/8, tracking shot |
| Lighting | Harsh top-left sunlight, high contrast, warm daylight |
| Color Grade | Desaturated blues, earthy beiges and tans |
| Style | 8K VFX concept art, particle simulation, cinematic |
| Mood | Surrealism × Sports Advertising × Epic Cinema |
