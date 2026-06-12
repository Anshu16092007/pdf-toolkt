import streamlit as st
import PyPDF2
from PIL import Image
import io

st.set_page_config(page_title="Ultimate PDF Toolkit", page_icon="📄", layout="centered")

st.title("📄 All-in-One PDF Toolkit")
st.write("Ek hi jagah par PDF Merge, Compress, aur Image to PDF convert karein!")

# Sidebar ya Tabs ke zariye option select karna
option = st.sidebar.selectbox(
    "Aapko kya karna hai?",
    ("PDFs Merge Karein", "JPG/JPEG to PDF", "PDF Compress Karein")
)

st.write("---")

# ==================== 1. MERGE PDF ====================
if option == "PDFs Merge Karein":
    st.header("🔗 Multiple PDF Files Merge Karein")
    
    uploaded_files = st.file_uploader("Apni PDF files upload karein", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Total {len(uploaded_files)} files select hui hain.")
        
        if st.button("Merge PDFs"):
            merger = PyPDF2.PdfMerger()
            try:
                for pdf in uploaded_files:
                    merger.append(pdf)
                
                # Memory mein file save karna bina desktop ka jhanjhat liye
                output = io.BytesIO()
                merger.write(output)
                merger.close()
                
                st.success("🎉 Saari PDFs kamyabi se merge ho gayi hain!")
                st.download_button(
                    label="📥 Merged PDF Download Karein",
                    data=output.getvalue(),
                    file_name="merged_output.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error aaya: {e}")

# ==================== 2. JPG/JPEG TO PDF ====================
elif option == "JPG/JPEG to PDF":
    st.header("🖼️ JPG / JPEG Se PDF Banayein")
    
    uploaded_images = st.file_uploader("Apni Images (.jpg/.jpeg) upload karein", type=["jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_images:
        st.write(f"{len(uploaded_images)} images upload hui hain.")
        
        if st.button("Convert to PDF"):
            try:
                image_list = []
                for img_file in uploaded_images:
                    image = Image.open(img_file)
                    # Image ko RGB mode mein convert karna zaroori hai PDF ke liye
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image_list.append(image)
                
                if image_list:
                    output = io.BytesIO()
                    # Pehli image par baaki saari images append karna
                    image_list[0].save(output, format="PDF", save_all=True, append_images=image_list[1:])
                    
                    st.success("🎉 Images successfully PDF mein convert ho gayi hain!")
                    st.download_button(
                        label="📥 Converted PDF Download Karein",
                        data=output.getvalue(),
                        file_name="images_to_pdf.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error aaya: {e}")

# ==================== 3. COMPRESS PDF ====================
elif option == "PDF Compress Karein":
    st.header("📉 PDF Ka Size (KB) Kam Karein")
    
    uploaded_pdf = st.file_uploader("Jis PDF ka size kam karna hai use upload karein", type=["pdf"])
    
    if uploaded_pdf:
        # File ka asli size nikalna
        original_size = len(uploaded_pdf.getvalue()) / 1024
        st.info(f"Asli Size: {original_size:.2f} KB")
        
        # User se compression level poochna
        quality = st.slider("Compression Level (Jitna kam karenge, size utna kam hoga aur quality thodi ghtegi)", 10, 100, 60)
        
        if st.button("Compress PDF"):
            try:
                # PDF reader aur writer setup karna
                reader = PyPDF2.PdfReader(uploaded_pdf)
                writer = PyPDF2.PdfWriter()
                
                for page in reader.pages:
                    # Naye PyPDF2 mein pages ko compress karne ka default function hota hai
                    page.compress_content_streams()
                    writer.add_page(page)
                
                output = io.BytesIO()
                writer.write(output)
                
                compressed_size = len(output.getvalue()) / 1024
                
                st.success(f"🎉 PDF Compress ho gayi! Naya Size: {compressed_size:.2f} KB")
                st.download_button(
                    label="📥 Compressed PDF Download Karein",
                    data=output.getvalue(),
                    file_name="compressed_output.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Compression mein dikkat aayi: {e}")