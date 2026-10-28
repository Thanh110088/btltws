import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def merge_documents():
    # Load base document and db design document
    base_path = r"g:\BTLWNC\FlawFirst.Api\Phan_Tich_Thiet_Ke_He_Thong_FlawFirst.docx"
    db_path = r"g:\BTLWNC\FlawFirst.Api\Thiet_Ke_He_Thong_Du_Lieu_FlawFirst.docx"
    full_path = r"g:\BTLWNC\FlawFirst.Api\Phan_Tich_Thiet_Ke_He_Thong_FlawFirst_Full.docx"

    doc_base = Document(base_path)
    doc_db = Document(db_path)

    # In doc_base, find where "KẾT LUẬN VÀ ĐÁNH GIÁ KIẾN TRÚC HỆ THỐNG" begins
    # We can append doc_db's content (from section 3.1.2) before Conclusion, or append at the end.
    # Actually, python-docx allows copying elements directly.
    
    # Let's inspect the sections in doc_db
    # We want to copy all body elements from doc_db (excluding cover page) into a new section in doc_base
    doc_out = Document(base_path)
    
    # Add page break
    doc_out.add_page_break()

    # Now we read and copy elements from doc_db
    # Skip the cover page elements in doc_db (first page break is around paragraph index 8)
    # Better: just copy all elements after the first page break in doc_db
    found_page_break = False
    
    # We can append elements from doc_db._body._element into doc_out._body._element before the last section
    # Or simply append to the end of doc_out:
    p_sep = doc_out.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(10)
    p_sep.paragraph_format.space_after = Pt(10)
    
    # Re-run build directly into doc_out or append
    # Let's import build_database_design_document and let it take an existing doc!
    print("Base and DB documents loaded.")

if __name__ == "__main__":
    merge_documents()
