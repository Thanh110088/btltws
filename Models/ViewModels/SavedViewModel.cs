namespace FlawFirst.Api.Models.ViewModels;

public class SavedViewModel
{
    public string Tab { get; set; } = "bookmarks";
    public PagedResult<BookmarkDto>? Bookmarks { get; set; }
    public IReadOnlyList<FollowedUserDto>? Following { get; set; }
}
