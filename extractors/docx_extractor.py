from docx import Document


def extract_docx(file_path):
    document = Document(file_path)
    full_text = []

    for paragraph in document.paragraphs:
        full_text.append(paragraph.text)

    return '\n'.join(full_text)


if __name__ == '__main__':
    text = extract_docx('data/products.docx')
    print(text[:500])