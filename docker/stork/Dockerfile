FROM debian:12-slim

# Pinned to match the stork version used elsewhere in this repo (see .dvenv/bin/stork).
ARG STORK_VERSION=1.6.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL -o /usr/local/bin/stork \
        "https://github.com/jameslittle230/stork/releases/download/v${STORK_VERSION}/stork-ubuntu-22-04" \
    && chmod +x /usr/local/bin/stork

WORKDIR /files
ENTRYPOINT ["stork"]
