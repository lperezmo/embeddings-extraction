#------------------------------------#
# Import Libraries
#------------------------------------#
import os
import re
import os
import PyPDF2
import re
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

#------------------------------------#
# Data Preparation for HTML Files
#------------------------------------#

def extract_metadata_from_html(html_content):
    """
    Extracts text, title, headings, and image names from an HTML document.

    Parameters
    ----------
    html_content : str

    Returns
    -------
    text : str
    title : str
    headings : list of str
    images : list of str
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title = soup.title.string if soup.title else None
    
    # Extract headings
    headings = []
    for h_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for heading in soup.find_all(h_tag):
            headings.append(heading.get_text(strip=True))

    # Extract images
    images = [img.get('src') for img in soup.find_all('img')]

    # Remove script and style elements to avoid extracting unwanted text
    for script in soup(['script', 'style']):
        script.decompose()
        
    text = soup.get_text()
    cleaned_text = re.sub(r'\s+', ' ', text).strip() # Remove extra whitespace and newlines

    return cleaned_text, title, headings, images

import chardet

def process_html_files(folder_path):
    """
    Extracts text, title, headings, and image names from all HTML files in a folder.
    
    Parameters
    ----------
    folder_path : str
    
    Returns
    -------
    extracted_data : list of dict
    
    Example
    -------
    >>> folder_path = 'Made2Manage' # Set the path to your HTML files folder
    >>> extracted_text_data = process_html_files(folder_path)
    """
    extracted_data = []
    
    for root, dirs, files in os.walk(folder_path): # Use os.walk to traverse subdirectories
        for file in files:
            if file.endswith('.htm'):
                file_path = os.path.join(root, file)

                # Detect file encoding using chardet
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    detected_encoding = chardet.detect(raw_data)['encoding']

                # Read the file using the detected encoding
                with open(file_path, 'r', encoding=detected_encoding) as f:
                    html_content = f.read()

                    text, title, headings, images = extract_metadata_from_html(html_content)

                    extracted_data.append({
                        'file': file,
                        'text': text,
                        'title': title,
                        'headings': headings,
                        'images': images,
                        'folder': os.path.relpath(root, folder_path), # Calculate the relative directory path
                    })

    return extracted_data


#------------------------------------#
# Data Preparation for PDF Files
#------------------------------------#

def extract_images_from_pdf_page(page):
    """
    Extracts images from a PDF page.
    
    Parameters
    ----------
    page : PyPDF2.pdf.PageObject
    
    Returns
    -------
    images : list of PIL.Image.Image
    """
    images = []
    xObject = page['/Resources']['/XObject'].get_object()

    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj].get_data()
            image = Image.open(BytesIO(data))
            images.append(image)

    return images

def extract_text_from_pdf(pdf_content):
    """
    Extracts text, title, headings, and image names from a PDF document.
    
    Parameters
    ----------
    pdf_content : file-like object
    
    Returns
    -------
    text : str
    title : str
    headings : list of str
    images : list of str
    
    Example
    -------
    >>> with open('sample.pdf', 'rb') as f:
    >>>     pdf_content = f # Pass in the file-like object
    >>>     text, title, headings, images = extract_text_from_pdf(pdf_content)  
    """
    pdf_reader = PyPDF2.PdfReader(pdf_content)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text() + ' '

    try:
        metadata = pdf_reader.metadata
    except:
        # Fill with fake data if metadata extraction fails
        metadata = {'/Title': pdf_content.name}
    title = metadata.get('/Title', pdf_content.name)

    # headings = extract_headings(text)
    headings = metadata.get('/Title', pdf_content.name)
    try:
        images = []
        for page_num in range(len(pdf_reader.pages)):
            images.extend(extract_images_from_pdf_page(pdf_reader.pages[page_num]))
    except:
        pass

    return text.strip(), title, headings, images

def process_pdf_files(folder_path):
    """
    Extracts text, title, headings, and image names from all PDF files in a folder.
    
    Parameters
    ----------
    folder_path : str
    
    Returns
    -------
    extracted_data : list of dict
    
    Example
    -------
    >>> folder_path = 'Made2Manage' # Set the path to your PDF files folder
    >>> extracted_text_data = process_pdf_files(folder_path)
    """
    extracted_data = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)

                with open(file_path, 'rb') as f:
                    pdf_content = f

                    extracted_text, title, headings, images = extract_text_from_pdf(pdf_content)
                    extracted_data.append({
                        'file': file,
                        'text': extracted_text,
                        'folder': os.path.relpath(root, folder_path),
                        'title': title,
                        'headings': headings,
                        'images': images,
                    })

    return extracted_data