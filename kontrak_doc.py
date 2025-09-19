import streamlit as st
import openai
from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(pdf_file):
    """
    Ekstrak teks dari file PDF.
    """
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_contract_with_openai(contract_text, openai_api_key):
    """
    Menganalisis teks kontrak menggunakan API OpenAI.
    """
    openai.api_key = openai_api_key
    
    # Anda bisa menyesuaikan prompt sesuai kebutuhan analisis Anda
    prompt = f"""
    Anda adalah seorang asisten hukum ahli. Analisis dokumen kontrak berikut ini dan berikan ringkasan poin-poin penting, klausul-klausul utama, potensi risiko, dan saran untuk revisi jika diperlukan.

    Kontrak:
    {contract_text}

    Analisis:
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # Anda bisa menggunakan model gpt-3.5-turbo atau gpt-4
            messages=[
                {"role": "system", "content": "Anda adalah asisten hukum yang cerdas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan saat menghubungi OpenAI API: {e}"

# --- Aplikasi Streamlit ---
st.set_page_config(page_title="Penganalisis Kontrak PDF dengan AI")

st.title("Penganalisis Kontrak PDF dengan AI")
st.write("Unggah dokumen kontrak Anda (PDF) dan biarkan AI menganalisisnya.")

# Sidebar untuk API Key OpenAI
with st.sidebar:
    st.header("Konfigurasi API")
    openai_api_key = st.text_input("Masukkan OpenAI API Key Anda", type="password")
    st.info("Dapatkan API Key Anda dari platform.openai.com")

st.markdown("---")

uploaded_file = st.file_uploader("Pilih dokumen kontrak PDF", type="pdf")

if uploaded_file is not None:
    if openai_api_key:
        st.success("File PDF berhasil diunggah.")
        
        # Ekstrak teks dari PDF
        with st.spinner("Mengekstrak teks dari PDF..."):
            contract_text = extract_text_from_pdf(uploaded_file)
        
        if contract_text:
            st.subheader("Teks yang Diekstrak dari Kontrak:")
            with st.expander("Lihat Teks Lengkap"):
                st.text(contract_text[:1000] + "..." if len(contract_text) > 1000 else contract_text) # Tampilkan sebagian kecil teks untuk menghindari overloading
            
            st.markdown("---")
            
            if st.button("Mulai Analisis Kontrak"):
                with st.spinner("Menganalisis kontrak dengan AI... Ini mungkin memakan waktu beberapa saat."):
                    analysis_result = analyze_contract_with_openai(contract_text, openai_api_key)
                
                st.subheader("Hasil Analisis AI:")
                st.write(analysis_result)
        else:
            st.error("Tidak dapat mengekstrak teks dari PDF. Pastikan PDF tidak kosong atau terenkripsi.")
    else:
        st.warning("Harap masukkan OpenAI API Key Anda di sidebar untuk melanjutkan.")
