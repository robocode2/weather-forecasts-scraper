# Weather Data Scraping Application

This is a Scrapy-based web scraping application designed to collect weather forecast data from multiple sources. The data is stored in a PostgreSQL database and can be retrieved through an API using a custom VPN connection. 

This file provides instructions for local development and testing.

## Getting Started with Local Development

### Requirements
- **pip**: Python package installer
- **Python 3.10**: Ensure you have `python3.10-venv` installed for virtual environment support.

### Installation Steps

1. **Clone the Repository**
    ```bash
    git clone git@github.com:robocode2/weather-forecasts-scraper.git
    cd weather-forecasts-scraper
    ```

2. **Set Up a Virtual Environment**
   Create a virtual environment at the same directory level as `weatherscraper`:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Python Dependencies**
   Install the required packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create and Configure the .env File**
   The application uses ScrapeOps for managing rotating proxies and user agents to avoid being detected as a bot.
   Register for a free account on ScrapeOps and get your API key. 

   Add your ScrapeOps API key to the `.env` file: 
    ```plaintext
    SCRAPEOPS_API_KEY=your_scrapeops_api_key
    ```

5. **Set Up the Database**
   1. Insert your database credentials in `pipelines.py` to connect to your database. Currently, the application is set to connect to the host DB. Fill in your credentials.
    ```bash
       self.connection = psycopg2.connect(
                host='',
                database='',
                user='',
                password='',
                port=''
            )
    ```

### Running the Spiders Locally

To run the spiders and save the scraped data to CSV files:

1. **Run Each Spider:** 
   
   These commands will scrape data from each source and save results as CSV files in the current directory.
    ```bash
    scrapy crawl TheWeatherChannel -O WeatherChannel_2024.csv -s LOG_LEVEL=ERROR
    scrapy crawl MeteoBlue -O Meteoblue_2024.csv -s LOG_LEVEL=ERROR
    scrapy crawl MeteoProg -O MeteoProg_2024.csv -s LOG_LEVEL=ERROR
    scrapy crawl TimeAndDate -O TimeAndDate_2024.csv -s LOG_LEVEL=ERROR
    ```
   You can also test Scrape0ps integration with this command. The spiders will console log the rotating IPS and user agents.

    ```bash
    scrapy crawl headers
    scrapy crawl proxies
    ```
    
2. **Optional**: If you prefer not to use a PostgreSQL database for local testing, you can comment out the following line to distable the PostgreSQL-DB insertion pipeline in `settings.py`.

    ```bash
    ITEM_PIPELINES = {
        # 'weatherscraper.pipelines.PostgreSQLPipeline': 200,
    }
    ```

### Running Tests

1. **Install pytest**:
    ```bash
    pip install pytest
    ```

2. **Set Up the Test Database**
    ```bash
    docker compose down -v && docker compose up --build -d
    ```
   Update the database credentials in `pipelines.py` to connect to the test database. // TODOX double check on laptop
    ```bash
    self.connection = psycopg2.connect(
                host='127.0.0.1',
                database='testforecastsdb',
                user='postgres',
                password='IDnowLOV123!', // enter your postgres user password
                port='5434'
            )
    ```

3. **Run Tests**:
   Run all tests using:
    ```bash
    pytest tests/
    ```
    You must be in the virtual environment. 