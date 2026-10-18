using System.ComponentModel.DataAnnotations;

namespace FlawFirst.Api.Models.ViewModels;

public class ReviewFormViewModel
{
    public int ProductId { get; set; }
    public string ProductName { get; set; } = string.Empty;
    public string? ProductBrand { get; set; }
    public int? ReviewId { get; set; }

    [Required(ErrorMessage = "Vui lòng chọn số sao.")]
    [Range(1, 5, ErrorMessage = "Số sao phải từ 1 đến 5.")]
    public int Rating { get; set; } = 5;

    [Required(ErrorMessage = "Vui lòng nhập điểm hài lòng (Pros).")]
    [StringLength(4000, MinimumLength = 10, ErrorMessage = "Pros cần từ 10 đến 4000 ký tự.")]
    public string Pros { get; set; } = string.Empty;

    [Required(ErrorMessage = "Vui lòng nhập hạn chế thực tế (Cons).")]
    [StringLength(4000, MinimumLength = 10, ErrorMessage = "Cons cần từ 10 đến 4000 ký tự.")]
    public string Cons { get; set; } = string.Empty;

    public bool IsAnonymous { get; set; }

    public List<string> ExistingImageUrls { get; set; } = new();
}
