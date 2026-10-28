import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_erd_diagram():
    # Setup high-res figure (width 17 inches, height 12 inches, 300 DPI)
    fig, ax = plt.subplots(figsize=(17, 12), dpi=300)
    ax.set_xlim(0, 170)
    ax.set_ylim(0, 120)
    ax.axis('off')

    # Color styling matching academic thesis ERD
    COLOR_BOX_BG = "#F8FAFC"
    COLOR_BORDER = "#1E293B"
    COLOR_HEADER_BG = "#E2E8F0"
    COLOR_LINE = "#334155"
    COLOR_CARD = "#DC2626"
    COLOR_TEXT = "#0F172A"

    # Entities with exact schema info from FlawFirst
    # [x, y, w, h]
    entities = {
        "Category": {
            "title": "Category (Danh mục)",
            "rect": [10, 95, 26, 15],
            "fields": [
                "PK: Id (int, Identity)",
                "• Name (nvarchar 120, Unique)",
                "• Description (nvarchar 500, Null)",
                "• CreatedAt (datetime2)"
            ]
        },
        "Product": {
            "title": "Product (Sản phẩm)",
            "rect": [48, 95, 30, 17],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: CategoryId (int)",
                "• Name (nvarchar 200)",
                "• Brand (nvarchar 120)",
                "• Price (decimal 18,2)",
                "• ImageUrl (nvarchar 500, Null)"
            ]
        },
        "User": {
            "title": "User (Người dùng)",
            "rect": [128, 93, 32, 20],
            "fields": [
                "PK: Id (int, Identity)",
                "• FullName (nvarchar 150)",
                "• Email (nvarchar 256, Unique)",
                "• PasswordHash (nvarchar 200)",
                "• Role (nvarchar 20: Admin/User)",
                "• IsLocked (bit)",
                "• CreatedAt (datetime2)"
            ]
        },
        "UserFollow": {
            "title": "UserFollow (Theo dõi)",
            "rect": [128, 62, 32, 14],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: FollowerId (int)",
                "FK: FollowingId (int)",
                "• CreatedAt (datetime2)",
                "CK: FollowerId <> FollowingId"
            ]
        },
        "Review": {
            "title": "Review (Đánh giá Flaw-First)",
            "rect": [64, 55, 36, 25],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: ProductId (int)",
                "FK: UserId (int)",
                "• Pros (nvarchar 4000) [Ưu điểm]",
                "• Cons (nvarchar 4000) [Nhược điểm]",
                "• Rating (int, 1-5★)",
                "• IsAnonymous (bit)",
                "• IsHidden (bit)",
                "• UpvoteCount (int)",
                "• DownvoteCount (int)",
                "• CreatedAt, UpdatedAt"
            ]
        },
        "ReviewImage": {
            "title": "ReviewImage (Ảnh review)",
            "rect": [8, 32, 25, 13],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: ReviewId (int)",
                "• ImageUrl (nvarchar 500)"
            ]
        },
        "Comment": {
            "title": "Comment (Bình luận)",
            "rect": [38, 30, 26, 15],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: ReviewId (int)",
                "FK: UserId (int)",
                "• Content (nvarchar 2000)",
                "• IsAnonymous (bit)",
                "• CreatedAt (datetime2)"
            ]
        },
        "ReviewVote": {
            "title": "ReviewVote (Bình chọn)",
            "rect": [68, 30, 26, 14],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: ReviewId (int)",
                "FK: UserId (int)",
                "• IsUpvote (bit: Up/Down)",
                "• CreatedAt (datetime2)",
                "UQ: (ReviewId, UserId)"
            ]
        },
        "Bookmark": {
            "title": "Bookmark (Lưu bài)",
            "rect": [98, 30, 26, 13],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: ReviewId (int)",
                "FK: UserId (int)",
                "• CreatedAt (datetime2)",
                "UQ: (ReviewId, UserId)"
            ]
        },
        "ReviewReport": {
            "title": "ReviewReport (Báo cáo vi phạm)",
            "rect": [58, 3, 38, 18],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: ReviewId (int, Nullable)",
                "FK: ReporterId (int)",
                "FK: ResolvedByAdminId (int, Null)",
                "• Reason (nvarchar 2000)",
                "• ReviewSnapshot (nvarchar 1000)",
                "• Status (Pending/Resolved/Dismissed)",
                "• Action, CreatedAt, ResolvedAt"
            ]
        },
        "ReportEvidence": {
            "title": "ReportEvidence (Bằng chứng vi phạm)",
            "rect": [10, 5, 30, 13],
            "fields": [
                "PK: Id (int, Identity)",
                "FK: ReportId (int)",
                "• ImageUrl (nvarchar 500)"
            ]
        }
    }

    # Draw boxes
    for name, data in entities.items():
        x, y, w, h = data["rect"]
        
        # Shadow
        shadow = patches.FancyBboxPatch(
            (x + 0.35, y - 0.35), w, h,
            boxstyle="round,pad=0.2,rounding_size=0.8",
            facecolor="#94A3B8", edgecolor="none", alpha=0.35, zorder=2
        )
        ax.add_patch(shadow)

        # Entity Main Box
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.2,rounding_size=0.8",
            facecolor=COLOR_BOX_BG, edgecolor=COLOR_BORDER,
            linewidth=1.6, zorder=3
        )
        ax.add_patch(box)

        # Header background banner
        header_h = 3.6
        header_box = patches.Rectangle(
            (x, y + h - header_h), w, header_h,
            facecolor=COLOR_HEADER_BG, edgecolor=COLOR_BORDER,
            linewidth=1.2, zorder=4
        )
        ax.add_patch(header_box)

        # Header text
        ax.text(
            x + w/2, y + h - header_h/2, data["title"],
            ha="center", va="center",
            fontsize=9.2, fontweight="bold", color="#0F172A",
            fontfamily="sans-serif", zorder=5
        )

        # Entity attributes text
        attr_text = "\n".join(data["fields"])
        ax.text(
            x + 1.2, y + (h - header_h)/2 + 0.2, attr_text,
            ha="left", va="center",
            fontsize=7.6, color=COLOR_TEXT,
            fontfamily="monospace", linespacing=1.2, zorder=5
        )

    # Helper function for drawing relationship connectors
    def draw_connection(p1, p2, card1="1", card2="N", label="", rad=0.0, offset_label=(0,0)):
        # Draw curved arrow
        arrow = patches.FancyArrowPatch(
            p1, p2,
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>",
            color=COLOR_LINE,
            linewidth=1.6,
            mutation_scale=12,
            zorder=2
        )
        ax.add_patch(arrow)

        # Cardinality labels
        ax.text(
            p1[0], p1[1] + (1.2 if p1[1] >= p2[1] else -1.2), card1,
            fontsize=9, fontweight="bold", color=COLOR_CARD,
            ha="center", va="center", zorder=6,
            bbox=dict(boxstyle="circle,pad=0.18", facecolor="#FEF2F2", edgecolor="#FCA5A5", linewidth=0.8)
        )
        ax.text(
            p2[0], p2[1] + (1.2 if p2[1] >= p1[1] else -1.2), card2,
            fontsize=9, fontweight="bold", color=COLOR_CARD,
            ha="center", va="center", zorder=6,
            bbox=dict(boxstyle="circle,pad=0.18", facecolor="#EFF6FF", edgecolor="#93C5FD", linewidth=0.8)
        )

        if label:
            mx = (p1[0] + p2[0]) / 2 + offset_label[0]
            my = (p1[1] + p2[1]) / 2 + offset_label[1]
            ax.text(
                mx, my, label,
                fontsize=7.5, color="#334155", style="italic",
                ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", alpha=0.9, linewidth=0.6)
            )

    # Connections
    # 1. Category -> Product
    draw_connection((36, 102), (48, 102), "1", "N", "phân loại", rad=0)
    
    # 2. Product -> Review
    draw_connection((63, 95), (73, 80), "1", "N", "được đánh giá", rad=-0.08)

    # 3. User -> Review
    draw_connection((128, 97), (100, 75), "1", "N", "viết review", rad=0.08)

    # 4. User -> UserFollow (Follower / Following)
    draw_connection((144, 93), (144, 76), "1", "N", "Follower / Following", rad=0)

    # 5. Review -> ReviewImage
    draw_connection((64, 65), (33, 41), "1", "N", "ảnh minh chứng", rad=-0.06)

    # 6. Review -> Comment
    draw_connection((70, 55), (51, 45), "1", "N", "thảo luận", rad=-0.04)

    # 7. User -> Comment
    draw_connection((130, 93), (60, 45), "1", "N", "gửi cmt", rad=0.25, offset_label=(5, 3))

    # 8. Review -> ReviewVote
    draw_connection((80, 55), (80, 44), "1", "N", "bình chọn", rad=0)

    # 9. Review -> Bookmark
    draw_connection((92, 55), (106, 43), "1", "N", "lưu bài", rad=0.04)

    # 10. Review -> ReviewReport
    draw_connection((78, 55), (78, 21), "1", "N", "bị tố cáo", rad=-0.05)

    # 11. ReviewReport -> ReportEvidence
    draw_connection((58, 11), (40, 11), "1", "N", "ảnh bằng chứng", rad=0)

    # 12. User -> ReviewReport (Reporter & Admin)
    draw_connection((135, 93), (96, 12), "1", "N", "báo cáo / kiểm duyệt", rad=0.22, offset_label=(6, 2))

    # Document Title Block at Top
    ax.text(
        85, 117, "HÌNH 3.2. BIỂU ĐỒ QUAN HỆ THỰC THỂ (ERD) — NỀN TẢNG FLAWFIRST",
        ha="center", va="center", fontsize=13, fontweight="bold", color="#1E3A8A", fontfamily="sans-serif"
    )
    ax.text(
        85, 114, "Biểu đồ mô hình hóa 11 thực thể nghiệp vụ, chuẩn hóa 3NF và các ràng buộc toàn vẹn",
        ha="center", va="center", fontsize=9.2, style="italic", color="#475569", fontfamily="sans-serif"
    )

    out_path = r"g:\BTLWNC\FlawFirst.Api\erd_flawfirst.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()
    print("ERD diagram successfully created at:", out_path)

if __name__ == "__main__":
    generate_erd_diagram()
