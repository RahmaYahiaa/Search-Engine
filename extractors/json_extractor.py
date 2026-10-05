import json


def extract_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


if __name__ == '__main__':
    products = extract_json('data/products.json')
    print(products[:2])