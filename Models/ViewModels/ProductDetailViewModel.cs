namespace FlawFirst.Api.Models.ViewModels;

public class ProductDetailViewModel
{
    public ProductDetailDto Product { get; set; } = new();
    public PagedResult<ReviewDto> Reviews { get; set; } = new();
    public FlawExtractionDto Flaws { get; set; } = new();
    public ReviewFilterQuery FilterQuery { get; set; } = new();
    public int? CurrentUserId { get; set; }
    public bool IsAdmin { get; set; }
}
