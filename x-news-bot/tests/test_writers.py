from x_news_bot.writers import draft_post
from x_news_bot.news import Story
def test_draft_is_within_limit():
    s=Story('A'*400,'https://example.com/story','Example',None)
    assert len(draft_post(s))<=280
