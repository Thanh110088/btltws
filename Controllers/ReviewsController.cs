namespace FlawFirst.Api.Controllers;

[Route("[controller]")]
public class ReviewsController : Controller
{
    private readonly IReviewService _reviews;
    private readonly IProductCatalogService _catalog;
    private readonly IFileStorageService _files;

    public ReviewsController(IReviewService reviews, IProductCatalogService catalog, IFileStorageService files)
    {
        _reviews = reviews;
        _catalog = catalog;
        _files = files;
    }

    [Authorize]
    [HttpGet("Create")]
    public async Task<IActionResult> Create(int? productId, string? keyword, bool isNew = false, CancellationToken cancellationToken = default)
    {
        if (!productId.HasValue || productId.Value <= 0)
        {
            var paged = await _catalog.SearchAsync(new ProductQuery
            {
                Keyword = keyword,
                Page = 1,
                PageSize = 12,
                Sort = "newest"
            }, cancellationToken);

            var categories = await _catalog.GetCategoriesAsync(cancellationToken);
            return View("Picker", new ProductPickerViewModel
            {
                Products = paged,
                Categories = categories,
                Keyword = keyword,
                IsCreatingNew = isNew
            });
        }

        var mine = await _reviews.GetMineAsync(User.GetUserId(), new PagingQuery { Page = 1, PageSize = 50 }, cancellationToken);
        var existing = mine.Items.FirstOrDefault(item => item.ProductId == productId.Value);
        if (existing != null)
        {
            TempData["Info"] = "Bạn đã có bài đánh giá cho sản phẩm này. Hãy cập nhật nội dung bên dưới.";
            return RedirectToAction("Edit", new { id = existing.Id });
        }

        var product = await _catalog.GetDetailAsync(productId.Value, cancellationToken);
        var model = new ReviewFormViewModel
        {
            ProductId = product.Id,
            ProductName = product.Name,
            ProductBrand = product.Brand,
            Rating = 5
        };
        return View(model);
    }

    [Authorize]
    [HttpPost("Create")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(ReviewFormViewModel model, List<IFormFile>? files, CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid)
        {
            var product = await _catalog.GetDetailAsync(model.ProductId, cancellationToken);
            model.ProductName = product.Name;
            model.ProductBrand = product.Brand;
            return View(model);
        }

        try
        {
            var imageUrls = new List<string>(model.ExistingImageUrls ?? new List<string>());
            if (files != null && files.Count > 0)
            {
                var uploaded = await _files.SaveImagesAsync(files, cancellationToken);
                imageUrls.AddRange(uploaded);
            }

            var request = new CreateReviewRequest
            {
                ProductId = model.ProductId,
                Rating = model.Rating,
                Pros = model.Pros,
                Cons = model.Cons,
                IsAnonymous = model.IsAnonymous,
                ImageUrls = imageUrls
            };

            await _reviews.CreateAsync(User.GetUserId(), request, cancellationToken);
            TempData["Success"] = "Đăng bài đánh giá thành công!";
            return RedirectToAction("Details", "Products", new { id = model.ProductId });
        }
        catch (AppException ex)
        {
            ModelState.AddModelError(string.Empty, ex.Message);
            var product = await _catalog.GetDetailAsync(model.ProductId, cancellationToken);
            model.ProductName = product.Name;
            model.ProductBrand = product.Brand;
            return View(model);
        }
    }

    [Authorize]
    [HttpGet("Edit/{id:int}")]
    public async Task<IActionResult> Edit(int id, CancellationToken cancellationToken)
    {
        var review = await _reviews.GetByIdAsync(id, User.GetUserId(), User.IsInRole(AppRoles.Admin), cancellationToken);
        if (review.AuthorId != User.GetUserId() && !User.IsInRole(AppRoles.Admin))
            return Forbid();

        var product = await _catalog.GetDetailAsync(review.ProductId, cancellationToken);
        var model = new ReviewFormViewModel
        {
            ReviewId = review.Id,
            ProductId = review.ProductId,
            ProductName = product.Name,
            ProductBrand = product.Brand,
            Rating = review.Rating,
            Pros = review.Pros,
            Cons = review.Cons,
            IsAnonymous = review.IsAnonymous,
            ExistingImageUrls = review.ImageUrls.ToList()
        };
        return View(model);
    }

    [Authorize]
    [HttpPost("Edit/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, ReviewFormViewModel model, List<IFormFile>? files, CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid)
        {
            var product = await _catalog.GetDetailAsync(model.ProductId, cancellationToken);
            model.ProductName = product.Name;
            model.ProductBrand = product.Brand;
            return View(model);
        }

        try
        {
            var imageUrls = new List<string>(model.ExistingImageUrls ?? new List<string>());
            if (files != null && files.Count > 0)
            {
                var uploaded = await _files.SaveImagesAsync(files, cancellationToken);
                imageUrls.AddRange(uploaded);
            }

            var request = new UpdateReviewRequest
            {
                Rating = model.Rating,
                Pros = model.Pros,
                Cons = model.Cons,
                IsAnonymous = model.IsAnonymous,
                ImageUrls = imageUrls
            };

            await _reviews.UpdateAsync(id, User.GetUserId(), request, cancellationToken);
            TempData["Success"] = "Cập nhật bài đánh giá thành công!";
            return RedirectToAction("Details", "Products", new { id = model.ProductId });
        }
        catch (AppException ex)
        {
            ModelState.AddModelError(string.Empty, ex.Message);
            var product = await _catalog.GetDetailAsync(model.ProductId, cancellationToken);
            model.ProductName = product.Name;
            model.ProductBrand = product.Brand;
            return View(model);
        }
    }

    [Authorize]
    [HttpGet("Mine")]
    public async Task<IActionResult> Mine([FromQuery] PagingQuery query, CancellationToken cancellationToken)
    {
        var reviews = await _reviews.GetMineAsync(User.GetUserId(), query, cancellationToken);
        return View(reviews);
    }

    [Authorize]
    [HttpPost("Delete/{id:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(int id, CancellationToken cancellationToken)
    {
        await _reviews.DeleteOwnedAsync(id, User.GetUserId(), cancellationToken);
        TempData["Success"] = "Đã xóa bài đánh giá thành công.";
        return RedirectToAction("Mine");
    }
}
