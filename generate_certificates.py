import csv
import subprocess
import os
from datetime import datetime
import argparse

def generate_certificates(reviewer_csv, template_tex, delete_tex=False):
    """! @brief reviewer.csv に記載された査読者ごとに、certificate_review.tex をテンプレートとしてPDFファイルを生成する。
     *  @param reviewer_csv (str) 査読者情報が記載されたCSVファイルのパス。
     *  @param template_tex (str) テンプレートとなるTeXファイルのパス。
     *  @param delete_tex (bool) TeXファイルを削除するかどうかのフラグ。
     *  @return なし
     *  @details
     *  - CSVファイルとTeXファイルが存在しない場合はエラーメッセージを出力する。
     *  - pdflatexコマンドが見つからない場合はエラーメッセージを出力する。
     *  - PDFファイルの生成に失敗した場合はエラーメッセージを出力する。
     """
    try:
        with open(template_tex, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"エラー: テンプレートファイル {template_tex} が見つかりません。")
        return
    
    try:
        with open(reviewer_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reviewer_name = row['Name']
                reviewer_number = row['Number']
                output_tex = f"Certificate_of_reviewer_{reviewer_name.replace(' ', '_')}.tex"
                output_pdf = f"Certificate_of_reviewer_{reviewer_name.replace(' ', '_')}.pdf"
                
                # テンプレートを置換
                tex_content = template.replace('[Reviewer Name]', reviewer_name)
                if reviewer_number == '1':
                    tex_content = tex_content.replace('[Number] papers', '1 paper')
                else:
                    tex_content = tex_content.replace('[Number] papers', reviewer_number + ' papers')

                # TeXファイルを作成
                with open(output_tex, 'w', encoding='utf-8') as tex_file:
                    tex_file.write(tex_content)
                # print(tex_content) # デバッグ用
                # PDFファイルを生成
                try:
                    # 絶対パスに変換
                    abs_tex_path = os.path.abspath(output_tex)
                    
                    # PDFを2回生成して座標を正しく計算
                    for _ in range(2):
                        subprocess.run([
                            'pdflatex',
                            '-shell-escape',
                            '-halt-on-error',
                            '-interaction=nonstopmode',
                            abs_tex_path
                        ], check=True, capture_output=True)
                    
                    # 不要なファイルを削除
                    for ext in ['.aux', '.log', '.out']:
                        try:
                            os.remove(f"{output_tex.replace('.tex', '')}{ext}")
                        except FileNotFoundError:
                            pass
                    
                    if delete_tex:
                        os.remove(output_tex)
                    
                    print(f"PDFファイル {output_pdf} を生成しました。")
                except subprocess.CalledProcessError as e:
                    print(f"エラー: PDFファイルの生成に失敗しました。{e.stderr.decode('utf-8')}")
                except FileNotFoundError:
                    print("エラー: pdflatex コマンドが見つかりません。LaTeXがインストールされているか確認してください。")
    except FileNotFoundError:
        print(f"エラー: CSVファイル {reviewer_csv} が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

def main():
    """! @brief コマンドライン引数を解析し、証明書生成関数を実行する。
     *  @param なし
     *  @return なし
     *  @details
     *  - reviewer_csv: 査読者情報が記載されたCSVファイルのパス (必須)
     *  - template_tex: テンプレートとなるTeXファイルのパス (必須)
     *  - -d, --delete_tex: TeXファイルを削除するかどうかのフラグ (オプション)
     *  @code
     *  python generate_certificates.py reviewer.csv certificate_review.tex -d
     *  @endcode
     """
    parser = argparse.ArgumentParser(description="査読者ごとに証明書を生成するスクリプト")
    parser.add_argument("reviewer_csv", help="査読者情報が記載されたCSVファイルのパス")
    parser.add_argument("template_tex", help="テンプレートとなるTeXファイルのパス")
    parser.add_argument("-d", "--delete_tex", action="store_true", help="TeXファイルを削除するかどうか")
    args = parser.parse_args()

    generate_certificates(args.reviewer_csv, args.template_tex, args.delete_tex)

if __name__ == "__main__":
    main()