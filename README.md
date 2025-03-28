# Cell Press Graphical Abstract Image Converter

[![View on GitHub](https://img.shields.io/badge/GitHub-View_on_GitHub-blue?logo=GitHub)](https://github.com/sami5001/graphical-abstract-converter)
[![Download](https://img.shields.io/badge/Download-Latest_Release-green?logo=github)](https://github.com/sami5001/graphical-abstract-converter/releases)

A Python script for converting images to journal submission specifications (1200px square at 300 DPI).

**Author:** [Hassan Sami Adnan](https://sami.cloud)

Nuffield Department of Primary Care Health Sciences, University of Oxford 

## Description

This tool converts images to the exact specifications required by Cell Press journals, specifically designed for the iScience journal's graphical abstract requirements. It handles various input formats (TIFF, PDF, JPG, PNG) and produces properly sized and formatted outputs.

Please use this at your own descretion. Always check the journal guidelines as specifications may change.

The conversion is based on the guidelines provided by Cell Press iScience journal:
- [Graphical Abstract Guidelines](https://www.cell.com/pb/assets/raw/shared/figureguidelines/GA_guide.pdf)
- [iScience Author Guidelines](https://www.cell.com/iscience/authors)

## Features

- Resizes images to exactly 1200×1200 pixels at 300 DPI
- Maintains aspect ratio by adding white padding where needed
- Creates multiple output formats (PDF, TIFF, PNG)
- Optional vector preservation for PDF inputs
- Handles various input formats

## Requirements

- Python 3.6+
- Required Python packages:
  - pillow
  - pypdf
  - reportlab
  - pdf2image
- Poppler (system dependency for pdf2image)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/journal-image-converter.git
   cd journal-image-converter
   ```

2. Install required Python packages:
   ```
   pip install pillow pypdf reportlab pdf2image
   ```

3. Install Poppler (required for PDF processing):
   - **macOS**: `brew install poppler`
   - **Linux**: `apt-get install poppler-utils`
   - **Windows**: Download from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases)

## Usage

### Basic Usage

```bash
python image_converter.py input_file.ext
```

This will create three output files in the same directory:
- `input_file_1200px_300dpi.pdf`
- `input_file_1200px_300dpi.tiff`
- `input_file_1200px_300dpi.png`

### Preserving Vector Elements (PDF only)

```bash
python image_converter.py input_file.pdf --preserve-vector --pdf-only
```

This preserves vector elements in PDF files (text, line art, etc.) and only outputs a PDF file.

### Options

- `--preserve-vector`: Preserves vector elements when processing PDF files (PDF output only)
- `--pdf-only`: Only generate the PDF output, skip TIFF and PNG outputs

## Examples

```bash
# Convert a TIFF image to all formats
python image_converter.py figure.tiff

# Convert a JPG image to all formats
python image_converter.py photo.jpg

# Convert a PDF while preserving vector elements
python image_converter.py diagram.pdf --preserve-vector --pdf-only

# Generate only the PDF output from any image
python image_converter.py image.png --pdf-only
```

## Use Cases

- Preparing graphical abstracts for journal submission
- Converting presentation slides to journal-ready figures
- Standardizing image dimensions for publication
- Ensuring proper DPI for print publication

## License

This project is licensed under the Creative Commons Attribution License - see the [LICENSE](LICENSE) file for details.

When using or adapting this tool, please provide attribution to Hassan Sami Adnan.

## Contributions

Contributions to improve this tool are welcome! Here's how you can contribute:

1. **Fork the repository** - Create your own fork of the project
2. **Create a feature branch** - `git checkout -b feature/your-feature-name`
3. **Commit your changes** - `git commit -m 'Add some feature'`
4. **Push to your branch** - `git push origin feature/your-feature-name`
5. **Open a Pull Request** - Go to the original repository and create a pull request

Please make sure your code follows the existing style and includes appropriate documentation. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Created based on the iScience journal submission guidelines
- Inspired by the needs of researchers preparing materials for publication

---

# Journal Image Converter

[![View on GitHub](https://img.shields.io/badge/GitHub-View_on_GitHub-blue?logo=GitHub)](https://github.com/sami5001/graphical-abstract-converter)
[![Download](https://img.shields.io/badge/Download-Latest_Release-green?logo=github)](https://github.com/sami5001/graphical-abstract-converter/releases)

A Python script for converting images to journal submission specifications (1200px square at 300 DPI).

**Author:** Hassan Sami Adnan

## Description

This tool converts images to the exact specifications required by academic journals, specifically designed for the iScience journal's graphical abstract requirements. It handles various input formats (TIFF, PDF, JPG, PNG) and produces properly sized and formatted outputs.

The conversion is based on the guidelines provided by the iScience journal:
- [Graphical Abstract Guidelines](https://www.cell.com/pb/assets/raw/shared/figureguidelines/GA_guide.pdf)
- [iScience Author Guidelines](https://www.cell.com/iscience/authors)

## Features

- Resizes images to exactly 1200×1200 pixels at 300 DPI
- Maintains aspect ratio by adding white padding where needed
- Creates multiple output formats (PDF, TIFF, PNG)
- Optional vector preservation for PDF inputs
- Handles various input formats

## Requirements

- Python 3.6+
- Required Python packages:
  - pillow
  - pypdf
  - reportlab
  - pdf2image
- Poppler (system dependency for pdf2image)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/journal-image-converter.git
   cd journal-image-converter
   ```

2. Install required Python packages:
   ```
   pip install pillow pypdf reportlab pdf2image
   ```

3. Install Poppler (required for PDF processing):
   - **macOS**: `brew install poppler`
   - **Linux**: `apt-get install poppler-utils`
   - **Windows**: Download from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases)

## Usage

### Basic Usage

```bash
python image_converter.py input_file.ext
```

This will create three output files in the same directory:
- `input_file_1200px_300dpi.pdf`
- `input_file_1200px_300dpi.tiff`
- `input_file_1200px_300dpi.png`

### Preserving Vector Elements (PDF only)

```bash
python image_converter.py input_file.pdf --preserve-vector --pdf-only
```

This preserves vector elements in PDF files (text, line art, etc.) and only outputs a PDF file.

### Options

- `--preserve-vector`: Preserves vector elements when processing PDF files (PDF output only)
- `--pdf-only`: Only generate the PDF output, skip TIFF and PNG outputs

## Examples

```bash
# Convert a TIFF image to all formats
python image_converter.py figure.tiff

# Convert a JPG image to all formats
python image_converter.py photo.jpg

# Convert a PDF while preserving vector elements
python image_converter.py diagram.pdf --preserve-vector --pdf-only

# Generate only the PDF output from any image
python image_converter.py image.png --pdf-only
```

## Use Cases

- Preparing graphical abstracts for journal submission
- Converting presentation slides to journal-ready figures
- Standardizing image dimensions for publication
- Ensuring proper DPI for print publication

## License

This project is licensed under the Creative Commons Attribution License - see the [LICENSE](LICENSE) file for details.

When using or adapting this tool, please provide attribution to Hassan Sami Adnan.

## Contributions

Contributions to improve this tool are welcome! Here's how you can contribute:

1. **Fork the repository** - Create your own fork of the project
2. **Create a feature branch** - `git checkout -b feature/your-feature-name`
3. **Commit your changes** - `git commit -m 'Add some feature'`
4. **Push to your branch** - `git push origin feature/your-feature-name`
5. **Open a Pull Request** - Go to the original repository and create a pull request

Please make sure your code follows the existing style and includes appropriate documentation. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Created based on the iScience journal submission guidelines
- Inspired by the needs of researchers preparing materials for publication