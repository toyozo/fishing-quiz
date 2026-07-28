#!/usr/bin/env bash
# 手動デプロイ用スクリプト。サーバー上のリポジトリディレクトリで実行する。
# 使い方: cd ~/apps/fishing-quiz && ./deploy/scripts/deploy.sh [ブランチ名(既定: master)]
# ※ main/develop/feature運用に整理されたらデフォルトをmainに変更すること
set -euo pipefail

BRANCH="${1:-master}"
cd "$(dirname "$0")/../.."

echo "==> ${BRANCH}ブランチを取得"
git fetch origin "$BRANCH"
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

echo "==> イメージをビルドしてコンテナを起動"
docker compose build
docker compose up -d

echo "==> 起動中のコンテナ:"
docker compose ps

echo ""
echo "==> 完了。ログを見る場合: docker compose logs -f"
