> Source : AgriciDaniel/claude-seo, skill seo-geo (MIT), état 08/2026.

## AI Crawler Detection

Check `robots.txt` for these AI crawlers:

| Crawler | Owner | Purpose | Obeys robots.txt? |
|---------|-------|---------|---|
| GPTBot | OpenAI | **Model training only** (NOT ChatGPT Search) | yes |
| OAI-SearchBot | OpenAI | **ChatGPT Search citability** (the crawler that decides it) | yes |
| ChatGPT-User | OpenAI | ChatGPT browsing (user-triggered) | no (user-triggered) |
| ClaudeBot | Anthropic | **Model training only** (NOT Claude's search features) | yes |
| Claude-SearchBot | Anthropic | **Claude/Claude.ai search-result citability** (the crawler that decides it) | yes |
| Claude-User | Anthropic | Claude browsing on a user's behalf (user-triggered) | no (user-triggered) |
| PerplexityBot | Perplexity | Perplexity AI search | yes |
| CCBot | Common Crawl | Training data (often blocked) | yes |
| Bytespider | ByteDance | TikTok/Douyin AI | yes |
| cohere-ai | Cohere | Cohere models | yes |
| Google-Extended | Google | **Gemini/Vertex training & grounding only** (NOT Google Search) | yes |
| Google-CloudVertexBot | Google | Site-owner-requested Vertex AI Agent crawls | yes |
| Google-Agent | Google | Agentic browsing (Project Mariner), acts for a user | **no (user-triggered)** |
| Google-NotebookLM | Google | Fetches individual user-added source URLs | **no (user-triggered)** |
| Google Messages | Google | User-triggered fetch | **no (user-triggered)** |
| Applebot-Extended | Apple | **Apple Intelligence / generative-AI training data opt-out only** (NOT Siri, Spotlight, or Safari search; does not itself crawl, it labels content already fetched by Applebot) | yes |

Sources: [OpenAI crawlers](https://platform.openai.com/docs/bots),
[Google crawlers overview](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers),
[Anthropic crawler support article](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler),
[Apple Applebot-Extended support article](https://support.apple.com/en-us/119829).
Anthropic's current crawler support article documents only ClaudeBot, Claude-User,
and Claude-SearchBot; it does not list `anthropic-ai`, so the previously-unverified
`anthropic-ai` row has been removed rather than kept as a guess.

**Recommendation:** Allow OAI-SearchBot, Claude-SearchBot, and PerplexityBot for AI
search visibility. GPTBot, ClaudeBot, CCBot, and Applebot-Extended are training-only
signals -- allow or block them on licensing preference, not on search-visibility
grounds.

### Check the right bot for the claim you are making

Two pairs are routinely conflated. **Each claim below may only be supported by its own
bot's robots.txt status** -- check them separately and report them separately.

| Claim you want to make | Bot to check | Bot that does NOT support this claim |
|---|---|---|
| "Content is citable in ChatGPT Search" | `OAI-SearchBot` | `GPTBot` |
| "Content is available for OpenAI model training" | `GPTBot` | `OAI-SearchBot` |
| "Content can be used for Gemini/Vertex training & grounding" | `Google-Extended` | `Googlebot` |
| "Content is eligible for Google Search / AI Overviews" | `Googlebot` | `Google-Extended` |
| "Content is citable in Claude's search features" | `Claude-SearchBot` | `ClaudeBot` |
| "Content is available for Anthropic model training" | `ClaudeBot` | `Claude-SearchBot` |
| "Content can be used for Apple Intelligence training" | `Applebot-Extended` | `Applebot` |
| "Content is discoverable via Siri, Spotlight, or Safari search" | `Applebot` | `Applebot-Extended` |

- **`Google-Extended` governs Gemini and Vertex AI training and grounding use only.
  It does not affect inclusion in ordinary Google Search, or in AI Overviews and AI
  Mode, both of which are served from the `Googlebot` index.** Never score
  `Google-Extended` as a "Google Search readiness" signal, and never cite a blocked
  `Google-Extended` as evidence that a site is missing from Google Search.
- **`OAI-SearchBot` is the crawler that determines ChatGPT Search citability.
  `GPTBot` is OpenAI's separate training crawler.** Checking `GPTBot` access tells
  you nothing about whether ChatGPT Search can cite the page. A site that blocks
  `GPTBot` and allows `OAI-SearchBot` is fully citable in ChatGPT Search.
- **`Claude-SearchBot` is the crawler that determines citability in Claude's own
  search features. `ClaudeBot` is Anthropic's separate training crawler** (per
  Anthropic's crawler support article). Checking `ClaudeBot` access tells you
  nothing about Claude search citability, and vice versa; report each separately.
- **`Applebot-Extended` is a training-data opt-out signal, not a crawler that
  fetches pages itself.** Per Apple's support article, disallowing
  `Applebot-Extended` opts a site out of Apple Intelligence / generative-model
  training use, but the page remains discoverable through Siri, Spotlight, and
  Safari as long as `Applebot` itself is allowed. Never cite a blocked
  `Applebot-Extended` as evidence a site is missing from Apple's search surfaces.

Do not use these names interchangeably in report prose. When reporting crawler access,
name the specific user-agent that was checked and the specific capability it governs.

> **User-triggered fetchers ignore robots.txt by design** (Google-Agent, Google-NotebookLM, Google Messages, ChatGPT-User). robots.txt cannot block them, use server-side access controls. Google's canonical crawling/robots reference moved to **developers.google.com/crawling** (migrated 2025-11-20); IP-range files now live at `/crawling/ipranges/` and `googlebot.json` was renamed `common-crawlers.json`. Emerging: **Web Bot Auth** (RFC 9421) lets bots authenticate via a `Signature-Agent` header + key directory (used by Google-Agent); reverse-DNS verification remains the fallback.

---
