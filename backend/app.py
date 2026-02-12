import subprocess
import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/analyze_url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data['url']

    if not url:
        return jsonify({'error': 'URLが提供されていません'}), 400

    try:
        # URLにリクエストを送信し、ヘッダーとHTMLコンテンツを取得
        response = requests.get(url,timeout=10)
        headers = response.headers
        html_content = response.text

        # BeautifulSoupを使用してHTMLを解析
        soup=BeautifulSoup(html_content, 'html.parser')

        # 入力フォームの検出
        forms = soup.find_all('form')
        has_forms = len(forms) > 0

        # 古いJSライブラリの使用検出
        script_tags = soup.find_all('script')
        old_js_libraries_detected = any(
            "jquery-1." in str(script.get('src', '')).lower() or
            "angular-1." in str(script.get('src', '')).lower()
            for script in script_tags
        )

        # セキュリティヘッダーのチェック
        security_headers = {
            "X-Frame-Options": headers.get("X-Frame-Options"),
            "Content-Security-Policy": headers.get("Content-Security-Policy"),
            "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
            "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
            "Referrer-Policy": headers.get("Referrer-Policy"),
        }

        prompt = f"""
        あなたはセキュリティの専門家であり、ユーザーのWebサイトを診断するマスコットです。
        https://animemanga33.com/archives/73795 このサイトのタチコマの台詞と同じ口調で喋ります。生成する文章に「」や(タチコマ)は不要です。一人称も文章に入れないでください。
        以下の情報と取得したURLから、セキュリティレベルを診断し、脆弱性、攻撃シナリオ、対策、そして犯罪係数をJSON形式で出力してください。

        [診断対象URL]
        {url}

        [HTTPレスポンスヘッダー]
        {json.dumps(security_headers, indent=2)}

        [HTML解析結果]
        - 入力フォームの有無: {has_forms} ({len(forms)}個のフォームが検出されました)
        - 古いJavaScriptライブラリの検出: {old_js_libraries_detected}
        - サイトタイトル: {soup.title.string if soup.title else 'なし'}
        - メタディスクリプション: {soup.find('meta', attrs={'name': 'description'}).get('content') if soup.find('meta', attrs={'name': 'description'}) else 'なし'}

        以下のJSON形式で回答してください。
        {{
            "security_rank": "S"から"E"の5段階評価 (AはSの次に良い)
            "crime_coefficient": 0から1000までの数値
            "summary": "このサイトの全体的なセキュリティ評価の要約。タチコマの口調で、ユーモラスに。"
            "vulnerabilities": [
                {{
                    "type": "脆弱性の種類 (例: Missing Security Headers, Old JS Library, XSS Potential)",
                    "description": "具体的な脆弱性の説明。",
                    "attack_scenario": "この脆弱性を利用した場合、攻撃者は具体的にどのような損害を与えられるか。",
                    "fix_advice": "タチコマの口調で、脆弱性を解決するための修正アドバイス。",
                    "risk_level": "High" | "Medium" | "Low"
                }}
            ],
            "data_flow_nodes": [
                {{"id": "user_input", "position": {{"x": 0, "y": 0}}, "data": {{"label": "ユーザー入力"}}}},
                {{"id": "database", "position": {{"x": 200, "y": 100}}, "data": {{"label": "データベース"}}}},
                {{"id": "output", "position": {{"x": 400, "y": 0}}, "data": {{"label": "出力"}}}}
            ],
            "data_flow_edges": [
                {{"id": "e1-2", "source": "user_input", "target": "database", "animated": true, "style": {{"stroke": "red"}}}}
            ]
        }}
        
        特にdata_flow_nodesとdata_flow_edgesは、Webサイトのデータフローと脆弱なパスを視覚化できるように、具体的な例を参考に生成してください。
        ユーザー入力から、どういった経路を辿って、どこに危険が潜んでいるのかを表現してください。
        """
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        ai_text = response.text

        if "```json" in ai_text:
            ai_text = ai_text.split("```json")[1].split("```")[0].strip()
        elif "```" in ai_text:
            ai_text = ai_text.split("```")[1].split("```")[0].strip()

        try:
            response_json = json.loads(ai_text)
            return jsonify(response_json)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Raw Text: {ai_text}")
            return jsonify({'error': 'AIの応答をJSONとして解析できませんでした'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'URLへのリクエスト中にエラーが発生しました: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'サーバーエラー: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5000)