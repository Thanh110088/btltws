using System.Security.Claims;
using System.Text;
using FlawFirst.Api.Common;
using FlawFirst.Api.Data;
using FlawFirst.Api.Middleware;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? throw new InvalidOperationException("Thiếu ConnectionStrings:DefaultConnection.");

var jwtSection = builder.Configuration.GetSection(JwtOptions.SectionName);
var jwt = jwtSection.Get<JwtOptions>() ?? throw new InvalidOperationException("Thiếu cấu hình Jwt.");
if (string.IsNullOrWhiteSpace(jwt.Key) || Encoding.UTF8.GetByteCount(jwt.Key) < 32)
    throw new InvalidOperationException("Jwt:Key phải dài ít nhất 32 bytes.");

builder.Services.Configure<JwtOptions>(jwtSection);
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString).EnableDetailedErrors(builder.Environment.IsDevelopment()));

builder.Services.AddScoped<IJwtTokenService, JwtTokenService>();
builder.Services.AddSingleton<IProfanityFilter, ProfanityFilter>();
builder.Services.AddScoped<IFileStorageService, FileStorageService>();
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IProductCatalogService, ProductCatalogService>();
builder.Services.AddScoped<IReviewService, ReviewService>();
builder.Services.AddScoped<ISocialService, SocialService>();
builder.Services.AddScoped<IAdminService, AdminService>();
builder.Services.AddSingleton<IAuthorizationMiddlewareResultHandler, FriendlyAuthorizationResultHandler>();

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateIssuerSigningKey = true,
            ValidateLifetime = true,
            ValidIssuer = jwt.Issuer,
            ValidAudience = jwt.Audience,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwt.Key)),
            ClockSkew = TimeSpan.FromMinutes(1),
            RoleClaimType = ClaimTypes.Role,
            NameClaimType = ClaimTypes.NameIdentifier
        };

        options.Events = new JwtBearerEvents
        {
            OnMessageReceived = context =>
            {
                var token = context.Request.Headers.Authorization.FirstOrDefault()?.Split(" ").Last();
                if (string.IsNullOrEmpty(token) && context.Request.Cookies.TryGetValue("jwt_token", out var cookieToken))
                {
                    token = cookieToken;
                }
                context.Token = token;
                return Task.CompletedTask;
            }
        };
    });

builder.Services.AddAuthorization();
builder.Services.AddControllersWithViews();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Home/Error");
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();

if (app.Environment.IsDevelopment())
    app.UseMiddleware<MockAuthMiddleware>();

app.UseMiddleware<LockedAccountMiddleware>();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Products}/{action=Index}/{id?}");

app.MapGet("/health", () => Results.Ok(new { status = "ok", service = "FlawFirst.Api" }));

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    var logger = scope.ServiceProvider.GetRequiredService<ILoggerFactory>().CreateLogger("Startup");
    try
    {
        await db.Database.MigrateAsync();
        await DbSeeder.SeedAsync(db);
        logger.LogInformation("FlawFirstDb đã sẵn sàng.");
    }
    catch (Exception exception)
    {
        logger.LogCritical(exception, "Không migrate được SQL Server. Hãy mở SSMS và kiểm tra connection string FlawFirstDb.");
        throw;
    }
}

app.Run();
