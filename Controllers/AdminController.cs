namespace FlawFirst.Api.Controllers;

[Authorize(Roles = AppRoles.Admin)]
[Route("[controller]")]
public class AdminController : Controller
{
    private readonly IAdminService _admin;

    public AdminController(IAdminService admin)
    {
        _admin = admin;
    }

    [HttpGet("")]
    [HttpGet("Index")]
    public async Task<IActionResult> Index(
        string tab = "reports",
        string status = "Pending",
        string keyword = "",
        int page = 1,
        CancellationToken cancellationToken = default)
    {
        var model = new AdminDashboardViewModel
        {
            Tab = tab,
            Status = status,
            Keyword = keyword
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
        else if (tab == "categories")
        {
            model.Categories = await _admin.GetCategoriesAsync(cancellationToken);
        }
        else
        {
            model.Reports = await _admin.GetReportsAsync(new ReportListQuery
            {
                Status = status,
                Page = page,
                PageSize = 20
            }, cancellationToken);
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
}
