# Copyright (c) 2020-2024 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM ghcr.io/cicirello/pyaction:4.32.0
COPY tidyjavadocs.py /tidyjavadocs.py
ENTRYPOINT ["/tidyjavadocs.py"]
