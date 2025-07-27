import os
import json
from PyPDF2 import PdfReader

def extract_headings_from_text(text):
    lines = text.split('\n')
    headings = []
    for line in lines:
        clean_line = line.strip()
        if clean_line and (
            clean_line.isupper() or
            (len(clean_line.split()) <= 6 and len(clean_line) < 60) or
            clean_line.istitle()
        ):
            headings.append(clean_line)
    return headings

def get_pdf_title(reader):
    title = reader.metadata.title
    return title if title else "Untitled PDF"

def main():
    input_folder = 'sample_dataset/pdfs'
    output_folder = 'sample_dataset/outputs'

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)

            try:
                reader = PdfReader(pdf_path)
            except Exception as e:
                print(f" Error reading {filename}: {e}")
                continue

            title = get_pdf_title(reader)
            outline = []

            for i, page in enumerate(reader.pages):
                try:
                    text = page.extract_text() or ""
                    headings = extract_headings_from_text(text)
                    for heading in headings:
                        outline.append({
                            "level": "1",
                            "text": heading,
                            "page": i + 1
                        })
                except Exception as e:
                    print(f" Failed to read page {i+1} of {filename}: {e}")

            output_json = {
                "title": title,
                "outline": outline
            }

            output_path = os.path.join(output_folder, filename.replace('.pdf', '.json'))
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_json, f, indent=2, ensure_ascii=False)

            print(f" Done: {output_path}")

if __name__ == "__main__":
    main()
