# Slide 2 — Source Sheet

Backup for *"Still manual. And that is where the money goes."*
Prepared 10 August 2026.

---

## On the slide

### ① 2500% — more software defects by 2028

> "By 2028, prompt-to-app approaches adopted by citizen developers will increase
> software defects by 2500%, triggering a software quality and reliability crisis."

| | |
|---|---|
| **Source** | Gartner, *Predicts 2026: AI Potential and Risks Emerge in Software Engineering Technologies* |
| **Document** | Gartner doc ID 7239930 |
| **Date** | 2025 (Predicts 2026 cycle) |
| **Basis** | Analyst prediction — **not** a survey or measurement |
| **Link** | https://www.gartner.com/en/documents/7239930 |
| **Free reprint** | https://www.armorcode.com/report/gartner-predicts-2026-ai-potential-and-risks-emerge-in-software-engineering-technologies |

**Supporting language from the same report** — this is the sentence that matches
AthenaRun's thesis most directly: Gartner attributes the defect surge to
*"context-deficient code"* — AI output that is syntactically correct but lacks
awareness of the broader system architecture and nuanced business rules.

Also in the same report: **by end of 2026, 75% of developers will spend more
time orchestrating and architecting than writing code directly.**

---

### ② 25% — of planned AI spend deferred to 2027

> "As AI's hype fades, enterprises will defer 25% of planned AI spend to 2027."

| | |
|---|---|
| **Source** | Forrester, *2026 Technology & Security Predictions* |
| **Date** | Published 28 October 2025 |
| **Basis** | Analyst prediction |
| **Link** | https://investor.forrester.com/news-releases/news-release-details/forresters-2026-technology-security-predictions-ais-hype-fades-0 |
| **Mirror** | https://www.businesswire.com/news/home/20251028226928/en/ |

**Companion figure, same release:** *fewer than one-third* of decision-makers
can tie the value of AI to their organisation's financial growth — which is why
CEOs will lean on CFOs to approve AI investment on ROI in 2026.

---

### ③ 153% — more architectural design flaws

> "Privilege escalation paths jumping 322%, and architectural design flaws
> spiking 153%."

| | |
|---|---|
| **Source** | Apiiro, *4x Velocity, 10x Vulnerabilities: AI Coding Assistants Are Shipping More Risks* |
| **Date** | September 2025 |
| **Sample** | Tens of thousands of repositories across Fortune 50 enterprises, analysed with Apiiro's Deep Code Analysis engine |
| **Basis** | **Measurement**, not prediction |
| **Link** | https://apiiro.com/blog/4x-velocity-10x-vulnerabilities-ai-coding-assistants-are-shipping-more-risks/ |

**The full contrast — this is the strongest single data point in the deck:**

| Metric | Change |
|---|---|
| Trivial syntax errors | **−76%** |
| Logic bugs | **−60%** |
| **Architectural design flaws** | **+153%** |
| Privilege escalation paths | **+322%** |
| Security findings, Dec 2024 → Jun 2025 | **10×** (>10,000/month) |
| Code volume, AI-assisted vs unassisted devs | **3–4×** |

Apiiro states explicitly that AI-assisted developers are more prone to
**design-level** flaws, where unassisted developers are more prone to logic
mistakes — the surface gets cleaner while the system layer gets worse.

