from bs4 import BeautifulSoup
import csv

def is_inside(tag, ancestor_name):
    for p in tag.parents:
        if p.name == ancestor_name:
            return True
    return False

def extract_changes_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html5lib')
    result = []

    for div in soup.find_all('div'):
        if div.get('class') and any(cls.startswith("WordSection") for cls in div['class']):
            page = int([cls for cls in div['class'] if cls.startswith("WordSection")][0].replace("WordSection", ""))

            # ✅ ページ6から処理
            if page < 6:
                continue

            print(f"===== Processing page {page} =====")

            paragraphs = div.find_all('p')

            for p in paragraphs:
                context_text = p.get_text(strip=True)
                spans = p.find_all('span')
                pending_add = None
                pending_del = None

                for span in spans:
                    style = span.get('style', '')
                    if 'color:#D13438' not in style:
                        continue

                    text = span.get_text(strip=True)
                    is_add = is_inside(span, 'u')
                    is_del = is_inside(span, 's')

                    print(f"DEBUG: text={repr(text)} | is_add={is_add}, is_del={is_del}")
                    print(f"DEBUG: current pending_add={pending_add}, pending_del={pending_del}")

                    if is_add and is_del:
                        result.append([page, text, text, context_text])
                        pending_add = None
                        pending_del = None
                    elif is_add:
                        if pending_del:
                            result.append([page, text, pending_del, context_text])
                            pending_del = None
                        else:
                            # 複数の追加が連続する場合に対応（+=ではなくそのまま上書き）
                            if pending_add:
                                result.append([page, pending_add, '', context_text])
                            pending_add = text
                    elif is_del:
                        if pending_add:
                            result.append([page, pending_add, text, context_text])
                            pending_add = None
                        else:
                            # 複数の削除が連続する場合に対応
                            if pending_del:
                                result.append([page, '', pending_del, context_text])
                            pending_del = text

                # ✅ 1つの<p>が終わったらflush（漏れ防止）
                if pending_add:
                    print(f"FLUSH: remaining pending_add={pending_add}")
                    result.append([page, pending_add, '', context_text])
                    pending_add = None
                if pending_del:
                    print(f"FLUSH: remaining pending_del={pending_del}")
                    result.append([page, '', pending_del, context_text])
                    pending_del = None

    return result

def save_to_csv(data, output_file='diff_output.csv'):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ページ数', '追加文字列', '削除文字列', '文脈'])
        writer.writerows(data)

# 使用例
with open('input.html', encoding='utf-8') as file:
    html_content = file.read()

changes = extract_changes_from_html(html_content)
save_to_csv(changes)
