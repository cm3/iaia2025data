import pandas as pd
from openai import OpenAI
import time
import os

# Initialize OpenAI client (replace with your actual API key)
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# === データ読み込み ===

# 変更点一覧
change_df = pd.read_csv("merged_diff_output.csv")
change_df = change_df.fillna("")

# パブコメ一覧
pabukome_df = pd.read_csv("6thPC_AnalysisData_full_20250209.csv")
pabukome_df = pabukome_df.fillna("")

# === 変更点リストを箇条書きの文字列に整形 ===

def make_change_list_text(df):
    items = []
    for idx, row in df.iterrows():
        change_id = idx + 1  # 1始まりのID
        add = row["追加文字列"]
        delete = row["削除文字列"]
        context = row["文脈"]
        entry = f"{change_id}. Addition:「{add}」、Deletion:「{delete}」\nContext: {context}"
        items.append(entry)
    return "\n\n".join(items)

change_list_text = make_change_list_text(change_df)

# === プロンプト生成 ===

def generate_prompt(comment, reply, score, justification, change_list_str):
    return f"""Please determine whether any of the policy document revisions listed below are directly related to the following public comment and the corresponding government reply.

---
Comment: {comment}

Reply: {reply}

This comment–reply pair has been rated a fulfillment score of {score}, indicating the likelihood that it led to an actual change in the policy document.

The fulfillment score indicates how closely the policy response aligns with the original public comment:

- Score 4: Fully fulfilled — the requested revision or addition was made as asked.
- Score 3: Partially fulfilled — the response addressed the comment in part or via alternative means.
- Score 2: No change made, but the response claims the request is already fulfilled.
- Score 1: Rejected — the request was not accepted or implemented.

In general, scores of 3 or 4 are more likely to correspond to actual changes made in the policy document. Therefore, when identifying relevant changes, give higher priority to these cases.

Justification for this score: {justification}

---

Below is a list of changes made to the policy document.  
Each change consists of (1) added phrases, (2) deleted phrases, and (3) the full surrounding context (including the strings of both additions and deletions).  
Note: Added or deleted phrases may include `///` as a delimiter, which indicates that multiple words were inserted or removed as part of a single change (e.g., "以下///」という。" = "以下", "」という。").

When identifying which changes are relevant to the comment–reply pair above, **do not rely on the context alone**.  
Instead, make your judgment **based on the combination of both added and deleted phrases**.  
The context can help clarify intent, but the primary evidence must come from the actual textual changes.

If any changes are clearly related to the comment and reply, list the corresponding change IDs and provide a brief justification.

If none of the changes are related, simply respond with:

Relevant changes: None

List:

{change_list_str}

---

Output format (strictly follow this format):

Relevant changes:
- Change ID: [number]
  Reason: [Brief explanation of the relationship (max 50 characters)]

or

Relevant changes: None
"""

# === 出力用リスト ===
results = []

# === API 実行 ===
for i, row in pabukome_df.iterrows():
    comment_id = row["id"]
    comment = row["comment"]
    reply = row["reply"]
    score = row["request_fulfillment_score"]
    justification = row["request_fulfillment_justification"]
    prompt = generate_prompt(comment, reply, score, justification, change_list_text)

    try:


        response = client.chat.completions.create(
            model="gpt-4o",  # Adjust model name as needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000,
            top_p=1
        )
        output = response.choices[0].message.content.strip()
        print(f"[{comment_id}] OK")

        results.append({
            "id": comment_id,
            "comment": comment,
            "reply": reply,
            "該当変更点情報": output
        })

    except Exception as e:
        print(f"[{comment_id}] Error: {e}")
        results.append({
            "id": comment_id,
            "comment": comment,
            "reply": reply,
            "該当変更点情報": f"ERROR: {e}"
        })

    time.sleep(1.2)  # レート制限対策

# === CSV出力 ===
result_df = pd.DataFrame(results)
result_df.to_csv("pabukome_matched_changes.csv", index=False, encoding="utf-8-sig")
