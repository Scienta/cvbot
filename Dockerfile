# syntax=docker/dockerfile:1.7-labs
# Based on https://gilgi.org/blog/python-docker-slim/

FROM python:3.11 AS dep-builder

COPY requirements-frozen.txt /build/requirements.txt
RUN pip wheel --no-deps -w /build/dist -r /build/requirements.txt

# base image: installs wheels for all dependencies
FROM python:3.11-slim AS base

# copy all wheels from builder and install
COPY --from=dep-builder [ "/build/dist/*.whl", "/install/" ]
RUN pip install --no-index /install/*.whl \
    && rm -rf /install

FROM base AS final

RUN adduser --home /app --disabled-password app
USER app
WORKDIR /app

COPY --parents ./.streamlit ./* ./
RUN find $(pwd)

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

ENTRYPOINT ["streamlit", "run", "cvbot.py", "--server.port=8080", "--server.address=0.0.0.0"]
