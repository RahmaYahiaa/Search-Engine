def extract_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


if __name__ == '__main__':
    text = extract_txt('data/products.txt')
    print(text[:500])