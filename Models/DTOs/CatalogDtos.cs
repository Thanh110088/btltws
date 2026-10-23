namespace FlawFirst.Api.Models.DTOs;

public class ProductQuery
{
    public string? Keyword { get; set; }
    public int? CategoryId { get; set; }
    public decimal? MinPrice { get; set; }
    public decimal? MaxPrice { get; set; }
    public double? MinRating { get; set; }
    public bool? HasImages { get; set; }
    public bool? VerifiedBuyer { get; set; }
    public bool? ExpertReviewer { get; set; }

    /// <summary>newest | rating | mostReviewed</summary>
    public string Sort { get; set; } = "newest";

    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 12;
}

public class ProductListItemDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Brand { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? ImageUrl { get; set; }
    public int CategoryId { get; set; }
    public string CategoryName { get; set; } = string.Empty;
    public double AvgRating { get; set; }
    public int TotalReviews { get; set; }
    public DateTime CreatedAt { get; set; }
    public string? LatestPros { get; set; }
    public string? LatestCons { get; set; }
    public string? AuthorName { get; set; }
    public int UpvoteCount { get; set; }
    public int CommentCount { get; set; }
    public DateTime? LatestReviewCreatedAt { get; set; }
    public int? LatestRating { get; set; }
}

public class StarDistributionDto
{
    public int Star1 { get; set; }
    public int Star2 { get; set; }
    public int Star3 { get; set; }
    public int Star4 { get; set; }
    public int Star5 { get; set; }
}

public class ProductDetailDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Brand { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public string? ImageUrl { get; set; }
    public int CategoryId { get; set; }
    public string CategoryName { get; set; } = string.Empty;
    public double AvgRating { get; set; }
    public int TotalReviews { get; set; }
    public StarDistributionDto StarDistribution { get; set; } = new();
    public DateTime CreatedAt { get; set; }
}

public class ReviewFilterQuery
{
    public int? Star { get; set; }
    public bool? HasImages { get; set; }

    /// <summary>newest | rating</summary>
    public string Sort { get; set; } = "newest";

    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 10;
}

public class FlawItemDto
{
    public int ReviewId { get; set; }
    public int Rating { get; set; }
    public string Cons { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}

public class FlawExtractionDto
{
    public int ProductId { get; set; }
    public string ProductName { get; set; } = string.Empty;
    public int FlawReviewCount { get; set; }
    public IReadOnlyList<FlawItemDto> Flaws { get; set; } = Array.Empty<FlawItemDto>();
}

public class CategoryDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public int ProductCount { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class TopReviewerDto
{
    public int UserId { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string AvatarInitial => !string.IsNullOrWhiteSpace(FullName) ? FullName.Trim().Substring(0, 1).ToUpper() : "U";
    public int ReviewCount { get; set; }
    public int TotalLikes { get; set; }
}

public class CategoryTopicDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public int ProductCount { get; set; }
    public int ReviewCount { get; set; }
}
