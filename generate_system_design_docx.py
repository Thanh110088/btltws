import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
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
        r_hdr = p_hdr.add_run("Tài liệu Phân tích & Thiết kế Hệ thống — Nền tảng FlawFirst")
        r_hdr.font.name = "Arial"
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
        
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_ftr = p_ftr.add_run("Học phần: Bài tập lớn Lập trình Web Nâng Cao — ASP.NET Core 9.0 MVC")
        r_ftr.font.name = "Arial"
        r_ftr.font.size = Pt(8.5)
        r_ftr.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # Style Helpers
    COLOR_PRIMARY = RGBColor(0x1E, 0x3A, 0x8A)      # Deep Navy
    COLOR_SECONDARY = RGBColor(0x02, 0x84, 0xC7)    # Light Blue / Sky
    COLOR_DARK = RGBColor(0x0F, 0x17, 0x2A)         # Slate Dark
    COLOR_MUTED = RGBColor(0x47, 0x55, 0x69)        # Slate Muted
    HEX_HEADER_BG = "1E3A8A"                        # Dark Navy Hex
    HEX_SUBHEADER_BG = "0284C7"                     # Light Blue Hex
    HEX_ZEBRA = "F8FAFC"                            # Light Gray/Slate
    HEX_BORDER = "CBD5E1"                           # Slate 300

    def format_run(run, font_name="Arial", size_pt=11, bold=False, italic=False, color=COLOR_DARK):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=6, line_spacing=1.18):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            format_run(r, "Arial", 11, False, False, COLOR_DARK)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        format_run(r, "Arial", 16, True, False, COLOR_PRIMARY)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        format_run(r, "Arial", 13.5, True, False, COLOR_SECONDARY)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        format_run(r, "Arial", 11.5, True, False, COLOR_DARK)
        return p

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
            node = OxmlElement(m)
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="none"/>'
            f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:right w:val="none"/>'
            f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def make_callout(text, title=None, border_color="2563EB", bg_color="F1F5F9"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:top w:val="none"/>'
            f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
            f'  <w:bottom w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if title:
            run_title = p.add_run(f"📌 {title}\n")
            format_run(run_title, "Arial", 10.5, True, False, COLOR_PRIMARY)
            
        run_text = p.add_run(text)
        format_run(run_text, "Arial", 10, False, True, COLOR_DARK)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    p_cov_inst = add_p("BÀI TẬP LỚN LẬP TRÌNH WEB NÂNG CAO", WD_ALIGN_PARAGRAPH.CENTER, 40, 4)
    format_run(p_cov_inst.runs[0], "Arial", 13, True, False, COLOR_MUTED)

    p_cov_sub = add_p("HỌC KỲ II — NĂM HỌC 2025 – 2026", WD_ALIGN_PARAGRAPH.CENTER, 2, 30)
    format_run(p_cov_sub.runs[0], "Arial", 11, False, False, COLOR_MUTED)

    # Title Line
    p_cov_title = doc.add_paragraph()
    p_cov_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_title.paragraph_format.space_before = Pt(30)
    p_cov_title.paragraph_format.space_after = Pt(12)
    p_cov_title.paragraph_format.line_spacing = 1.25
    r_title = p_cov_title.add_run("TÀI LIỆU PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG\n")
    format_run(r_title, "Arial", 22, True, False, COLOR_PRIMARY)

    r_title_sub = p_cov_title.add_run("NỀN TẢNG ĐÁNH GIÁ SẢN PHẨM BÓC TÁCH ƯU VÀ NHƯỢC ĐIỂM\n(FLAWFIRST PLATFORM)")
    format_run(r_title_sub, "Arial", 15, True, False, COLOR_SECONDARY)

    p_cov_divider = add_p("═══════════════════════════════════════", WD_ALIGN_PARAGRAPH.CENTER, 8, 30)
    format_run(p_cov_divider.runs[0], "Arial", 10, False, False, RGBColor(0x94, 0xA3, 0xB8))

    # Details Box
    tbl_meta = doc.add_table(rows=6, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    set_table_borders(tbl_meta, color="E2E8F0", sz="4", val="none")

    meta_info = [
        ("Tên dự án:", "FlawFirst — Flaw-First Product Review Web Application"),
        ("Kiến trúc công nghệ:", "ASP.NET Core 9.0 (MVC) + Entity Framework Core + SQL Server"),
        ("Kỹ thuật giao tiếp:", "Server-Side Rendering (Razor) + Modern Fetch API (AJAX)"),
        ("Cơ chế bảo mật:", "Cookie-based JWT Authentication, BCrypt Password Hashing"),
        ("Tài liệu đặc tả:", "1. Tác nhân hệ thống | 2. Bảng Use Case tổng quát | 3. Đặc tả chi tiết"),
        ("Ngày hoàn thiện:", "Tháng 10 / 2026")
    ]

    for idx, (lbl, val) in enumerate(meta_info):
        c0 = tbl_meta.cell(idx, 0)
        c1 = tbl_meta.cell(idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        format_run(r0, "Arial", 10.5, True, False, COLOR_PRIMARY)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        format_run(r1, "Arial", 10.5, False, False, COLOR_DARK)

    doc.add_page_break()

    # ----------------------------------------------------
    # LỜI NÓI ĐẦU & TỔNG QUAN
    # ----------------------------------------------------
    add_h1("TỔNG QUAN HỆ THỐNG FLAWFIRST")

    add_p(
        "Trong bối cảnh thương mại điện tử bùng nổ, đánh giá trực tuyến đóng vai trò quyết định đến hành vi mua sắm "
        "của người tiêu dùng. Tuy nhiên, phần lớn các nền tảng thương mại điện tử hiện nay đang gặp phải vấn nạn "
        "đánh giá ảo (seeding), đánh giá 5 sao dễ dãi, hoặc nội dung review chung chung làm mờ nhạt đi các lỗi kỹ thuật, "
        "nhược điểm thiết kế thực tế của sản phẩm. Người tiêu dùng thường chỉ phát hiện ra các điểm hạn chế đáng tiếc sau "
        "khi đã thanh toán và nhận hàng."
    )

    add_p(
        "Dự án FlawFirst được xây dựng như một nền tảng đánh giá sản phẩm độc lập, tiên phong áp dụng mô hình "
        "Flaw-First Review: Bắt buộc người đánh giá phải bóc tách rành mạch giữa Điểm hài lòng (Pros) và "
        "Hạn chế thực tế (Cons). Điểm độc đáo nhất của hệ thống là cơ chế tự động trích xuất các hạn chế (Flaw-First Extraction) "
        "từ toàn bộ các đánh giá 1–2 sao, giúp người mua sau dễ dàng nhận diện ngay các rủi ro cốt lõi trước khi ra quyết định."
    )

    make_callout(
        "FlawFirst hướng tới tính minh bạch, khách quan và trải nghiệm người dùng hiện đại: "
        "Kết hợp giữa sức mạnh kiến trúc Server-Side Rendering (Razor MVC) để tối ưu SEO, bảo mật phiên Cookie JWT, "
        "với kỹ thuật Modern AJAX (Fetch API) cho phép vote hữu ích, lưu bài, bình luận tức thời mà không cần tải lại trang.",
        "MỤC TIÊU CỐT LÕI CỦA DỰ ÁN"
    )

    # ----------------------------------------------------
    # PHẦN 1: CÁC TÁC NHÂN TRONG HỆ THỐNG
    # ----------------------------------------------------
    add_h1("PHẦN 1: CÁC TÁC NHÂN TRONG HỆ THỐNG (ACTORS SPECIFICATION)")

    add_p(
        "Tác nhân (Actor) trong hệ thống là đối tượng tương tác trực tiếp hoặc gián tiếp với hệ thống FlawFirst "
        "để thực hiện các mục tiêu nghiệp vụ. Trong hệ thống FlawFirst, các tác nhân được phân cấp rõ ràng "
        "dựa trên vai trò bảo mật và quyền hạn chức năng."
    )

    add_h2("1.1. Danh sách các tác nhân")

    tbl_actors = doc.add_table(rows=5, cols=4)
    tbl_actors.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_actors.autofit = False
    set_table_borders(tbl_actors, color=HEX_BORDER, sz="4", val="single")

    actor_headers = ["STT", "Tác nhân", "Ký hiệu", "Mô tả vai trò trong hệ thống"]
    col_widths_act = [Inches(0.6), Inches(1.8), Inches(1.1), Inches(3.0)]

    for c_idx, h_text in enumerate(actor_headers):
        cell = tbl_actors.cell(0, c_idx)
        cell.width = col_widths_act[c_idx]
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        format_run(r, "Arial", 10, True, False, RGBColor(0xFF, 0xFF, 0xFF))

    actors_data = [
        ("1", "Khách vãng lai (Guest)", "GUEST", "Người dùng chưa đăng nhập, chỉ có quyền tra cứu, khám phá sản phẩm và đọc review."),
        ("2", "Thành viên (Member / User)", "USER", "Người dùng đã đăng ký & đăng nhập thành công. Có quyền viết review, bóc tách Pros/Cons, tương tác xã hội (vote, bookmark, comment, report)."),
        ("3", "Quản trị viên (Administrator)", "ADMIN", "Có quyền quản trị tối cao: kiểm duyệt báo cáo vi phạm, ẩn/xóa bài viết, khóa/mở khóa tài khoản, quản lý danh mục ngành hàng."),
        ("4", "Hệ thống tự động (Automated Subsystems)", "SYSTEM", "Các module tự động: Bộ lọc từ cấm (Profanity Filter), Middleware kiểm tra tài khoản khóa, Lưu trữ tệp tin upload.")
    ]

    for r_idx, row_vals in enumerate(actors_data):
        row_cells = tbl_actors.rows[r_idx + 1].cells
        bg_color = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row_cells[c_idx]
            cell.width = col_widths_act[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, 100, 100, 120, 120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            format_run(r, "Arial", 9.5, (c_idx == 1), False, COLOR_DARK)

    add_p("", space_after=4)

    add_h2("1.2. Đặc tả chi tiết quyền hạn và trách nhiệm của từng tác nhân")

    add_h3("a) Tác nhân: Khách vãng lai (Guest)")
    add_p(
        "• Khái niệm: Là bất kỳ người truy cập internet nào truy cập vào trang web FlawFirst mà chưa xác thực danh tính.\n"
        "• Quyền hạn trong hệ thống:\n"
        "   + Xem trang chủ khám phá sản phẩm (/Products), tìm kiếm từ khóa theo tên máy, thương hiệu.\n"
        "   + Lọc sản phẩm theo danh mục (Category Chips), lọc theo khoảng giá nhanh (dưới 5tr, 5-15tr, 15-30tr, trên 30tr).\n"
        "   + Sắp xếp sản phẩm theo ngày mới nhất, số sao cao nhất, nhiều bài đánh giá nhất.\n"
        "   + Xem chi tiết sản phẩm (/Products/Details/{id}): Xem thông tin cấu hình, phân bố tỷ lệ 5 sao, khối Flaw-First trích xuất nhược điểm 1-2 sao.\n"
        "   + Lọc danh sách đánh giá theo từng mức sao hoặc lọc bài có hình ảnh thực tế.\n"
        "   + Xem hồ sơ tác giả (/Social/UserProfile/{id}) và số lượng người theo dõi.\n"
        "   + Đăng ký tài khoản mới (/Auth/Register) hoặc đăng nhập vào hệ thống (/Auth/Login).\n"
        "• Hạn chế: Không thể viết review, không thể bình luận, vote, bookmark, report hay follow tác giả. Nếu nhấn vào các hành động này, hệ thống sẽ tự động điều hướng sang trang Đăng nhập."
    )

    add_h3("b) Tác nhân: Thành viên / Người dùng đã đăng nhập (Registered User)")
    add_p(
        "• Khái niệm: Là người dùng đã có tài khoản hợp lệ, đã đăng nhập thành công và sở hữu phiên JWT Cookie đang hoạt động (Role: User).\n"
        "• Kế thừa: Toàn bộ quyền hạn tra cứu thông tin của Khách vãng lai.\n"
        "• Quyền hạn mở rộng:\n"
        "   + Viết bài đánh giá bóc tách Flaw-First: Chọn sản phẩm (hoặc thêm sản phẩm mới nếu chưa có trong danh mục), chọn xếp hạng sao (1–5 sao), nhập Điểm hài lòng (Pros), nhập Hạn chế thực tế (Cons), chọn ẩn danh (IsAnonymous) hoặc công khai họ tên, đính kèm tối đa 5 hình ảnh minh chứng thực tế.\n"
        "   + Quản lý bài đánh giá của tôi (/Reviews/Mine): Xem danh sách bài viết do chính mình tạo, chỉnh sửa nội dung bài viết, thêm/xóa ảnh minh chứng, hoặc xóa bài đánh giá.\n"
        "   + Tương tác xã hội mượt mà qua AJAX:\n"
        "       - Bấm Upvote (Hữu ích) hoặc Downvote (Không hữu ích) trên từng bài review.\n"
        "       - Lưu bài review (Bookmark) để xem lại trong thư viện cá nhân (/Social/Saved).\n"
        "       - Bình luận trao đổi dưới bài review, có tùy chọn bình luận ẩn danh; Xóa bình luận của chính mình.\n"
        "       - Báo cáo vi phạm (Report): Gửi tố cáo bài review kèm lý do, mô tả chi tiết và hình ảnh bằng chứng vi phạm.\n"
        "       - Theo dõi / Bỏ theo dõi tác giả bài viết (Follow / Unfollow).\n"
        "• Ràng buộc nghiệp vụ: Mỗi thành viên chỉ được đăng duy nhất 01 bài đánh giá cho 01 sản phẩm cụ thể. Nếu người dùng chọn viết review cho sản phẩm đã từng đánh giá, hệ thống sẽ tự động chuyển sang giao diện Chỉnh sửa (Edit) bài cũ để đảm bảo tính toàn vẹn dữ liệu."
    )

    add_h3("c) Tác nhân: Quản trị viên (Administrator - Admin)")
    add_p(
        "• Khái niệm: Là tài khoản có đặc quyền quản trị cao nhất của hệ thống (Role: Admin).\n"
        "• Kế thừa: Toàn bộ quyền hạn của Thành viên thông thường.\n"
        "• Quyền hạn quản trị đặc thù (/Admin):\n"
        "   + Kiểm duyệt nội dung & Xử lý báo cáo vi phạm: Xem danh sách bài đánh giá bị cộng đồng tố cáo kèm ảnh bằng chứng. Thực hiện 4 hành động dứt điểm:\n"
        "       (1) Ẩn bài viết khỏi trang sản phẩm (IsHidden = true).\n"
        "       (2) Xóa vĩnh viễn bài viết khỏi cơ sở dữ liệu.\n"
        "       (3) Phạt & Khóa vĩnh viễn tài khoản tác giả vi phạm (IsLocked = true).\n"
        "       (4) Bỏ qua báo cáo (nếu báo cáo sai sự thật hoặc không vi phạm).\n"
        "   + Quản lý tài khoản người dùng: Tra cứu danh sách thành viên toàn hệ thống, tìm kiếm theo tên hoặc email, xem trạng thái hoạt động, thực hiện Khóa hoặc Mở khóa tài khoản.\n"
        "   + Quản lý danh mục ngành hàng: Xem danh sách ngành hàng kèm số lượng sản phẩm liên kết, thêm ngành hàng mới, xóa ngành hàng rỗng (chỉ cho phép xóa khi ProductCount == 0 để bảo toàn quan hệ toàn vẹn dữ liệu).\n"
        "   + Thêm sản phẩm nhanh vào hệ thống phục vụ người dùng review."
    )

    add_h3("d) Tác nhân: Hệ thống tự động / Dịch vụ nền (System Actors)")
    add_p(
        "• Khái niệm: Các thành phần phần mềm tự động chạy ngầm trong kiến trúc ASP.NET Core để thực thi nghiệp vụ tự động mà không cần sự can thiệp thủ công của con người:\n"
        "   + Bộ lọc từ ngữ thô tục (Profanity Filter Service): Tự động quét và nhận diện các từ ngữ tục tĩu, vi phạm thuần phong mỹ tục trong cả 2 trường Pros và Cons khi người dùng gửi review. Hệ thống sẽ chặn và trả về cảnh báo cụ thể.\n"
        "   + Middleware kiểm soát tài khoản khóa (LockedAccountMiddleware): Được kích hoạt tại mỗi HTTP Request. Khi phát hiện tài khoản người dùng đã bị Admin gắn cờ IsLocked = true, middleware lập tức thu hồi cookie JWT, hủy bỏ phiên làm việc và ép người dùng quay về trang Login thông báo tài khoản bị khóa.\n"
        "   + Dịch vụ lưu trữ tệp tin (File Storage Service): Tự động kiểm tra định dạng ảnh hợp lệ (.jpg, .jpeg, .png, .webp), sinh tên tệp tin ngẫu nhiên chống trùng lặp (GUID), lưu trữ vào thư mục máy chủ wwwroot/uploads/ và trả về URL."
    )

    add_h2("1.3. Ma trận phân quyền chức năng theo tác nhân (Actor - Permission Matrix)")

    tbl_matrix = doc.add_table(rows=11, cols=4)
    tbl_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_matrix.autofit = False
    set_table_borders(tbl_matrix, color=HEX_BORDER, sz="4", val="single")

    matrix_headers = ["Nhóm chức năng nghiệp vụ", "Khách vãng lai (Guest)", "Thành viên (Member)", "Quản trị viên (Admin)"]
    col_widths_mat = [Inches(2.5), Inches(1.3), Inches(1.3), Inches(1.4)]

    for c_idx, h_text in enumerate(matrix_headers):
        cell = tbl_matrix.cell(0, c_idx)
        cell.width = col_widths_mat[c_idx]
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        format_run(r, "Arial", 9.5, True, False, RGBColor(0xFF, 0xFF, 0xFF))

    matrix_data = [
        ("Tìm kiếm, lọc, xem sản phẩm & Flaw-First", "Cho phép", "Cho phép", "Cho phép"),
        ("Xem đánh giá, lọc số sao, xem ảnh review", "Cho phép", "Cho phép", "Cho phép"),
        ("Đăng ký tài khoản, Đăng nhập hệ thống", "Cho phép", "Đã xác thực", "Đã xác thực"),
        ("Viết đánh giá Flaw-First (Pros / Cons)", "Chặn (Y/c Login)", "Cho phép", "Cho phép"),
        ("Sửa / Xóa bài đánh giá của chính mình", "Chặn", "Cho phép", "Cho phép"),
        ("Tương tác AJAX (Upvote, Downvote, Bookmark)", "Chặn (Y/c Login)", "Cho phép", "Cho phép"),
        ("Bình luận, Xóa bình luận của bản thân", "Chặn (Y/c Login)", "Cho phép", "Cho phép"),
        ("Báo cáo vi phạm bài đánh giá (Report)", "Chặn (Y/c Login)", "Cho phép", "Cho phép"),
        ("Kiểm duyệt báo cáo (Ẩn bài, Xóa bài, Phạt)", "Chặn", "Chặn", "Toàn quyền"),
        ("Quản lý tài khoản (Khóa / Mở khóa)", "Chặn", "Chặn", "Toàn quyền")
    ]

    for r_idx, row_vals in enumerate(matrix_data):
        row_cells = tbl_matrix.rows[r_idx + 1].cells
        bg_color = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row_cells[c_idx]
            cell.width = col_widths_mat[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, 90, 90, 110, 110)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            is_bold = (c_idx == 0 or "Toàn quyền" in val)
            text_color = RGBColor(0x15, 0x80, 0x3D) if "Cho phép" in val or "Toàn quyền" in val else (RGBColor(0xDC, 0x26, 0x26) if "Chặn" in val else COLOR_DARK)
            format_run(r, "Arial", 9, is_bold, False, text_color)

    doc.add_page_break()

    # ----------------------------------------------------
    # PHẦN 2: BẢNG ĐẶC TẢ USE CASE TỔNG QUÁT
    # ----------------------------------------------------
    add_h1("PHẦN 2: BẢNG ĐẶC TẢ USE CASE TỔNG QUÁT (OVERALL USE CASE SPECIFICATION)")

    add_p(
        "Hệ thống FlawFirst bao gồm 22 Use Case nghiệp vụ chính, được tổ chức thành 5 phân hệ cốt lõi. "
        "Mỗi Use Case đại diện cho một chuỗi tương tác có chủ đích giữa Tác nhân và Hệ thống nhằm hoàn thành một mục tiêu xác định."
    )

    add_h2("2.1. Phân rã chức năng theo phân hệ nghiệp vụ")
    add_p(
        "1. Phân hệ 1: Xác thực & Quản lý người dùng (Authentication & User Profile) — 4 Use Case.\n"
        "2. Phân hệ 2: Khám phá & Tra cứu sản phẩm (Product Catalog & Exploration) — 5 Use Case.\n"
        "3. Phân hệ 3: Đánh giá & Bóc tách ưu nhược điểm (Flaw-First Review Management) — 5 Use Case.\n"
        "4. Phân hệ 4: Tương tác cộng đồng & Xã hội (Social Interactions & Engagement) — 4 Use Case.\n"
        "5. Phân hệ 5: Quản trị hệ thống & Kiểm duyệt nội dung (Administration & Content Moderation) — 4 Use Case."
    )

    add_h2("2.2. Bảng đặc tả Use Case tổng quát toàn hệ thống")

    tbl_all_uc = doc.add_table(rows=23, cols=6)
    tbl_all_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_all_uc.autofit = False
    set_table_borders(tbl_all_uc, color=HEX_BORDER, sz="4", val="single")

    uc_headers = ["Mã UC", "Tên Use Case", "Phân hệ", "Tác nhân chính", "Mô tả tóm tắt nghiệp vụ", "Ưu tiên"]
    col_widths_uc = [Inches(0.7), Inches(1.5), Inches(1.3), Inches(1.1), Inches(1.5), Inches(0.6)]

    for c_idx, h_text in enumerate(uc_headers):
        cell = tbl_all_uc.cell(0, c_idx)
        cell.width = col_widths_uc[c_idx]
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, 120, 120, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        format_run(r, "Arial", 9.5, True, False, RGBColor(0xFF, 0xFF, 0xFF))

    all_uc_data = [
        # Phân hệ 1: Auth
        ("UC-01", "Đăng ký tài khoản", "Xác thực", "Guest", "Tạo tài khoản mới bằng Email, Tên và Mật khẩu (băm BCrypt).", "Cao"),
        ("UC-02", "Đăng nhập hệ thống", "Xác thực", "Guest", "Xác thực tài khoản, cấp JWT lưu cookie HTTP-Only thời hạn 7 ngày.", "Bắt buộc"),
        ("UC-03", "Đăng xuất tài khoản", "Xác thực", "User, Admin", "Xóa Cookie JWT, kết thúc phiên làm việc an toàn.", "Cao"),
        ("UC-04", "Xem hồ sơ người dùng", "Xác thực", "Guest, User", "Xem trang cá nhân của tác giả, danh sách review công khai và số follow.", "Trung bình"),

        # Phân hệ 2: Catalog
        ("UC-05", "Tìm kiếm sản phẩm", "Khám phá", "Guest, User", "Tìm kiếm theo từ khóa tên sản phẩm hoặc tên thương hiệu.", "Bắt buộc"),
        ("UC-06", "Lọc sản phẩm đa tiêu chí", "Khám phá", "Guest, User", "Lọc kết hợp: Chip danh mục, khoảng giá nhanh, khoảng giá tùy chỉnh.", "Bắt buộc"),
        ("UC-07", "Sắp xếp danh sách SP", "Khám phá", "Guest, User", "Sắp xếp tự động theo Mới nhất, Sao cao nhất, Nhiều review nhất.", "Cao"),
        ("UC-08", "Xem chi tiết sản phẩm", "Khám phá", "Guest, User", "Xem thông tin giá, danh mục, mô tả và biểu đồ phân bố 1–5 sao.", "Bắt buộc"),
        ("UC-09", "Xem nhược điểm Flaw-First", "Khám phá", "Guest, User", "Tự động trích xuất toàn bộ Cons từ bài review 1–2 sao để cảnh báo.", "Bắt buộc"),

        # Phân hệ 3: Review
        ("UC-10", "Chọn SP để đánh giá", "Đánh giá", "User", "Giao diện Picker tìm và chọn sản phẩm để viết review, hoặc thêm mới.", "Cao"),
        ("UC-11", "Viết đánh giá Flaw-First", "Đánh giá", "User", "Đánh giá sao 1-5, bóc tách Pros/Cons, chọn ẩn danh, đính kèm ảnh.", "Bắt buộc"),
        ("UC-12", "Chỉnh sửa bài đánh giá", "Đánh giá", "User", "Tác giả chỉnh sửa điểm số, nội dung Pros/Cons, thêm/xóa ảnh đính kèm.", "Cao"),
        ("UC-13", "Xóa bài đánh giá", "Đánh giá", "User", "Tác giả xóa bài review của chính mình; hệ thống cập nhật lại điểm SP.", "Cao"),
        ("UC-14", "Quản lý bài viết của tôi", "Đánh giá", "User", "Xem danh sách toàn bộ các bài review đã đăng (/Reviews/Mine).", "Cao"),

        # Phân hệ 4: Social
        ("UC-15", "Vote hữu ích (Up/Down)", "Tương tác", "User", "Bình chọn Upvote hoặc Downvote bài review bằng AJAX không reload.", "Bắt buộc"),
        ("UC-16", "Lưu bài viết (Bookmark)", "Tương tác", "User", "Lưu bài viết yêu thích vào kho lưu trữ cá nhân (/Social/Saved).", "Cao"),
        ("UC-17", "Bình luận bài đánh giá", "Tương tác", "User", "Gửi và xem bình luận trao đổi thảo luận dưới bài review qua AJAX.", "Bắt buộc"),
        ("UC-18", "Báo cáo vi phạm (Report)", "Tương tác", "User", "Gửi tố cáo bài viết vi phạm kèm lý do, mô tả và ảnh bằng chứng.", "Bắt buộc"),

        # Phân hệ 5: Admin
        ("UC-19", "Kiểm duyệt báo cáo vi phạm", "Quản trị", "Admin", "Xem danh sách vi phạm; thực hiện Ẩn bài, Xóa bài, Phạt khóa tác giả.", "Bắt buộc"),
        ("UC-20", "Khóa / Mở khóa tài khoản", "Quản trị", "Admin", "Tra cứu người dùng, gắn cờ IsLocked để chặn quyền truy cập tức thời.", "Bắt buộc"),
        ("UC-21", "Quản lý ngành hàng", "Quản trị", "Admin", "Thêm ngành hàng mới, xóa ngành hàng rỗng (ProductCount == 0).", "Cao"),
        ("UC-22", "Thêm nhanh sản phẩm", "Quản trị", "Admin", "Nhập thông tin sản phẩm trực tiếp từ trang Admin Dashboard.", "Trung bình")
    ]

    for r_idx, row_vals in enumerate(all_uc_data):
        row_cells = tbl_all_uc.rows[r_idx + 1].cells
        bg_color = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row_cells[c_idx]
            cell.width = col_widths_uc[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, 80, 80, 90, 90)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 5] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            is_bold = (c_idx == 0 or "Bắt buộc" in val)
            text_color = RGBColor(0x99, 0x1B, 0x1B) if "Bắt buộc" in val else COLOR_DARK
            format_run(r, "Arial", 8.5, is_bold, False, text_color)

    doc.add_page_break()

    # ----------------------------------------------------
    # PHẦN 3: ĐẶC TẢ CHI TIẾT CÁC USE CASE TIÊU BIỂU
    # ----------------------------------------------------
    add_h1("PHẦN 3: ĐẶC TẢ CHI TIẾT CÁC USE CASE TIÊU BIỂU (DETAILED SPECIFICATIONS)")

    add_p(
        "Nhằm làm rõ quy trình xử lý dữ liệu và luồng tương tác chuẩn công nghiệp giữa Người dùng và Hệ thống, "
        "dưới đây là đặc tả chi tiết 6 Use Case cốt lõi và mang tính chất đại diện tiêu biểu nhất cho dự án FlawFirst, "
        "tuân thủ theo chuẩn tài liệu đặc tả quốc tế (RUP / IEEE Software Requirements Specification)."
    )

    def render_detailed_uc_table(uc_meta, main_flow, alt_flows, exc_flows, non_func):
        """Helper to render a full IEEE/RUP style detailed use case."""
        # Info Table
        tbl_info = doc.add_table(rows=len(uc_meta), cols=2)
        tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_info.autofit = False
        set_table_borders(tbl_info, color=HEX_BORDER, sz="4", val="single")

        for idx, (lbl, val) in enumerate(uc_meta):
            c0 = tbl_info.cell(idx, 0)
            c1 = tbl_info.cell(idx, 1)
            c0.width = Inches(2.0)
            c1.width = Inches(4.5)
            set_cell_margins(c0, 70, 70, 110, 110)
            set_cell_margins(c1, 70, 70, 110, 110)
            
            p0 = c0.paragraphs[0]
            r0 = p0.add_run(lbl)
            format_run(r0, "Arial", 9.5, True, False, COLOR_PRIMARY)
            
            p1 = c1.paragraphs[0]
            r1 = p1.add_run(val)
            format_run(r1, "Arial", 9.5, False, False, COLOR_DARK)

        add_p("", space_after=4)

        # Main Flow Table
        add_h3("Luồng sự kiện chính (Main Flow / Happy Path):")
        tbl_mf = doc.add_table(rows=len(main_flow) + 1, cols=3)
        tbl_mf.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_mf.autofit = False
        set_table_borders(tbl_mf, color=HEX_BORDER, sz="4", val="single")

        mf_headers = ["Bước", "Hành động của Tác nhân", "Phản hồi / Xử lý của Hệ thống"]
        mf_widths = [Inches(0.6), Inches(3.0), Inches(2.9)]

        for c_idx, h_text in enumerate(mf_headers):
            cell = tbl_mf.cell(0, c_idx)
            cell.width = mf_widths[c_idx]
            set_cell_background(cell, HEX_SUBHEADER_BG)
            set_cell_margins(cell, 90, 90, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(h_text)
            format_run(r, "Arial", 9, True, False, RGBColor(0xFF, 0xFF, 0xFF))

        for r_idx, (st, act, sys_res) in enumerate(main_flow):
            cells = tbl_mf.rows[r_idx + 1].cells
            bg = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate([st, act, sys_res]):
                c = cells[c_idx]
                c.width = mf_widths[c_idx]
                set_cell_background(c, bg)
                set_cell_margins(c, 70, 70, 100, 100)
                p = c.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                format_run(r, "Arial", 9, (c_idx == 0), False, COLOR_DARK)

        add_p("", space_after=4)

        # Alternative & Exception Flows
        if alt_flows:
            add_h3("Các luồng rẽ nhánh (Alternative Flows):")
            for af_code, af_desc in alt_flows:
                p = add_p(f"• [{af_code}] {af_desc}", space_before=1, space_after=3)
                p.runs[0].bold = False

        if exc_flows:
            add_h3("Các luồng ngoại lệ & lỗi (Exception Flows):")
            for ef_code, ef_desc in exc_flows:
                p = add_p(f"• [{ef_code}] {ef_desc}", space_before=1, space_after=3)
                p.runs[0].bold = False

        if non_func:
            add_h3("Yêu cầu phi chức năng & Bảo mật:")
            for nf in non_func:
                add_p(f"• {nf}", space_before=1, space_after=3)

        add_p("", space_after=8)

    # ----------------------------------------------------
    # ĐẶC TẢ 1: UC-02 ĐĂNG NHẬP HỆ THỐNG
    # ----------------------------------------------------
    add_h2("ĐẶC TẢ USE CASE 1: UC-02 — ĐĂNG NHẬP HỆ THỐNG (AUTHENTICATION FLOW)")

    render_detailed_uc_table(
        uc_meta=[
            ("Mã Use Case", "UC-02"),
            ("Tên Use Case", "Đăng nhập hệ thống (User & Admin Authentication)"),
            ("Tác nhân chính", "Khách vãng lai (Guest), Người dùng (User), Quản trị viên (Admin)"),
            ("Phân hệ nghiệp vụ", "Xác thực & Quản lý phiên (Auth Module)"),
            ("Mục đích", "Xác thực danh tính người dùng qua Email và Mật khẩu, cấp JWT Token lưu an toàn trong Cookie."),
            ("Điều kiện tiên quyết", "Người dùng đã có tài khoản tồn tại trong cơ sở dữ liệu (Users table)."),
            ("Điều kiện kết thúc", "Hệ thống xác thực thành công, ghi nhận Cookie 'jwt_token' (HttpOnly), chuyển hướng về trang yêu cầu trước đó hoặc trang chủ.")
        ],
        main_flow=[
            ("1", "Người dùng truy cập vào liên kết '/Auth/Login' từ thanh điều hướng (hoặc do bị điều hướng khi thực hiện hành động yêu cầu quyền).", "Hệ thống hiển thị giao diện form đăng nhập gồm ô nhập Email, Mật khẩu, nút Đăng nhập và các nút điền nhanh tài khoản mẫu."),
            ("2", "Người dùng nhập Email và Mật khẩu hợp lệ, sau đó nhấn nút 'Đăng nhập'.", "Hệ thống tiếp nhận yêu cầu POST '/Auth/Login', kiểm tra tính hợp lệ dữ liệu (Model validation)."),
            ("3", "Hệ thống tiến hành xác minh thông tin tài khoản.", "AuthService truy vấn CSDL tìm User theo Email. Sử dụng BCrypt.Verify(password, passwordHash) để so khớp mật khẩu."),
            ("4", "Hệ thống kiểm tra trạng thái khóa của tài khoản.", "Kiểm tra thuộc tính User.IsLocked. Nếu IsLocked == false, tiếp tục luồng xử lý."),
            ("5", "Hệ thống sinh chuỗi JWT Token.", "JwtTokenService sinh token mang các Claim: NameIdentifier (Id), Email, Role (User/Admin). Thời hạn token: 7 ngày."),
            ("6", "Hệ thống lưu Token vào Cookie trình duyệt.", "Ghi Cookie 'jwt_token' với cờ HttpOnly = true, SameSite = Lax, Secure = true (nếu chạy HTTPS)."),
            ("7", "Hệ thống chuyển hướng người dùng.", "Nếu có tham số returnUrl hợp lệ thì chuyển hướng về returnUrl; nếu không thì chuyển hướng về Trang chủ (/Products).")
        ],
        alt_flows=[
            ("AF-01 (Đăng nhập nhanh thử nghiệm)", "Tại màn hình đăng nhập, người dùng nhấn nút 'Tài khoản Admin' hoặc 'Tài khoản User', mã JavaScript lập tức tự động điền sẵn email và mật khẩu mẫu vào các ô input để người dùng đăng nhập ngay lập tức.")
        ],
        exc_flows=[
            ("EF-01 (Sai thông tin đăng nhập)", "Nếu email không tồn tại trong hệ thống hoặc mật khẩu không khớp mã băm BCrypt, hệ thống hiển thị thông báo lỗi: 'Email hoặc mật khẩu không chính xác.' và giữ nguyên email trên form."),
            ("EF-02 (Tài khoản đã bị khóa)", "Nếu tài khoản có thuộc tính IsLocked == true (do Admin khóa), hệ thống chặn đăng nhập và hiển thị thông báo: 'Tài khoản của bạn đã bị khóa do vi phạm tiêu chuẩn cộng đồng. Vui lòng liên hệ Admin.'"),
            ("EF-03 (Bỏ trống trường bắt buộc)", "Nếu người dùng nhấn Đăng nhập khi chưa điền Email hoặc Mật khẩu, hệ thống báo lỗi validation trực tiếp dưới trường dữ liệu.")
        ],
        non_func=[
            "Mật khẩu không bao giờ được lưu dạng văn bản thuần (plain-text), bắt buộc mã hóa băm một chiều bằng thư viện BCrypt.",
            "JWT Token được lưu trong Cookie HttpOnly để ngăn chặn hoàn toàn các cuộc tấn công đánh cắp phiên qua mã độc XSS (Cross-Site Scripting).",
            "Thời gian phản hồi đăng nhập phải dưới 500ms."
        ]
    )

    # ----------------------------------------------------
    # ĐẶC TẢ 2: UC-06 LỌC SẢN PHẨM ĐA TIÊU CHÍ
    # ----------------------------------------------------
    add_h2("ĐẶC TẢ USE CASE 2: UC-06 — TÌM KIẾM & LỌC SẢN PHẨM ĐA TIÊU CHÍ")

    render_detailed_uc_table(
        uc_meta=[
            ("Mã Use Case", "UC-06"),
            ("Tên Use Case", "Khám phá, Tìm kiếm & Lọc sản phẩm đa tiêu chí"),
            ("Tác nhân chính", "Khách vãng lai (Guest), Người dùng (User), Quản trị viên (Admin)"),
            ("Phân hệ nghiệp vụ", "Danh mục & Khám phá sản phẩm (Product Catalog Module)"),
            ("Mục đích", "Cho phép người dùng tra cứu sản phẩm chính xác theo từ khóa, danh mục ngành hàng, khoảng giá linh hoạt và các tiêu chí sắp xếp."),
            ("Điều kiện tiên quyết", "Cơ sở dữ liệu đã có dữ liệu sản phẩm (Products) và danh mục (Categories)."),
            ("Điều kiện kết thúc", "Hệ thống trả về danh sách sản phẩm khớp toàn bộ điều kiện lọc kết hợp, hiển thị trực quan kèm phân trang.")
        ],
        main_flow=[
            ("1", "Người dùng truy cập trang chủ khám phá sản phẩm ('/Products' hoặc '/').", "Hệ thống tải danh sách sản phẩm mặc định (sắp xếp mới nhất, 12 sản phẩm/trang) cùng thanh công cụ lọc."),
            ("2", "Người dùng thực hiện thao tác lọc theo danh mục (Category Chip).", "Người dùng bấm chọn chip danh mục (ví dụ: 'Điện thoại'). Giao diện tự động gửi request lọc theo categoryId."),
            ("3", "Người dùng chọn khoảng giá nhanh (Quick Price Range).", "Người dùng bấm chọn một nút giá tiện lợi: 'Dưới 5 triệu', '5 – 15 triệu', '15 – 30 triệu', hoặc 'Trên 30 triệu'."),
            ("4", "Người dùng nhập từ khóa tìm kiếm (Search Keyword).", "Người dùng gõ từ khóa tìm kiếm (ví dụ: 'iPhone') vào ô tìm kiếm và nhấn Enter."),
            ("5", "Người dùng chọn cách sắp xếp (Instant Sort).", "Người dùng chọn sắp xếp theo 'Số sao cao nhất'. Trình duyệt bắt sự kiện onchange và tự động submit form ngay lập tức."),
            ("6", "Hệ thống truy vấn dữ liệu động qua LINQ.", "ProductCatalogService xây dựng câu truy vấn IQueryable kết hợp toàn bộ điều kiện: Keyword, CategoryId, MinPrice, MaxPrice, Sort và Page."),
            ("7", "Hệ thống trả về giao diện kết quả.", "Render lưới thẻ sản phẩm (_ProductCard), hiển thị tổng số kết quả tìm thấy và thanh phân trang (_Pager).")
        ],
        alt_flows=[
            ("AF-01 (Nhập khoảng giá tùy chỉnh)", "Người dùng không chọn nút giá nhanh mà tự nhập thủ công minPrice và maxPrice vào 2 ô nhập tùy chỉnh, sau đó nhấn nút 'Áp dụng giá'."),
            ("AF-02 (Đặt lại bộ lọc 1-Click Reset)", "Người dùng nhấn nút '✕ Đặt lại bộ lọc', hệ thống lập tức xóa sạch toàn bộ tham số truy vấn trên URL và nạp lại trang chủ mặc định ban đầu.")
        ],
        exc_flows=[
            ("EF-01 (Không tìm thấy sản phẩm phù hợp)", "Nếu bộ lọc quá hẹp dẫn đến không có sản phẩm nào thỏa mãn, hệ thống hiển thị thông báo thân thiện: 'Không tìm thấy sản phẩm nào phù hợp với bộ lọc hiện tại' kèm nút 'Xóa bộ lọc để xem tất cả'.")
        ],
        non_func=[
            "Toàn bộ trạng thái bộ lọc (Keyword, CategoryId, MinPrice, MaxPrice, Sort, Page) phải được duy trì trên Query String để người dùng có thể chia sẻ URL hoặc lưu Bookmark trình duyệt.",
            "Truy vấn CSDL sử dụng AsNoTracking() trong Entity Framework Core để tối ưu hóa bộ nhớ và tăng tốc độ phản hồi."
        ]
    )

    # ----------------------------------------------------
    # ĐẶC TẢ 3: UC-11 VIẾT ĐÁNH GIÁ FLAW-FIRST
    # ----------------------------------------------------
    add_h2("ĐẶC TẢ USE CASE 3: UC-11 — VIẾT ĐÁNH GIÁ BÓC TÁCH FLAW-FIRST (PROS / CONS)")

    render_detailed_uc_table(
        uc_meta=[
            ("Mã Use Case", "UC-11"),
            ("Tên Use Case", "Viết đánh giá sản phẩm bóc tách ưu và nhược điểm (Flaw-First Review Creation)"),
            ("Tác nhân chính", "Thành viên (Registered User)"),
            ("Tác nhân phụ", "Hệ thống tự động: Profanity Filter, File Storage Service"),
            ("Phân hệ nghiệp vụ", "Đánh giá & Bóc tách nhược điểm (Review Module) — CỐT LÕI HỆ THỐNG"),
            ("Mục đích", "Cho phép người dùng đã trải nghiệm sản phẩm đăng tải nhận xét chân thực, bắt buộc phân tách rõ ràng giữa Điểm hài lòng (Pros) và Hạn chế thực tế (Cons)."),
            ("Điều kiện tiên quyết", "Người dùng đã đăng nhập vào hệ thống; Sản phẩm muốn đánh giá đã tồn tại trong CSDL."),
            ("Điều kiện kết thúc", "Bài đánh giá được lưu thành công vào bảng Reviews; Thống kê số sao của sản phẩm được cập nhật; Nhược điểm được trích xuất vào khối Flaw-First.")
        ],
        main_flow=[
            ("1", "Người dùng nhấn nút 'Viết đánh giá' trên thẻ sản phẩm hoặc chọn sản phẩm từ màn hình Picker ('/Reviews/Create?productId=...').", "Hệ thống kiểm tra xem người dùng đã từng đánh giá sản phẩm này chưa. Nếu chưa, hiển thị Form viết review."),
            ("2", "Người dùng chọn số sao đánh giá (Rating).", "Người dùng nhấp vào bộ chọn 5 sao tương tác SVG (1 sao đến 5 sao). Nhãn hiển thị cảm xúc tương ứng (VD: '1.0 - Rất thất vọng', '5.0 - Rất hài lòng')."),
            ("3", "Người dùng nhập Điểm hài lòng (Pros).", "Người dùng nhập các ưu điểm thực tế vào khung 'Ưu điểm / Điểm hài lòng' (bắt buộc nhập, tối thiểu 10 ký tự)."),
            ("4", "Người dùng nhập Hạn chế thực tế (Cons).", "Người dùng nhập các điểm chưa tốt, lỗi vặt vào khung 'Hạn chế / Nhược điểm thực tế' (bắt buộc nhập, tối thiểu 10 ký tự)."),
            ("5", "Người dùng thiết lập tùy chọn quyền riêng tư.", "Người dùng tick chọn ô 'Đăng ẩn danh' nếu muốn giấu danh tính cá nhân trên bài review."),
            ("6", "Người dùng tải lên hình ảnh minh chứng thực tế.", "Người dùng chọn từ 1 đến 5 tệp ảnh thực tế của sản phẩm. Trình duyệt hiển thị thumbnail xem trước (preview)."),
            ("7", "Người dùng nhấn nút 'Đăng đánh giá ngay'.", "Hệ thống tiếp nhận form POST '/Reviews/Create' kèm tệp tin đính kèm."),
            ("8", "Hệ thống kiểm duyệt từ ngữ qua Profanity Filter.", "ProfanityFilterService quét văn bản Pros và Cons để phát hiện các từ cấm, từ ngữ thô tục."),
            ("9", "Hệ thống lưu trữ ảnh và ghi dữ liệu CSDL.", "FileStorageService lưu các file ảnh hợp lệ vào 'wwwroot/uploads'. ReviewService thêm bản ghi Review và ReviewImage."),
            ("10", "Hệ thống hoàn tất và điều hướng.", "Hệ thống hiển thị Toast thông báo thành công và chuyển hướng người dùng về trang chi tiết sản phẩm (/Products/Details/{id}).")
        ],
        alt_flows=[
            ("AF-01 (Tự động chuyển sang Chỉnh sửa)", "Nếu người dùng đã từng đánh giá sản phẩm này trong quá khứ, hệ thống phát hiện bản ghi cũ và tự động chuyển hướng sang giao diện '/Reviews/Edit/{id}' để người dùng cập nhật bài viết thay vì tạo mới, đảm bảo nguyên tắc 1 người - 1 bài review trên 1 sản phẩm.")
        ],
        exc_flows=[
            ("EF-01 (Phát hiện từ ngữ thô tục / Vi phạm)", "Nếu nội dung Pros hoặc Cons chứa từ ngữ cấm trong từ điển ProfanityFilter, hệ thống chặn lưu dữ liệu và báo lỗi: 'Nội dung chứa từ ngữ không phù hợp thuần phong mỹ tục: [Từ cấm]. Vui lòng chỉnh sửa trước khi đăng.'"),
            ("EF-02 (Tệp ảnh vượt quá giới hạn hoặc sai định dạng)", "Nếu người dùng tải file không phải ảnh (không phải .jpg, .png, .webp) hoặc file lớn hơn 5MB, hệ thống từ chối tệp và yêu cầu chọn lại."),
            ("EF-03 (Chưa chọn số sao hoặc để trống nội dung)", "Hệ thống kiểm tra ModelState, nếu Rating = 0 hoặc Pros/Cons trống, hiển thị cảnh báo đỏ yêu cầu hoàn thiện đầy đủ.")
        ],
        non_func=[
            "Tự động tính toán lại điểm đánh giá trung bình (Average Rating) và cơ cấu tỷ lệ sao (Star Distribution) của sản phẩm ngay khi bài review được lưu.",
            "Tự động đưa nhược điểm (Cons) vào khối trích xuất Flaw-First nếu bài viết có số sao là 1 hoặc 2 sao."
        ]
    )

    # ----------------------------------------------------
    # ĐẶC TẢ 4: UC-15 & UC-17 TƯƠNG TÁC XÃ HỘI AJAX
    # ----------------------------------------------------
    add_h2("ĐẶC TẢ USE CASE 4: UC-15 & UC-17 — TƯƠNG TÁC XÃ HỘI QUA AJAX (VOTE & COMMENT)")

    render_detailed_uc_table(
        uc_meta=[
            ("Mã Use Case", "UC-15 & UC-17"),
            ("Tên Use Case", "Tương tác xã hội mượt mà qua AJAX (Upvote/Downvote & Bình luận bài review)"),
            ("Tác nhân chính", "Thành viên (Registered User)"),
            ("Phân hệ nghiệp vụ", "Tương tác cộng đồng (Social Module) — KIẾN TRÚC FETCH AJAX"),
            ("Mục đích", "Cho phép người dùng tương tác ngay trên dòng thời gian (Like/Dislike, gửi bình luận) bằng Modern Fetch API mà KHÔNG cần tải lại toàn bộ trang web."),
            ("Điều kiện tiên quyết", "Người dùng đã đăng nhập vào hệ thống; Đang xem danh sách review hoặc chi tiết sản phẩm."),
            ("Điều kiện kết thúc", "Cơ sở dữ liệu cập nhật lượt tương tác; DOM giao diện thay đổi số liệu tức thì kèm hiệu ứng Toast phản hồi.")
        ],
        main_flow=[
            ("1", "Người dùng đọc một bài review và bấm nút 'Hữu ích' (Upvote) hoặc 'Không hữu ích' (Downvote).", "JavaScript bắt sự kiện onclick, gọi hàm handleVote(reviewId, voteType, button)."),
            ("2", "Trình duyệt gửi AJAX request ngầm.", "Gửi 'fetch(\"/Social/Vote\", { method: \"POST\", headers: { \"X-Requested-With\": \"XMLHttpRequest\" }, body: ... })'."),
            ("3", "SocialController tiếp nhận và xử lý nghiệp vụ.", "SocialService kiểm tra trạng thái vote hiện tại của User trên Review này: Nếu chưa vote thì thêm mới; Nếu vote trùng thì hủy bỏ (toggle); Nếu vote ngược thì đảo trạng thái."),
            ("4", "Hệ thống cập nhật bộ đếm trong CSDL.", "Tính toán lại UpvoteCount và DownvoteCount của bài Review, lưu vào CSDL."),
            ("5", "Server phản hồi dữ liệu JSON.", "Trả về mã HTTP 200 kèm payload JSON: { success: true, upvoteCount: X, downvoteCount: Y, currentVote: 'Up' }."),
            ("6", "Client cập nhật giao diện không reload.", "JavaScript giải mã JSON, cập nhật trực tiếp con số trên 2 nút Up/Down của thẻ review, đổi màu nút và hiển thị Toast: 'Đã ghi nhận hữu ích'."),
            ("7", "Người dùng bấm nút 'Bình luận' trên thẻ review.", "JavaScript mở hộp thoại modal bình luận và gọi AJAX 'fetch(\"/Social/Comments/{id}\")' để tải danh sách bình luận (Lazy Loading)."),
            ("8", "Người dùng nhập nội dung trao đổi và nhấn 'Gửi'.", "Gửi AJAX POST '/Social/Comment'. Server lưu bình luận và trả về object Comment mới. Trình duyệt render thêm bình luận mới vào đầu danh sách mà không reload.")
        ],
        alt_flows=[
            ("AF-01 (Xóa bình luận cá nhân)", "Tác giả của bình luận hoặc Quản trị viên có thể nhấn nút '✕ Xóa' bên cạnh bình luận của mình. Trình duyệt gửi AJAX POST '/Social/DeleteComment/{id}', server xóa bình luận và JavaScript xóa phần tử HTML tương ứng trên màn hình.")
        ],
        exc_flows=[
            ("EF-01 (Người dùng chưa đăng nhập bấm Vote/Comment)", "SocialController và FriendlyAuthorizationResultHandler phát hiện request có header 'X-Requested-With: XMLHttpRequest' nhưng chưa xác thực (401 Unauthorized), frontend lập tức nhận diện và chuyển hướng người dùng tới trang Đăng nhập '/Auth/Login?returnUrl=...'."),
            ("EF-02 (Tài khoản bị khóa đột xuất)", "LockedAccountMiddleware phát hiện tài khoản bị khóa trong phiên AJAX, trả về mã 401/JSON để client chuyển hướng thông báo khóa tài khoản.")
        ],
        non_func=[
            "Sử dụng thuần Vanilla JavaScript Fetch API (không phụ thuộc thư viện jQuery hoặc Axios), giảm kích thước tải trang.",
            "Tốc độ phản hồi tương tác AJAX phải đạt dưới 100ms trên môi trường mạng thông thường."
        ]
    )

    # ----------------------------------------------------
    # ĐẶC TẢ 5: UC-18 & UC-19 BÁO CÁO VI PHẠM & KIỂM DUYỆT
    # ----------------------------------------------------
    add_h2("ĐẶC TẢ USE CASE 5: UC-18 & UC-19 — BÁO CÁO VI PHẠM & KIỂM DUYỆT NỘI DUNG")

    render_detailed_uc_table(
        uc_meta=[
            ("Mã Use Case", "UC-18 & UC-19"),
            ("Tên Use Case", "Báo cáo vi phạm bài đánh giá & Xử lý kiểm duyệt (Moderation Workflow)"),
            ("Tác nhân chính", "Thành viên (Người tố cáo) & Quản trị viên (Người kiểm duyệt)"),
            ("Phân hệ nghiệp vụ", "Cộng đồng & Quản trị hệ thống (Social & Admin Moderation)"),
            ("Mục đích", "Bảo vệ cộng đồng khỏi nội dung sai lệch, thù ghét, quảng cáo rác (spam) thông qua cơ chế tự quản và kiểm duyệt tập trung."),
            ("Điều kiện tiên quyết", "Người dùng gửi báo cáo đã đăng nhập; Quản trị viên đăng nhập với Role Admin."),
            ("Điều kiện kết thúc", "Báo cáo được ghi nhận hoặc xử lý triệt để (Ẩn bài, Xóa bài, Khóa tài khoản hoặc Bỏ qua).")
        ],
        main_flow=[
            ("1", "Thành viên phát hiện bài review có nội dung vi phạm, bấm nút 'Báo cáo vi phạm' trên thẻ review.", "Hệ thống mở hộp thoại Modal Báo cáo vi phạm."),
            ("2", "Thành viên chọn lý do vi phạm.", "Chọn một trong các lý do: 'Quảng cáo / Spam', 'Ngôn từ xúc phạm, thù ghét', 'Thông tin sai lệch / Gian dối', 'Hình ảnh phản cảm'."),
            ("3", "Thành viên nhập mô tả và tải ảnh bằng chứng.", "Nhập mô tả cụ thể về hành vi vi phạm và đính kèm tệp ảnh chụp màn hình bằng chứng (tùy chọn)."),
            ("4", "Thành viên nhấn nút 'Gửi báo cáo'.", "Hệ thống lưu thông tin vào bảng ReviewReports với trạng thái 'Pending', lưu ảnh bằng chứng vào ReportEvidences. Hiển thị thông báo: 'Đã gửi báo cáo thành công'."),
            ("5", "Quản trị viên truy cập trang Quản trị (/Admin).", "AdminService tải danh sách các báo cáo đang ở trạng thái Pending, hiển thị đầy đủ thông tin bài viết bị tố cáo, người tố cáo, lý do và ảnh bằng chứng."),
            ("6", "Quản trị viên xem xét và ra quyết định xử lý.", "Quản trị viên chọn 1 trong 4 nút hành động dứt điểm trên giao diện:"),
            ("7a", "Hành động 1: 'Ẩn bài viết'", "Hệ thống cập nhật Review.IsHidden = true. Bài viết lập tức biến mất khỏi trang chi tiết sản phẩm."),
            ("7b", "Hành động 2: 'Xóa vĩnh viễn bài'", "Hệ thống xóa bản ghi Review, các ảnh liên quan và cập nhật lại điểm số sản phẩm."),
            ("7c", "Hành động 3: 'Phạt & Khóa tác giả'", "Hệ thống ẩn bài viết, đồng thời cập nhật User.IsLocked = true của tác giả viết bài. Tác giả bị tước quyền đăng nhập ngay lập tức."),
            ("7d", "Hành động 4: 'Bỏ qua báo cáo'", "Cập nhật trạng thái báo cáo thành 'Dismissed' nếu báo cáo không có căn cứ xác thực.")
        ],
        alt_flows=[],
        exc_flows=[
            ("EF-01 (Báo cáo trùng lặp)", "Nếu một người dùng liên tục bấm báo cáo cùng 1 bài viết trong thời gian ngắn, hệ thống hiển thị thông báo: 'Bạn đã gửi báo cáo cho bài viết này rồi, vui lòng chờ Admin xử lý.'")
        ],
        non_func=[
            "Lưu vết đầy đủ thời gian báo cáo và thời gian xử lý của Admin để phục vụ việc tra soát kiểm toán hệ thống (Audit Trail)."
        ]
    )

    # ----------------------------------------------------
    # ĐẶC TẢ 6: UC-20 QUẢN LÝ NGƯỜI DÙNG & KHÓA TÀI KHOẢN
    # ----------------------------------------------------
    add_h2("ĐẶC TẢ USE CASE 6: UC-20 — QUẢN LÝ NGƯỜI DÙNG & KHÓA TÀI KHOẢN VI PHẠM")

    render_detailed_uc_table(
        uc_meta=[
            ("Mã Use Case", "UC-20"),
            ("Tên Use Case", "Quản lý người dùng, Tìm kiếm & Khóa tài khoản vi phạm"),
            ("Tác nhân chính", "Quản trị viên (Administrator - Admin)"),
            ("Tác nhân phụ", "Hệ thống tự động: LockedAccountMiddleware"),
            ("Phân hệ nghiệp vụ", "Quản trị hệ thống (Administration Module)"),
            ("Mục đích", "Cho phép Admin giám sát toàn bộ người dùng, tìm kiếm theo tên/email, khóa các tài khoản vi phạm để ngăn chặn truy cập ngay lập tức."),
            ("Điều kiện tiên quyết", "Người thực hiện phải đăng nhập với tài khoản có quyền Quản trị viên (Role: Admin)."),
            ("Điều kiện kết thúc", "Trạng thái IsLocked của người dùng được cập nhật trong CSDL; Người dùng bị khóa bị từ chối truy cập ngay lập tức.")
        ],
        main_flow=[
            ("1", "Admin truy cập vào menu 'Quản trị' (/Admin) và chuyển sang tab 'Quản lý người dùng'.", "Hệ thống hiển thị danh sách toàn bộ người dùng, phân trang 10 người/trang kèm trạng thái hoạt động ('Hoạt động' màu xanh, 'Đã khóa' màu đỏ)."),
            ("2", "Admin nhập từ khóa tìm kiếm (họ tên hoặc email của thành viên cần kiểm tra).", "Hệ thống lọc danh sách người dùng theo từ khóa và hiển thị kết quả."),
            ("3", "Admin nhấn nút 'Khóa tài khoản' trên dòng người dùng vi phạm.", "Trình duyệt gửi form POST '/Admin/SetLock/{id}' với tham số lock=true."),
            ("4", "AdminService cập nhật cơ sở dữ liệu.", "Cập nhật trường IsLocked = true của User tương ứng trong bảng Users."),
            ("5", "Hệ thống phản hồi giao diện Admin.", "Trang nạp lại, trạng thái của người dùng chuyển sang huy hiệu đỏ 'Đã khóa', nút bấm đổi thành 'Mở khóa'."),
            ("6", "Cơ chế tự động thực thi tại request kế tiếp của người dùng bị khóa.", "Khi người dùng bị khóa gửi bất kỳ request nào, LockedAccountMiddleware chặn lại, kiểm tra CSDL thấy IsLocked == true -> Tự động xóa Cookie JWT, chuyển hướng về '/Auth/Login?locked=1'.")
        ],
        alt_flows=[
            ("AF-01 (Mở khóa tài khoản)", "Nếu người dùng đã hết thời hạn phạt hoặc giải trình hợp lệ, Admin nhấn nút 'Mở khóa'. Hệ thống cập nhật IsLocked = false, người dùng có thể đăng nhập lại bình thường.")
        ],
        exc_flows=[
            ("EF-01 (Admin tự khóa chính mình)", "Nếu Admin vô tình thao tác khóa trên chính tài khoản đang đăng nhập của mình, hệ thống phát hiện UserId trùng khớp với danh tính hiện tại và từ chối thao tác: 'Không thể tự khóa tài khoản của chính bạn.'")
        ],
        non_func=[
            "Cơ chế Middleware chặn truy cập phải hoạt động theo thời gian thực (Real-time enforcement): Không cần đợi Cookie JWT hết hạn (7 ngày), chỉ cần Admin bấm Khóa thì ở lượt click tiếp theo người dùng sẽ bị đẩy ra màn hình đăng nhập ngay lập tức."
        ]
    )

    # ----------------------------------------------------
    # KẾT LUẬN & ĐÁNH GIÁ KIẾN TRÚC
    # ----------------------------------------------------
    add_h1("KẾT LUẬN VÀ ĐÁNH GIÁ KIẾN TRÚC HỆ THỐNG")

    add_p(
        "Tài liệu phân tích và thiết kế hệ thống FlawFirst đã làm rõ cấu trúc phân cấp tác nhân, "
        "bản đồ 22 Use Case tổng quát và đặc tả chi tiết 6 Use Case nghiệp vụ linh hồn của dự án. "
        "Qua quá trình phân tích và hiện thực hóa, hệ thống thể hiện các ưu điểm vượt trội về mặt kỹ thuật và nghiệp vụ:"
    )

    add_p(
        "1. Tính mới và độc đáo trong nghiệp vụ: Mô hình Flaw-First giải quyết trực diện bài toán nhức nhối "
        "của thương mại điện tử bằng việc bắt buộc bóc tách Pros/Cons và cơ chế tự động gom các nhược điểm từ bài đánh giá "
        "1–2 sao để cảnh báo người tiêu dùng.\n\n"
        "2. Kiến trúc chuẩn mực và phân tầng sạch sẽ: Ứng dụng mô hình ASP.NET Core MVC kết hợp Service Layer, "
        "tách biệt hoàn toàn giữa Controllers (tiếp nhận HTTP), Services (xử lý logic nghiệp vụ và tính toán), "
        "Entities / DbContext (truy vấn dữ liệu EF Core) và ViewModels (đóng gói dữ liệu hiển thị).\n\n"
        "3. Trải nghiệm người dùng mượt mà (Hybrid Architecture): Kết hợp ưu thế của Server-Side Rendering (Razor) "
        "để tải trang nhanh, chuẩn SEO và bảo mật phiên với Modern Fetch API (AJAX) để mang lại phản hồi tức thì "
        "khi tương tác xã hội (Vote, Bookmark, Comment).\n\n"
        "4. An toàn & Bảo mật đa tầng: Xác thực an toàn với BCrypt, JWT lưu Cookie HttpOnly chống XSS, "
        "kiểm duyệt từ ngữ thô tục tự động (ProfanityFilter) và Middleware kiểm soát tài khoản khóa trong thời gian thực."
    )

    # Output path
    output_filename = "Phan_Tich_Thiet_Ke_He_Thong_FlawFirst.docx"
    output_path = os.path.join(r"g:\BTLWNC\FlawFirst.Api", output_filename)
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()
