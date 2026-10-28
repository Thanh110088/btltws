import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def build_database_design_document():
    doc = Document()

    # Configure Margins (Normal 1 inch = 72 pt = 1440 dxa)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Header / Footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("Tài liệu Thiết kế Cơ sở Dữ liệu & Biểu đồ ERD — FlawFirst Platform")
        r_hdr.font.name = "Times New Roman"
        r_hdr.font.size = Pt(9)
        r_hdr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
        
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_ftr = p_ftr.add_run("Bài tập lớn Lập trình Web Nâng Cao — Học kỳ II, Năm học 2025 – 2026")
        r_ftr.font.name = "Times New Roman"
        r_ftr.font.size = Pt(9)
        r_ftr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Palette
    COLOR_PRIMARY = RGBColor(0x0F, 0x17, 0x2A)     # Dark Slate
    COLOR_TITLE = RGBColor(0x1E, 0x3A, 0x8A)       # Navy
    COLOR_SUB = RGBColor(0x03, 0x69, 0xA1)         # Ocean
    COLOR_TEXT = RGBColor(0x1E, 0x29, 0x3B)        # Slate 800
    COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)       # Slate 500

    HEX_HEADER_BG = "1E3A8A"                       # Dark Navy
    HEX_SUBHEADER_BG = "0284C7"                    # Light Blue
    HEX_ZEBRA = "F8FAFC"                           # Soft Gray
    HEX_BORDER = "CBD5E1"                          # Slate Border

    FONT_FAMILY = "Times New Roman"

    def format_run(run, font_name=FONT_FAMILY, size_pt=12, bold=False, italic=False, color=COLOR_TEXT):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=6, line_spacing=1.25):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            format_run(r, FONT_FAMILY, 12, False, False, COLOR_TEXT)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        format_run(r, FONT_FAMILY, 15, True, False, COLOR_TITLE)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        format_run(r, FONT_FAMILY, 13.5, True, False, COLOR_TITLE)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        format_run(r, FONT_FAMILY, 12, True, False, COLOR_PRIMARY)
        return p

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
            node = OxmlElement(m)
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_table_title(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title_text)
        format_run(r, FONT_FAMILY, 11.5, True, False, COLOR_PRIMARY)
        return p

    def add_image_title(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(14)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title_text)
        format_run(r, FONT_FAMILY, 11, False, True, COLOR_PRIMARY)
        return p

    # ----------------------------------------------------
    # TRANG BÌA (COVER PAGE)
    # ----------------------------------------------------
    p_inst = add_p("BÀI TẬP LỚN LẬP TRÌNH WEB NÂNG CAO", WD_ALIGN_PARAGRAPH.CENTER, 40, 4)
    format_run(p_inst.runs[0], FONT_FAMILY, 13, True, False, COLOR_MUTED)

    p_sub = add_p("HỌC KỲ II — NĂM HỌC 2025 – 2026", WD_ALIGN_PARAGRAPH.CENTER, 2, 35)
    format_run(p_sub.runs[0], FONT_FAMILY, 11, False, False, COLOR_MUTED)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(30)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.3
    r_t1 = p_title.add_run("THIẾT KẾ HỆ THỐNG DỮ LIỆU\n")
    format_run(r_t1, FONT_FAMILY, 22, True, False, COLOR_TITLE)
    r_t2 = p_title.add_run("MÔ HÌNH HÓA THỰC THỂ & CƠ SỞ DỮ LIỆU FLAWFIRST\n(FLAWFIRST PLATFORM)")
    format_run(r_t2, FONT_FAMILY, 14.5, True, False, COLOR_SUB)

    p_div = add_p("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", WD_ALIGN_PARAGRAPH.CENTER, 10, 30)
    format_run(p_div.runs[0], FONT_FAMILY, 10, False, False, RGBColor(0x94, 0xA3, 0xB8))

    tbl_cov = doc.add_table(rows=6, cols=2)
    tbl_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cov.autofit = False
    set_table_borders(tbl_cov, color="E2E8F0", sz="4", val="none")

    cov_info = [
        ("Tên dự án:", "FlawFirst — Nền tảng Đánh giá Sản phẩm Bóc tách Ưu / Nhược điểm"),
        ("Kiến trúc công nghệ:", "ASP.NET Core 9.0 (MVC) + Entity Framework Core 9.0 + MS SQL Server"),
        ("Mô hình dữ liệu:", "11 Thực thể (Entities), Chuẩn hóa 3NF kết hợp Bán chuẩn hóa"),
        ("Cơ chế toàn vẹn:", "Foreign Keys, Unique Indexes, Check Constraints, Transaction Safety"),
        ("Nội dung tài liệu:", "1. Danh sách thực thể | 2. Mối quan hệ | 3. Sơ đồ ERD | 4. Đánh giá chuẩn hóa | 5. Từ điển dữ liệu 11 bảng"),
        ("Thời gian thực hiện:", "Tháng 10 / 2026")
    ]

    for idx, (lbl, val) in enumerate(cov_info):
        c0 = tbl_cov.cell(idx, 0)
        c1 = tbl_cov.cell(idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_margins(c0, 60, 60, 80, 80)
        set_cell_margins(c1, 60, 60, 80, 80)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lbl)
        format_run(r0, FONT_FAMILY, 11, True, False, COLOR_TITLE)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        format_run(r1, FONT_FAMILY, 11, False, False, COLOR_TEXT)

    doc.add_page_break()

    # ----------------------------------------------------
    # MỤC 3.1.2: PHÂN TÍCH HỆ THỐNG VỀ DỮ LIỆU
    # ----------------------------------------------------
    add_h1("3.1.2. Phân tích hệ thống về dữ liệu")

    # a. Xác định thực thể (Entity) và mối quan hệ
    add_h2("a. Xác định thực thể (Entity) và mối quan hệ")

    add_p(
        "Dựa trên các yêu cầu nghiệp vụ và các quy trình khảo sát thực tế của dự án FlawFirst, "
        "hệ thống được thiết kế gồm 11 thực thể (Entities). Các thực thể này được phân chia thành hai nhóm chính: "
        "nhóm thực thể nghiệp vụ cốt lõi (lưu trữ thông tin người dùng, sản phẩm công nghệ, bài viết đánh giá bóc tách ưu và nhược điểm, "
        "các tương tác xã hội như bình luận, bình chọn hữu ích, đánh dấu lưu bài, theo dõi tác giả, cùng phân hệ xử lý báo cáo vi phạm) "
        "và nhóm thực thể danh mục & phụ trợ (quản lý phân loại ngành hàng, lưu trữ hình ảnh minh chứng thực tế của bài đánh giá, "
        "hình ảnh bằng chứng tố cáo vi phạm). Các thực thể nghiệp vụ chính và các thực thể danh mục phụ trợ được mô tả chi tiết trong Bảng 3.10."
    )

    # ----------------------------------------------------
    # BẢNG 3.10: CÁC THỰC THỂ CỦA HỆ THỐNG
    # ----------------------------------------------------
    add_table_title("Bảng 3.10. Các thực thể của hệ thống")

    tbl_entities = doc.add_table(rows=12, cols=4)
    tbl_entities.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_entities.autofit = False
    set_table_borders(tbl_entities, color=HEX_BORDER, sz="4", val="single")

    ent_headers = ["STT", "Thực thể", "Nhóm", "Mô tả vai trò nghiệp vụ"]
    ent_widths = [Inches(0.6), Inches(1.6), Inches(1.4), Inches(2.9)]

    for c_idx, h_text in enumerate(ent_headers):
        cell = tbl_entities.cell(0, c_idx)
        cell.width = ent_widths[c_idx]
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        format_run(r, FONT_FAMILY, 10.5, True, False, RGBColor(0xFF, 0xFF, 0xFF))

    entities_data = [
        ("1", "User\n(Người dùng)", "Nghiệp vụ", "Tài khoản người dùng trong hệ thống: lưu trữ họ tên, email định danh (duy nhất), mật khẩu băm mã hóa BCrypt, vai trò phân quyền (Admin, User), trạng thái khóa tài khoản và thời điểm tạo."),
        ("2", "Category\n(Danh mục)", "Danh mục", "Phân loại ngành hàng của sản phẩm (ví dụ: Điện thoại, Laptop, Máy tính bảng, Tai nghe...): tên danh mục là duy nhất, kèm theo mô tả tóm tắt."),
        ("3", "Product\n(Sản phẩm)", "Nghiệp vụ", "Thông tin sản phẩm công nghệ cần được cộng đồng đánh giá: tên sản phẩm, thương hiệu sản xuất, mô tả cấu hình, mức giá niêm yết, đường dẫn ảnh đại diện và liên kết tới danh mục ngành hàng."),
        ("4", "Review\n(Đánh giá Flaw-First)", "Nghiệp vụ", "Thực thể trọng tâm mang tính đột phá của hệ thống: bắt buộc bóc tách rành mạch giữa Ưu điểm (Pros) và Nhược điểm thực tế (Cons), điểm xếp hạng (1–5 sao), cờ ẩn danh, cờ kiểm duyệt ẩn bài, bộ đếm Upvote/Downvote."),
        ("5", "ReviewImage\n(Ảnh đánh giá)", "Phụ trợ", "Lưu trữ danh sách hình ảnh thực tế do người đánh giá chụp và tải lên kèm theo bài review (tối đa 5 ảnh / bài), phục vụ minh chứng cho các điểm ưu/nhược điểm đã nêu."),
        ("6", "Comment\n(Bình luận)", "Nghiệp vụ", "Lưu trữ các phản hồi, trao đổi, thảo luận của cộng đồng dưới mỗi bài viết đánh giá; hỗ trợ tùy chọn bình luận ẩn danh để bảo vệ quyền riêng tư."),
        ("7", "ReviewVote\n(Bình chọn)", "Nghiệp vụ", "Ghi nhận lượt đánh giá chất lượng bài review: người dùng bình chọn 'Hữu ích' (Upvote) hoặc 'Không hữu ích' (Downvote); mỗi người dùng chỉ được vote duy nhất 1 lần trên 1 review."),
        ("8", "Bookmark\n(Lưu đánh giá)", "Nghiệp vụ", "Lưu trữ danh sách các bài đánh giá tâm đắc mà người dùng đánh dấu để xem lại trong thư viện cá nhân; tránh trùng lặp thông qua ràng buộc duy nhất (ReviewId, UserId)."),
        ("9", "UserFollow\n(Theo dõi)", "Nghiệp vụ", "Mạng lưới tương tác xã hội giữa các thành viên: ghi nhận quan hệ người theo dõi (Follower) và người được theo dõi (Following); ràng buộc không cho phép tự theo dõi chính mình."),
        ("10", "ReviewReport\n(Báo cáo vi phạm)", "Nghiệp vụ", "Quản lý quy trình kiểm duyệt nội dung: lưu trữ tố cáo từ người dùng về bài review vi phạm chính sách (Spam, xúc phạm, sai lệch), ảnh chụp nội dung tại thời điểm tố cáo, trạng thái và quyết định của Admin."),
        ("11", "ReportEvidence\n(Bằng chứng tố cáo)", "Phụ trợ", "Lưu trữ các hình ảnh chụp màn hình bằng chứng vi phạm do người tố cáo đính kèm khi gửi báo cáo vi phạm lên Quản trị viên.")
    ]

    for r_idx, row_vals in enumerate(entities_data):
        row_cells = tbl_entities.rows[r_idx + 1].cells
        bg_color = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row_cells[c_idx]
            cell.width = ent_widths[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            format_run(r, FONT_FAMILY, 10, (c_idx == 1), False, COLOR_TEXT)

    add_p("", space_after=4)

    # ----------------------------------------------------
    # BẢNG 3.11: CÁC MỐI QUAN HỆ GIỮA CÁC THỰC THỂ
    # ----------------------------------------------------
    add_p(
        "Các mối quan hệ giữa các thực thể trong cơ sở dữ liệu FlawFirst được tổng hợp trong Bảng 3.11 "
        "(ký hiệu 1 – N: một – nhiều; 1 – 1: một – một). Mỗi mối quan hệ đều được thiết lập chặt chẽ thông qua các "
        "khóa ngoại (Foreign Key) cùng các quy tắc hành vi toàn vẹn dữ liệu (Cascade, Restrict, SetNull) "
        "nhằm đảm bảo tính nhất quán tuyệt đối trong suốt vòng đời vận hành hệ thống."
    )

    add_table_title("Bảng 3.11. Các mối quan hệ giữa các thực thể")

    tbl_relations = doc.add_table(rows=17, cols=4)
    tbl_relations.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_relations.autofit = False
    set_table_borders(tbl_relations, color=HEX_BORDER, sz="4", val="single")

    rel_headers = ["Thực thể cha", "Bản số", "Thực thể con", "Ý nghĩa nghiệp vụ & Ràng buộc toàn vẹn"]
    rel_widths = [Inches(1.5), Inches(0.9), Inches(1.5), Inches(2.6)]

    for c_idx, h_text in enumerate(rel_headers):
        cell = tbl_relations.cell(0, c_idx)
        cell.width = rel_widths[c_idx]
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        format_run(r, FONT_FAMILY, 10.5, True, False, RGBColor(0xFF, 0xFF, 0xFF))

    relations_data = [
        ("Category", "1 – N", "Product", "Một danh mục chứa nhiều sản phẩm; mỗi sản phẩm thuộc đúng một danh mục. Ràng buộc Restrict (không được xóa danh mục khi còn sản phẩm trực thuộc)."),
        ("Product", "1 – N", "Review", "Một sản phẩm có nhiều bài đánh giá từ cộng đồng; mỗi bài đánh giá chỉ dành cho một sản phẩm. Ràng buộc Restrict; Unique Index (ProductId, UserId) đảm bảo 1 người chỉ review 1 lần."),
        ("User", "1 – N", "Review", "Một người dùng có thể viết nhiều bài review cho các sản phẩm khác nhau; mỗi bài review do đúng một người dùng tạo. Ràng buộc Restrict."),
        ("Review", "1 – N", "ReviewImage", "Một bài review có thể đính kèm nhiều hình ảnh minh chứng thực tế (0–5 ảnh); mỗi ảnh thuộc về đúng một bài review. Ràng buộc Cascade Delete (xóa review thì ảnh tự động bị xóa)."),
        ("Review", "1 – N", "Comment", "Một bài review có nhiều bình luận thảo luận; mỗi bình luận thuộc về một bài review. Ràng buộc Cascade Delete."),
        ("User", "1 – N", "Comment", "Một người dùng có thể đăng nhiều bình luận; mỗi bình luận do đúng một người dùng thực hiện. Ràng buộc Restrict."),
        ("Review", "1 – N", "ReviewVote", "Một bài review nhận nhiều lượt bình chọn; mỗi lượt bình chọn ghi nhận cho một review. Ràng buộc Cascade Delete; Unique Index (ReviewId, UserId) ngăn vote nhiều lần."),
        ("User", "1 – N", "ReviewVote", "Một người dùng có thể vote cho nhiều bài review khác nhau; mỗi lượt vote do một người dùng thực hiện. Ràng buộc Restrict."),
        ("Review", "1 – N", "Bookmark", "Một bài review có thể được nhiều người dùng đánh dấu lưu lại; mỗi bản ghi bookmark trỏ đến một review. Ràng buộc Cascade Delete."),
        ("User", "1 – N", "Bookmark", "Một người dùng có thể lưu nhiều bài review vào bộ sưu tập cá nhân. Ràng buộc Restrict; Unique Index (ReviewId, UserId) tránh lưu trùng lặp."),
        ("User", "1 – N", "UserFollow (Follower)", "Một người dùng có thể theo dõi nhiều tác giả khác nhau (danh sách Following). Ràng buộc Restrict; CHECK FollowerId <> FollowingId (không được tự theo dõi chính mình)."),
        ("User", "1 – N", "UserFollow (Following)", "Một người dùng có thể được theo dõi bởi nhiều người khác (danh sách Followers). Ràng buộc Restrict; Unique Index (FollowerId, FollowingId)."),
        ("Review", "1 – N", "ReviewReport", "Một bài review có thể nhận nhiều lượt báo cáo vi phạm; mỗi báo cáo gắn liền với một review. Ràng buộc SetNull (khi bài review bị xóa vĩnh viễn, ReviewId đổi thành NULL để lưu lại lịch sử xử lý của Admin)."),
        ("User", "1 – N", "ReviewReport (Reporter)", "Một người dùng có thể gửi nhiều báo cáo vi phạm cho các bài review vi phạm chính sách; mỗi báo cáo ghi nhận người tố cáo. Ràng buộc Restrict."),
        ("User", "1 – N", "ReviewReport (ResolvedAdmin)", "Một Quản trị viên (Admin) có thể thụ lý và xử lý nhiều báo cáo vi phạm; báo cáo đã giải quyết ghi nhận Admin phụ trách. Ràng buộc Restrict."),
        ("ReviewReport", "1 – N", "ReportEvidence", "Một báo cáo vi phạm có thể đính kèm nhiều hình ảnh chụp màn hình làm bằng chứng; mỗi ảnh bằng chứng thuộc về một báo cáo. Ràng buộc Cascade Delete.")
    ]

    for r_idx, row_vals in enumerate(relations_data):
        row_cells = tbl_relations.rows[r_idx + 1].cells
        bg_color = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row_cells[c_idx]
            cell.width = rel_widths[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            is_bold = (c_idx in [0, 2])
            format_run(r, FONT_FAMILY, 9.5, is_bold, False, COLOR_TEXT)

    doc.add_page_break()

    # ----------------------------------------------------
    # MỤC b: BIỂU ĐỒ QUAN HỆ THỰC THỂ (ERD)
    # ----------------------------------------------------
    add_h2("b. Biểu đồ quan hệ thực thể — ERD (mô tả quan hệ)")

    add_p(
        "Sơ đồ ERD thể hiện mối liên kết logic giữa các thực thể, đảm bảo tính toàn vẹn dữ liệu, "
        "phản ánh chính xác luồng nghiệp vụ đánh giá Flaw-First và được chuẩn hóa ở mức 3NF (Third Normal Form). "
        "Trong biểu đồ, thực thể Review đóng vai trò là thực thể trung tâm của toàn bộ hệ thống, kết nối trực tiếp "
        "với Sản phẩm (Product), Người đánh giá (User), đồng thời phân nhánh tới toàn bộ các tương tác xoay quanh bài viết "
        "như Hình ảnh minh chứng (ReviewImage), Bình luận (Comment), Bình chọn hữu ích (ReviewVote), Đánh dấu lưu bài (Bookmark) "
        "và Phân hệ kiểm duyệt tố cáo vi phạm (ReviewReport, ReportEvidence)."
    )

    # Chèn ảnh ERD vào tài liệu
    erd_img_path = r"g:\BTLWNC\FlawFirst.Api\erd_flawfirst.png"
    if os.path.exists(erd_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(erd_img_path, width=Inches(6.5))

    add_image_title("Hình 3.2. Biểu đồ quan hệ thực thể (ERD) của hệ thống FlawFirst")

    add_p(
        "Diễn giải luồng liên kết và kiến trúc thực thể trên biểu đồ ERD:\n"
        "1. Phân cấp Danh mục — Sản phẩm: Thực thể Category liên kết 1 – N với Product thông qua khóa ngoại CategoryId. "
        "Quy tắc Restrict ngăn chặn xóa danh mục khi vẫn còn sản phẩm đang lưu hành.\n"
        "2. Điểm hội tụ Đánh giá (Review Hub): Mỗi bài Review là giao điểm giữa Product (sản phẩm được đánh giá) và User (người viết bài). "
        "Ràng buộc Unique Index trên cặp (ProductId, UserId) đảm bảo tính minh bạch: một tài khoản chỉ được để lại 01 bài đánh giá duy nhất cho 01 sản phẩm.\n"
        "3. Tương tác đa chiều xoay quanh Review: Các thực thể vệ tinh ReviewImage, Comment, ReviewVote, Bookmark đều liên kết 1 – N "
        "với Review theo cơ chế Cascade Delete. Khi một bài đánh giá bị xóa, tất cả ảnh, bình luận, vote và bookmark tương ứng sẽ tự động được dọn sạch.\n"
        "4. Mạng xã hội theo dõi (Social Network Graph): Thực thể UserFollow đại diện cho quan hệ tự thân (Self-Referencing Many-to-Many) "
        "của User, tách biệt giữa FollowerId và FollowingId kèm ràng buộc kiểm tra ngăn chặn người dùng tự theo dõi chính mình.\n"
        "5. Phân hệ Báo cáo & Kiểm duyệt (Moderation Pipeline): ReviewReport liên kết tới Review (OnDelete: SetNull), Reporter (Người tố cáo) "
        "và ResolvedByAdmin (Admin xử lý). Khi bài viết bị xóa khỏi hệ thống, báo cáo vẫn được giữ lại với ReviewId = NULL kèm ReviewSnapshot "
        "để phục vụ việc tra soát kiểm toán (Audit Trail)."
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # MỤC c: ĐÁNH GIÁ MỨC ĐỘ CHUẨN HÓA DỮ LIỆU
    # ----------------------------------------------------
    add_h2("c. Đánh giá mức độ chuẩn hóa dữ liệu của hệ thống")

    add_p(
        "Cơ sở dữ liệu của hệ thống FlawFirst được thiết kế tuân thủ nghiêm ngặt các quy tắc lý thuyết cơ sở dữ liệu quan hệ, "
        "đạt mức độ chuẩn hóa Dạng chuẩn 3 (3NF — Third Normal Form), đồng thời áp dụng kỹ thuật Bán chuẩn hóa có kiểm soát "
        "(Controlled Denormalization) tại các điểm nghẽn hiệu năng trọng yếu nhằm tối ưu hóa tốc độ tải trang trong môi trường thực tế."
    )

    add_h3("1. Đánh giá Dạng chuẩn 1 (1NF — First Normal Form)")
    add_p(
        "• Định nghĩa: Một lược đồ quan hệ đạt 1NF nếu và chỉ nếu toàn bộ các thuộc tính đều chứa giá trị nguyên tố (Atomic Value), "
        "không chứa các nhóm lặp (Repeating Groups) hoặc mảng giá trị đa trị (Multi-valued Attributes).\n"
        "• Hiện thực trong FlawFirst:\n"
        "   + Không có bất kỳ cột nào lưu trữ dữ liệu dạng mảng JSON thô hoặc chuỗi ngăn cách bởi dấu phẩy. "
        "Ví dụ: Danh sách ảnh minh chứng của bài review không lưu dưới dạng 'anh1.jpg,anh2.jpg' trong bảng Reviews, "
        "mà được tách riêng thành thực thể ReviewImages với quan hệ 1 – N.\n"
        "   + Tương tự, danh sách ảnh bằng chứng vi phạm được tách thành thực thể ReportEvidences riêng biệt.\n"
        "   + Mọi bảng đều có khóa chính định danh duy nhất (Surrogate Key Id) với kiểu số nguyên tự tăng (INT IDENTITY).\n"
        "• Kết luận: Hệ thống thỏa mãn 100% chuẩn 1NF."
    )

    add_h3("2. Đánh giá Dạng chuẩn 2 (2NF — Second Normal Form)")
    add_p(
        "• Định nghĩa: Một lược đồ quan hệ đạt 2NF nếu đã đạt 1NF và không tồn tại bất kỳ thuộc tính không khóa nào phụ thuộc hàm "
        "từng phần vào một phần của khóa chính (Partial Functional Dependency).\n"
        "• Hiện thực trong FlawFirst:\n"
        "   + Tất cả 11 bảng trong hệ thống đều sử dụng khóa chính đơn tính chất đại diện (Single-column Surrogate Key: Id). "
        "Do khóa chính chỉ bao gồm duy nhất 01 thuộc tính số nguyên, về mặt toán học và lý thuyết quan hệ, không thể tồn tại "
        "bất kỳ tập con thực sự nào của khóa chính.\n"
        "   + Mọi thuộc tính không khóa trong mỗi bảng đều phụ thuộc hàm đầy đủ (Full Functional Dependency) vào thuộc tính Id đại diện.\n"
        "   + Các cặp thuộc tính mang tính chất định danh tự nhiên (Natural Keys) như (ProductId, UserId) trong Reviews, "
        "(ReviewId, UserId) trong ReviewVotes/Bookmarks, hay (FollowerId, FollowingId) trong UserFollows được bảo vệ "
        "thông qua chỉ mục duy nhất (Unique Index), đảm bảo tính toàn vẹn nghiệp vụ mà không phá vỡ cấu trúc 2NF.\n"
        "• Kết luận: Hệ thống thỏa mãn 100% chuẩn 2NF."
    )

    add_h3("3. Đánh giá Dạng chuẩn 3 (3NF — Third Normal Form)")
    add_p(
        "• Định nghĩa: Một lược đồ quan hệ đạt 3NF nếu đã đạt 2NF và không tồn tại bất kỳ thuộc tính không khóa nào phụ thuộc bắc cầu "
        "(Transitive Dependency) vào khóa chính (nghĩa là không có phụ thuộc hàm dạng X → Y với Y là thuộc tính không khóa và X không phải là siêu khóa).\n"
        "• Hiện thực trong FlawFirst:\n"
        "   + Bảng Products chỉ lưu CategoryId trỏ sang Categories, hoàn toàn không lưu dư thừa tên danh mục hay mô tả danh mục.\n"
        "   + Bảng Reviews chỉ lưu ProductId và UserId, không lưu dư thừa tên sản phẩm, giá hay họ tên người đánh giá. Muốn hiển thị thông tin sản phẩm hoặc tác giả, hệ thống thực hiện phép kết (JOIN) thông qua Entity Framework Core Navigation Properties.\n"
        "   + Bảng Comments chỉ lưu ReviewId và UserId, không lưu thông tin bài viết hay thông tin tài khoản.\n"
        "   + Bảng ReviewReports chỉ lưu ReporterId và ResolvedByAdminId trỏ sang Users, không trùng lặp bất kỳ thuộc tính cá nhân nào của người dùng.\n"
        "• Kết luận: Cơ sở dữ liệu thỏa mãn kiến trúc chuẩn mực 3NF."
    )

    add_h3("4. Phân tích Kỹ thuật Bán chuẩn hóa có kiểm soát (Controlled Denormalization)")
    add_p(
        "Trong thực tế triển khai các nền tảng Web có lượng tương tác cao, việc tuân thủ 3NF tuyệt đối đôi khi dẫn đến hiện tượng suy giảm hiệu năng "
        "(Performance Bottleneck) do phải thực hiện quá nhiều phép tính tổng hợp (Aggregate Functions) trên các bảng có dữ liệu lớn. "
        "FlawFirst đã áp dụng kỹ thuật Bán chuẩn hóa có chủ đích tại 2 vị trí quan trọng:\n\n"
        "1. Lưu trữ thuộc tính UpvoteCount và DownvoteCount trong bảng Reviews:\n"
        "   • Về mặt lý thuyết 3NF: Điểm vote có thể được tính toán bất kỳ lúc nào bằng câu lệnh COUNT(*) từ bảng ReviewVotes "
        "với điều kiện IsUpvote = 1 hoặc 0.\n"
        "   • Thách thức thực tế: Một trang chi tiết sản phẩm có thể nạp từ 20 đến 50 bài review cùng lúc. Nếu mỗi bài review đều phải "
        "thực hiện 2 truy vấn COUNT(*) trên bảng ReviewVotes (có thể chứa hàng chục nghìn bản ghi), tổng số phép quét bảng sẽ gây nghẽn I/O nghiêm trọng.\n"
        "   • Giải pháp của FlawFirst: Lưu sẵn UpvoteCount và DownvoteCount ngay trên dòng dữ liệu Review. Khi người dùng bấm vote, "
        "ReviewService thực hiện cập nhật đồng thời bản ghi ReviewVote và tăng/giảm trường đếm của Review trong cùng một Database Transaction. "
        "Kỹ thuật này giúp việc đọc trang đạt độ phức tạp tức thì O(1) mà vẫn đảm bảo tính toàn vẹn dữ liệu.\n\n"
        "2. Lưu trữ thuộc tính ReviewSnapshot trong bảng ReviewReports:\n"
        "   • Khi người dùng gửi tố cáo một bài viết, hệ thống sao chép trích đoạn nội dung đánh giá vào trường ReviewSnapshot.\n"
        "   • Mục đích: Bảo toàn bằng chứng gốc ngay cả khi tác giả bài viết cố tình sửa đổi nội dung sau đó để che giấu hành vi vi phạm, "
        "hoặc bài viết bị xóa vĩnh viễn (khiến ReviewId bị SET NULL) thì Quản trị viên vẫn có đầy đủ thông tin để kiểm toán lịch sử xử lý vi phạm."
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # MỤC d: TỪ ĐIỂN DỮ LIỆU CỦA CÁC BẢNG (DATA DICTIONARY)
    # ----------------------------------------------------
    add_h2("d. Từ điển dữ liệu của các bảng (Data Dictionary)")

    add_p(
        "Từ điển dữ liệu (Data Dictionary) mô tả chi tiết cấu trúc lưu trữ vật lý của toàn bộ 11 bảng trong cơ sở dữ liệu FlawFirst. "
        "Mỗi bảng từ điển dữ liệu cung cấp đầy đủ thông tin: Thứ tự thuộc tính (STT), Tên trường (Column Name), "
        "Kiểu dữ liệu trong hệ quản trị cơ sở dữ liệu SQL Server (Data Type) kèm ánh xạ trong C#, Phân loại khóa (PK / FK), "
        "Khả năng chấp nhận giá trị Null (Allow Null), Giá trị mặc định hoặc các ràng buộc toàn vẹn dữ liệu (Constraints), "
        "và Diễn giải ý nghĩa nghiệp vụ cụ thể của trường."
    )

    # Helper function to create data dictionary table
    def render_data_dict_table(table_num, table_name, table_desc, columns_data):
        add_table_title(f"Bảng {table_num}. Từ điển dữ liệu bảng {table_name}")
        add_p(f"• Mục đích lưu trữ: {table_desc}", space_before=1, space_after=4)

        tbl = doc.add_table(rows=len(columns_data) + 1, cols=7)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        set_table_borders(tbl, color=HEX_BORDER, sz="4", val="single")

        dict_headers = ["STT", "Tên trường", "Kiểu dữ liệu", "Khóa", "Null", "Ràng buộc / Mặc định", "Diễn giải ý nghĩa"]
        dict_widths = [Inches(0.45), Inches(1.2), Inches(1.2), Inches(0.6), Inches(0.55), Inches(1.3), Inches(1.5)]

        for c_idx, h_text in enumerate(dict_headers):
            cell = tbl.cell(0, c_idx)
            cell.width = dict_widths[c_idx]
            set_cell_background(cell, HEX_HEADER_BG)
            set_cell_margins(cell, 80, 80, 90, 90)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(h_text)
            format_run(r, FONT_FAMILY, 9.5, True, False, RGBColor(0xFF, 0xFF, 0xFF))

        for r_idx, row_vals in enumerate(columns_data):
            row_cells = tbl.rows[r_idx + 1].cells
            bg_color = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_vals):
                cell = row_cells[c_idx]
                cell.width = dict_widths[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, 70, 70, 80, 80)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                is_bold = (c_idx == 1 or "PK" in val)
                text_color = RGBColor(0x1E, 0x40, 0xAF) if "PK" in val else (RGBColor(0x9A, 0x34, 0x12) if "FK" in val else COLOR_TEXT)
                format_run(r, FONT_FAMILY, 9, is_bold, False, text_color)

        add_p("", space_after=6)

    # 1. Bảng Users
    render_data_dict_table(
        "3.12", "Users",
        "Lưu trữ danh sách tài khoản định danh người dùng trong hệ thống FlawFirst, phân quyền truy cập và kiểm soát trạng thái khóa.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng, định danh duy nhất mỗi người dùng."),
            ("2", "FullName", "nvarchar(150) (string)", "-", "No", "Not Empty", "Họ và tên đầy đủ hiển thị trên hệ thống."),
            ("3", "Email", "nvarchar(256) (string)", "-", "No", "UNIQUE INDEX", "Địa chỉ email duy nhất, dùng làm tên đăng nhập."),
            ("4", "PasswordHash", "nvarchar(200) (string)", "-", "No", "BCrypt Hashed", "Chuỗi mật khẩu đã được băm an toàn bằng thuật toán BCrypt."),
            ("5", "Role", "nvarchar(20) (string)", "-", "No", "CHECK in ('Admin','User')", "Vai trò tài khoản: 'Admin' (Quản trị viên) hoặc 'User' (Thành viên)."),
            ("6", "IsLocked", "bit (bool)", "-", "No", "Default 0 (false)", "Trạng thái khóa tài khoản: 1 = Bị khóa bởi Admin, 0 = Đang hoạt động."),
            ("7", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm tạo tài khoản trên hệ thống.")
        ]
    )

    # 2. Bảng Categories
    render_data_dict_table(
        "3.13", "Categories",
        "Quản lý danh mục ngành hàng sản phẩm, phục vụ phân loại và lọc sản phẩm trên giao diện khám phá.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng, định danh danh mục."),
            ("2", "Name", "nvarchar(120) (string)", "-", "No", "UNIQUE INDEX", "Tên danh mục ngành hàng (ví dụ: Điện thoại, Laptop...)."),
            ("3", "Description", "nvarchar(500) (string)", "-", "Yes", "Null", "Mô tả ngắn gọn về đặc trưng ngành hàng."),
            ("4", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm khởi tạo danh mục.")
        ]
    )

    # 3. Bảng Products
    render_data_dict_table(
        "3.14", "Products",
        "Lưu trữ thông tin chi tiết về sản phẩm công nghệ cần được cộng đồng đánh giá và bóc tách lỗi.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng, định danh sản phẩm."),
            ("2", "Name", "nvarchar(200) (string)", "-", "No", "Not Empty", "Tên thương mại đầy đủ của sản phẩm."),
            ("3", "Brand", "nvarchar(120) (string)", "-", "No", "Not Empty", "Thương hiệu sản xuất (Apple, Samsung, Dell...)."),
            ("4", "Description", "nvarchar(4000) (string)", "-", "Yes", "Null", "Mô tả chi tiết cấu hình, thông số kỹ thuật sản phẩm."),
            ("5", "Price", "decimal(18,2) (decimal)", "-", "No", "INDEX (Giá tiền)", "Giá bán niêm yết tham khảo tính theo VNĐ."),
            ("6", "ImageUrl", "nvarchar(500) (string)", "-", "Yes", "Null", "Đường dẫn URL ảnh minh họa đại diện của sản phẩm."),
            ("7", "CategoryId", "int (int)", "FK", "No", "FK -> Categories(Id), Restrict", "Mã danh mục ngành hàng mà sản phẩm trực thuộc."),
            ("8", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm thêm sản phẩm vào hệ thống.")
        ]
    )

    # 4. Bảng Reviews
    render_data_dict_table(
        "3.15", "Reviews",
        "Thực thể trung tâm lưu trữ bài đánh giá bóc tách ưu và nhược điểm (Flaw-First Review), điểm số và các cờ kiểm duyệt.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng, định danh bài đánh giá."),
            ("2", "ProductId", "int (int)", "FK", "No", "FK -> Products(Id), Restrict", "Mã sản phẩm được đánh giá."),
            ("3", "UserId", "int (int)", "FK", "No", "FK -> Users(Id), Restrict", "Mã người dùng viết bài đánh giá."),
            ("4", "Pros", "nvarchar(4000) (string)", "-", "No", "Not Empty", "Nội dung các điểm hài lòng, ưu điểm thực tế."),
            ("5", "Cons", "nvarchar(4000) (string)", "-", "No", "Not Empty", "Nội dung các nhược điểm, hạn chế cốt lõi (Flaw-First)."),
            ("6", "Rating", "int (int)", "-", "No", "CHECK [Rating] 1..5", "Số sao đánh giá tổng quan (từ 1 đến 5 sao)."),
            ("7", "IsAnonymous", "bit (bool)", "-", "No", "Default 0 (false)", "Tùy chọn hiển thị ẩn danh tên tác giả với cộng đồng."),
            ("8", "IsHidden", "bit (bool)", "-", "No", "Default 0 (false)", "Cờ ẩn bài viết khỏi trang công khai bởi Admin."),
            ("9", "UpvoteCount", "int (int)", "-", "No", "Default 0 (Denormalized)", "Tổng số lượt bình chọn Hữu ích."),
            ("10", "DownvoteCount", "int (int)", "-", "No", "Default 0 (Denormalized)", "Tổng số lượt bình chọn Không hữu ích."),
            ("11", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm đăng bài đánh giá."),
            ("12", "UpdatedAt", "datetime2 (DateTime)", "-", "Yes", "Null", "Thời điểm cập nhật chỉnh sửa bài review lần cuối.")
        ]
    )

    # 5. Bảng ReviewImages
    render_data_dict_table(
        "3.16", "ReviewImages",
        "Lưu trữ đường dẫn các tệp ảnh thực tế đính kèm trong bài review do người dùng tải lên để làm minh chứng.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng của bản ghi hình ảnh."),
            ("2", "ReviewId", "int (int)", "FK", "No", "FK -> Reviews(Id), Cascade", "Mã bài review sở hữu hình ảnh minh chứng."),
            ("3", "ImageUrl", "nvarchar(500) (string)", "-", "No", "URL format", "Đường dẫn tệp ảnh lưu trữ trên máy chủ (/uploads/reviews/...).")
        ]
    )

    # 6. Bảng Comments
    render_data_dict_table(
        "3.17", "Comments",
        "Lưu trữ bình luận, trao đổi, hỏi đáp giữa các thành viên cộng đồng dưới mỗi bài viết đánh giá.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng của bình luận."),
            ("2", "ReviewId", "int (int)", "FK", "No", "FK -> Reviews(Id), Cascade", "Mã bài review được bình luận."),
            ("3", "UserId", "int (int)", "FK", "No", "FK -> Users(Id), Restrict", "Mã người dùng gửi bình luận."),
            ("4", "Content", "nvarchar(2000) (string)", "-", "No", "Not Empty", "Nội dung văn bản trao đổi của bình luận."),
            ("5", "IsAnonymous", "bit (bool)", "-", "No", "Default 0 (false)", "Tùy chọn ẩn danh tác giả bình luận."),
            ("6", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm gửi bình luận lên hệ thống.")
        ]
    )

    # 7. Bảng ReviewVotes
    render_data_dict_table(
        "3.18", "ReviewVotes",
        "Ghi nhận tương tác bình chọn hữu ích (Upvote) hoặc không hữu ích (Downvote) của từng người dùng trên mỗi bài review.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng của lượt bình chọn."),
            ("2", "ReviewId", "int (int)", "FK", "No", "FK -> Reviews(Id), Cascade", "Mã bài review nhận lượt bình chọn."),
            ("3", "UserId", "int (int)", "FK", "No", "FK -> Users(Id), Restrict", "Mã người dùng thực hiện bình chọn."),
            ("4", "IsUpvote", "bit (bool)", "-", "No", "1: Upvote, 0: Downvote", "Loại bình chọn: True = Hữu ích, False = Không hữu ích."),
            ("5", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm thực hiện hành động vote.")
        ]
    )

    # 8. Bảng Bookmarks
    render_data_dict_table(
        "3.19", "Bookmarks",
        "Lưu trữ danh sách bài viết đánh giá mà người dùng đánh dấu để lưu trữ và xem lại trong bộ sưu tập cá nhân.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng của bản ghi lưu bài."),
            ("2", "ReviewId", "int (int)", "FK", "No", "FK -> Reviews(Id), Cascade", "Mã bài review được đánh dấu lưu."),
            ("3", "UserId", "int (int)", "FK", "No", "FK -> Users(Id), Restrict", "Mã người dùng thực hiện lưu bài."),
            ("4", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm thực hiện đánh dấu lưu bài.")
        ]
    )

    # 9. Bảng UserFollows
    render_data_dict_table(
        "3.20", "UserFollows",
        "Mô hình hóa quan hệ theo dõi tác giả (Follower / Following) giữa các thành viên trên mạng xã hội FlawFirst.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng của quan hệ theo dõi."),
            ("2", "FollowerId", "int (int)", "FK", "No", "FK -> Users(Id), Restrict", "Mã người dùng nhấn theo dõi (Người theo dõi)."),
            ("3", "FollowingId", "int (int)", "FK", "No", "FK -> Users(Id), Restrict", "Mã người dùng được theo dõi (Tác giả được follow)."),
            ("4", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm bắt đầu mối quan hệ theo dõi.")
        ]
    )

    # 10. Bảng ReviewReports
    render_data_dict_table(
        "3.21", "ReviewReports",
        "Lưu trữ các báo cáo vi phạm nội dung từ cộng đồng, snapshot bài viết và quyết định xử lý kiểm duyệt của Quản trị viên.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng của báo cáo vi phạm."),
            ("2", "ReviewId", "int (int)", "FK", "Yes", "FK -> Reviews(Id), SetNull", "Mã bài review bị báo cáo (chuyển NULL nếu review bị xóa)."),
            ("3", "ReporterId", "int (int)", "FK", "No", "FK -> Users(Id), Restrict", "Mã người dùng gửi báo cáo vi phạm."),
            ("4", "Reason", "nvarchar(2000) (string)", "-", "No", "Not Empty", "Lý do và mô tả chi tiết hành vi vi phạm."),
            ("5", "ReviewSnapshot", "nvarchar(1000) (string)", "-", "Yes", "Null", "Trích đoạn nội dung review tại thời điểm báo cáo vi phạm."),
            ("6", "Status", "nvarchar(20) (string)", "-", "No", "CHECK in ('Pending','Resolved','Dismissed')", "Trạng thái báo cáo: Chờ xử lý, Đã giải quyết, hoặc Bị bác bỏ."),
            ("7", "Action", "nvarchar(20) (string)", "-", "Yes", "Null", "Hành động xử lý của Admin ('Hide', 'Delete', 'Ban', 'Dismiss')."),
            ("8", "ResolvedByAdminId", "int (int)", "FK", "Yes", "FK -> Users(Id), Restrict", "Mã Quản trị viên đã thụ lý và giải quyết báo cáo."),
            ("9", "CreatedAt", "datetime2 (DateTime)", "-", "No", "Default UTC Now", "Thời điểm gửi báo cáo vi phạm."),
            ("10", "ResolvedAt", "datetime2 (DateTime)", "-", "Yes", "Null", "Thời điểm Admin hoàn tất xử lý báo cáo.")
        ]
    )

    # 11. Bảng ReportEvidences
    render_data_dict_table(
        "3.22", "ReportEvidences",
        "Lưu trữ các hình ảnh chụp màn hình làm bằng chứng vi phạm do người tố cáo tải lên đính kèm báo cáo.",
        [
            ("1", "Id", "int (int)", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng của bằng chứng ảnh."),
            ("2", "ReportId", "int (int)", "FK", "No", "FK -> ReviewReports(Id), Cascade", "Mã báo cáo vi phạm mà hình ảnh thuộc về."),
            ("3", "ImageUrl", "nvarchar(500) (string)", "-", "No", "URL format", "Đường dẫn tệp ảnh bằng chứng trên máy chủ (/uploads/evidences/...).")
        ]
    )

    # ----------------------------------------------------
    # TỔNG KẾT VÀ ĐÁNH GIÁ THIẾT KẾ DỮ LIỆU
    # ----------------------------------------------------
    add_h1("TỔNG KẾT VÀ ĐÁNH GIÁ THIẾT KẾ HỆ THỐNG DỮ LIỆU")
    add_p(
        "Mô hình dữ liệu của FlawFirst được xây dựng bài bản, khoa học và chặt chẽ, "
        "đáp ứng hoàn hảo cả về mặt lý thuyết cơ sở dữ liệu lẫn yêu cầu vận hành thực tiễn của một nền tảng Web hiện đại:\n\n"
        "1. Tính toàn vẹn và an toàn dữ liệu cao: Sử dụng hệ thống khóa ngoại chuẩn mực, các ràng buộc duy nhất (Unique Index), "
        "ràng buộc miền giá trị (Check Constraints) và cơ chế Cascade/Restrict/SetNull phù hợp cho từng nghiệp vụ đặc thù, "
        "ngăn chặn tuyệt đối hiện tượng dữ liệu mồ côi (Orphaned Records) hoặc trùng lặp tương tác (vote/bookmark/review trùng).\n\n"
        "2. Cân bằng hoàn hảo giữa Chuẩn hóa 3NF và Hiệu năng truy vấn O(1): Kiến trúc dữ liệu đảm bảo 3NF không dư thừa dữ liệu "
        "ở các quan hệ nghiệp vụ, đồng thời áp dụng Denormalization có kiểm soát tại các điểm truy vấn đọc thường xuyên "
        "(UpvoteCount, DownvoteCount), kết hợp chỉ mục tổng hợp (ProductId, IsHidden, Rating) giúp hệ thống phản hồi tức thì "
        "ngay cả khi số lượng đánh giá tăng lên hàng triệu bản ghi.\n\n"
        "3. Khả năng mở rộng và kiểm toán mạnh mẽ: Bảng ReviewReports kết hợp ReportEvidences và ReviewSnapshot mang lại "
        "khả năng truy vết kiểm toán (Audit Trail) tuyệt vời, hỗ trợ đội ngũ Quản trị viên kiểm duyệt nội dung công bằng, "
        "minh bạch và bảo vệ uy tín nền tảng FlawFirst."
    )

    out_name = "Thiet_Ke_He_Thong_Du_Lieu_FlawFirst.docx"
    out_path = os.path.join(r"g:\BTLWNC\FlawFirst.Api", out_name)
    doc.save(out_path)
    print("Database design document successfully generated at:", out_path)

if __name__ == "__main__":
    build_database_design_document()
