namespace FlawFirst.Api.Models.ViewModels;

public class ProductPickerViewModel
{
    public PagedResult<ProductListItemDto> Products { get; set; } = new();
    public IReadOnlyList<CategoryDto> Categories { get; set; } = Array.Empty<CategoryDto>();
    public string? Keyword { get; set; }
    public bool IsCreatingNew { get; set; }
    public UpsertProductRequest NewProduct { get; set; } = new();
}
