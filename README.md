Summary: Fine-tuning LLM to generate summaries of news stories based on text-scraping stories from major news sites

Process:
1. Web scraper to take news articles from major websites *(categories: international, sports, technology, business)*
2. Text similarity model should classify articles/headlines/keys to separate stories
3. NewsGPT will summarise all 5 news articles into one story

Project Plan:
- Build news scraper *(initial target websites: BBC, The Guardian, CNN, ABC news)*
- Fine-tune NewsGPT from LLM model (e.g. BERT)
- Build text similarity model
- Build application (API, interface - website/app, etc.)

Potential Problems:


Further Improvements:
- Allow users to pick type of news - Asia, Technology, etc.
- Work on other types of live scraping (e.g. scraping Steam for fresh games/deals/reviews)

