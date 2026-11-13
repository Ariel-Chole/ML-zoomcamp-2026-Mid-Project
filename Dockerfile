FROM python:3.12-slim-bookworm@sha256:d29f48a31a8b408ed19272ca1e7b10ebae13b240a27e862d3d4217c528e2e0c3
COPY --from=ghcr.io/astral-sh/uv:0.10.11@sha256:3472e43b4e738cf911c99d41bb34331280efad54c73b1def654a6227bb59b2b4 /uv /uvx /bin/

ENV PATH="/life_expectancy_code/.venv/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /life_expectancy_code

COPY ["pyproject.toml", "uv.lock", ".python-version", "./"]
RUN uv sync --locked --no-dev --no-install-project

COPY ["life_expectancy_predict.py", "life-expectancy-model.bin", "./"]

EXPOSE 9696
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "life_expectancy_predict:app"]

