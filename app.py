"""
app.py
Streamlit Web Application: AI Stylist & Virtual Try-On Studio.
Upload Full-Body and Face photos to get:
- Body slenderness, hand/arm proportions, body fat estimate
- Skin tone, undertone, color season palette, hair style, face shape
- Personalized styling rules (necklines, sleeves, fabrics)
- Curated shopping items ("The Brain") with direct shopping links
- Virtual Try-On (VTON) visualization
"""

import os
import streamlit as st
from PIL import Image, ImageDraw
import io

from stylist_engine import (
    AIStylistEngine,
    FullStylingProfile,
    OutfitLook,
    generate_shopping_url
)

# ---------------------------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="VogueAI - AI Stylist & Virtual Try-On",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #9B51E0, #4A90E2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #8892B0;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #1A1F2C;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #2E384D;
        margin-bottom: 0.8rem;
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        color: #8892B0;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.25rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-top: 0.3rem;
    }
    .color-swatch {
        display: inline-block;
        width: 100%;
        height: 60px;
        border-radius: 8px;
        margin-bottom: 6px;
        border: 1px solid rgba(255,255,255,0.15);
    }
    .outfit-card {
        background: #161B26;
        border: 1px solid #2B3548;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.4rem;
        background: #2D3748;
        color: #CBD5E0;
    }
    .badge-primary {
        background: rgba(155, 81, 224, 0.25);
        color: #D6BCFA;
        border: 1px solid #9B51E0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Demo Image Helper
# ---------------------------------------------------------------------------
def create_demo_body_image() -> Image.Image:
    """Creates a sample stylized silhouette full body image for demo testing."""
    img = Image.new("RGB", (400, 600), color=(240, 243, 246))
    d = ImageDraw.Draw(img)
    # Background gradient or frame
    d.rectangle([(20, 20), (380, 580)], outline=(200, 210, 225), width=2)
    # Head
    d.ellipse([(175, 50), (225, 115)], fill=(215, 175, 145))
    # Hair
    d.arc([(172, 45), (228, 90)], 180, 360, fill=(35, 25, 20), width=12)
    # Neck & Torso (Slender / Lean build)
    d.polygon([(192, 115), (208, 115), (218, 160), (182, 160)], fill=(215, 175, 145))
    d.polygon([(150, 160), (250, 160), (230, 320), (170, 320)], fill=(75, 85, 99))  # Upper body
    # Arms & Hands (Demonstrating slender long arms)
    d.polygon([(150, 160), (135, 180), (120, 290), (135, 290), (160, 170)], fill=(75, 85, 99))
    d.polygon([(250, 160), (265, 180), (280, 290), (265, 290), (240, 170)], fill=(75, 85, 99))
    d.ellipse([(112, 285), (135, 325)], fill=(215, 175, 145))  # Left hand
    d.ellipse([(265, 285), (288, 325)], fill=(215, 175, 145))  # Right hand
    # Legs
    d.polygon([(170, 320), (198, 320), (195, 530), (168, 530)], fill=(45, 55, 72))  # Left leg
    d.polygon([(202, 320), (230, 320), (232, 530), (205, 530)], fill=(45, 55, 72))  # Right leg
    # Shoes
    d.ellipse([(160, 525), (198, 545)], fill=(25, 30, 35))
    d.ellipse([(202, 525), (240, 545)], fill=(25, 30, 35))
    d.text((120, 560), "Sample Full-Body Reference", fill=(100, 116, 139))
    return img


def create_demo_face_image() -> Image.Image:
    """Creates a sample stylized face close-up image for demo testing."""
    img = Image.new("RGB", (400, 400), color=(245, 245, 247))
    d = ImageDraw.Draw(img)
    d.rectangle([(20, 20), (380, 380)], outline=(210, 215, 225), width=2)
    # Head / Face
    d.ellipse([(110, 70), (290, 310)], fill=(215, 175, 145))
    # Hair (Textured crop)
    d.polygon([(100, 110), (130, 45), (200, 35), (270, 45), (300, 110), (290, 130), (270, 85), (130, 85), (110, 130)], fill=(30, 22, 18))
    # Eyes
    d.ellipse([(150, 160), (175, 175)], fill=(40, 30, 25))
    d.ellipse([(225, 160), (250, 175)], fill=(40, 30, 25))
    # Eyebrows
    d.line([(145, 150), (180, 147)], fill=(30, 22, 18), width=3)
    d.line([(220, 147), (255, 150)], fill=(30, 22, 18), width=3)
    # Nose & Jawline
    d.line([(200, 170), (195, 215), (208, 218)], fill=(180, 140, 115), width=2)
    d.arc([(175, 235), (225, 255)], 0, 180, fill=(160, 90, 80), width=3)
    # Groomed stubble
    d.arc([(130, 200), (270, 305)], 20, 160, fill=(120, 95, 80), width=2)
    d.text((115, 355), "Sample Face Close-Up Reference", fill=(100, 116, 139))
    return img


# ---------------------------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings & Configuration")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Google Gemini API Key दर्ज करें। अगर नहीं है, तो आप 'Demo Mode' में भी टेस्ट कर सकते हैं।"
    )

    if not api_key_input:
        st.info("💡 **Tips**: API key नहीं होने पर ऐप ऑटोमैटिकली स्मार्ट डेमो इंजन का उपयोग करेगा।")

    st.markdown("---")
    st.markdown("### 👤 User Persona Profile")
    gender_pref = st.selectbox("Styling For", ["Men", "Women", "Unisex"], index=0)
    user_height = st.number_input("User Height (cm) [Optional]", min_value=120, max_value=220, value=175, step=1)
    target_vibe = st.multiselect(
        "Preferred Style Vibes",
        ["Minimalist Smart Casual", "Streetwear & Layering", "Classic Tailored", "Old Money / Quiet Luxury", "Indo-Western / Festive"],
        default=["Minimalist Smart Casual", "Old Money / Quiet Luxury"]
    )

    st.markdown("---")
    st.markdown("**Powered by:** Google Gemini 3.8 Flash & Google GenAI SDK")


