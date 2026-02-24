import pdfplumber

def extract(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_path, 'w') as f:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    f.write(text)
                    f.write("\n\n--- PAGE BREAK ---\n\n")

if __name__ == "__main__":
    extract("第三章.pdf", "chapter3_text.txt")
