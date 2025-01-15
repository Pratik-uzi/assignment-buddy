from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
import os
import concurrent.futures

def process_file(file_path, output_folder):
    # Get text from file
    ext = os.path.splitext(file_path)[1].lower()
    text = extract_text_from_pdf(file_path) if ext == '.pdf' else extract_text_from_docx(file_path)
    
    # Load and cache resources
    font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    bg = Image.open(os.path.join(font_dir, "bg.png"))
    space_width = Image.open(os.path.join(font_dir, "space.png")).width

    # Preload all characters in parallel
    char_cache = {}
    def load_char(i):
        try:
            return chr(i), Image.open(os.path.join(font_dir, f"{i}.png"))
        except:
            return None

    # Use thread pool for faster image loading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(load_char, range(32, 127))
        char_cache = dict(filter(None, results))

    # Initialize page variables
    pages = []
    gap, ht = 50, 50
    line_height = 120
    current_page = bg.copy()
    
    # Process words in chunks for better performance
    words = text.split()
    chunk_size = 50  # Process 50 words at a time
    
    for i in range(0, len(words), chunk_size):
        word_chunk = words[i:i + chunk_size]
        
        for word in word_chunk:
            # Quick word width calculation
            word_width = sum(char_cache[c].width for c in word if c in char_cache)
            
            # New line check
            if gap + word_width > bg.width - 50:
                gap = 50
                ht += line_height
                
                # New page check
                if ht > bg.height - 100:
                    pages.append(current_page)
                    current_page = bg.copy()
                    gap, ht = 50, 50
            
            # Write word
            for char in word:
                if char in char_cache:
                    char_img = char_cache[char]
                    y_offset = -20 if ord(char) in [103, 106, 112, 113, 121] else 0
                    current_page.paste(char_img, (gap, ht + y_offset))
                    gap += char_img.width
            
            gap += space_width
    
    # Add final page
    pages.append(current_page)
    
    # Save as PDF
    output_filename = f"handwritten_{os.path.splitext(os.path.basename(file_path))[0]}.pdf"
    output_path = os.path.join(output_folder, output_filename)
    
    pages[0].save(
        output_path, 
        'PDF', 
        resolution=100.0,
        save_all=True if len(pages) > 1 else False,
        append_images=pages[1:] if len(pages) > 1 else None
    )
    
    return output_path

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        return ' '.join(page.extract_text() for page in reader.pages)

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return ' '.join(paragraph.text for paragraph in doc.paragraphs)