from agents.news_agent import NewsAgent
from agents.papers_agent import PapersAgent
from agents.grants_agent import GrantsAgent
from agents.funding_agent import FundingAgent
from agents.github_agent import GitHubAgent

ALL_AGENTS = {
    "news": NewsAgent,
    "papers": PapersAgent,
    "grants": GrantsAgent,
    "funding": FundingAgent,
    "github": GitHubAgent,
}

COLLECTIBLE_AGENTS = ALL_AGENTS
