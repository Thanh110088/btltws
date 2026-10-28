namespace FlawFirst.Api.Controllers;

[Route("[controller]")]
public class ProductsController : Controller
{
    private readonly IProductCatalogService _catalog;
    private readonly IAdminService _admin;

    public ProductsController(IProductCatalogService catalog, IAdminService admin)
    {
        _catalog = catalog;
        _admin = admin;
    }

    [HttpGet("")]
    [HttpGet("/")]
    [HttpGet("Index")]
    public async Task<IActionResult> Index([FromQuery] ProductQuery query, CancellationToken cancellationToken)
    {
        var products = await _catalog.SearchAsync(query, cancellationToken);
        var categories = await _catalog.GetCategoriesAsync(cancellationToken);
        var latestReviews = await _catalog.GetLatestReviewsAsync(4, cancellationToken);
        var topReviewers = await _catalog.GetTopReviewersAsync(5, cancellationToken);
        var hotTopics = await _catalog.GetHotTopicsAsync(cancellationToken);
        var (totalReviews, totalMembers) = await _catalog.GetPlatformStatsAsync(cancellationToken);
        var model = new ProductIndexViewModel
        {
            Products = products,
            Categories = categories,
            Query = query,
            LatestReviews = latestReviews,
            TopReviewers = topReviewers,
            HotTopics = hotTopics,
            TotalReviews = totalReviews,
            TotalMembers = totalMembers
        };
        return View(model);
    }

    [HttpGet("Details/{id:int}")]
    public async Task<IActionResult> Details(int id, [FromQuery] ReviewFilterQuery query, CancellationToken cancellationToken)
    {
        var product = await _catalog.GetDetailAsync(id, cancellationToken);
        var reviews = await _catalog.GetReviewsAsync(id, query, cancellationToken);
        var flaws = await _catalog.GetFlawsAsync(id, cancellationToken);

        int? currentUserId = null;
        if (User.Identity?.IsAuthenticated == true)
        {
            try { currentUserId = User.GetUserId(); } catch { }
        }

        var model = new ProductDetailViewModel
        {
            Product = product,
            Reviews = reviews,
            Flaws = flaws,
            FilterQuery = query,
            CurrentUserId = currentUserId,
            IsAdmin = User.IsInRole(AppRoles.Admin)
        };
        return View(model);
    }

    [Authorize]
    [HttpGet("Create")]
    public async Task<IActionResult> Create(string? name, CancellationToken cancellationToken)
    {
        ViewBag.Categories = await _catalog.GetCategoriesAsync(cancellationToken);
        return View(new UpsertProductRequest { Name = name ?? string.Empty });
    }

    [Authorize]
    [HttpPost("Create")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(UpsertProductRequest request, CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid)
        {
            ViewBag.Categories = await _catalog.GetCategoriesAsync(cancellationToken);
            return View(request);
        }

        try
        {
            var product = await _admin.CreateProductAsync(request, cancellationToken);
            TempData["Success"] = $"Đã thêm sản phẩm \"{product.Name}\" thành công!";
            return RedirectToAction("Create", "Reviews", new { productId = product.Id });
        }
        catch (AppException ex)
        {
            ModelState.AddModelError(string.Empty, ex.Message);
            ViewBag.Categories = await _catalog.GetCategoriesAsync(cancellationToken);
            return View(request);
        }
    }
}
