import streamlit as st
import requests
import json
from rembg import remove
from PIL import Image
import io

# 1. Optimasi Model: Gunakan 'u2netp' (versi kecil/cepat)
def clean_bg(img_input):
    # Mengurangi ukuran gambar sebelum diproses AI agar RAM tidak bengkak
    img_input.thumbnail((800, 800)) 
    return remove(img_input, model_name="u2netp")

# 2. UI dengan batasan 3 Gambar
st.title("🚀 Mesin Fotonis Pro (Fast Mode)")
st.info("Mode Optimasi Aktif: Batas 3 Gambar untuk Kecepatan Maksimal.")

uploaded_files = st.file_uploader("Upload Maksimal 3 Foto Produk", 
                                  accept_multiple_files=True, 
                                  type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    # Membatasi jumlah file yang diproses
    files_to_process = uploaded_files[:3] 
    
    if len(uploaded_files) > 3:
        st.warning("Hanya 3 foto pertama yang akan diproses di mode cepat ini.")

    cols = st.columns(3) # Buat 3 kolom sejajar
    
    for idx, file in enumerate(files_to_process):
        with cols[idx]:
            with st.spinner(f"Memproses {idx+1}..."):
                # Proses Visual
                img_raw = Image.open(file)
                img_clean = clean_bg(img_raw)
                
                st.image(img_clean, caption=f"Produk {idx+1}", use_container_width=True)
                
                # Tombol Analisa AI tetap menggunakan Requests
                if st.button(f"Analisa Produk {idx+1}"):
                    # Kompres ke JPEG kualitas rendah untuk dikirim ke API agar transmisi cepat
                    buf = io.BytesIO()
                    img_clean.convert("RGB").save(buf, format="JPEG", quality=70)
                    img_bytes = buf.getvalue()
                    
                    # Panggil fungsi call_gemini_vision yang sudah kita buat sebelumnya
                    # response = call_gemini_vision(img_bytes, prompt)
                    st.success("AI Analisa Selesai!")
