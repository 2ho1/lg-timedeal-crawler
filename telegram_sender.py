"""Telegram notification sender for LG Time Deal products."""
import logging
import requests
from typing import List, Dict
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, PRIORITY_PRODUCTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramSender:
    """Send product notifications via Telegram."""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.priority_products = [code.upper() for code in PRIORITY_PRODUCTS]
    
    def is_priority_product(self, product: Dict) -> bool:
        """Check if product is a priority product."""
        product_name = product.get('name', '').upper()
        product_model = product.get('model', '').upper()
        
        # Check if any priority code is in product name or model
        for code in self.priority_products:
            if code in product_name or code in product_model:
                return True
        return False
    
    def format_price(self, price: int) -> str:
        """Format price with commas."""
        if price is None:
            return "N/A"
        return f"{price:,}원"
    
    def format_product_message(self, product: Dict) -> str:
        """Format a single product as a message."""
        name = product.get('name', 'N/A')
        model = product.get('model', '')
        discount_rate = product.get('discount_rate')
        sale_price = product.get('sale_price')
        original_price = product.get('original_price')
        max_benefit_price = product.get('max_benefit_price')
        stock = product.get('stock')
        link = product.get('link', '')
        
        message = f"*{name}*\n"
        
        if model:
            message += f"모델명: `{model}`\n"
        
        if discount_rate:
            message += f"할인율: {discount_rate}%\n"
        
        if sale_price:
            message += f"할인 후: {self.format_price(sale_price)}\n"
        
        if original_price:
            message += f"할인 전: {self.format_price(original_price)}\n"
        
        if max_benefit_price:
            message += f"최대혜택가: {self.format_price(max_benefit_price)}\n"
        
        if stock is not None:
            message += f"재고: {stock}개 남음\n"
        
        if link:
            message += f"[상품 보기]({link})\n"
        
        return message
    
    def create_message(self, products: List[Dict]) -> str:
        """Create formatted message from products list (only priority products)."""
        if not products:
            return "오늘 타임딜 상품이 없습니다."
        
        # Filter only priority products
        priority_products = []
        for product in products:
            if self.is_priority_product(product):
                priority_products.append(product)
        
        # Build message
        message_parts = []
        
        if priority_products:
            message_parts.append("🔥 *원하는 상품 발견!* 🔥\n\n")
            for product in priority_products:
                message_parts.append(self.format_product_message(product))
                message_parts.append("---\n")
            message_parts.append(f"\n총 {len(priority_products)}개의 원하는 상품이 있습니다.")
        else:
            message_parts.append("오늘 원하는 상품(42C5, 42C4, 48C5, 48C4)이 없습니다.")
        
        return "\n".join(message_parts)
    
    def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
        """Send message to Telegram."""
        if not self.bot_token or not self.chat_id:
            logger.error("Telegram bot token or chat ID not configured")
            return False
        
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Message sent successfully to Telegram")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message to Telegram: {e}")
            return False
    
    def send_products(self, products: List[Dict]) -> bool:
        """Send only priority products to Telegram."""
        # Filter only priority products
        priority_products = [p for p in products if self.is_priority_product(p)]
        
        if not priority_products:
            logger.info("No priority products found. Skipping notification.")
            return True  # Not an error, just no products to send
        
        message = self.create_message(priority_products)
        
        # Telegram has a message length limit of 4096 characters
        # Split message if too long
        max_length = 4000  # Leave some buffer
        
        if len(message) <= max_length:
            return self.send_message(message)
        else:
            # Split into multiple messages if too long
            success = True
            chunk_size = 3  # Send 3 products per message
            for i in range(0, len(priority_products), chunk_size):
                chunk = priority_products[i:i + chunk_size]
                chunk_message = self.create_message(chunk)
                if not self.send_message(chunk_message):
                    success = False
            
            return success


if __name__ == "__main__":
    # Test with sample data
    sample_products = [
        {
            "name": "LG OLED TV OLED42C4ENA",
            "model": "OLED42C4ENA",
            "link": "https://www.lge.co.kr/tv/oled42c4ena",
            "discount_rate": 20,
            "sale_price": 1200000,
            "original_price": 1500000,
            "max_benefit_price": 1100000,
            "stock": 10,
        },
        {
            "name": "LG 가습기 HW500DAS",
            "model": "HW500DAS",
            "link": "https://www.lge.co.kr/humidifier/hw500das",
            "discount_rate": 15,
            "sale_price": 250000,
            "original_price": 300000,
            "stock": 50,
        },
    ]
    
    sender = TelegramSender()
    sender.send_products(sample_products)