**Independent press coverage** (use these if an investor wants a non-vendor
confirmation): [The Register](https://www.theregister.com/2025/09/05/ai_code_assistants_security_problems/)
· [CSO Online](https://www.csoonline.com/article/4062720/ai-coding-assistants-amplify-deeper-cybersecurity-risks.html)
· [SiliconANGLE](https://siliconangle.com/2025/09/04/apiiro-report-finds-ai-code-assistants-increase-developer-speed-heighten-security-risk/)

*Disclosure to make if asked: Apiiro sells code-analysis tooling. The figures
come from their own telemetry. The press coverage above is the independent check.*

---

## Bench — swap in if a stat is challenged

| Stat | Source | Sample / basis | Date |
|---|---|---|---|
| **61%** agree AI "often produces code that looks correct but isn't reliable"; **96%** don't fully trust AI output but only **48%** always verify; **38%** say AI code review takes more effort than human code review; AI = **42%** of committed code, expected **65%** by 2027 | [Sonar, *State of Code Developer Survey*](https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/) · [PDF](https://www.sonarsource.com/state-of-code-developer-survey-report.pdf) | >1,100 professional developers | Jan 2026 |
| Developers "are no longer just writing code: they're generating entire applications, **orchestrating workflows, guiding agents**, and ensuring harmony across complex systems" | [Forrester, *Predictions 2026: Software Development Goes From Jamming To A Full Orchestra*](https://www.forrester.com/blogs/predictions-2026-software-development-goes-from-jamming-to-full-orchestra) | Analyst prediction | Dec 2025 |
| **>40%** of agentic AI projects cancelled by end-2027 — escalating costs, **unclear business value**, weak risk controls | [Gartner press release](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) | Analyst prediction | 25 Jun 2025 |
| Technical debt at moderate-or-high severity: **>50%** of tech decision-makers in 2025 → **75%** in 2026 ("tech debt tsunami") | [Forrester via CFO Dive](https://www.cfodive.com/news/tech-debt-tsunami-building-amid-ai-craze-forrester/733984/) | Analyst survey + prediction | 2024–25 |
| Only **39%** of organisations attribute *any* EBIT impact to AI, most under 5%; ~**6%** are high performers; nearly **two-thirds** haven't begun scaling | [McKinsey, *The State of AI in 2025*](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) | Global survey | 2025 |
| Developers were **19% slower** with AI tools while estimating they were **20% faster** | [METR RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) · [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) | RCT, 16 experienced devs, 246 real tasks | Jul 2025 |
| **66%** cite "AI solutions that are almost right, but not quite" as top frustration; **45%** say debugging AI code takes longer; trust in AI accuracy down to **29%** from 40% | [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/ai/) | Global developer survey | 2025 |
| Workflow runs **+59% YoY**, median team's main-branch throughput **−7%**, success rates at a five-year low | [CircleCI, *2026 State of Software Delivery*](https://circleci.com/resources/2026-state-of-software-delivery/) | ~28M workflows, 22,000+ orgs, 149 countries | Feb 2026 |
| AI acts as an **amplifier** of existing organisational strengths and dysfunction; most orgs see no end-to-end improvement | [DORA / Google Cloud, *State of AI-assisted Software Development*](https://dora.dev/dora-report-2025/) | ~5,000 practitioners | 2025 |

---

## Removed from slide 2 — and why

| Old stat | Old citation | Reason removed |
|---|---|---|
| **80%** of failures trace back to requirements | Standish CHAOS | Not traceable to any CHAOS edition. Standish's own factor breakdown totals ~37% for requirements + user-input causes (12.8 / 12.3 / 11.8). The circulating "80%" appears to be a garbled version of a different, real claim: *70–85% of **rework cost** stems from requirements defects* (Leffingwell 1997, after Boehm). |
| **45%** median cost overrun, large IT | McKinsey | Number is real but mislabelled — McKinsey–Oxford (2012, 5,400+ projects >$15M) reports it as an **average**, not a median. Also 14 years old. |
| **39%** caused by unclear requirements | *(implied Standish/McKinsey)* | Neither source says this. Traces to Zipdo, an AI-generated statistics aggregator, with no underlying study. |

---

## Do not use

Citations that look authoritative but could not be traced to any primary
document. Each of these appears widely online; none survives a check.

- **"Gartner: 75% of enterprise software projects fail to meet business objectives within three years"** (attributed to 2022) — no source document found.
- **"Forrester: poorly defined applications cause a 66% project failure rate"** — no source document found.
- **"Meta Group: 60–80% of project failures traced to poor requirements"** — Meta Group was acquired by Gartner in **2005**. A 2026 deck citing it is a diligence flag.
- **"IBM Systems Sciences Institute"** defect-cost-multiplier figures — the institute and study have never been located (documented in Bossavit, *The Leprechauns of Software Engineering*).
- **"Standish CHAOS 2024 / 2025"** — no such publication. The final edition is **CHAOS 2020: Beyond Infinity** (31% successful / 50% challenged / 19% failed).
- **Statistics aggregators** — gitnux, zipdo, apollotechnical, speakwiseapp, rockstardeveloperuniversity, reworkcost.com. They cite one another in a loop and invent attributions.

---

## Licensing note

Gartner and Forrester both restrict use of their name and content in marketing
and investor materials.

- **Free press releases** (Forrester's 2026 Predictions, Gartner's agentic-AI release) are published for citation — no permission needed.
- **Paywalled documents** (Gartner *Predicts 2026*, doc 7239930) should be cited via a **licensed reprint** — the ArmorCode link above is one.
- Quoting a paywalled document ID without a reprint is both the riskier path and the one an investor cannot verify.

Of the three stats on the slide, ② and ③ are fully free to cite, and ① has a
public reprint.
