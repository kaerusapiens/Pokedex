

# 🧪実現したいこと
1.TerraformでGCP構成を管理する。
- service account作成
- IAM policy binding
- GCS作成, GCF作成(HTTPトリガー)
- GCLBセットアップ + Cloud Armorによるセキュリティー担保

2.appについて

ポケモン世代別の図鑑(Pokedex)をデータベース化する
- 開発はFlaskで
- Pokemon REST APIでデータを取得
 https://pokeapi.co/docs/v2
- そのデータをBQへロード
- パラメーターにより、特定世代のデータを取得できる

3.Compute - Cloud Fuctionで稼働

4.HTTP Trigger

generationをパラメーターに入れれば、
その世代のポケモンがデータベース上に上がってくる

例
`curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" https://{GFC_URL}?generation=2`


# 📝Pokémon データベース

| フィールド名         | 型           | モード       | 説明                                 |
|----------------------|--------------|--------------|--------------------------------------|
| `generation`         | INTEGER      | NULLABLE     | ポケモンの世代を表します。           |
| `pokemon_id`         | INTEGER      | NULLABLE     | ポケモンの一意の識別子です。         |
| `name_en`            | STRING       | NULLABLE     | ポケモンの英語名です。               |
| `name_ja`            | STRING       | NULLABLE     | ポケモンの日本語名です。             |
| `name_ko`            | STRING       | NULLABLE     | ポケモンの韓国語名です。             |
| `capture_rate`       | INTEGER      | NULLABLE     | ポケモンの捕獲率を表します。         |
| `base_happiness`     | INTEGER      | NULLABLE     | ポケモンの基本幸福度です。           |
| `is_baby`            | BOOLEAN      | NULLABLE     | ポケモンがベビーポケモンかどうかを示します。 |
| `is_legendary`       | BOOLEAN      | NULLABLE     | ポケモンが伝説のポケモンかどうかを示します。 |
| `is_mythical`        | BOOLEAN      | NULLABLE     | ポケモンが幻のポケモンかどうかを示します。 |


# 🪲開発バグ解決備忘録


https://kaerusapiens.notion.site/GCP-d38b24cf489048cc95ae39df842644d0#f3fba7fde93f4c4295795dc06682685e




