import streamlit as st
import requests
import base64
import io
from PIL import Image

# --- KONFIGURASI ---
# Kita tetap gunakan Requests Murni agar "Power"
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
# Jika Anda punya API Key Remove.bg, masukkan di sini
# Jika tidak, kita bisa gunakan endpoint alternatif
REMOVE_BG_API_KEY = st.secrets.get("REMOVE_BG_API_KEY", "YOUR_FREE_KEY")

st.title("🚀 Mesin Fotonis Pro: Ultralight")

def remove_bg_api(image_bytes):
    # Mengirim gambar ke API eksternal (CPU Server Streamlit 0%)
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_bytes},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
    )
    if response.status_code == requests.codes.ok:
        return response.content
    else:
        st.error("Gagal hapus background. Pastikan API Key benar.")
        return None

# --- UI ---
uploaded_file = st.file_uploader("Upload Foto Produk", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    file_bytes = uploaded_file.read()
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(file_bytes, caption="Original")
    
    with col2:
        if st.button("Proses Cepat"):
            with st.spinner("Eksekusi via API..."):
                # Proses sangat ringan karena dikerjakan server lain
                result = remove_bg_api(file_bytes)
                if result:
                    st.image(result, caption="Hasil Bersih")
                    
    # Lanjut ke Analisa Gemini (Tetap pakai Requests Murni Anda)
    if st.button("Analisa AI Global"):
        # Panggil fungsi requests ke Gemini Anda di sini...
        st.success("Siap ekspor ke pasar Global!")
