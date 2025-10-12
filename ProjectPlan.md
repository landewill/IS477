# Project Plan – “Talk Is Expensive: Quantifying the AI-Hype Effect in Corporate Disclosures”

## Overview
This project investigates whether public companies that emphasize **artificial intelligence (AI)** terminology in their mandatory SEC filings experience measurable short-term stock market reactions.  
By combining **text mining of 10-K/10-Q filings** with **event-study econometric analysis** of market data, we will quantify the “AI-hype premium”—the degree to which firms benefit from invoking AI in investor communications regardless of fundamentals.  
Our end goal is to produce a **reproducible workflow** that automatically downloads filings, detects AI-related language, links it to stock returns around filing dates, and visualizes how this effect evolved from 2022 to 2025.

---

## Research Questions
1. **Primary Question:**  
   Do firms that mention “AI” more frequently in SEC 10-K/10-Q filings experience statistically significant short-term abnormal returns following the filing date?  
2. **Secondary Questions:**  
   - Has the magnitude of this “AI-hype premium” changed between 2022 and 2025?  
   - Are the effects concentrated in technology firms or spread across all sectors?  
   - Does the tone or context (positive vs cautionary) of AI mentions influence the market reaction?

---

## Team and Roles
| Member | Major | Roles & Responsibilities |
|---------|--------|--------------------------|
| **Will Lande** | Econometrics & Quantitative Economics | Lead data integration and econometric modeling. Implement event-study regressions, statistical tests, and visualizations. Maintain workflow automation scripts and documentation. |
| **[Partner Name]** | Accounting | Lead text-mining and disclosure analysis. Collect and preprocess SEC filings, perform keyword and sentiment extraction, evaluate ethical and reporting implications, and help interpret results in an accounting context. |

Both members will contribute equally to Git commits, markdown documentation, and report writing.

---

## Datasets
We will integrate at least **two distinct datasets** from different sources and formats:

1. **SEC EDGAR Filings Dataset**  
   - *Access:* [`sec-api`](https://sec-api.io/) or `edgar` Python library  
   - *Format:* JSON / HTML text files  
   - *Description:* All 10-K and 10-Q filings from 2022–2025 for S&P 500 companies.  Each document will be parsed for AI-related keywords (e.g., “artificial intelligence,” “machine learning,” “neural network”) and sentiment scored.  
   - *Purpose:* Independent variable—frequency and tone of AI references.  

2. **Financial Market Data**  
   - *Access:* Yahoo Finance API or Alpha Vantage API  
   - *Format:* CSV or JSON time-series data  
   - *Description:* Daily closing prices, volume, and market indices. We will calculate abnormal returns using a market-model approach surrounding each filing date.  
   - *Purpose:* Dependent variable—stock performance reaction to AI disclosure intensity.  

**Integration Plan:**  
Filings will be matched to stock tickers and filing dates; abnormal returns will be aligned with keyword metrics in a combined Pandas DataFrame or relational table.  

---

## Timeline & Task Assignments
| Week | Dates (approx.) | Tasks | Responsible Member(s) |
|------|-----------------|-------|------------------------|
| 1 | Oct 13 – Oct 20 | Finalize research design; test SEC and Yahoo APIs; create repo structure and data schema. | Both |
| 2 | Oct 21 – Oct 27 | Implement SEC filing download and parsing scripts; begin keyword extraction. | Partner |
| 3 | Oct 28 – Nov 3 | Acquire stock data; merge datasets by ticker/date; initial cleaning. | Will |
| 4 | Nov 4 – Nov 11 | Conduct preliminary analysis for Interim Status Report (event-study prototype, plots). | Both |
| 5 | Nov 12 – Nov 24 | Expand sample; improve NLP (sentiment, context); refine econometric models. | Both |
| 6 | Nov 25 – Dec 5 | Automate workflow with Snakemake or “Run All” script; finalize visualizations; prepare README report. | Will |
| 7 | Dec 6 – Dec 10 | Quality-check reproducibility; upload final data package to Box; submit final release. | Both |

---

## Constraints
- **Data Access Limits:** Some filings may be large or rate-limited by the SEC API. We will respect API usage policies and throttle requests.  
- **Text Processing Challenges:** Filings vary in formatting and may contain OCR errors. We will normalize text and document limitations.  
- **Market Confounders:** Other news events near filing dates may influence prices. We will control using market indices and sector effects.  
- **Ethical Use:** All data are public; no personal or confidential information will be collected. We will cite APIs and licenses appropriately.

---

## Gaps / Areas for Input
- **Event window selection:** Optimal number of days before/after filing for abnormal return calculation (to be refined with instructor feedback).  
- **Sentiment classification:** May need faculty input on whether to use pretrained FinBERT model or simpler lexicon approach.  
- **Computational resources:** Parsing thousands of filings may require batching on Illinois compute nodes or Colab Pro.  

---

## Anticipated Later Topics
Our workflow will connect directly to later IS 477 modules:  
- **Data quality** profiling (Module 9) – assess missing or duplicate filings.  
- **Data cleaning** (Module 10) – standardize ticker symbols, dates, formats.  
- **Workflow automation / provenance** (Modules 11–12) – Snakemake workflow to run pipeline end-to-end.  
- **Reproducibility and metadata** (Modules 13 & 15) – include requirements.txt, data dictionary, and Box data link.

---

**Deliverables:**  
- `ProjectPlan.md` (this document)  
- `data/` directory with schema README  
- Initial Python notebooks or scripts for API testing  
- GitHub tag: `project-plan` for release submission  

---

*This plan will evolve as feedback is received.  All updates will be documented in GitHub commit history to ensure full transparency and reproducibility.*