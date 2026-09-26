from .config import Settings
from .news import fetch_stories
from .writers import draft_post
from .team import JuniorDeveloper,ProjectManager
from .x_client import XClient
def main():
    s=Settings(); stories=fetch_stories(s.news_feeds,s.max_news_age_hours); junior=JuniorDeveloper(); pm=ProjectManager(); published=0
    if not stories: print('Project Manager: no fresh stories. Next step: check feeds.'); return
    for story in stories[:s.max_posts_per_run]:
        post=junior.prepare(draft_post(story)); decision=pm.coordinate(story,post); print('\n'+post+'\nProject Manager: '+decision.report)
        if decision.approved and s.x_enabled: XClient(s.x_access_token).create_post(post); published+=1
    print(f'Project Manager: run complete. Published: {published}. Next step: review logs, then enable live mode after credentials are configured.')
if __name__=='__main__': main()
