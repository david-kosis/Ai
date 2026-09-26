import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
@dataclass(frozen=True)
class Settings:
    x_enabled: bool = os.getenv('X_ENABLED','false').lower() == 'true'
    x_access_token: str = os.getenv('X_ACCESS_TOKEN','')
    news_feeds: tuple[str,...] = tuple(u.strip() for u in os.getenv('NEWS_FEEDS','').split(',') if u.strip())
    max_posts_per_run: int = int(os.getenv('MAX_POSTS_PER_RUN','3'))
    max_news_age_hours: int = int(os.getenv('MAX_NEWS_AGE_HOURS','24'))
