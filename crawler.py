"""LG Time Deal product crawler."""
import json
import os
import re
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser
import logging
from config import LG_TIMEDEAL_URL, PRODUCTS_JSON, DATA_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LGTimedealCrawler:
    """Crawler for LG Time Deal products."""
    
    def __init__(self):
        self.url = LG_TIMEDEAL_URL
        self.products = []
        
    def extract_price(self, text: str) -> Optional[int]:
        """Extract price from text (remove commas and '원')."""
        if not text:
            return None
        # Remove commas and '원', then extract numbers
        price_str = re.sub(r'[,\s원]', '', text)
        try:
            return int(price_str)
        except ValueError:
            return None
    
    def extract_discount_rate(self, text: str) -> Optional[int]:
        """Extract discount rate from text."""
        if not text:
            return None
        # Extract number before %
        match = re.search(r'(\d+)%', text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None
    
    def extract_stock(self, text: str) -> Optional[int]:
        """Extract stock quantity from text."""
        if not text:
            return None
        # Extract number before '개 남음'
        match = re.search(r'(\d+)개\s*남음', text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None
    
    def extract_product_info(self, page: Page, product_element) -> Optional[Dict]:
        """Extract product information from a product element."""
        try:
            # Get all text content first
            full_text = product_element.inner_text()
            
            # Skip if doesn't contain essential product info
            if '할인' not in full_text or '판매가' not in full_text:
                return None
            
            # Get product name - try multiple selectors
            product_name = ""
            product_link = ""
            
            # Try to find product name link
            name_selectors = [
                'a[href*="/"]',
                'a[href*="lge.co.kr"]',
                'link',
            ]
            
            for selector in name_selectors:
                name_element = product_element.query_selector(selector)
                if name_element:
                    product_name = name_element.inner_text().strip()
                    product_link = name_element.get_attribute('href') or ""
                    if product_link and not product_link.startswith('http'):
                        product_link = f"https://www.lge.co.kr{product_link}"
                    break
            
            # If no name found, try to extract from text
            if not product_name:
                # Look for product name pattern (usually before model number)
                name_match = re.search(r'^([^0-9]+?)([A-Z0-9]{6,})', full_text)
                if name_match:
                    product_name = name_match.group(1).strip()
                else:
                    # Fallback: take first line or first meaningful text
                    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                    if lines:
                        product_name = lines[0]
            
            # Extract model number - look for alphanumeric codes (usually 6+ chars)
            model_number = ""
            model_match = re.search(r'\b([A-Z]{2,}\d{2,}[A-Z0-9]*)\b', full_text)
            if model_match:
                model_number = model_match.group(1)
            
            # Extract discount rate
            discount_rate = None
            discount_match = re.search(r'할인\s*율[^\d]*(\d+)%', full_text)
            if discount_match:
                discount_rate = int(discount_match.group(1))
            else:
                # Try alternative pattern
                discount_match = re.search(r'(\d+)%\s*할인', full_text)
                if discount_match:
                    discount_rate = int(discount_match.group(1))
            
            # Extract sale price (할인 후 판매가)
            sale_price = None
            sale_match = re.search(r'할인\s*후\s*판매가[^\d]*([\d,]+)', full_text)
            if sale_match:
                sale_price = self.extract_price(sale_match.group(1))
            else:
                # Try alternative: look for price after "할인 후"
                sale_match = re.search(r'할인\s*후[^\d]*([\d,]+)', full_text)
                if sale_match:
                    sale_price = self.extract_price(sale_match.group(1))
            
            # Extract original price (할인 전 정가)
            original_price = None
            original_match = re.search(r'할인\s*전\s*정가[^\d]*([\d,]+)', full_text)
            if original_match:
                original_price = self.extract_price(original_match.group(1))
            else:
                # Try alternative pattern
                original_match = re.search(r'정가[^\d]*([\d,]+)', full_text)
                if original_match:
                    original_price = self.extract_price(original_match.group(1))
            
            # Extract max benefit price (최대혜택가)
            max_benefit_price = None
            max_benefit_match = re.search(r'최대혜택가[^\d]*([\d,]+)', full_text)
            if max_benefit_match:
                max_benefit_price = self.extract_price(max_benefit_match.group(1))
            
            # Extract stock
            stock = self.extract_stock(full_text)
            
            # Only return if we have at least a name
            if not product_name:
                return None
            
            product_info = {
                "name": product_name,
                "model": model_number,
                "link": product_link,
                "discount_rate": discount_rate,
                "sale_price": sale_price,
                "original_price": original_price,
                "max_benefit_price": max_benefit_price,
                "stock": stock,
            }
            
            return product_info
            
        except Exception as e:
            logger.error(f"Error extracting product info: {e}")
            return None
    
    def crawl(self) -> List[Dict]:
        """Crawl products from LG Time Deal page."""
        logger.info(f"Starting crawl of {self.url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                page.goto(self.url, wait_until="networkidle", timeout=60000)
                
                # Wait for products to load
                page.wait_for_timeout(3000)
                
                # Find all product elements with data-ec-product attribute
                products = []
                
                # Try multiple selectors to find products
                selectors = [
                    '[data-ec-product]',
                    '.product-item',
                    'li[class*="product"]',
                    'div[class*="product"]',
                ]
                
                product_elements = []
                for selector in selectors:
                    elements = page.query_selector_all(selector)
                    if elements:
                        product_elements = elements
                        logger.info(f"Found {len(elements)} products using selector: {selector}")
                        break
                
                # If no products found with data-ec-product, try to find by tabpanel content
                if not product_elements:
                    # Get all tabpanels
                    tabpanels = page.query_selector_all('div[role="tabpanel"]')
                    logger.info(f"Found {len(tabpanels)} tabpanels")
                    
                    for tabpanel in tabpanels:
                        # Find all list items in tabpanel
                        list_items = tabpanel.query_selector_all('li')
                        for item in list_items:
                            # Check if it contains product information
                            text = item.inner_text()
                            if '할인' in text and ('판매가' in text or '정가' in text):
                                product_elements.append(item)
                
                # Also try to find products by data-ec-product attribute using JavaScript
                if not product_elements:
                    try:
                        # Execute JavaScript to find all elements with data-ec-product
                        product_elements_js = page.evaluate("""
                            () => {
                                const products = document.querySelectorAll('[data-ec-product]');
                                return Array.from(products).map(el => ({
                                    name: el.querySelector('a')?.textContent?.trim() || '',
                                    link: el.querySelector('a')?.href || '',
                                    text: el.innerText
                                }));
                            }
                        """)
                        
                        if product_elements_js:
                            logger.info(f"Found {len(product_elements_js)} products via JavaScript")
                            # Re-query elements to get actual DOM elements
                            product_elements = page.query_selector_all('[data-ec-product]')
                    except Exception as e:
                        logger.warning(f"JavaScript product detection failed: {e}")
                
                logger.info(f"Total product elements found: {len(product_elements)}")
                
                # Extract product information
                for element in product_elements:
                    product_info = self.extract_product_info(page, element)
                    if product_info and product_info.get('name'):
                        products.append(product_info)
                        logger.info(f"Extracted: {product_info['name']}")
                
                browser.close()
                
                logger.info(f"Crawled {len(products)} products")
                self.products = products
                return products
                
            except Exception as e:
                logger.error(f"Error during crawl: {e}")
                browser.close()
                return []
    
    def save_products(self, products: Optional[List[Dict]] = None):
        """Save products to JSON file."""
        if products is None:
            products = self.products
        
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Save to JSON
        with open(PRODUCTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(products)} products to {PRODUCTS_JSON}")
    
    def load_products(self) -> List[Dict]:
        """Load products from JSON file."""
        if os.path.exists(PRODUCTS_JSON):
            with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
                products = json.load(f)
            logger.info(f"Loaded {len(products)} products from {PRODUCTS_JSON}")
            return products
        return []


if __name__ == "__main__":
    crawler = LGTimedealCrawler()
    products = crawler.crawl()
    crawler.save_products(products)

