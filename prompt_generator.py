"""
Generates AI image prompts from the surreal athlete-cheetah scene specification.
Supports brand/clothing customization and multiple AI image platform formats.
"""

import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class BrandConfig:
    brand: str = "Nike"
    product: str = "Running Collection"
    clothing_color: str = "light grey"
    shoe_accent: str = "white"


def load_scene(path: str = "scene.json") -> dict:
    with open(path) as f:
        return json.load(f)


def build_prompt(scene: dict, brand: Optional[BrandConfig] = None) -> str:
    brand = brand or BrandConfig()

    clothing_desc = (
        f"{brand.clothing_color} {brand.brand} athletic t-shirt with the {brand.brand} swoosh logo "
        f"on the chest, matching {brand.clothing_color} {brand.brand} athletic shorts"
    )

    prompt = (
        # Core concept
        "Surreal cinematic concept art, epic sports advertising, "
        "a lean muscular male athlete in his late 20s sprinting across desert sand dunes, "
        f"wearing {clothing_desc}, "
        "tanned bronzed sweat-glistening skin, intense determined expression, "
        "mouth slightly open in exertion, mid-stride leaning forward dynamically, "
        "movement from left to right, "

        # Sand cheetah
        "pursued by a colossal kaiju-sized cheetah entity emerging from a massive sandstorm behind him, "
        "the cheetah is NOT solid — it is a volumetric simulation of millions of swirling sand grains and dust, "
        "hyper-realistic cheetah head and massive front paw, fur edges dissolving into the sandstorm, "
        "the runner's kicked-up sand trail connects him to the sand creature, "

        # Environment
        "vast sun-drenched Sahara desert sand dunes, "
        "flying sand particles and motion-blurred dust in the foreground, "
        "deep blue sky with white cumulus clouds in the background, "
        "rolling sand hills on the horizon, "

        # Composition
        "low angle wide tracking shot, 24mm cinema prime lens, f/8 deep depth of field, "
        "foreground runner mid-ground sand cheetah background sky depth layering, "
        "motion blur on the edges, "

        # Lighting
        "harsh top-left sunlight, bright warm daylight key light, "
        "deep sharp shadows defining sand ripples and athlete muscles, "
        "atmospheric sandstorm haze, sun flares peeking through clouds, "

        # Color grade
        "desaturated blues, rich earthy beige and tan tones, high contrast, "

        # Style/quality
        "digital art VFX concept, surrealism, 8K resolution, "
        "hyper-detailed particle simulation, grainy sand texture, "
        "subsurface scattering in dust clouds, cinematic composition"
    )

    return prompt


def build_negative_prompt() -> str:
    return (
        "solid cheetah, realistic cheetah, normal-sized cheetah, cartoon, anime, "
        "low quality, blurry, text, watermark, logo overlap, ugly, deformed, "
        "indoor, nighttime, rain, snow, urban, city"
    )


def format_for_midjourney(scene: dict, brand: Optional[BrandConfig] = None) -> str:
    prompt = build_prompt(scene, brand)
    return f"{prompt} --ar 16:9 --v 6.1 --style raw --q 2"


def format_for_stable_diffusion(scene: dict, brand: Optional[BrandConfig] = None) -> str:
    positive = build_prompt(scene, brand)
    negative = build_negative_prompt()
    return f"Positive:\n{positive}\n\nNegative:\n{negative}"


def format_for_dalle(scene: dict, brand: Optional[BrandConfig] = None) -> str:
    prompt = build_prompt(scene, brand)
    return (
        f"Create a photorealistic digital concept art image. {prompt} "
        "The style should look like a high-end sports brand campaign advertisement."
    )


if __name__ == "__main__":
    scene = load_scene()

    brands = [
        BrandConfig(brand="Nike", product="Air Zoom Running Collection", clothing_color="light grey", shoe_accent="volt green"),
        BrandConfig(brand="Adidas", product="Ultraboost Running Collection", clothing_color="white", shoe_accent="coral"),
        BrandConfig(brand="Puma", product="Nitro Running Collection", clothing_color="black", shoe_accent="neon yellow"),
    ]

    for brand in brands:
        print(f"\n{'='*70}")
        print(f"BRAND: {brand.brand} — {brand.product}")
        print('='*70)

        print("\n[Midjourney]")
        print(format_for_midjourney(scene, brand))

        print("\n[Stable Diffusion / SDXL]")
        print(format_for_stable_diffusion(scene, brand))

        print("\n[DALL-E 3]")
        print(format_for_dalle(scene, brand))
