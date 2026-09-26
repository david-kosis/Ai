from dataclasses import dataclass
from .review import SeniorReviewer,SeniorNewsReviewer
@dataclass(frozen=True)
class TeamDecision:
    approved: bool
    report: str
class JuniorDeveloper:
    def prepare(self,post): return post.strip()
class ProjectManager:
    def coordinate(self,story,post):
        reviews=[SeniorReviewer().review(story,post),SeniorNewsReviewer().review(story,post)]
        failures=[f'{name}: {reason}' for name,review in zip(('Senior Developer 1','Senior Developer 2'),reviews) for reason in review.reasons]
        if failures: return TeamDecision(False,'BLOCKED. '+ '; '.join(failures)+'. Next step: fix and rerun.')
        return TeamDecision(True,'APPROVED. Next step: publish if live mode is enabled.')
