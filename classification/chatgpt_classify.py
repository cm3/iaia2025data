import openai
import pandas as pd
import time
from openai import OpenAI
import os

# Initialize OpenAI client (replace with your actual API key)
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# 入力ファイル
df = pd.read_csv("merged_diff_output.csv")

# 出力用列の初期化
df["分類カテゴリ"] = ""
df["分類理由"] = ""

# 1件ずつAPIを叩いて処理
for i, row in df.iterrows():
    prompt = f"""次の文章における変更内容を、以下の6つのカテゴリのうち最も適切なもの1つに分類してください。
分類は、変更された語句の性質や目的に注目して行ってください。

---

追加された語句:
{row['追加文字列']}

削除された語句:
{row['削除文字列']}

文脈全文:
{row['文脈']}

---

分類カテゴリの説明（必ず1つだけ選んでください）：

1. てにをは、フォーマットの正規化  
　助詞や接続詞（てにをは）の修正や、表記の統一（漢字→ひらがな、半角→全角など）です。  
　例：「更に」→「さらに」、「2.1℃」→「２．１℃」、「は」→「が」など。

2. 数字のアップデート  
　年号、割合、統計値などの数値情報の修正・更新です。  
　例：「2023」→「2024」、「30%」→「35%」、「50万人」→「52万人」など。

3. 略語・正式名称への変換、引用・出典の補完  
　略称を正式名称にしたり、出典・法律名・注釈などを明記・補足したものです。  
　例：「COP28」→「第28回締約国会議（COP28）」、  
　　　「...という（平成xx年法律第yy号）」のような挿入など。

4. 修辞の調整、語順変更や文構造整理  
　語の強弱や曖昧さを調整したり、語順を変えて文章を読みやすくしたものです。  
　例：「～が望まれる」→「～が必要である」、  
　　　「AでありBである」→「BでありAでもある」など。

5. その他意味に踏み込まない変更  
　上記のいずれにも明確に当てはまらないが、文の意味に影響を与えない軽微な変更です。  
　例：句読点、不要な括弧、空白、軽い語調の修正など。

6. その他意味に踏み込んだ変更  
　内容そのものや意味が変わるような表現・単語の変更です。ちゃんと意味が変わっていることを確認するように、厳し目に判定してください。

---

出力形式（以下の形式に厳密に従ってください）：

カテゴリ: [1〜6の番号]  
理由: [分類の根拠となる簡潔な説明（50文字以内）]
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Adjust model name as needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500,
            top_p=1
        )
        output = response.choices[0].message.content
        print(f"[{i}] {output.strip()}")
        # 結果を解析
        lines = output.strip().splitlines()
        for line in lines:
            if line.startswith("カテゴリ:"):
                df.at[i, "分類カテゴリ"] = line.replace("カテゴリ:", "").strip()
            elif line.startswith("理由:"):
                df.at[i, "分類理由"] = line.replace("理由:", "").strip()
        time.sleep(1.2)  # API制限対策でウェイトをかける（必要に応じて）
    except Exception as e:
        print(f"[{i}] Error: {e}")
        df.at[i, "分類カテゴリ"] = "エラー"
        df.at[i, "分類理由"] = str(e)

# 保存
df.to_csv("merged_with_classification.csv", index=False, encoding="utf-8-sig")
