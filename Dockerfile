# Copyright (c) 2020-2022 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM ghcr.io/cicirello/pyaction:4.7.1
COPY tidyjavadocs.py /tidyjavadocs.py
ENTRYPOINT ["/tidyjavadocs.py"]
