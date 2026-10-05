import pandas as pd


def extract_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')


if __name__ == '__main__':
    products = extract_csv('data/products.csv')
    print(products[:2])