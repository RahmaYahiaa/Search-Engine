import os

from json_extractor import extract_json
from csv_extractor import extract_csv
from excel_extractor import extract_excel
from txt_extractor import extract_txt
from docx_extractor import extract_docx
from pdf_extractor import extract_pdf


def extract_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.json':
        return extract_json(file_path)

    elif extension == '.csv':
        return extract_csv(file_path)

    elif extension == '.xlsx':
        return extract_excel(file_path)

    elif extension == '.txt':
        return extract_txt(file_path)

    elif extension == '.docx':
        return extract_docx(file_path)

    elif extension == '.pdf':
        return extract_pdf(file_path)

    else:
        raise ValueError('Unsupported file type')


if __name__ == '__main__':
    data = extract_file('data/products.csv')
    print(data[:2])