import pandas as pd
import json

# Carrega o arquivo CSV
file_path = "data.csv"  # Atualize com o caminho correto do arquivo
df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)

# Obtém o nome da primeira coluna
primeira_coluna = df.columns[0]

# Converte cada linha em um dicionário e usa o valor da primeira coluna como chave
data_dict = {row[primeira_coluna]: {k: v for k, v in row.items() if k != primeira_coluna} for row in df.to_dict(orient="records")}

# Salva o dicionário em um arquivo JSON
json_path = "processed_data.json"
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

print(f"Arquivo JSON salvo como {json_path}")