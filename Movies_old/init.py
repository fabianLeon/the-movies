import zipfile

with zipfile.ZipFile('credits.csv.zip', 'r') as zip_ref:
    zip_ref.extractall('.')

with zipfile.ZipFile('keywords.csv.zip', 'r') as zip_ref:
    zip_ref.extractall('.')

with zipfile.ZipFile('movies_metadata.csv.zip', 'r') as zip_ref:
    zip_ref.extractall('.')