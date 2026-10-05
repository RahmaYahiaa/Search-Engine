from PyPDF2 import PdfReader


def extract_pdf(file_path):
    reader = PdfReader(file_path)
    full_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)

    return "\n".join(full_text)


if __name__ == '__main__':
    text = extract_pdf('data/products.pdf')
    print(text[:500])