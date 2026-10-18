# TÀI LIỆU HƯỚNG DẪN KIẾN TRÚC & PHÁT TRIỂN CHỨC NĂNG
## Dự án FlawFirst — Nền tảng đánh giá sản phẩm bóc tách ưu và nhược điểm (ASP.NET Core MVC)

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG (ASP.NET CORE MVC)

Dự án được xây dựng theo chuẩn mô hình **Model - View - Controller (MVC)** kết hợp với **Service Layer** trong ASP.NET Core .NET 9.

### Luồng xử lý một chức năng (Request Lifecycle)
```text
Trình duyệt (Browser)
       │  HTTP Request (GET / POST)
       ▼
Controllers/ (Tiếp nhận request, kiểm tra ModelState)
       │  Gọi hàm nghiệp vụ
       ▼
Services/ (Xử lý logic, tính toán điểm số, băm mật khẩu, validate nghiệp vụ)
       │  Truy vấn CSDL qua EF Core
       ▼
Data/ (AppDbContext) ──► CSDL SQL Server (FlawFirstDb)
       │  Trả về dữ liệu Entities
       ▼
Models/ViewModels/ & Models/DTOs/ (Gói dữ liệu trả về cho View)
       │  Truyền Model vào View
       ▼
Views/ (*.cshtml) (Razor Server-Side Rendering sinh mã HTML)
       │  HTTP Response (HTML/CSS)
       ▼
Trình duyệt hiển thị cho người dùng
```

---

## 2. BẢN ĐỒ TỆP TIN THEO TỪNG MODULE

### 🛒 Module 1: Product (Sản phẩm)
Quản lý thông tin sản phẩm, tìm kiếm, lọc theo giá và ngành hàng, hiển thị chi tiết và thống kê số sao.

* **Database Entity**:
  * [Product.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/Product.cs): Khai báo bảng `Products` (`Id`, `Name`, `Brand`, `Price`, `CategoryId`, `ImageUrl`, `Description`, `CreatedAt`).
* **DTOs & Form Requests**:
  * [CatalogDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/CatalogDtos.cs):
    * `ProductQuery`: Chứa các tham số lọc tìm kiếm (`Keyword`, `CategoryId`, `MinPrice`, `MaxPrice`, `Sort`, `Page`, `PageSize`).
    * `ProductListItemDto`: Dữ liệu tóm tắt sản phẩm để hiển thị lưới.
    * `ProductDetailDto`: Dữ liệu chi tiết sản phẩm kèm `StarDistribution` (thống kê phân bố 1–5 sao).
    * `FlawExtractionDto` & `FlawItemDto`: Danh sách các hạn chế thực tế trích xuất từ đánh giá 1–2 sao.
  * [AdminDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/AdminDtos.cs):
    * `UpsertProductRequest`: Form dữ liệu khi thêm mới sản phẩm.
* **ViewModels**:
  * [ProductIndexViewModel.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ViewModels/ProductIndexViewModel.cs): Gói danh sách sản phẩm phân trang, danh sách ngành hàng và bộ lọc hiện tại.
  * [ProductDetailViewModel.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ViewModels/ProductDetailViewModel.cs): Gói chi tiết sản phẩm, danh sách review, cụm Flaw-first và quyền tác giả/admin.
  * [ProductPickerViewModel.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ViewModels/ProductPickerViewModel.cs): Gói dữ liệu khi chọn sản phẩm để viết review.
* **Service (Nghiệp vụ)**:
  * [ProductCatalogService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/ProductCatalogService.cs) (`IProductCatalogService`):
    * `SearchAsync()`: Lọc sản phẩm theo từ khóa, ngành hàng, khoảng giá, sắp xếp theo sao hoặc ngày tạo.
    * `GetDetailAsync()`: Lấy thông tin chi tiết kèm phân bố tỷ lệ sao.
    * `GetFlawsAsync()`: Gom toàn bộ review 1–2 sao để bóc tách Cons thực tế.
    * `GetReviewsAsync()`: Lấy danh sách review có lọc theo số sao hoặc có ảnh.
