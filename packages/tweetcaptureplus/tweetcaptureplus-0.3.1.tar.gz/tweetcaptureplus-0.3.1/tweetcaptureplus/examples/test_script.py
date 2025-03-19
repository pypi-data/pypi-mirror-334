from tweetcaptureplus import TweetCapturePlus
import asyncio
import os

os.environ["auth_token"] = "cf5b30dd7b339f90d304281331f40e76d6305165"

"""
tweetcaptureplus --gui -sp --cookies auth_token=cf5b30dd7b339f90d304281331f40e76d6305165; https://x.com/sheela_96/status/1898877185085288923
"""

tweet = TweetCapturePlus(gui=True)
# Full thread
asyncio.run(
    tweet.screenshot(
        "https://x.com/sheela_96/status/1898877185085288923",
        show_parent_tweets=True,
    )
)
"""
asyncio.run(
    tweet.screenshot(
        "https://x.com/elonmusk/status/1519480761749016577",
    )
)
# Full thread
asyncio.run(
    tweet.screenshot(
        "https://x.com/elonmusk/status/1746970616060580326",
        show_parent_tweets=True,
    )
)
asyncio.run(
    tweet.screenshot(
        "https://x.com/PerceptivTrader/status/1788923630618890632",
    )
)

# Full thread
asyncio.run(
    tweet.screenshot(
        "https://x.com/elhllos/status/1897131652494815698",
        show_parent_tweets=True,
    )
)
# Reply, show parent tweets
asyncio.run(
    tweet.screenshot(
        "https://x.com/elonmusk/status/1898779023234236437",
        show_parent_tweets=True,
    )
)
# Reply, show parent tweets
asyncio.run(
    tweet.screenshot(
        "https://x.com/elonmusk/status/1587911540770222081",
        show_parent_tweets=True,
    )
)
# Long main tweet
asyncio.run(
    tweet.screenshot(
        "https://x.com/3asief_/status/1898145582138396674",
    )
)
# Regular tweet
asyncio.run(
    tweet.screenshot(
        "https://x.com/David_Syriac/status/1898363932915691670",
    )
)
# Mentions
asyncio.run(
    tweet.screenshot(
        "https://x.com/elonmusk/status/1898803897038221743",
        overwrite=True,
        show_mentions_count=7,
    )
)
"""
