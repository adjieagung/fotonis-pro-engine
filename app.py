import streamlit as st
import requests
import base64
import json

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Mesin Fotonis Pro", page_icon="🚀", layout="wide")

# --- AMBIL API KEYS DARI SECRETS ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    REMOVE_BG_API_KEY = st.secrets["REMOVE_BG_API_KEY"]
except KeyError:
    st.error("⚠️ API Key belum lengkap. Pastikan GEMINI_API_KEY dan REMOVE_BG_API_KEY sudah terisi di Streamlit Secrets.")
    st.stop()

st.title("🚀 Mesin Fotonis Pro: Ultralight")
st.markdown("**Sistem Pembuat Katalog Otomatis & Analisa Ekspor Global**")

# --- FUNGSI HAPUS BACKGROUND VIA API (0% CPU Server) ---
def remove_bg_api(image_bytes):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_bytes},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
    )
    if response.status_code == requests.codes.ok:
        return response.content
    else:
        st.error(f"Gagal hapus background: {response.text}")
        return None

# --- FUNGSI ANALISA GEMINI VIA REQUESTS MURNI ---
def analisa_gemini(image_bytes):
    img_b64 = base64.b64encode(image_bytes).decode('utf-8')
    prompt_text = """
    Anda adalah pakar pemasaran alat berat dan industrial global. 
    Analisa gambar produk ini dan berikan output berikut:
    1. **Nama Produk:** (Komersial & Profesional)
    2. **Spesifikasi Utama:** (Estimasi teknis berdasarkan visual)
    3. **Copywriting Sales Global:** (Gunakan metode AIDA dalam Bahasa Inggris untuk target pasar Ekspor)
    Format jawaban menggunakan Markdown yang rapi dan profesional.
    """
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt_text},
                {"inline_data": {"mime_type": "image/png", "data": img_b64}}
            ]
        }]
    }
    # Kendali penuh ada di baris ini:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()['candidates'][0]['content']['parts'][0]['text']

# --- UI UTAMA ---
uploaded_file = st.file_uploader("Upload Foto Produk", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    file_bytes = uploaded_file.read()
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(file_bytes, caption="Original", use_container_width=True)
    
    with col2:
        if st.button("✨ Proses Cepat"):
            with st.spinner("Memotong background dalam hitungan detik..."):
                result_bytes = remove_bg_api(file_bytes)
                if result_bytes:
                    # Simpan hasil bersih ke memory Streamlit
                    st.session_state['gambar_bersih'] = result_bytes 
                    st.image(result_bytes, caption="Hasil Bersih", use_container_width=True)
                    st.success("Background berhasil dihapus!")

    st.divider()
    
    # --- TOMBOL AI GLOBAL ---
    if st.button("🌍 Analisa AI Global"):
        if 'gambar_bersih' not in st.session_state:
            st.warning("⚠️ Silakan klik 'Proses Cepat' terlebih dahulu untuk membersihkan gambar sebelum dianalisa.")
        else:
            with st.spinner("Gemini sedang menyusun spesifikasi ekspor global..."):
                try:
                    hasil_ai = analisa_gemini(st.session_state['gambar_bersih'])
                    st.success("✅ Analisa Selesai!")
                    
                    # Tampilkan hasil di dalam kotak yang rapi
                    with st.container(border=True):
                        st.markdown(hasil_ai)
                        
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghubungi Gemini: {e}")
