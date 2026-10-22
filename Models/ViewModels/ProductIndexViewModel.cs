namespace FlawFirst.Api.Models.ViewModels;

public class ProductIndexViewModel
{
    public PagedResult<ProductListItemDto> Products { get; set; } = new();
    public IReadOnlyList<CategoryDto> Categories { get; set; } = Array.Empty<CategoryDto>();
    public ProductQuery Query { get; set; } = new();
    public IReadOnlyList<ReviewDto> LatestReviews { get; set; } = Array.Empty<ReviewDto>();
    public IReadOnlyList<TopReviewerDto> TopReviewers { get; set; } = Array.Empty<TopReviewerDto>();
    public IReadOnlyList<CategoryTopicDto> HotTopics { get; set; } = Array.Empty<CategoryTopicDto>();
    public int TotalReviews { get; set; }
    public int TotalMembers { get; set; }
}
