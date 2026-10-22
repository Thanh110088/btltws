namespace FlawFirst.Api.Controllers;

[Authorize(Roles = AppRoles.Admin)]
[Route("[controller]")]
public class AdminController : Controller
{
    private readonly IAdminService _admin;
    private readonly IProductCatalogService _catalog;

    public AdminController(IAdminService admin, IProductCatalogService catalog)
    {
        _admin = admin;
        _catalog = catalog;
    }

    [HttpGet("")]
    [HttpGet("Index")]
    public async Task<IActionResult> Index(
        string tab = "overview",
        string status = "Pending",
        string keyword = "",
        int? categoryId = null,
        int page = 1,
        CancellationToken cancellationToken = default)
    {
        var model = new AdminDashboardViewModel
        {
            Tab = tab,
            Status = status,
            Keyword = keyword,
            CategoryId = categoryId,
            Stats = await _admin.GetStatsAsync(cancellationToken),
            Categories = await _admin.GetCategoriesAsync(cancellationToken)
        };

        if (tab == "users")
        {
            model.Users = await _admin.GetUsersAsync(new UserListQuery
            {
                Keyword = keyword,
                Page = page,
                PageSize = 20
            }, cancellationToken);
        }
        else if (tab == "products")
        {
            model.Products = await _catalog.SearchAsync(new ProductQuery
            {
                Keyword = keyword,
                CategoryId = categoryId,
                Page = page,
                PageSize = 15,
                Sort = "newest"
            }, cancellationToken);
        }
        else if (tab == "reviews")
        {
            model.Reviews = await _admin.GetReviewsAsync(keyword, status, page, 15, cancellationToken);
        }
        else if (tab == "categories")
        {
            // Already loaded Categories in model
        }
        else if (tab == "reports")
        {
            model.Reports = await _admin.GetReportsAsync(new ReportListQuery
            {
                Status = status,
                Page = page,
                PageSize = 20
            }, cancellationToken);
        }
        else // "overview"
        {
            model.Reports = await _admin.GetReportsAsync(new ReportListQuery
            {
                Status = "Pending",
                Page = 1,
                PageSize = 5
            }, cancellationToken);
            model.Reviews = await _admin.GetReviewsAsync(null, null, 1, 5, cancellationToken);
        }

        return View(model);
    }

    [HttpPost("Moderate/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Moderate(int id, ModerateReportRequest request, CancellationToken cancellationToken)
    {
        var result = await _admin.ModerateAsync(id, User.GetUserId(), request.Action, cancellationToken);
        TempData["Success"] = result.Message;
        return RedirectToAction("Index", new { tab = "reports" });
    }

    [HttpPost("SetLock/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> SetLock(int id, SetLockRequest request, CancellationToken cancellationToken)
    {
        await _admin.SetLockAsync(id, User.GetUserId(), request.IsLocked, cancellationToken);
        TempData["Success"] = request.IsLocked ? "Đã khóa tài khoản thành công." : "Đã mở khóa tài khoản thành công.";
        return RedirectToAction("Index", new { tab = "users" });
    }

    [HttpPost("CreateCategory")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> CreateCategory(UpsertCategoryRequest request, CancellationToken cancellationToken)
    {
        if (ModelState.IsValid)
        {
            try
            {
                await _admin.CreateCategoryAsync(request, cancellationToken);
                TempData["Success"] = $"Đã thêm ngành hàng \"{request.Name}\".";
            }
            catch (AppException ex)
            {
                TempData["Error"] = ex.Message;
            }
        }
        return RedirectToAction("Index", new { tab = "categories" });
    }

    [HttpPost("UpdateCategory/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> UpdateCategory(int id, UpsertCategoryRequest request, CancellationToken cancellationToken)
    {
        if (ModelState.IsValid)
        {
            try
            {
                await _admin.UpdateCategoryAsync(id, request, cancellationToken);
                TempData["Success"] = $"Đã cập nhật ngành hàng \"{request.Name}\".";
            }
            catch (AppException ex)
            {
                TempData["Error"] = ex.Message;
            }
        }
        return RedirectToAction("Index", new { tab = "categories" });
    }

    [HttpPost("DeleteCategory/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteCategory(int id, CancellationToken cancellationToken)
    {
        try
        {
            await _admin.DeleteCategoryAsync(id, cancellationToken);
            TempData["Success"] = "Đã xóa ngành hàng.";
        }
        catch (AppException ex)
        {
            TempData["Error"] = ex.Message;
        }
        return RedirectToAction("Index", new { tab = "categories" });
    }

    [HttpPost("CreateProduct")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> CreateProduct(UpsertProductRequest request, CancellationToken cancellationToken)
    {
        if (ModelState.IsValid)
        {
            try
            {
                var p = await _admin.CreateProductAsync(request, cancellationToken);
                TempData["Success"] = $"Đã thêm sản phẩm \"{p.Name}\" thành công!";
            }
            catch (AppException ex)
            {
                TempData["Error"] = ex.Message;
            }
        }
        return RedirectToAction("Index", new { tab = "products" });
    }

    [HttpPost("UpdateProduct/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> UpdateProduct(int id, UpsertProductRequest request, CancellationToken cancellationToken)
    {
        if (ModelState.IsValid)
        {
            try
            {
                var p = await _admin.UpdateProductAsync(id, request, cancellationToken);
                TempData["Success"] = $"Đã cập nhật sản phẩm \"{p.Name}\" thành công!";
            }
            catch (AppException ex)
            {
                TempData["Error"] = ex.Message;
            }
        }
        return RedirectToAction("Index", new { tab = "products" });
    }

    [HttpPost("DeleteProduct/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteProduct(int id, CancellationToken cancellationToken)
    {
        try
        {
            await _admin.DeleteProductAsync(id, cancellationToken);
            TempData["Success"] = "Đã xóa sản phẩm thành công.";
        }
        catch (AppException ex)
        {
            TempData["Error"] = ex.Message;
        }
        return RedirectToAction("Index", new { tab = "products" });
    }

    [HttpPost("ToggleHideReview/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> ToggleHideReview(int id, string? returnTab = "reviews", CancellationToken cancellationToken = default)
    {
        await _admin.ToggleHideReviewAsync(id, cancellationToken);
        TempData["Success"] = "Đã thay đổi trạng thái hiển thị của bài review.";
        return RedirectToAction("Index", new { tab = returnTab });
    }

    [HttpPost("DeleteReview/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteReview(int id, string? returnTab = "reviews", CancellationToken cancellationToken = default)
    {
        await _admin.DeleteReviewAsync(id, cancellationToken);
        TempData["Success"] = "Đã xóa bài review thành công.";
        return RedirectToAction("Index", new { tab = returnTab });
    }
}
