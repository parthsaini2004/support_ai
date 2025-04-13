# utils/pdf_parser.py
import PyPDF2
import logging
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFInstructionsParser:
    def __init__(self):
        pass
    
    def parse(self, pdf_path):
        """Parse instructions from a PDF file"""
        try:
            logger.info(f"Parsing instructions from {pdf_path}")
            
            # Open the PDF file
            with open(pdf_path, "rb") as file:
                # Create a PDF reader object
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Get the number of pages
                num_pages = len(pdf_reader.pages)
                
                # Extract text from each page
                full_text = ""
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    full_text += page.extract_text()
                
                # Process the extracted text
                instructions = self._process_text(full_text)
                
                return instructions
                
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            return None
    
    def _process_text(self, text):
        """Process the extracted text to identify instructions"""
        # Split text into sections (this is a simple implementation and can be enhanced)
        sections = re.split(r'\n\s*\n', text)
        
        # Initialize instructions dictionary
        instructions = {
            "general": [],
            "refund_policy": [],
            "order_tracking": [],
            "faqs": []
        }
        
        # Process each section to categorize instructions
        current_category = "general"
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
                
            # Try to identify section headers
            lower_section = section.lower()
            
            if any(keyword in lower_section for keyword in ["refund", "return", "money back"]):
                current_category = "refund_policy"
                
            elif any(keyword in lower_section for keyword in ["track", "shipping", "delivery", "order status"]):
                current_category = "order_tracking"
                
            elif any(keyword in lower_section for keyword in ["faq", "frequently asked", "common question"]):
                current_category = "faqs"
            
            # Add the section to the appropriate category
            if section not in instructions[current_category]:
                instructions[current_category].append(section)
        
        return instructions