# ✨ VogueAI: AI Body Stylist & Virtual Try-On Studio

एक सम्पूर्ण AI-पावर्ड स्टाइलिंग और वर्चुअल ट्राई-ऑन (Virtual Try-On) सिस्टम जो दो तस्वीरों (फुल बॉडी और फेस क्लोज़-अप) का विश्लेषण करके शरीर का माप, हाथ की लंबाई, स्किन टोन, हेयर स्टाइल और बेस्ट कपड़े सुझाता है।

---

## 🌟 मुख्य विशेषताएँ (Key Features)

1. **फुल बॉडी इमेज एनालिसिस (Full-Body Biometrics)**:
   - **पतलापन / स्लिमनेस (Slenderness Level)** व विजुअल बॉडी फैट प्रतिशत का आंकलन।
   - **हाथ और बाजू का माप (Arm & Hand Measurement)**: बाजू की लंबाई, बाइसेप/फोरआर्म की बनावट, कलाई का माप और हथेली का अनुपात।
   - **अनुपात (Proportions)**: कंधे (Shoulder width), धड़-से-पैर का अनुपात (Torso-to-Leg ratio), पोस्चर और बॉडी सिल्हूट (Trapezoid, Rectangle, Hourglass, Inverted Triangle आदि)।

2. **फेस और स्किन टोन एनालिसिस (Face & Tone Analysis)**:
   - **स्किन अंडरटोन (Skin Undertone)**: Warm, Cool, Neutral, Olive.
   - **स्किन शेड और सीजन पैलेट (Color Season)**: Deep Autumn, Warm Spring, Cool Winter आदि।
   - **हेयर स्टाइल और टेक्सचर (Hair Style & Cut)**: वर्तमान कट, वॉल्यूम, टेक्सचर और चेहरे के अनुसार सुझाई गई सर्वश्रेष्ठ हेयर स्टाइल।
   - **फेस शेप और ग्रूमिंग (Face Shape & Grooming)**: चश्मा (Eyewear) और बियर्ड/जॉलाइन ग्रूमिंग सुझाव।

3. **कस्टम स्टाइलिंग रूल्स इंजन (Styling Blueprint)**:
   - आपके शरीर और चेहरे के अनुसार बेस्ट कॉलर / नेकलाइन (Cuban, Mandarin, V-neck)।
   - पतले हाथों और कंधों को बैलेंस करने वाले स्लीव कट्स (Sleeve length & Cuffs)।
   - बेस्ट फैब्रिक्स और टेक्सचर (Linen, Waffle Knit, Corduroy)।
   - क्या पहनें (Do's) और किन गलतियों से बचें (Don'ts)।

4. **शॉपिंग ब्रेन (Curated Outfits & Live Shopping Links)**:
   - 3 पूर्ण लुक्स (Casual Weekend, Smart Work/College, Evening/Festive Party)।
   - हर कपड़े के लिए सटीक साइज और फिटिंग सलाह (जैसे `Size M - Relaxed Fit with tapered sleeves`)।
   - डायरेक्ट 1-क्लिक शॉपिंग लिंक्स: **Myntra, Amazon, Zara, Google Shopping**।

5. **वर्चुअल ट्राई-ऑन स्टूडियो (AI Virtual Try-On - VTON)**:
   - चुने हुए ऑउटफिट में यूजर की फोटो को AI के साथ कंबाइन करके वास्तविक ट्राई-ऑन इमेज जनरेट करता है।
   - ओरिजिनल फोटो और ट्राई-ऑन फोटो को साइड-बाई-साइड देखने और डाउनलोड करने की सुविधा।

---

## 📂 फ़ाइल संरचना (Project Structure)

```
C:\Users\Shubham\.gemini\antigravity\scratch\ai_styling_app\
│
├── stylist_engine.py       # कोर AI इंजन (Pydantic स्कीमा, Gemini 3.8 Vision, VTON)
├── app.py                  # आधुनिक Streamlit वेब ऐप्लिकेशन (Interactive Web UI)
├── sample_run.py           # स्टैंडअलोन CLI टेस्ट स्क्रिप्ट (बिना UI के तुरंत रन करें)
├── virtual_try_on_output.png # जनरेट किया गया वर्चुअल ट्राई-ऑन आउटपुट
├── requirements.txt        # आवश्यक Python पैकेज
└── README.md               # यह गाइड
```

---

## 🚀 चलाने का तरीका (How to Run)

### विकल्प 1: इंटरैक्टिव वेब ऐप्लिकेशन (Streamlit Web UI)

कमांड प्रॉम्प्ट या टर्मिनल में यह कमांड चलाएँ:

```bash
cd "C:\Users\Shubham\.gemini\antigravity\scratch\ai_styling_app"
streamlit run app.py
```

ब्राउज़र में अपने आप `http://localhost:8501` खुल जाएगा जहाँ आप:
- अपनी फोटो ड्रैग-एंड-ड्रॉप कर सकते हैं।
- साइडबार में अपनी Gemini API Key डाल सकते हैं (या बिना API Key के सैंपल टेस्ट कर सकते हैं)।
- 1-क्लिक में पूरी एनालिसिस, कलर स्वॉचेस, शॉपिंग लिंक्स और वर्चुअल ट्राई-ऑन देख सकते हैं।

### विकल्प 2: स्टैंडअलोन स्क्रिप्ट (Python CLI)

टर्मिनल में सीधे चलाएँ:

```bash
cd "C:\Users\Shubham\.gemini\antigravity\scratch\ai_styling_app"
python sample_run.py
```

यह तुरंत सारी एनालिसिस कंसोल में दिखाएगा और `virtual_try_on_output.png` फाइल जनरेट कर देगा।

---

## 🔑 API Key सेटअप (वैकल्पिक)

यदि आप लाइव Gemini Vision API का उपयोग करना चाहते हैं:
1. [Google AI Studio](https://aistudio.google.com/) से अपनी मुफ्त API Key प्राप्त करें।
2. टर्मिनल में सेट करें:
   ```powershell
   $env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
   ```
   या सीधे Streamlit ऐप के साइडबार में दर्ज करें।
*(अगर API Key नहीं भी डालते हैं, तो ऐप में बना इन-बिल्ट स्मार्ट सिम्युलेटर पूरा फ्लो टेस्ट करने की सुविधा देता है)*
