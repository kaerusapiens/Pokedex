from flask import Flask, request, jsonify
import pandas as pd
import yaml
import os
from google.cloud import bigquery
import models

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main(request): # entry_pointと一緒の名前にする。
    generation = request.args.get('generation', 1, type=int) #基本取得ポケモン世代設定
    df = models.fetch_pokemon_data(generation)
    save_to_bigquery(df,generation)
    result = df.to_dict(orient='records') 
    return jsonify(result)


# YAML取得
def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config


#データBQへアップロード
def save_to_bigquery(df, generation):
    config = load_config()
    dataset_id = config['bq_dataset_id']
    table_id = f"generation_{generation}"
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)
    
    try:
        client.delete_table(table_ref, not_found_ok=True)
        print(f"テーブル {table_id} は存在する場合削除されました。")
        
        job = client.load_table_from_dataframe(df, table_ref)
        job.result()
        print(f"データが {table_id} に正常にロードされました。")
    except Exception as e:
        print(f"BigQuery へのデータロード中にエラーが発生しました: {e}")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)