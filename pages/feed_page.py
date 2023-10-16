from playwright.sync_api import Page


class FeedPage:
    def __init__(self, page: Page):
        self.page = page
        self.main_header = page.get_by_role("heading", name="conduit")
        self.your_feed_link = page.get_by_role("link", name="Your Feed")
        self.global_feed_link = page.get_by_role("link", name="Global Feed")
        self.popular_tags_list = page.locator(".sidebar > .tag-list")
        self.tag_items = page.locator(".tag-pill")
        self.article_items = page.locator(".article-preview")
        self.article_favorite_button = page.get_by_role(
            "button", name="Toggle Favorite"
        )
        self.article_details_link = page.locator("h1")
        self.article_author_link = page.locator("a.author").first
        self.pagination_pages = page.get_by_label("Go to page number")
