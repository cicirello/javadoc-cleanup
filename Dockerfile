# Copyright (c) 2020 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM cicirello/pyaction:latest
COPY tidyjavadocs.py /tidyjavadocs.py
ENTRYPOINT ["/tidyjavadocs.py"]
