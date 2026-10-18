namespace FlawFirst.Api.Models.ViewModels;

public class AdminDashboardViewModel
{
    public string Tab { get; set; } = "reports";
    public string Status { get; set; } = "Pending";
    public string Keyword { get; set; } = string.Empty;
    public PagedResult<ReportDto>? Reports { get; set; }
    public PagedResult<UserProfileDto>? Users { get; set; }
    public IReadOnlyList<CategoryDto>? Categories { get; set; }
    public UpsertCategoryRequest NewCategory { get; set; } = new();
}
