import firebase_admin
import requests
from firebase_admin import auth, credentials

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

FIREBASE_EMULATOR_AUTH_URL = "http://localhost:9099"
FIREBASE_EMULATOR_FIRESTORE_URL = "http://localhost:8080"
auth._auth_service_url = f"{FIREBASE_EMULATOR_AUTH_URL}/identitytoolkit.googleapis.com/v1"

# 2024 1-1
firestore_data_2024_1_1 = {
    "collections": {
        "arrayValue": {
            "values": [
                {"stringValue": "daisuke.suzuki"},
                {"stringValue": "ai.takahashi"},
                {"stringValue": "shota.watanabe"},
                {"stringValue": "anna.ito"},
                {"stringValue": "riku.nakamura"},
                {"stringValue": "nao.kobayashi"},
                {"stringValue": "kaito.yamamoto"},
                {"stringValue": "ayaka.kato"},
                {"stringValue": "yuto.yoshida"}
            ]
        }
    }
}

# 2024 1-2
firestore_data_2024_1_2 = {
    "collections": {
        "arrayValue": {
            "values": [
                {"stringValue": "mao.yamada"},
                {"stringValue": "tomoya.sasaki"},
                {"stringValue": "yuka.matsumoto"},
                {"stringValue": "daiki.inoue"},
                {"stringValue": "ayane.kimura"},
                {"stringValue": "takumi.hayashi"},
                {"stringValue": "miyu.saito"},
                {"stringValue": "tsubasa.shimizu"},
                {"stringValue": "rena.yamaguchi"}
            ]
        }
    }
}

# 2023 1-1
firestore_data_2023_1_1 = {
    "collections": {
        "arrayValue": {
            "values": [
                {"stringValue": "souta.hasegawa"},
                {"stringValue": "yui.okada"},
                {"stringValue": "ren.fujita"},
                {"stringValue": "mao.kondo"},
                {"stringValue": "hinata.arai"},
                {"stringValue": "riku.uchida"},
                {"stringValue": "minami.hara"},
                {"stringValue": "ryota.kojima"},
                {"stringValue": "haruka.shinohara"}
            ]
        }
    }
}

# 2023 1-2
firestore_data_2023_1_2 = {
    "collections": {
        "arrayValue": {
            "values": [
                {"stringValue": "koki.yamashita"},
                {"stringValue": "asuka.morita"},
                {"stringValue": "itsuki.kawai"},
                {"stringValue": "mei.tsuchiya"},
                {"stringValue": "shun.matsuda"},
                {"stringValue": "rio.hashimoto"},
                {"stringValue": "sena.nishida"},
                {"stringValue": "akari.tamura"},
                {"stringValue": "kenta.sakurai"}
            ]
        }
    }
}

# 2024 2-1
firestore_data_2024_2_1 = {
    "collections": {
        "arrayValue": {
            "values": [
                {"stringValue": "souta.hasegawa"},
                {"stringValue": "ren.fujita"},
                {"stringValue": "hinata.arai"},
                {"stringValue": "minami.hara"},
                {"stringValue": "haruka.shinohara"},
                {"stringValue": "asuka.morita"},
                {"stringValue": "mei.tsuchiya"},
                {"stringValue": "rio.hashimoto"},
                {"stringValue": "akari.tamura"}
            ]
        }
    }
}

# 2024 2-2
firestore_data_2024_2_2 = {
    "collections": {
        "arrayValue": {
            "values": [
                {"stringValue": "yui.okada"},
                {"stringValue": "mao.kondo"},
                {"stringValue": "riku.uchida"},
                {"stringValue": "ryota.kojima"},
                {"stringValue": "koki.yamashita"},
                {"stringValue": "itsuki.kawai"},
                {"stringValue": "shun.matsuda"},
                {"stringValue": "sena.nishida"},
                {"stringValue": "kenta.sakurai"}
            ]
        }
    }
}

def sign_in(email, password):
    try:
        # Authentication Emulator に直接リクエストを送信
        response = requests.post(
            f"{FIREBASE_EMULATOR_AUTH_URL}/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=any",
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True,
            }
        )
        response.raise_for_status()
        print("ログイン成功")
        return response.json()
    except requests.exceptions.RequestException as e:
        print("ログイン失敗:", e)

def convert_to_firestore_format(data):
    firestore_data = {}
    for key, value in data.items():
        if isinstance(value, int):
            firestore_data[key] = {"integerValue": value}
        elif isinstance(value, float):
            firestore_data[key] = {"doubleValue": value}
        elif isinstance(value, bool):
            firestore_data[key] = {"booleanValue": value}
        else:  # デフォルトは文字列
            firestore_data[key] = {"stringValue": str(value)}
    return firestore_data

def write_to_firestore(id_token, url, data):
    try:
        # fields = convert_to_firestore_format(data)

        body = {
            "fields": data
        }

        headers = {
            "Authorization": f"Bearer {id_token}",  # ID トークンをヘッダーに追加
            "Content-Type": "application/json",
        }
        response = requests.patch(
            f"{FIREBASE_EMULATOR_FIRESTORE_URL}/v1/projects/demo-manabiya-ai/databases/(default)/documents/{url}",
            json=body,
            headers=headers,
        )
        response.raise_for_status()
        print("Firestore 書き込み成功:", response.json())
    except requests.exceptions.RequestException as e:
        print("Firestore 書き込み失敗:", e.response.text)


def get_document_from_firestore(id_token, url):
    try:
        # Authorization ヘッダーの設定
        headers = {
            "Authorization": f"Bearer {id_token}",
        }

        # Firestore API エンドポイント
        url = f"{FIREBASE_EMULATOR_FIRESTORE_URL}/v1/projects/demo-manabiya-ai/databases/(default)/documents/{url}"


        # リクエスト送信
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # データを取得
        document = response.json()
        print("Firestore ドキュメント取得成功:", document)
        return document
    except requests.exceptions.RequestException as e:
        if e.response:
            print("Firestore ドキュメント取得失敗:", e.response.text)
        else:
            print("Firestore ドキュメント取得失敗: リクエスト自体に失敗しました:", e)

email = "admin@manabiya.ai.com"
password = "Manab1yaa1.Admin"

teachers = ["kenta.tanaka", "misaki.sato", "haruto.takeda", "aoi.fujimoto"]

user = sign_in(email, password)
id_token = user["idToken"]
if id_token:
    # path = "2023/1-2"
    # for data in firestore_data_2023_1_2["collections"]["arrayValue"]["values"]:
    #     name = data["stringValue"]
    #     write_to_firestore(id_token, f"{path}/{name}/国語", {})
    #     write_to_firestore(id_token, f"{path}/{name}/数学", {})
    #     write_to_firestore(id_token, f"{path}/{name}/英語", {})
    #     write_to_firestore(id_token, f"{path}/{name}/理科", {})
    #     write_to_firestore(id_token, f"{path}/{name}/社会", {})

    for teacher in teachers:
        write_to_firestore(id_token, f"teachers/{teacher}", {})
    
    # write_to_firestore(id_token, f"{path}/共通/国語", {})
    # write_to_firestore(id_token, f"{path}/共通/数学", {})
    # write_to_firestore(id_token, f"{path}/共通/英語", {})
    # write_to_firestore(id_token, f"{path}/共通/理科", {})
    # write_to_firestore(id_token, f"{path}/共通/社会", {})
