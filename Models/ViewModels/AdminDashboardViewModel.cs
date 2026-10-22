namespace FlawFirst.Api.Models.ViewModels;

public class AdminStatsDto
{
    public int TotalUsers { get; set; }
    public int TotalProducts { get; set; }
    public int TotalReviews { get; set; }
    public int TotalCategories { get; set; }
    public int PendingReports { get; set; }
    public int TotalComments { get; set; }
}

public class AdminDashboardViewModel
{
    public string Tab { get; set; } = "overview";
    public string Status { get; set; } = "Pending";
    public string Keyword { get; set; } = string.Empty;
    public int? CategoryId { get; set; }

    public AdminStatsDto Stats { get; set; } = new();

    public PagedResult<ReportDto>? Reports { get; set; }
    public PagedResult<UserProfileDto>? Users { get; set; }
    public IReadOnlyList<CategoryDto>? Categories { get; set; }
    public PagedResult<ProductListItemDto>? Products { get; set; }
    public PagedResult<ReviewDto>? Reviews { get; set; }

    public UpsertCategoryRequest NewCategory { get; set; } = new();
    public UpsertProductRequest NewProduct { get; set; } = new();
}
