import requests
from bs4 import BeautifulSoup
import json
import time
import csv
from urllib.parse import urljoin, urlparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

class WebScraper:
    def __init__(self, base_url="", headers=None, delay=1):
        """
        Initialize the web scraper
        
        Args:
            base_url (str): The base URL of the website to scrape
            headers (dict): Custom headers for requests
            delay (int): Delay between requests in seconds
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        
        # Default headers to avoid being blocked
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
    
    def get_page(self, url):
        """
        Fetch a single page
        
        Args:
            url (str): URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            # Add delay to be respectful to the server
            time.sleep(self.delay)
            
            # Make the request
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            logging.info(f"Successfully scraped: {url}")
            return soup
            
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_links(self, soup, selector="a", base_url=None):
        """
        Extract all links from a page
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            selector (str): CSS selector for links
            base_url (str): Base URL to convert relative links
            
        Returns:
            List of URLs
        """
        if not soup:
            return []
        
        links = []
        for link in soup.select(selector):
            href = link.get('href')
            if href:
                # Convert relative URLs to absolute
                if base_url:
                    href = urljoin(base_url, href)
                links.append(href)
        
        return list(set(links))  # Remove duplicates
    
    def extract_text(self, soup, selector):
        """
        Extract text from elements matching the selector
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            selector (str): CSS selector
            
        Returns:
            List of text content
        """
        if not soup:
            return []
        
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    
    def extract_attributes(self, soup, selector, attribute):
        """
        Extract specific attributes from elements
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            selector (str): CSS selector
            attribute (str): Attribute name to extract
            
        Returns:
            List of attribute values
        """
        if not soup:
            return []
        
        elements = soup.select(selector)
        return [elem.get(attribute) for elem in elements if elem.get(attribute)]
    
    def scrape_page_data(self, url, selectors):
        """
        Scrape specific data from a page using CSS selectors
        
        Args:
            url (str): URL to scrape
            selectors (dict): Dictionary of data_name: css_selector pairs
            
        Returns:
            Dictionary of scraped data
        """
        soup = self.get_page(url)
        if not soup:
            return {}
        
        data = {}
        for data_name, selector in selectors.items():
            try:
                elements = soup.select(selector)
                if elements:
                    # If multiple elements, return list of text
                    if len(elements) > 1:
                        data[data_name] = [elem.get_text(strip=True) for elem in elements]
                    else:
                        data[data_name] = elements[0].get_text(strip=True)
                else:
                    data[data_name] = None
            except Exception as e:
                logging.error(f"Error extracting {data_name}: {e}")
                data[data_name] = None
        
        return data
    
    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving to JSON: {e}")
    
    def save_to_csv(self, data, filename, fieldnames=None):
        """Save data to CSV file"""
        try:
            if not data:
                return
            
            if not fieldnames:
                fieldnames = data[0].keys() if isinstance(data, list) else data.keys()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                if isinstance(data, list):
                    writer.writerows(data)
                else:
                    writer.writerow(data)
            
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")

# Example usage functions
def example_scrape_news():
    """Example: Scrape news headlines"""
    scraper = WebScraper()
    
    # Example selectors for a news website
    selectors = {
        'headlines': 'h2.headline',  # Adjust selector as needed
        'summaries': '.article-summary',
        'dates': '.publish-date'
    }
    
    url = "https://example-news-site.com"  # Replace with actual URL
    data = scraper.scrape_page_data(url, selectors)
    
    # Save results
    scraper.save_to_json(data, 'news_data.json')
    return data

def example_scrape_products():
    """Example: Scrape product information"""
    scraper = WebScraper(delay=2)  # Be more respectful with 2-second delay
    
    selectors = {
        'product_names': '.product-title',
        'prices': '.price',
        'ratings': '.rating-value',
        'availability': '.stock-status'
    }
    
    url = "https://example-store.com/products"  # Replace with actual URL
    data = scraper.scrape_page_data(url, selectors)
    
    # Save results
    scraper.save_to_json(data, 'products_data.json')
    return data

def example_scrape_multiple_pages():
    """Example: Scrape multiple pages"""
    scraper = WebScraper()
    all_data = []
    
    # List of URLs to scrape
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    
    selectors = {
        'title': 'h1',
        'content': '.main-content',
        'author': '.author-name'
    }
    
    for url in urls:
        data = scraper.scrape_page_data(url, selectors)
        data['url'] = url  # Add source URL
        all_data.append(data)
    
    # Save all results
    scraper.save_to_json(all_data, 'multiple_pages_data.json')
    scraper.save_to_csv(all_data, 'multiple_pages_data.csv')
    
    return all_data

if __name__ == "__main__":
    """
    Main execution block - customize this for your specific scraping needs
    """
    
    print("🕷️  Web Scraper Ready!")
    print("=" * 50)
    
    # Example 1: Basic scraping
    print("Example 1: Basic Page Scraping")
    scraper = WebScraper()
    
    # Replace this URL with your target website
    target_url = "https://www.fifacm.com/players"  # Safe test URL
    
    # Define what you want to scrape (customize these selectors)
    target_selectors = {
        'player_name': 'div.player-name a',
        'player_ovr': 'div.player-overall.rating-search.cm25.fifa-green-b'
    }
    
    # Scrape the data
    result = scraper.scrape_page_data(target_url, target_selectors)
    print("Scraped data:", result)
    
    # Save results
    scraper.save_to_json(result, 'scraped_data.json')
    
    print("\n" + "=" * 50)
    print("✅ Scraping completed! Check the output files.")
    print("📝 Customize the URL and selectors for your specific needs.")
