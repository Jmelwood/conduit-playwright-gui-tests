import re
import pytest
from playwright.sync_api import Page, expect
from mimesis import Numeric

from pages.feed_page import FeedPage


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.goto("/#/")
    yield


def test_global_feed_loads_articles(page: Page):
    feed_page = FeedPage(page)
    feed_page.global_feed_link.click()
    expect(feed_page.article_items.first).to_be_visible()


def test_selecting_tag_filters_articles(page: Page):
    feed_page = FeedPage(page)
    # Pick a random tag from the popular tags list
    numeric = Numeric()
    popular_tags = feed_page.popular_tags_list.locator(feed_page.tag_items)
    # But before picking, ensure they have loaded on the page
    popular_tags.first.wait_for(state="visible")
    popular_tag_element = popular_tags.nth(
        numeric.integer_number(start=1, end=popular_tags.count())
    )
    popular_tag_text = popular_tag_element.inner_text()
    # Click on the tag to filter the feed
    popular_tag_element.click()
    # Ensure that each of the remaining articles have the selected tag present
    for article_item in feed_page.article_items.all():
        expect(
            article_item.locator(feed_page.tag_items).filter(has_text=popular_tag_text)
        ).to_be_visible()


def test_guest_cannot_favorite_article(page: Page):
    # Instead of favoriting the article, it will redirect to the login page
    feed_page = FeedPage(page)
    feed_page.global_feed_link.click()
    feed_page.article_favorite_button.first.click()
    expect(page).to_have_url("/#/login")


@pytest.mark.browser_context_args(storage_state="fixtures/generic_user.json")
def test_loggedin_user_favorites_article(page: Page):
    feed_page = FeedPage(page)
    feed_page.global_feed_link.click()
    # Button should be outlined (not filled) and record current count
    favorite_button = feed_page.article_favorite_button.first
    expect(favorite_button).to_have_class(re.compile(r"btn-outline-primary"))
    favorite_button_count = int(favorite_button.inner_text())
    favorite_button.click()
    expect(favorite_button).to_have_class(re.compile(r"btn-primary"))
    expect(favorite_button).to_have_text(str(favorite_button_count + 1))
    # Verify it can also be unfavorited
    favorite_button.click()
    expect(favorite_button).to_have_class(re.compile(r"btn-outline-primary"))
    expect(favorite_button).to_have_text(str(favorite_button_count))


def test_click_article_for_details_page(page: Page):
    feed_page = FeedPage(page)
    feed_page.global_feed_link.click()
    # Pick a random article
    numeric = Numeric()
    article = feed_page.article_items.nth(
        numeric.integer_number(start=1, end=feed_page.article_items.count())
    )
    article_title = article.locator(feed_page.article_details_link)
    article_title_url = article_title.inner_text().replace(" ", "-").replace(",", "")
    article_title.click()
    expect(page).to_have_url(re.compile(article_title_url))


def test_pagination_set_to_10(page: Page):
    """
    Simple check to ensure there's only 10 articles at a time.
    Chronological order would also be good to check, but the content
    is mostly spam on a particular date, so it's not very useful.
    """
    feed_page = FeedPage(page)
    feed_page.global_feed_link.click()
    # Check the first 5 pages to minimize time
    for i in range(5):
        feed_page.pagination_pages.nth(i).click()
        expect(feed_page.article_items).to_have_count(10)