# ---------------------------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------------------------
st.markdown('<div class="main-title">✨ VogueAI: Personal Stylist & Virtual Try-On</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">फुल बॉडी व फेस इमेज से सटीक बॉडी मेजरमेंट, हाथ का माप, स्किन टोन, हेयर स्टाइल एनालिसिस और क्लोथ्स रिकमेंडेशन + वर्चुअल ट्राई-ऑन स्टूडियो</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Image Upload Section
# ---------------------------------------------------------------------------
col_upload_1, col_upload_2 = st.columns(2)

with col_upload_1:
    st.markdown("#### 1. 🧍 Full Body Photo (फुल बॉडी पिक्चर)")
    st.caption("बॉडी का पतलापन (Slenderness), हाथ की मेजरमेंट, कंधों और पैरों के अनुपात के लिए।")
    body_file = st.file_uploader("Upload Full Body Image", type=["jpg", "jpeg", "png", "webp"], key="body_img")

with col_upload_2:
    st.markdown("#### 2. 👤 Face Close-Up Photo (चेहरे की पिक्चर)")
    st.caption("स्किन अंडरटोन, कलर सीजन (Season Palette), हेयर स्टाइल और फेस शेप के लिए।")
    face_file = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png", "webp"], key="face_img")

# Quick Demo Sample Toggle
col_demo, _ = st.columns([2, 3])
with col_demo:
    use_sample_images = st.checkbox("⚡ Use Sample Demo Photos (अगर आपके पास अभी फोटो नहीं हैं तो इसे चुनें)")

body_image = None
face_image = None

if use_sample_images:
    body_image = create_demo_body_image()
    face_image = create_demo_face_image()
else:
    if body_file is not None:
        body_image = Image.open(body_file)
    if face_file is not None:
        face_image = Image.open(face_file)

# Show preview if images are loaded
if body_image and face_image:
    preview_col1, preview_col2 = st.columns(2)
    with preview_col1:
        st.image(body_image, caption="Uploaded Full Body Photo", use_container_width=True)
    with preview_col2:
        st.image(face_image, caption="Uploaded Face Close-Up Photo", use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------------------
# Trigger Analysis
# ---------------------------------------------------------------------------
analyze_btn = st.button("🚀 Analyze Body, Face & Generate Style Plan", type="primary", use_container_width=True)

if analyze_btn:
    if not body_image or not face_image:
        st.error("⚠️ कृपया दोनों तस्वीरें अपलोड करें: (1) फुल बॉडी फोटो और (2) फेस फोटो, या 'Use Sample Demo Photos' चेकबॉक्स चुनें।")
    else:
        with st.spinner("🔍 Gemini Multimodal Vision शरीर का माप, हाथ की लंबाई, स्किन टोन और हेयर स्टाइल एनालाइज कर रहा है..."):
            engine = AIStylistEngine(api_key=api_key_input)
            profile = engine.analyze_styling_profile(
                full_body_image=body_image,
                face_image=face_image,
                gender_preference=gender_pref,
                user_height_cm=user_height
            )
            # Store in session state
            st.session_state["profile"] = profile
            st.session_state["body_image"] = body_image
            st.session_state["face_image"] = face_image
            st.session_state["engine"] = engine
            st.success("✅ एनालिसिस पूरी हो गई! नीचे अपने पर्सनलाइज्ड परिणाम देखें:")

# ---------------------------------------------------------------------------
# Dashboard Results Display
# ---------------------------------------------------------------------------
if "profile" in st.session_state:
    profile: FullStylingProfile = st.session_state["profile"]
    body_img = st.session_state["body_image"]
    face_img = st.session_state["face_image"]
    engine: AIStylistEngine = st.session_state["engine"]

    # User Summary Banner
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1E2638, #2A1F3D); border-left: 5px solid #9B51E0; padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem;">
        <h4 style="margin: 0; color: #E2E8F0;">✨ Fashion Identity & Archetype</h4>
        <p style="margin-top: 0.5rem; color: #CBD5E0; font-size: 1.05rem;">{profile.user_summary}</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📏 1. Body & Hand Measurements",
        "🎨 2. Face, Skin & Hair Tone",
        "👔 3. Styling & Fit Rules",
        "🛍️ 4. Shopping Brain & Outfits",
        "🪞 5. Virtual Try-On Studio"
    ])

    # -----------------------------------------------------------------------
    # TAB 1: Body & Measurement Analysis
    # -----------------------------------------------------------------------
    with tab1:
        st.markdown("### 🧬 Body Structure & Proportional Measurement Analysis")
        st.caption("फुल बॉडी इमेज से एक्सट्रैक्ट किया गया माप और बॉडी फैट / स्लिमनेस का आंकलन:")

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Slenderness / Build</div>
                <div class="metric-value">{profile.body_analysis.slenderness_level}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Est. Body Fat</div>
                <div class="metric-value">{profile.body_analysis.estimated_body_fat_range}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Somatotype</div>
                <div class="metric-value">{profile.body_analysis.somatotype}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Silhouette Shape</div>
                <div class="metric-value">{profile.body_analysis.body_silhouette_shape}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 🖐️ Arm & Hand Measurement Details (हाथ और बाजू का माप)")
        arm = profile.body_analysis.arm_and_hand
        arm_c1, arm_c2, arm_c3, arm_c4 = st.columns(4)
        with arm_c1:
            st.info(f"**Arm Length Proportion:**\n\n{arm.arm_length_proportion}")
        with arm_c2:
            st.info(f"**Bicep & Forearm Build:**\n\n{arm.bicep_forearm_build}")
        with arm_c3:
            st.info(f"**Wrist Thickness:**\n\n{arm.wrist_thickness}")
        with arm_c4:
            st.info(f"**Hand Proportion:**\n\n{arm.hand_size_proportion}")

        st.markdown(f"**विशेष ऑब्जर्वेशन:** {arm.detailed_hand_arm_observation}")

        st.markdown("#### 📐 Proportions & Frame Breakdown")
        prop_c1, prop_c2 = st.columns(2)
        with prop_c1:
            st.write(f"• **Shoulder Ratio:** {profile.body_analysis.shoulder_proportion}")
            st.write(f"• **Torso to Leg Ratio:** {profile.body_analysis.torso_to_leg_ratio}")
        with prop_c2:
            st.write(f"• **Chest & Waist Taper:** {profile.body_analysis.chest_waist_hip_summary}")
            st.write(f"• **Posture & Bone Frame:** {profile.body_analysis.posture_and_frame}")

    # -----------------------------------------------------------------------
    # TAB 2: Face, Skin & Hair Tone
    # -----------------------------------------------------------------------
    with tab2:
        st.markdown("### 🎨 Complexion, Hair & Facial Geometry Analysis")
        face = profile.face_and_color_analysis

        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Skin Undertone</div>
                <div class="metric-value">{face.skin_undertone}</div>
            </div>
            """, unsafe_allow_html=True)
        with fc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Skin Depth</div>
                <div class="metric-value">{face.skin_shade_depth}</div>
            </div>
            """, unsafe_allow_html=True)
        with fc3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Color Season</div>
                <div class="metric-value">{face.seasonal_color_palette}</div>
            </div>
            """, unsafe_allow_html=True)
        with fc4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Face Shape</div>
                <div class="metric-value">{face.face_shape}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 🌟 Top Flattering Colors (आपके लिए सबसे अच्छे रंग)")
        st.caption("ये रंग आपकी स्किन टोन और फेस के ग्लो को अधिकतम निखारते हैं:")
        cols = st.columns(len(face.flattering_colors))
        for idx, color_item in enumerate(face.flattering_colors):
            with cols[idx]:
                st.markdown(f"""
                <div style="background:{color_item.hex_code};" class="color-swatch"></div>
                <div style="font-weight:600; font-size:0.95rem; color:#F7FAFC;">{color_item.color_name}</div>
                <div style="font-size:0.75rem; color:#A0AEC0;">{color_item.hex_code}</div>
                <div style="font-size:0.75rem; color:#CBD5E0; margin-top:4px;">{color_item.why_flattering}</div>
                """, unsafe_allow_html=True)

        st.markdown("#### 🚫 Colors to Avoid (इन रंगों से बचें)")
        avoid_cols = st.columns(len(face.colors_to_avoid))
        for idx, avoid_c in enumerate(face.colors_to_avoid):
            with avoid_cols[idx]:
                st.error(f"❌ {avoid_c}")

        st.markdown("#### 💇 Hair Style & Grooming Analysis")
        hair = face.hair
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            st.write(f"• **Current Cut / Style:** {hair.current_cut_and_style}")
            st.write(f"• **Hair Texture:** {hair.hair_texture}")
            st.write(f"• **Hair Color / Shade:** {hair.hair_color_shade}")
        with h_col2:
            st.success(f"**Recommended Haircut & Styling for Face Shape:**\n\n{hair.haircut_advice_for_face}")

        st.markdown(f"**🕶️ Eyewear & Facial Grooming Advice:** {face.facial_features_and_accessories}")

    # -----------------------------------------------------------------------
    # TAB 3: Styling & Fit Rules
    # -----------------------------------------------------------------------
    with tab3:
        st.markdown("### 👔 Tailored Styling Blueprint (What Will Best Suit You)")
        rules = profile.styling_rules

        rule_col1, rule_col2 = st.columns(2)
        with rule_col1:
            st.markdown("#### 🎯 Best Necklines & Collars")
            for item in rules.best_necklines_and_collars:
                st.markdown(f"• **{item}**")

            st.markdown("#### 📏 Best Sleeve Lengths & Cuffs")
            st.caption("हाथ के माप और स्लिम आर्म्स को बैलेंस करने के लिए:")
            for item in rules.best_sleeve_lengths_and_cuffs:
                st.markdown(f"• **{item}**")

        with rule_col2:
            st.markdown("#### ✂️ Flattering Fits & Silhouettes")
            for item in rules.flattering_fits_and_silhouettes:
                st.markdown(f"• **{item}**")

            st.markdown("#### 🧵 Recommended Fabrics & Textures")
            st.caption("जो बॉडी में स्ट्रक्चर और प्रीमियम लुक जोड़ते हैं:")
            for item in rules.recommended_fabrics_and_textures:
                st.markdown(f"• **{item}**")

        st.markdown("---")
        do_col, dont_col = st.columns(2)
        with do_col:
            st.markdown("#### ✅ Golden Styling Do's")
            for do in rules.styling_dos:
                st.markdown(f"✔️ {do}")
        with dont_col:
            st.markdown("#### ❌ Styling Pitfalls to Avoid")
            for dont in rules.styling_donts:
                st.markdown(f"⚠️ {dont}")

    # -----------------------------------------------------------------------
    # TAB 4: Shopping Brain & Outfits
    # -----------------------------------------------------------------------
    with tab4:
        st.markdown("### 🛍️ The Recommendation Brain: Curated Outfits & Shopping Links")
        st.caption("आपकी सटीक मेजरमेंट्स, स्किन टोन और स्टाइलिंग रूल्स के आधार पर तैयार किए गए 3 संपूर्ण लुक्स:")

        for look_idx, look in enumerate(profile.curated_outfits, start=1):
            with st.expander(f"✨ LOOK {look_idx}: {look.look_title} ({look.occasion})", expanded=(look_idx == 1)):
                st.markdown(f"**Style Vibe:** *{look.style_vibe_summary}*")
                st.markdown("##### 📦 Outfit Components & Direct Shopping Links:")

                for item in look.items:
                    st.markdown(f"""
                    <div class="outfit-card">
                        <span class="badge badge-primary">{item.item_category}</span>
                        <span class="badge">{item.color}</span>
                        <span class="badge">{item.fabric}</span>
                        <span class="badge" style="background:#234E52; color:#81E6D9;">{item.approx_price_inr}</span>
                        <h4 style="margin: 0.5rem 0 0.2rem 0; color:#F7FAFC;">{item.item_name}</h4>
                        <p style="margin: 0.2rem 0; color:#A0AEC0;"><strong>Recommended Fit & Size:</strong> {item.recommended_fit_and_size}</p>
                        <p style="margin: 0.2rem 0; color:#CBD5E0; font-size:0.9rem;"><strong>Why It Suits You:</strong> {item.why_it_suits_user}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_c1, btn_c2, btn_c3, btn_c4 = st.columns(4)
                    with btn_c1:
                        st.link_button("🛍️ Find on Myntra", generate_shopping_url(item.search_keywords, "myntra"), use_container_width=True)
                    with btn_c2:
                        st.link_button("📦 Find on Amazon", generate_shopping_url(item.search_keywords, "amazon"), use_container_width=True)
                    with btn_c3:
                        st.link_button("✨ Find on Zara", generate_shopping_url(item.search_keywords, "zara"), use_container_width=True)
                    with btn_c4:
                        st.link_button("🔍 Google Shopping", generate_shopping_url(item.search_keywords, "google"), use_container_width=True)

    # -----------------------------------------------------------------------
    # TAB 5: Virtual Try-On Studio
    # -----------------------------------------------------------------------
    with tab5:
        st.markdown("### 🪞 AI Virtual Try-On Studio (वर्चुअल ट्राई-ऑन)")
        st.caption("चुनें कि आप किस ऑउटफिट में खुद को देखना चाहते हैं और AI जनरेटेड वर्चुअल ट्राई-ऑन देखें:")

        look_titles = [f"{l.look_title} ({l.occasion})" for l in profile.curated_outfits]
        selected_look_title = st.selectbox("Select Outfit to Virtually Try On:", look_titles)
        selected_look_idx = look_titles.index(selected_look_title)
        chosen_look = profile.curated_outfits[selected_look_idx]

        st.markdown(f"**Curated Items in this Look:**")
        for it in chosen_look.items:
            st.write(f"• **{it.item_category}:** {it.item_name} ({it.color}, {it.fabric}) — *Fit: {it.recommended_fit_and_size}*")

        vton_btn = st.button("✨ Generate AI Virtual Try-On", type="primary", key="vton_generate")

        if vton_btn or "vton_result" in st.session_state:
            if vton_btn:
                with st.spinner("🎨 AI आपके शरीर और चेहरे के संदर्भ को जोड़कर इस ऑउटफिट के साथ वर्चुअल ट्राई-ऑन तैयार कर रहा है..."):
                    vton_img = engine.generate_virtual_try_on(
                        full_body_image=body_img,
                        face_image=face_img,
                        selected_look=chosen_look,
                        styling_profile=profile
                    )
                    st.session_state["vton_result"] = vton_img
                    st.session_state["vton_look_title"] = chosen_look.look_title

            vton_img = st.session_state["vton_result"]

            v_col1, v_col2 = st.columns([1, 1.2])
            with v_col1:
                st.markdown("##### 📷 Original Full-Body Reference")
                st.image(body_img, use_container_width=True)
            with v_col2:
                st.markdown(f"##### 🪞 Virtual Try-On Result ({st.session_state.get('vton_look_title', 'Curated Look')})")
                st.image(vton_img, use_container_width=True)

                # Download Button
                buf = io.BytesIO()
                vton_img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="💾 Download Virtual Try-On Image",
                    data=byte_im,
                    file_name="virtual_try_on_vogue_ai.png",
                    mime="image/png",
                    use_container_width=True
                )