* **Controller**:
  * [ProductsController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/ProductsController.cs):
    * `GET /Products` (hoặc `/`): Trang chủ khám phá sản phẩm.
    * `GET /Products/Details/{id}`: Xem chi tiết sản phẩm, điểm hạn chế Flaw-First và đánh giá cộng đồng.
    * `GET /Products/Create` & `POST /Products/Create`: Form thêm sản phẩm mới.
* **Views (.cshtml)**:
  * [Index.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Index.cshtml): Giao diện banner Hero, bộ lọc chip ngành hàng, lọc giá và lưới sản phẩm.
  * [Details.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Details.cshtml): Giao diện chi tiết sản phẩm, thanh tỷ lệ 5 sao, khối Flaw-First màu nóng, bộ lọc review.
  * [Create.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Create.cshtml): Form nhập thông tin thêm sản phẩm mới.
  * [_ProductCard.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Shared/_ProductCard.cshtml): Thẻ sản phẩm tái sử dụng.

---

### 🏷️ Module 2: Category (Ngành hàng)
Danh mục phân loại sản phẩm.

* **Database Entity**:
  * [Category.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/Category.cs): Bảng `Categories` (`Id`, `Name`, `Description`, `CreatedAt`).
* **DTOs**:
  * [CatalogDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/CatalogDtos.cs): `CategoryDto` (`Id`, `Name`, `Description`, `ProductCount`).
  * [AdminDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/AdminDtos.cs): `UpsertCategoryRequest` (`Name`, `Description`).
* **Service**:
  * [ProductCatalogService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/ProductCatalogService.cs): `GetCategoriesAsync()` (lấy danh sách ngành hàng để hiển thị bộ lọc).
  * [AdminService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/AdminService.cs): `CreateCategoryAsync()`, `DeleteCategoryAsync()` (chỉ cho phép xóa khi `ProductCount == 0`).
* **Controller**:
  * [AdminController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/AdminController.cs): Tiếp nhận tạo mới và xóa ngành hàng.
