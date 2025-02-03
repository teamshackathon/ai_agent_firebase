# ai_agent_firebase

## 初期構築


voltaのインストール

https://docs.volta.sh/reference/

https://github.com/volta-cli/volta/releases/v2.0.2

```sh
volta -v
```
versionが出れば問題なし

nodeとnpmをインストール
```sh
volta install node@v22.7.0
volta install npm@10.8.2
```

function のnpm環境作成（一個下のfunctionのディレクトリ）
```sh
cd functions
npm install -D
```

firebaseのinstall(カレントディレクトリ)
```sh
cd ..
npm install -g firebase-tools
```

エミュレータの起動
```sh
cd seeds/default
mkdir database_export
cd ..
firebase emulators:start --import ./seeds/default --project demo-manabiya-ai
```