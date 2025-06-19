
import streamlit as st
import fitz  # PyMuPDF
import re
import io

st.title("📦 Exportador de Facturas por Todos los IDs")

st.write("Sube dos archivos: uno con las facturas y otro con la hoja de ruta.")

factura_file = st.file_uploader("📄 Archivo de Facturas", type="pdf")
hoja_ruta_file = st.file_uploader("📋 Hoja de Ruta", type="pdf")

def extraer_ids(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    texto = ""
    for page in doc:
        texto += page.get_text()
    ids = re.findall(r"\b(13\d{4})\b", texto)
    return sorted(set(ids))

def filtrar_facturas_por_ids(pdf_bytes, lista_ids):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    nuevo_pdf = fitz.open()

    for page in doc:
        texto = page.get_text()
        if any(id_ in texto for id_ in lista_ids):
            nuevo_pdf.insert_pdf(doc, from_page=page.number, to_page=page.number)

    output = io.BytesIO()
    nuevo_pdf.save(output)
    nuevo_pdf.close()
    return output.getvalue()

if factura_file and hoja_ruta_file:
    hoja_bytes = hoja_ruta_file.read()
    ids_encontrados = extraer_ids(hoja_bytes)

    if ids_encontrados:
        if st.button("📥 Generar y Descargar Todas las Facturas"):
            pdf_filtrado = filtrar_facturas_por_ids(factura_file.read(), ids_encontrados)
            st.success("✅ PDF generado con todas las facturas encontradas")
            st.download_button(
                label="📥 Descargar PDF",
                data=pdf_filtrado,
                file_name="facturas_filtradas_por_todos_los_ids.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("No se encontraron IDs en la hoja de ruta.")
