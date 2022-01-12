# Copyright 2018-2021 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import re
from typing import cast, Any


PAGE_PATTERN = re.compile("([0-9]*)[_ -]*(.*).py")


def open_python_file(filename):
    """Open a read-only Python file taking proper care of its encoding.

    In Python 3, we would like all files to be opened with utf-8 encoding.
    However, some author like to specify PEP263 headers in their source files
    with their own encodings. In that case, we should respect the author's
    encoding.
    """
    import tokenize

    if hasattr(tokenize, "open"):  # Added in Python 3.2
        # Open file respecting PEP263 encoding. If no encoding header is
        # found, opens as utf-8.
        return tokenize.open(filename)
    else:
        return open(filename, "r", encoding="utf-8")


def find_pages(dir_path):
    return [
        os.path.join(dir_path, file_path)
        for file_path in os.listdir(dir_path)
        if re.match(PAGE_PATTERN, file_path)
    ]


def page_sort_key(filename):
    [(number, label)] = re.findall(PAGE_PATTERN, os.path.basename(filename))

    if number == "":
        return (float("inf"), label)

    return (int(number), label)


def page_label(filename: str) -> str:
    extraction: re.Match[str] = cast(
        # This weirdness is done because a cast(re.Match[str], ...) explodes
        # at runtime since Python interprets it as an attempt to index into
        # re.Match instead of a type annotation.
        Any,
        re.search(PAGE_PATTERN, os.path.basename(filename)),
    )
    page_label = extraction.group(2).replace("_", " ").strip()
    if not page_label:
        page_label = extraction.group(1)
    return str(page_label)


def get_pages_and_labels(dir_path):
    sorted_files = sorted(find_pages(dir_path), key=page_sort_key)
    return [{"file": file, "label": page_label(file)} for file in sorted_files]
