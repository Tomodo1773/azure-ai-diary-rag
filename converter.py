import os
from docx import Document as DocxDocument

def convert_docx_to_txt(directory_path):
    # 指定されたディレクトリ内のすべてのdocxファイルを探索
    for filename in os.listdir(directory_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(directory_path, filename)
            doc = DocxDocument(file_path)
            text_content = []
            # ドキュメント内の全ての段落を読み込み、テキストを抽出する
            for para in doc.paragraphs:
                text_content.append(para.text)
            # txtファイルとして保存
            txt_filename = filename.replace('.docx', '.txt')
            txt_path = os.path.join(directory_path, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write('\n'.join(text_content))
            print(f"{txt_filename}に変換されました。")

# ディレクトリパスを指定
directory_path = "./diary/bk"
convert_docx_to_txt(directory_path)
