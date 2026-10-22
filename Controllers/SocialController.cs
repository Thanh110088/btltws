using FlawFirst.Api.Common;

namespace FlawFirst.Api.Controllers;

[Route("[controller]")]
public class SocialController : Controller
{
    private readonly ISocialService _social;
    private readonly IFileStorageService _files;

    public SocialController(ISocialService social, IFileStorageService files)
    {
        _social = social;
        _files = files;
    }

    [Authorize]
    [HttpGet("Saved")]
    public async Task<IActionResult> Saved(string tab = "bookmarks", int page = 1, CancellationToken cancellationToken = default)
    {
        var model = new SavedViewModel { Tab = tab };
        var baseUrl = $"{Request.Scheme}://{Request.Host}";

        if (tab == "following")
        {
            model.Following = await _social.GetFollowingAsync(User.GetUserId(), cancellationToken);
        }
        else
        {
            model.Bookmarks = await _social.GetBookmarksAsync(User.GetUserId(), new PagingQuery { Page = page, PageSize = 10 }, baseUrl, cancellationToken);
        }

        return View(model);
    }

    [AllowAnonymous]
    [HttpGet("UserProfile/{id:int}")]
    public async Task<IActionResult> UserProfile(int id, CancellationToken cancellationToken)
    {
        int? viewerId = null;
        if (User.Identity?.IsAuthenticated == true)
        {
            try { viewerId = User.GetUserId(); } catch { }
        }

        var profile = await _social.GetPublicProfileAsync(id, viewerId, cancellationToken);
        return View(profile);
    }

    [Authorize]
    [HttpPost("Vote")]
    public async Task<IActionResult> Vote(int reviewId, string voteType, string? returnUrl = null, CancellationToken cancellationToken = default)
    {
        var result = await _social.VoteAsync(reviewId, User.GetUserId(), voteType, cancellationToken);
        if (IsAjax())
            return Json(result);

        return Redirect(returnUrl ?? "/");
    }

    [Authorize]
    [HttpPost("Bookmark")]
    public async Task<IActionResult> Bookmark(int reviewId, bool remove = false, string? returnUrl = null, CancellationToken cancellationToken = default)
    {
        var baseUrl = $"{Request.Scheme}://{Request.Host}";
        if (remove)
        {
            await _social.RemoveBookmarkAsync(reviewId, User.GetUserId(), cancellationToken);
            if (IsAjax()) return Json(new { bookmarked = false });
        }
        else
        {
            await _social.BookmarkAsync(reviewId, User.GetUserId(), baseUrl, cancellationToken);
            if (IsAjax()) return Json(new { bookmarked = true });
        }

        return Redirect(returnUrl ?? "/Social/Saved");
    }

    [Authorize]
    [HttpPost("Comment")]
    public async Task<IActionResult> Comment(int reviewId, CreateCommentRequest request, string? returnUrl = null, CancellationToken cancellationToken = default)
    {
        if (!ModelState.IsValid)
        {
            if (IsAjax())
                return BadRequest(ModelState);
            TempData["Error"] = "Vui lòng nhập nội dung bình luận.";
            return Redirect(returnUrl ?? "/");
        }

        var comment = await _social.AddCommentAsync(reviewId, User.GetUserId(), request, cancellationToken);
        if (IsAjax())
            return Json(new { success = true, comment });

        TempData["Success"] = "Đã gửi bình luận!";
        return Redirect(returnUrl ?? "/");
    }

    [Authorize]
    [HttpPost("DeleteComment/{id:int}")]
    public async Task<IActionResult> DeleteComment(int id, string? returnUrl = null, CancellationToken cancellationToken = default)
    {
        var isAdmin = User.IsInRole(AppRoles.Admin);
        await _social.DeleteCommentAsync(id, User.GetUserId(), isAdmin, cancellationToken);
        if (IsAjax())
            return Json(new { success = true, id });

        TempData["Success"] = "Đã xóa bình luận!";
        return Redirect(returnUrl ?? "/");
    }

    [Authorize]
    [HttpPost("Follow")]
    public async Task<IActionResult> Follow(int userId, bool unfollow = false, string? returnUrl = null, CancellationToken cancellationToken = default)
    {
        if (unfollow)
        {
            await _social.UnfollowAsync(User.GetUserId(), userId, cancellationToken);
            TempData["Success"] = "Đã bỏ theo dõi.";
        }
        else
        {
            await _social.FollowAsync(User.GetUserId(), userId, cancellationToken);
            TempData["Success"] = "Đang theo dõi người dùng này.";
        }

        return Redirect(returnUrl ?? $"/Social/UserProfile/{userId}");
    }

    [Authorize]
    [HttpPost("Report")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Report(CreateReportRequest request, List<IFormFile>? files, string? returnUrl = null, CancellationToken cancellationToken = default)
    {
        if (files != null && files.Count > 0)
        {
            var urls = await _files.SaveImagesAsync(files, cancellationToken);
            request.EvidenceImageUrls = urls.ToList();
        }

        if (ModelState.IsValid)
        {
            await _social.CreateReportAsync(User.GetUserId(), request, cancellationToken);
            TempData["Success"] = "Cảm ơn bạn đã báo cáo vi phạm. Quản trị viên sẽ xem xét sớm.";
        }

        return Redirect(returnUrl ?? "/");
    }

    [AllowAnonymous]
    [HttpGet("Comments/{reviewId:int}")]
    public async Task<IActionResult> Comments(int reviewId, int page = 1, CancellationToken cancellationToken = default)
    {
        var comments = await _social.GetCommentsAsync(reviewId, new PagingQuery { Page = page, PageSize = 20 }, cancellationToken);
        return Json(comments);
    }

    private bool IsAjax()
    {
        return string.Equals(Request.Headers["X-Requested-With"], "XMLHttpRequest", StringComparison.OrdinalIgnoreCase)
            || Request.Headers.Accept.ToString().Contains("application/json");
    }
}
