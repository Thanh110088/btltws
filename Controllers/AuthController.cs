namespace FlawFirst.Api.Controllers;

[Route("[controller]")]
public class AuthController : Controller
{
    private readonly IAuthService _auth;

    public AuthController(IAuthService auth)
    {
        _auth = auth;
    }

    [AllowAnonymous]
    [HttpGet("Login")]
    public IActionResult Login(string? returnUrl = null)
    {
        if (User.Identity?.IsAuthenticated == true)
            return RedirectToAction("Index", "Products");

        ViewBag.ReturnUrl = returnUrl;
        return View(new LoginRequest());
    }

    [AllowAnonymous]
    [HttpPost("Login")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Login(LoginRequest request, string? returnUrl = null, CancellationToken cancellationToken = default)
    {
        ViewBag.ReturnUrl = returnUrl;
        if (!ModelState.IsValid)
            return View(request);

        try
        {
            var response = await _auth.LoginAsync(request, cancellationToken);
            Response.Cookies.Append("jwt_token", response.Token, new CookieOptions
            {
                HttpOnly = true,
                Secure = Request.IsHttps,
                SameSite = SameSiteMode.Lax,
                Expires = response.ExpiresAt
            });

            TempData["Success"] = $"Đăng nhập thành công! Chào mừng {response.FullName}.";
            if (!string.IsNullOrWhiteSpace(returnUrl) && Url.IsLocalUrl(returnUrl))
                return Redirect(returnUrl);

            return RedirectToAction("Index", "Products");
        }
        catch (AppException ex)
        {
            ModelState.AddModelError(string.Empty, ex.Message);
            return View(request);
        }
    }

    [AllowAnonymous]
    [HttpGet("Register")]
    public IActionResult Register()
    {
        if (User.Identity?.IsAuthenticated == true)
            return RedirectToAction("Index", "Products");

        return View(new RegisterRequest());
    }

    [AllowAnonymous]
    [HttpPost("Register")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Register(RegisterRequest request, CancellationToken cancellationToken = default)
    {
        if (!ModelState.IsValid)
            return View(request);

        try
        {
            var response = await _auth.RegisterAsync(request, cancellationToken);
            Response.Cookies.Append("jwt_token", response.Token, new CookieOptions
            {
                HttpOnly = true,
                Secure = Request.IsHttps,
                SameSite = SameSiteMode.Lax,
                Expires = response.ExpiresAt
            });

            TempData["Success"] = "Đăng ký tài khoản thành công!";
            return RedirectToAction("Index", "Products");
        }
        catch (AppException ex)
        {
            ModelState.AddModelError(string.Empty, ex.Message);
            return View(request);
        }
    }

    [HttpGet("Logout")]
    [HttpPost("Logout")]
    public IActionResult Logout()
    {
        Response.Cookies.Delete("jwt_token");
        TempData["Success"] = "Đã đăng xuất.";
        return RedirectToAction("Index", "Products");
    }

    [AllowAnonymous]
    [HttpGet("AccessDenied")]
    public IActionResult AccessDenied()
    {
        return View();
    }
}
