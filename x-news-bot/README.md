# X News Bot — 4-Agent Team

Built inside david-kosis/Ai.

Agents: 1 Junior Developer, 2 Senior Developers, and 1 Project Manager who reports the next step.

Flow: RSS news -> deduplication -> factual draft -> two senior review gates -> X publishing -> project-manager report.

Default is DRY RUN. Set X_ENABLED=true only after configuring X_ACCESS_TOKEN securely as an environment variable.

Political/news posts are factual and attributed; the bot does not endorse candidates, parties, policies, or political choices.

Run: python -m x_news_bot
