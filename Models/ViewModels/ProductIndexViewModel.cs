namespace FlawFirst.Api.Models.ViewModels;

public class ProductIndexViewModel
{
    public PagedResult<ProductListItemDto> Products { get; set; } = new();
    public IReadOnlyList<CategoryDto> Categories { get; set; } = Array.Empty<CategoryDto>();
    public ProductQuery Query { get; set; } = new();
}
