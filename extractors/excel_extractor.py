import pandas as pd


def extract_excel(file_path):
    df = pd.read_excel(file_path)
    return df.to_dict(orient='records')


if __name__ == '__main__':
    products = extract_excel('data/products.xlsx')
    print(products[:2])