ARG PYSETUP_PATH=/opt/pysetup
ARG UV_VERSION=0.7.3
ARG DEBIAN_VERSION=12
ARG DEBIAN_VERSION_CODENAME=bookworm

#############################################
# base ステージ
# ビルダーや開発環境の共通設定
#############################################
FROM ghcr.io/astral-sh/uv:${UV_VERSION}-${DEBIAN_VERSION_CODENAME} AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

#############################################
# devcontainer ステージ
# devcontainer でアタッチするコンテナ用のイメージ
#############################################
FROM base AS dev
ARG USER_NAME=devuser
ARG USER_UID=1000
ARG USER_GID=1000
ENV PYTHONPATH="src"
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]
# apt で install したいパッケージがあったらここに追加
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        htop \
        jq \
        less \
        sudo \
        tmux \
        tree \
        vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN if getent group ${USER_GID} > /dev/null 2>&1; then \
        echo "Group with GID ${USER_GID} already exists. Skipping group creation."; \
    else \
        groupadd --gid "${USER_GID}" "${USER_NAME}"; \
    fi \
    && useradd --uid "${USER_UID}" --gid "${USER_GID}" -m "${USER_NAME}" -s /bin/bash \
    # sudo グループにユーザーを追加
    && usermod -aG sudo "${USER_NAME}" \
    && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/${USER_NAME}" \
    && chmod 0440 "/etc/sudoers.d/${USER_NAME}"
CMD ["bash"]

#############################################
# build ステージ
# プロジェクトのビルドをするためのイメージ
#############################################
FROM base AS build
ARG PYSETUP_PATH
ENV UV_PROJECT_ENVIRONMENT=${PYSETUP_PATH}/.venv/ \
    UV_PYTHON_INSTALL_DIR=${PYSETUP_PATH}/
WORKDIR ${PYSETUP_PATH}
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]
COPY pyproject.toml .python-version poetry.lock* ./
RUN uv sync --no-cache-dir --no-dev \
    && rm -rf pyproject.toml .python-version uv.lock

#############################################
# production 用ステージ
# ビルドした依存関係やソースを build ステージからコピーする
#############################################
FROM gcr.io/distroless/base-debian${DEBIAN_VERSION}:nonroot AS prod
ARG PYSETUP_PATH
ENV PATH=${PYSETUP_PATH}/.venv/bin:$PATH \
    PYTHONPATH="src" \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=build ${PYSETUP_PATH}/ ${PYSETUP_PATH}/
COPY src src
CMD ["python", "-m", "my_package.main"]
