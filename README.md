devcontainer を使った Python プロジェクトのサンプル
===

# 起動確認

```shell
uv run -m my_package.main
```

# テスト実行

```shell
uv run pytest
```

# 本番用コンテナ実行確認

イメージビルド
```shell
docker build . -f docker/Dockerfile --target prod --tag my_package
```

実行
```shell
$ docker run --rm my_package
INFO:__main__:Hello, World!
```
