"""
sample_run.py
Standalone CLI runner to test the AI Styling & Virtual Try-On Engine.
Can be executed via:
    python sample_run.py
"""

import os
import sys
from PIL import Image, ImageDraw
from stylist_engine import AIStylistEngine, generate_shopping_url


def create_sample_images():
    """Generates synthetic full-body and face reference images for testing."""
    # Full Body
    body_img = Image.new("RGB", (400, 600), color=(242, 245, 248))
    d1 = ImageDraw.Draw(body_img)
    d1.rectangle([(20, 20), (380, 580)], outline=(180, 190, 210), width=2)
    d1.ellipse([(175, 50), (225, 115)], fill=(215, 175, 145))
    d1.polygon([(150, 160), (250, 160), (230, 320), (170, 320)], fill=(75, 85, 99))
    d1.polygon([(150, 160), (135, 180), (120, 290), (135, 290), (160, 170)], fill=(75, 85, 99))
    d1.polygon([(250, 160), (265, 180), (280, 290), (265, 290), (240, 170)], fill=(75, 85, 99))
    d1.ellipse([(112, 285), (135, 325)], fill=(215, 175, 145))
    d1.ellipse([(265, 285), (288, 325)], fill=(215, 175, 145))
    d1.polygon([(170, 320), (198, 320), (195, 530), (168, 530)], fill=(45, 55, 72))
    d1.polygon([(202, 320), (230, 320), (232, 530), (205, 530)], fill=(45, 55, 72))

    # Face Close-Up
    face_img = Image.new("RGB", (400, 400), color=(245, 245, 248))
    d2 = ImageDraw.Draw(face_img)
    d2.rectangle([(20, 20), (380, 380)], outline=(190, 200, 220), width=2)
    d2.ellipse([(110, 70), (290, 310)], fill=(215, 175, 145))
    d2.polygon([(100, 110), (130, 45), (200, 35), (270, 45), (300, 110), (290, 130), (270, 85), (130, 85), (110, 130)], fill=(30, 22, 18))
    d2.ellipse([(150, 160), (175, 175)], fill=(40, 30, 25))
    d2.ellipse([(225, 160), (250, 175)], fill=(40, 30, 25))

    return body_img, face_img


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    print("=" * 70)
    print("✨ VogueAI - Personal Styling & Virtual Try-On Engine Test")
    print("=" * 70)

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("\n[NOTE] GEMINI_API_KEY environment variable is not set.")
        print("Running in High-Fidelity Demo Simulation Mode.\n")
    else:
        print("\n[OK] Gemini API Key detected. Connected to Gemini 3.8 Flash.\n")

    # Load or generate sample images
    body_img, face_img = create_sample_images()
    print("✅ Reference images prepared (Full Body & Face).")

    # Initialize Engine
    engine = AIStylistEngine(api_key=api_key)

    # Run Analysis
    print("⏳ Running multimodal vision analysis...")
    profile = engine.analyze_styling_profile(
        full_body_image=body_img,
        face_image=face_img,
        gender_preference="Men",
        user_height_cm=175
    )

    print("\n" + "=" * 70)
    print("🎯 ANALYSIS RESULTS")
    print("=" * 70)
    print(f"User Summary: {profile.user_summary}\n")

    print("[1] BODY & MEASUREMENT ANALYSIS:")
    print(f"  • Slenderness / Build: {profile.body_analysis.slenderness_level}")
    print(f"  • Estimated Body Fat:  {profile.body_analysis.estimated_body_fat_range}")
    print(f"  • Somatotype:          {profile.body_analysis.somatotype}")
    print(f"  • Silhouette:          {profile.body_analysis.body_silhouette_shape}")
    print(f"  • Arm Length:          {profile.body_analysis.arm_and_hand.arm_length_proportion}")
    print(f"  • Bicep / Forearm:     {profile.body_analysis.arm_and_hand.bicep_forearm_build}")
    print(f"  • Wrist Thickness:     {profile.body_analysis.arm_and_hand.wrist_thickness}")
    print(f"  • Hand Details:        {profile.body_analysis.arm_and_hand.detailed_hand_arm_observation}")

    print("\n[2] FACE, SKIN & HAIR ANALYSIS:")
    face = profile.face_and_color_analysis
    print(f"  • Skin Undertone:      {face.skin_undertone}")
    print(f"  • Skin Shade Depth:    {face.skin_shade_depth}")
    print(f"  • Color Season:        {face.seasonal_color_palette}")
    print(f"  • Face Shape:          {face.face_shape}")
    print(f"  • Haircut Advice:      {face.hair.haircut_advice_for_face}")
    print("  • Best Flattering Colors:")
    for c in face.flattering_colors:
        print(f"    - {c.color_name} ({c.hex_code}): {c.why_flattering}")

    print("\n[3] STYLING & FIT RULES:")
    print(f"  • Best Collars:        {', '.join(profile.styling_rules.best_necklines_and_collars)}")
    print(f"  • Best Sleeve Cuts:    {', '.join(profile.styling_rules.best_sleeve_lengths_and_cuffs)}")
    print(f"  • Flattering Fits:     {', '.join(profile.styling_rules.flattering_fits_and_silhouettes)}")
    print(f"  • Recommended Fabrics: {', '.join(profile.styling_rules.recommended_fabrics_and_textures)}")

    print("\n[4] CURATED OUTFIT RECOMMENDATIONS (THE BRAIN):")
    for i, look in enumerate(profile.curated_outfits, 1):
        print(f"\n  LOOK {i}: {look.look_title} ({look.occasion})")
        print(f"  Vibe: {look.style_vibe_summary}")
        for item in look.items:
            url = generate_shopping_url(item.search_keywords, "myntra")
            print(f"    • [{item.item_category}] {item.item_name} ({item.color}, {item.fabric})")
            print(f"      Size & Fit: {item.recommended_fit_and_size}")
            print(f"      Why it suits: {item.why_it_suits_user}")
            print(f"      Shop Link: {url}")

    print("\n" + "=" * 70)
    print("🪞 GENERATING VIRTUAL TRY-ON (LOOK 1)...")
    chosen_look = profile.curated_outfits[0]
    vton_result = engine.generate_virtual_try_on(
        full_body_image=body_img,
        face_image=face_img,
        selected_look=chosen_look,
        styling_profile=profile
    )

    output_path = "virtual_try_on_output.png"
    vton_result.save(output_path)
    print(f"✅ Virtual Try-On generated and saved to: {output_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
