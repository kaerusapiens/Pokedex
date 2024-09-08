import os
from flask import Flask, request, jsonify
import models
from bigquery_client import save_to_bigquery

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main(request): # entry_pointと一緒の名前にする。
    generation = request.args.get('generation', 1, type=int) #基本取得ポケモン世代設定
    df = models.fetch_pokemon_data(generation)
    save_to_bigquery(df,generation)
    result = df.to_dict(orient='records') 
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)