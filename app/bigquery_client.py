import yaml
from google.cloud import bigquery


def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config


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