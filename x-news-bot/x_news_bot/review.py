from dataclasses import dataclass
from .news import Story
@dataclass(frozen=True)
class Review:
    approved: bool
    reasons: tuple[str,...]
class SeniorReviewer:
    name='Senior Developer 1'
    def review(self,story,post):
        r=[]
        if not story.url.startswith(('http://','https://')): r.append('invalid source URL')
        if not story.title.strip(): r.append('missing headline')
        if len(post)>280: r.append('post exceeds 280 characters')
        return Review(not r,tuple(r))
class SeniorNewsReviewer(SeniorReviewer):
    name='Senior Developer 2'
    def review(self,story,post):
        base=super().review(story,post); r=list(base.reasons)
        if not story.source.strip(): r.append('missing source attribution')
        return Review(not r,tuple(r))
