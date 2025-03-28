#!/usr/bin/env python3
"""
Graphical Abstract Image Converter - Resizes images to 1200px square at 300dpi
This script converts images to a standard size and resolution for graphical abstracts.
By Sami Adnan.

Usage:
    python image_converter.py input_file.ext [--options]

This script takes an input image file (TIFF, PDF, JPG, PNG) and creates:
- PDF  (1200px square at 300dpi)
- TIFF (1200px square at 300dpi)
- PNG  (1200px square at 300dpi)

The output file names will include dimensions and resolution information.

Options:
    --preserve-vector  When used with PDF input, preserves vector elements in the PDF output.
                       This preserves text, line art, and other vector graphics.
                       Requires --pdf-only to avoid rasterization.
                       
    --pdf-only        Only generate the PDF output, skip TIFF and PNG outputs.
                      Useful when you only need the PDF version or when combined
                      with --preserve-vector to maintain vector quality.

Examples:
    # Basic usage (creates all three formats, rasterized)
    python image_converter.py your-image.tiff
    
    # Preserve vector elements in PDF (vector PDF only)
    python image_converter.py your-image.pdf --preserve-vector --pdf-only
    
    # Generate only PDF output, but rasterized
    python image_converter.py your-image.png --pdf-only

Requirements:
    pip install pillow pypdf reportlab pdf2image
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import pypdf

# Check if pdf2image is available
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

def process_pdf_preserve_vector(pdf_path, output_dir, base_name):
    """
    Process PDF while preserving vector elements (for PDF output only)
    """
    try:
        print("Processing PDF with vector preservation...")
        # Open the input PDF
        pdf_reader = pypdf.PdfReader(pdf_path)
        if len(pdf_reader.pages) == 0:
            print("Error: Input PDF has no pages")
            return False

        # Get the first page
        page = pdf_reader.pages[0]
        
        # Get the original page dimensions
        orig_width = float(page.mediabox.width)
        orig_height = float(page.mediabox.height)
        
        # Calculate target size in points (72 points per inch)
        target_size_pt = 1200 / 300 * 72  # = 288 points
        
        # Calculate the scale to fit to a square while preserving aspect ratio
        if orig_width > orig_height:
            scale_width = target_size_pt / orig_width
            scale_height = scale_width
        else:
            scale_height = target_size_pt / orig_height
            scale_width = scale_height
            
        # Calculate new dimensions
        new_width = orig_width * scale_width
        new_height = orig_height * scale_height
        
        # Calculate centering offsets to place in center of square
        x_offset = (target_size_pt - new_width) / 2
        y_offset = (target_size_pt - new_height) / 2
        
        # Create a new PDF writer
        pdf_writer = pypdf.PdfWriter()
        
        # Create a new blank PDF page with the target square dimensions
        # This is tricky with pypdf, so we'll use reportlab to create a blank page
        temp_blank_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_blank_pdf.close()
        c = canvas.Canvas(temp_blank_pdf.name, pagesize=(target_size_pt, target_size_pt))
        c.setFillColorRGB(1, 1, 1)  # White background
        c.rect(0, 0, target_size_pt, target_size_pt, fill=True)
        c.save()
        
        # Read the blank page
        blank_pdf = pypdf.PdfReader(temp_blank_pdf.name)
        blank_page = blank_pdf.pages[0]
        
        # Add the blank page to the writer
        pdf_writer.add_page(blank_page)
        
        # Get the target page
        target_page = pdf_writer.pages[0]
        
        # Merge the original page onto the blank page with scaling and offset
        target_page.merge_transformed_page(
            page, 
            pypdf.Transformation().scale(scale_width, scale_height).translate(x_offset, y_offset)
        )
        
        # Generate output filename
        pdf_output = os.path.join(output_dir, f"{base_name}_1200px_300dpi.pdf")
        
        # Save the new PDF
        with open(pdf_output, 'wb') as f:
            pdf_writer.write(f)
            
        print(f"PDF saved with vector elements preserved: {pdf_output}")
        
        # Clean up the temporary file
        os.unlink(temp_blank_pdf.name)
        
        return True
        
    except Exception as e:
        print(f"Error processing PDF with vector preservation: {e}")
        return False

def process_pdf(pdf_path):
    """
    Extract the first page of a PDF as an image
    """
    if PDF2IMAGE_AVAILABLE:
        try:
            # Convert the first page of the PDF to an image using pdf2image
            print("Converting PDF to image using pdf2image...")
            images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=300)
            if images:
                return images[0]  # Return the first page as an image
        except Exception as e:
            print(f"Warning: pdf2image conversion failed: {e}")
            print("Falling back to alternative method...")
    
    # Fallback method using PyPDF
    try:
        print("Converting PDF using PyPDF...")
        # Create a temporary file to save an intermediate PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_pdf_path = temp_file.name
        
        # Extract the first page of the PDF
        pdf_reader = pypdf.PdfReader(pdf_path)
        pdf_writer = pypdf.PdfWriter()
        if len(pdf_reader.pages) > 0:
            pdf_writer.add_page(pdf_reader.pages[0])
            with open(temp_pdf_path, 'wb') as f:
                pdf_writer.write(f)
        
        # Try to convert using pdf2image if available or warn user
        if PDF2IMAGE_AVAILABLE:
            images = convert_from_path(temp_pdf_path, dpi=300)
            if images:
                # Remove the temporary file
                os.unlink(temp_pdf_path)
                return images[0]
        else:
            print("Warning: pdf2image module not available. Cannot convert PDF to image directly.")
            print("Please install poppler and pdf2image:")
            print("  Mac: brew install poppler && pip install pdf2image")
            print("  Linux: apt-get install poppler-utils && pip install pdf2image")
            print("  Windows: Install poppler from https://github.com/oschwartz10612/poppler-windows/releases")
            print("           Then: pip install pdf2image")
            print("\nAlternatively, convert your PDF to an image format first using another tool.")
            
        # Remove the temporary file
        os.unlink(temp_pdf_path)
    except Exception as e:
        print(f"Error processing PDF: {e}")
    
    return None

def resize_and_save(input_path, preserve_vector=False, pdf_only=False):
    """
    Resize the input image to 1200x1200 pixels at 300dpi and save in multiple formats
    """
    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.dirname(input_path) or '.'
    
    # Check file extension
    ext = os.path.splitext(input_path)[1].lower()
    
    # Special handling for PDF with vector preservation
    if ext == '.pdf' and preserve_vector:
        if not pdf_only:
            print("Error: --preserve-vector requires --pdf-only to avoid rasterization.")
            return False
        
        return process_pdf_preserve_vector(input_path, output_dir, base_name)
    
    # Handle PDF files for rasterization
    if ext == '.pdf':
        img = process_pdf(input_path)
        if img is None:
            print("Could not process PDF. Please convert it to an image format first.")
            return False
    else:
        # Open the image file
        try:
            img = Image.open(input_path)
        except Exception as e:
            print(f"Error opening input file: {e}")
            return False
    
    # Convert to RGB if it's RGBA (for PDF compatibility)
    if img.mode == 'RGBA':
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        img = rgb_img
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize the image to 1200x1200 while maintaining aspect ratio
    # Calculate the new dimensions while preserving aspect ratio
    width, height = img.size
    if width > height:
        new_height = int(1200 * height / width)
        new_width = 1200
    else:
        new_width = int(1200 * width / height)
        new_height = 1200
    
    # Create a white background image of 1200x1200
    resized_img = Image.new('RGB', (1200, 1200), (255, 255, 255))
    
    # Resize the original image
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Paste the resized image centered on the white background
    offset = ((1200 - new_width) // 2, (1200 - new_height) // 2)
    resized_img.paste(img, offset)
    
    # Set DPI to 300
    dpi = (300, 300)
    
    # Generate output filenames with informative suffixes
    tiff_output = os.path.join(output_dir, f"{base_name}_1200px_300dpi.tiff")
    png_output = os.path.join(output_dir, f"{base_name}_1200px_300dpi.png")
    pdf_output = os.path.join(output_dir, f"{base_name}_1200px_300dpi.pdf")
    
    # Save as TIFF with 300 DPI (unless pdf_only is specified)
    if not pdf_only:
        resized_img.save(
            tiff_output, 
            format='TIFF', 
            dpi=dpi, 
            compression='tiff_lzw'
        )
        print(f"TIFF saved: {tiff_output}")
        
        # Save as PNG with 300 DPI
        resized_img.save(
            png_output, 
            format='PNG', 
            dpi=dpi
        )
        print(f"PNG saved: {png_output}")
    
    # Create PDF with ReportLab (this gives better control over DPI)
    pdf_width = 1200 / 300 * 72  # Convert to points (72 points per inch)
    pdf_height = 1200 / 300 * 72
    
    c = canvas.Canvas(pdf_output, pagesize=(pdf_width, pdf_height))
    c.setPageSize((pdf_width, pdf_height))
    c.drawImage(
        ImageReader(resized_img), 
        0, 0, 
        width=pdf_width, 
        height=pdf_height
    )
    c.save()
    print(f"PDF saved: {pdf_output}")
    
    return True

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert images to 1200px square at 300dpi in various formats')
    parser.add_argument('input_file', help='Input image file path')
    parser.add_argument('--preserve-vector', action='store_true', 
                        help='Preserve vector elements when processing PDF files (PDF output only)')
    parser.add_argument('--pdf-only', action='store_true',
                        help='Only generate PDF output, skip TIFF and PNG')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Enforce that --preserve-vector requires --pdf-only
    if args.preserve_vector and not args.pdf_only:
        print("Error: --preserve-vector requires --pdf-only to avoid rasterization.")
        print("Please add the --pdf-only option when using --preserve-vector.")
        return 1
    
    # Check if input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return 1
    
    # Process the image
    if resize_and_save(args.input_file, args.preserve_vector, args.pdf_only):
        print("Conversion completed successfully!")
        return 0
    else:
        print("Conversion failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())