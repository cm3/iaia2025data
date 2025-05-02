import csv
from collections import defaultdict

def are_strings_consecutive_in_context(strings, context):
    """
    文字列リストが文脈内で連続して出現しているかを判定
    例: ['平成', '11', '年'] → "平成11年" が context にあるかどうか
    """
    if not strings:
        return False
    combined = ''.join(strings)
    return combined in context

def merge_csv_rows_context_sensitive(input_file, output_file, sep='///'):
    merged = defaultdict(lambda: {'add_list': [], 'del_list': [], 'context': ''})

    with open(input_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['ページ数'], row['文脈'])

            add = row['追加文字列'].strip()
            delete = row['削除文字列'].strip()
            if add:
                merged[key]['add_list'].append(add)
            if delete:
                merged[key]['del_list'].append(delete)

            merged[key]['context'] = row['文脈']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ページ数', '追加文字列', '削除文字列', '文脈'])

        for (page, context), values in merged.items():
            add_list = values['add_list']
            del_list = values['del_list']

            # 追加文字列
            if len(add_list) > 1 and are_strings_consecutive_in_context(add_list, context):
                add_joined = ''.join(add_list)
            else:
                add_joined = sep.join(add_list)

            # 削除文字列
            if len(del_list) > 1 and are_strings_consecutive_in_context(del_list, context):
                del_joined = ''.join(del_list)
            else:
                del_joined = sep.join(del_list)

            writer.writerow([page, add_joined, del_joined, context])

# 使用例
merge_csv_rows_context_sensitive('diff_output.csv', 'merged_diff_output.csv')
