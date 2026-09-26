from .news import Story
def draft_post(story: Story) -> str:
    suffix=f'\n\nSource: {story.source}\n{story.url}'
    if len(story.title)+len(suffix) <= 280: return story.title+suffix
    return story.title[:max(0,278-len(suffix))].rstrip(' .,:;')+'…'+suffix
