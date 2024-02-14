# Yahoo Finance Scrape Workflow

## Overview
This workflow automates the process of scraping Yahoo Finance (YF) news page for links and relevant data, extracting detailed news content, relevant tickers, and other data, and then feeding this data into a news sentiment analysis pipeline. The entire process is orchestrated using GitHub Actions.

## Workflow Steps

1. **Scrape YF News Page**: A GitHub Action is scheduled to run every 6 hours to scrape all links and relevant data from the Yahoo Finance news page.

2. **Extract News Contents**: Following the initial scrape, another GitHub Action is triggered that extracts the news contents, relevant tickers, and other pertinent data from the scraped links.

3. **News Sentiment Pipeline**: The extracted news content and data are then sent to a news sentiment analysis pipeline for further processing.

## GitHub Actions

- **Scrape Action**: Scheduled every 6 hours to scrape Yahoo Finance news page.
- **Extract Action**: Runs after the scrape action to process the scraped data.
- **Pipeline Integration**: The extracted data is automatically read from the news sentiment pipeline for further processing.
