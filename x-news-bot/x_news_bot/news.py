from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import hashlib
import feedparser
@dataclass(frozen=True)
class Story:
    title: str
    url: str
    source: str
    published_at: datetime | None
    @property
    def id(self): return hashlib.sha256(self.url.encode()).hexdigest()[:16]
def fetch_stories(feeds, max_age_hours=24):
    cutoff=datetime.now(timezone.utc)-timedelta(hours=max_age_hours); out=[]; seen=set()
    for feed_url in feeds:
        f=feedparser.parse(feed_url); source=f.feed.get('title',feed_url)
        for item in f.entries:
            url=item.get('link','').strip(); title=item.get('title','').strip()
            if not url or not title or url in seen: continue
            published=None; raw=item.get('published') or item.get('updated')
            if raw:
                try: published=parsedate_to_datetime(raw).astimezone(timezone.utc)
                except (TypeError,ValueError,OverflowError): pass
            if published and published < cutoff: continue
            seen.add(url); out.append(Story(title,url,source,published))
    return sorted(out,key=lambda s:s.published_at or datetime.min.replace(tzinfo=timezone.utc),reverse=True)
