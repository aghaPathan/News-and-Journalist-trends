# News and Journalist Trends Analysis

A data mining project using the Apriori algorithm to discover trends in news articles and journalist publications.

## Overview

This project applies association rule mining to analyze patterns in news content, identifying trends across various dimensions.

## Technique

**Apriori Algorithm** — A classic algorithm for mining frequent itemsets and discovering association rules.

## Features

- 📰 **News Pattern Analysis** — Discover common themes in articles
- 👤 **Journalist Trends** — Analyze writing patterns by author
- 📊 **Multi-dimensional Analysis** — Explore trends across topics, time, sources
- 🔗 **Association Rules** — Find related concepts in news content

## Requirements

- Python 3.x
- pandas
- mlxtend (for Apriori)
- matplotlib

## Usage

```bash
python trends_analysis.py
```

## Methodology

1. **Data Collection** — Gather news articles dataset
2. **Preprocessing** — Clean and tokenize content
3. **Frequent Itemsets** — Apply Apriori to find common patterns
4. **Rule Generation** — Extract association rules
5. **Visualization** — Present trend findings

## Output

- Frequent topics and themes
- Journalist writing patterns
- Topic associations and correlations

## License

MIT