* **Views (.cshtml)**:
  * [Index.cshtml (Admin)](file:///g:/BTLWNC/FlawFirst.Api/Views/Admin/Index.cshtml): Tab Quản lý ngành hàng.
  * [Index.cshtml (Products)](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Index.cshtml): Các nút chip lọc ngành hàng.

---

### 👤 Module 3: User & Auth (Người dùng & Phân quyền)
Đăng ký, đăng nhập qua JWT lưu Cookie, phân quyền `User` / `Admin`, xem thông tin cá nhân.

* **Database Entities**:
  * [User.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/User.cs): Bảng `Users` (`Id`, `FullName`, `Email`, `PasswordHash`, `Role`, `IsLocked`, `CreatedAt`).
  * [UserFollow.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/UserFollow.cs): Bảng theo dõi tác giả giữa các thành viên.
* **DTOs**:
  * [AuthDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/AuthDtos.cs): `LoginRequest`, `RegisterRequest`, `AuthResponse`, `UserProfileDto`.
  * [AdminDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/AdminDtos.cs): `UserListQuery`, `SetLockRequest`.
* **Services**:
  * [AuthService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/AuthService.cs) (`IAuthService`): Băm và kiểm tra mật khẩu bằng BCrypt, tạo tài khoản mới.
  * [JwtTokenService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/JwtTokenService.cs) (`IJwtTokenService`): Sinh JWT token hạn 7 ngày chứa `NameIdentifier`, `Email`, `Role`.
* **Middlewares**:
  * [LockedAccountMiddleware.cs](file:///g:/BTLWNC/FlawFirst.Api/Infrastructure/Middleware/LockedAccountMiddleware.cs): Tự động phát hiện tài khoản bị khóa để thu hồi cookie và chuyển hướng về đăng nhập.
  * [FriendlyAuthorizationResultHandler.cs](file:///g:/BTLWNC/FlawFirst.Api/Infrastructure/Middleware/FriendlyAuthorizationResultHandler.cs): Tự động chuyển hướng yêu cầu chưa đăng nhập về `/Auth/Login?returnUrl=...`.
* **Controller**:
  * [AuthController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/AuthController.cs):
    * `GET /Auth/Login` & `POST /Auth/Login`: Đăng nhập, lưu cookie `jwt_token`.
    * `GET /Auth/Register` & `POST /Auth/Register`: Đăng ký tài khoản mới.
    * `GET /Auth/Logout`: Xóa cookie `jwt_token`, đăng xuất.
    * `GET /Auth/AccessDenied`: Trang báo không đủ quyền.
  * [AdminController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/AdminController.cs):
    * `POST /Admin/SetLock/{id}`: Khóa hoặc mở khóa tài khoản người dùng.
* **Views (.cshtml)**:
  * [Login.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Auth/Login.cshtml): Form đăng nhập có 2 nút bấm tự điền nhanh tài khoản Admin/User.
  * [Register.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Auth/Register.cshtml): Form tạo tài khoản.
  * [AccessDenied.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Auth/AccessDenied.cshtml): Thông báo không đủ quyền.
  * [UserProfile.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Social/UserProfile.cshtml): Xem hồ sơ tác giả, số người theo dõi và nút Theo dõi / Bỏ theo dõi.

---

### ⭐ Module 4: Review (Đánh giá Flaw-First)
Trọng tâm đồ án: Đánh giá bóc tách điểm hài lòng (Pros) và hạn chế thực tế (Cons), chọn số sao 1–5, đăng ẩn danh, upload ảnh minh chứng, quản lý bài viết của tôi.

* **Database Entities**:
  * [Review.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/Review.cs): Bảng `Reviews` (`ProductId`, `AuthorId`, `Rating`, `Pros`, `Cons`, `IsAnonymous`, `IsHidden`, `UpvoteCount`, `DownvoteCount`, `CommentCount`).
  * [ReviewImage.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ReviewImage.cs): Lưu đường dẫn ảnh đính kèm bài review.
* **DTOs & ViewModels**:
  * [ReviewDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/ReviewDtos.cs): `CreateReviewRequest`, `UpdateReviewRequest`, `ReviewDto`, `PagingQuery`.
  * [ReviewFormViewModel.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ViewModels/ReviewFormViewModel.cs): Dữ liệu truyền cho Form viết và sửa review.
* **Services**:
  * [ReviewService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/ReviewService.cs) (`IReviewService`): Lưu đánh giá, kiểm tra trùng lặp bài viết trên cùng sản phẩm, cập nhật và xóa bài thuộc sở hữu của người dùng.
  * [ProfanityFilter.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/ProfanityFilter.cs) (`IProfanityFilter`): Lọc và chặn từ ngữ thô tục trong Pros và Cons.
  * [FileStorageService.cs](file:///g:/BTLWNC/FlawFirst.Api/Infrastructure/FileStorageService.cs) (`IFileStorageService`): Lưu ảnh minh chứng vào thư mục `wwwroot/uploads`.
* **Controller**:
  * [ReviewsController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/ReviewsController.cs):
    * `GET /Reviews/Create`: Nếu chưa chọn sản phẩm thì chuyển đến Picker; nếu đã chọn thì mở form viết review (hoặc tự động chuyển sang Edit nếu người dùng đã có bài).
    * `POST /Reviews/Create`: Xử lý đăng bài và lưu ảnh.
    * `GET /Reviews/Edit/{id}` & `POST /Reviews/Edit/{id}`: Chỉnh sửa bài review.
    * `GET /Reviews/Mine`: Xem toàn bộ bài viết của chính mình.
    * `POST /Reviews/Delete/{id}`: Xóa bài viết của chính mình.
* **Views (.cshtml)**:
  * [Picker.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Reviews/Picker.cshtml): Chọn sản phẩm hoặc thêm sản phẩm mới để review.
  * [Create.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Reviews/Create.cshtml): Form viết đánh giá với picker 5 sao tương tác.
  * [Edit.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Reviews/Edit.cshtml): Form sửa review (có nút xóa ảnh cũ và upload ảnh mới).
  * [Mine.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Reviews/Mine.cshtml): Danh sách bài của tôi kèm nút Sửa và Xóa.
  * [_ReviewCard.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Shared/_ReviewCard.cshtml): Card bài review dùng chung trên toàn hệ thống.

---

### 💬 Module 5: Social & Tương tác
Bình luận, Upvote/Downvote, Bookmark lưu bài, Báo cáo vi phạm (Report).

* **Database Entities**:
  * [Comment.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/Comment.cs)
  * [ReviewVote.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ReviewVote.cs)
  * [Bookmark.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/Bookmark.cs)
  * [ReviewReport.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ReviewReport.cs) & [ReportEvidence.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ReportEvidence.cs)
* **DTOs & ViewModel**:
  * [SocialDtos.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/DTOs/SocialDtos.cs): `CreateCommentRequest`, `CommentDto`, `VoteRequest`, `BookmarkDto`, `CreateReportRequest`...
  * [SavedViewModel.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ViewModels/SavedViewModel.cs): Quản lý 2 tab "Đã lưu" và "Đang theo dõi".
* **Service**:
  * [SocialService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/SocialService.cs) (`ISocialService`): Xử lý vote chuyển trạng thái, bookmark bài viết, lưu báo cáo vi phạm.
* **Controller**:
  * [SocialController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/SocialController.cs):
    * `GET /Social/Saved`: Trang xem bài đã lưu & tác giả đang theo dõi.
    * `POST /Social/Vote`: Upvote / Downvote (hỗ trợ cả AJAX mượt mà không reload).
    * `POST /Social/Bookmark`: Lưu / Bỏ lưu bài review.
    * `POST /Social/Comment`: Bình luận vào bài review.
    * `POST /Social/Report`: Gửi báo cáo vi phạm kèm ảnh bằng chứng.
* **Views (.cshtml)**:
  * [Saved.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Social/Saved.cshtml)
  * [_ReviewCard.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Shared/_ReviewCard.cshtml) (Chứa các nút thao tác tương tác)

---

### 🛡️ Module 6: Admin (Quản trị & Kiểm duyệt)
* **Controller**: [AdminController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/AdminController.cs)
* **Service**: [AdminService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/AdminService.cs)
* **ViewModel**: [AdminDashboardViewModel.cs](file:///g:/BTLWNC/FlawFirst.Api/Models/ViewModels/AdminDashboardViewModel.cs)
* **View**: [Index.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Admin/Index.cshtml)
  * **Tab 1: Kiểm duyệt báo cáo**: Xem danh sách bài vi phạm, có 4 nút hành động: *Ẩn bài*, *Xóa bài*, *Phạt & Khóa tác giả*, *Bỏ qua*.
  * **Tab 2: Quản lý người dùng**: Tìm kiếm tài khoản, Khóa / Mở khóa tài khoản.
  * **Tab 3: Quản lý ngành hàng**: Thêm ngành hàng mới, Xóa ngành hàng rỗng.

---

---

## 3. LỘ TRÌNH THỰC HIỆN ƯU TIÊN (THEO YÊU CẦU: LÀM TRƯỚC CHO NGƯỜI DÙNG & TRANG KHÁM PHÁ)

> **Lưu ý cốt lõi**: Toàn bộ chức năng Quản trị (Admin) được **tạm gác lại làm sau cùng**. Trọng tâm giai đoạn đầu là các chức năng dễ làm, trực quan nhất dành cho **Người Dùng (End-user)**, bắt đầu ngay tại **Trang Khám Phá (`/Products` hoặc `/`)**.

### 🟢 GIAI ĐOẠN 1: CÁC CHỨC NĂNG DỄ LÀM NHẤT TRÊN TRANG KHÁM PHÁ (ƯU TIÊN SỐ 1)
Toàn bộ các chức năng này đã được triển khai sẵn sàng và chạy mượt mà trên giao diện Razor `.cshtml`:

1. **Lọc theo Danh mục (Category Chips)**:
   * Bấm vào các chip danh mục (*Tất cả, Điện thoại, Laptop, Mỹ phẩm, Gia dụng*). Thẻ đang chọn tự sáng highlight.
   * *Tệp tin liên quan*: [Views/Products/Index.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Index.cshtml#L26-L48)
2. **Tìm kiếm theo Từ khóa (Search Keyword)**:
   * Nhập tên máy (*iPhone, Galaxy, MacBook...*) hoặc tên hãng vào ô tìm kiếm.
   * *Tệp tin liên quan*: [ProductsController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/ProductsController.cs#L18-L29), [ProductCatalogService.cs](file:///g:/BTLWNC/FlawFirst.Api/Services/ProductCatalogService.cs#L34-L41)
3. **Lọc nhanh khoảng giá (Quick Price Ranges)**:
   * Bấm 1 chạm chọn nhanh các mốc: **Dưới 5 triệu**, **5 – 15 triệu**, **15 – 30 triệu**, **Trên 30 triệu** (không cần gõ số thủ công).
   * Kèm 2 ô nhập tùy chỉnh `minPrice` - `maxPrice` cho người dùng muốn tìm giá chính xác.
   * *Tệp tin liên quan*: [Views/Products/Index.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Index.cshtml#L50-L63)
4. **Sắp xếp linh hoạt & Tự động áp dụng (Instant Sort)**:
   * Chọn *Mới nhất*, *Số sao cao nhất*, *Nhiều bài review nhất*. Đã gắn `onchange="this.form.submit()"` để trang tự động tải lại ngay lập tức khi đổi lựa chọn.
   * *Tệp tin liên quan*: [Views/Products/Index.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Index.cshtml#L70-L77)
5. **Thẻ sản phẩm trực quan (Product Card UI)**:
   * Hiển thị: Avatar/ảnh màu sắc, Tên hãng + Danh mục, Tên sản phẩm, Giá định dạng chuẩn (`22.990.000 ₫`), Số sao vẽ bằng SVG (1–5 sao), Tổng số lượt review.
   * *Tệp tin liên quan*: [Views/Shared/_ProductCard.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Shared/_ProductCard.cshtml)
6. **Nút "Viết đánh giá" trực tiếp trên Thẻ**:
   * Bấm nút "Viết đánh giá" ngay trên thẻ sản phẩm ở Trang Khám Phá sẽ dẫn thẳng vào form review với sản phẩm đã được chọn sẵn (`/Reviews/Create?productId=...`).
   * *Tệp tin liên quan*: [Views/Shared/_ProductCard.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Shared/_ProductCard.cshtml#L38)
7. **Đặt lại bộ lọc (1-Click Reset)**:
   * Hiển thị thông báo *"Tìm thấy X sản phẩm"* và nút `✕ Đặt lại bộ lọc` để xóa sạch query chỉ với 1 click.
   * *Tệp tin liên quan*: [Views/Products/Index.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Index.cshtml#L91-L107)
8. **Phân trang (Pagination)**:
   * Phân chia 12 sản phẩm/trang, chuyển trang vẫn giữ nguyên từ khóa, danh mục và khoảng giá đang chọn.
   * *Tệp tin liên quan*: [Views/Shared/_Pager.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Shared/_Pager.cshtml)

---

### 🟡 GIAI ĐOẠN 2: XEM CHI TIẾT SẢN PHẨM & BÓC TÁCH ĐÁNH GIÁ (ƯU TIÊN SỐ 2)
1. **Xem trang chi tiết sản phẩm**:
   * Mở [ProductsController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/ProductsController.cs#L31-L54) action `Details(int id, ReviewFilterQuery query)`.
   * Mở [Views/Products/Details.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Products/Details.cshtml).
2. **Các tính năng người dùng tại trang này**:
   * Biểu đồ tỷ lệ 5 sao trực quan (Star Distribution).
   * Khối **Flaw-First** trích xuất toàn bộ hạn chế thực tế (Cons) từ các bài đánh giá 1–2 sao.
   * Lọc danh sách đánh giá theo số sao (1 sao đến 5 sao) hoặc lọc bài có hình ảnh thực tế.

---

### 🟠 GIAI ĐOẠN 3: VIẾT ĐÁNH GIÁ & ĐĂNG NHẬP NGƯỜI DÙNG (ƯU TIÊN SỐ 3)
1. **Đăng nhập & Đăng ký**:
   * Mở [Views/Auth/Login.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Auth/Login.cshtml) và [AuthController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/AuthController.cs).
   * Hỗ trợ nút click 1 chạm để điền tài khoản mẫu. Token lưu tự động vào HTTP-only cookie.
2. **Viết đánh giá bóc tách Flaw-First**:
   * Mở [Views/Reviews/Create.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Reviews/Create.cshtml) và [ReviewsController.cs](file:///g:/BTLWNC/FlawFirst.Api/Controllers/ReviewsController.cs).
   * Nhập tách biệt: Điểm hài lòng (Pros) và Hạn chế thực tế (Cons).
   * Hỗ trợ tùy chọn **Đăng ẩn danh** (ẩn họ tên, email).
3. **Quản lý bài viết của tôi**:
   * Mở [Views/Reviews/Mine.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Reviews/Mine.cshtml) xem lại các bài đã viết, sửa bài hoặc xóa bài.

---

### 🔵 GIAI ĐOẠN 4: TƯƠNG TÁC CỘNG ĐỒNG NHẸ NHÀNG (ƯU TIÊN SỐ 4)
* **Bấm Hữu ích / Không hữu ích (Vote Up/Down)** trên từng review (Ajax cập nhật số lượt ngay không load lại trang).
* **Lưu bài review (Bookmark)** để xem lại trong trang [Views/Social/Saved.cshtml](file:///g:/BTLWNC/FlawFirst.Api/Views/Social/Saved.cshtml).
* **Bình luận trao đổi** dưới từng bài đánh giá.

---

### ⚪ GIAI ĐOẠN 5: CHỨC NĂNG ADMIN & KIỂM DUYỆT (LÀM SAU CÙNG)
*(Chỉ bắt đầu làm sau khi các luồng người dùng trên đã hoàn tất và kiểm thử trơn tru)*
* Quản trị báo cáo vi phạm, ẩn/xóa bài đánh giá tiêu cực vi phạm quy tắc.
* Khóa / mở khóa tài khoản thành viên vi phạm.
* Quản lý tạo mới và xóa ngành hàng.

---

## 4. TÀI KHOẢN SEED SẴN ĐỂ TEST
Hệ thống đã tự động seed dữ liệu mẫu trong CSDL SQL Server:
* **Quản trị viên (Admin)**: `admin@flawfirst.local` / Mật khẩu: `Admin@123`
* **Người dùng 1 (User)**: `user@flawfirst.local` / Mật khẩu: `User@123`
* **Người dùng 2 (User)**: `binh.tran@flawfirst.local` / Mật khẩu: `User@123`
* **Người dùng 3 (User)**: `chi.le@flawfirst.local` / Mật khẩu: `User@123`

