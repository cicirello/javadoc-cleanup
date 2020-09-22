#!/usr/bin/env python3
#
# javadoc-cleanup: Github action for tidying up javadocs
# 
# Copyright (c) 2020 Vincent A Cicirello
# https://www.cicirello.org/
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

import sys
import os
import os.path

def tidy(filename) :
    modified = False
    with open(filename, 'r+') as f :
        contents = f.readlines()
        for i, line in enumerate(contents) :
            if line.strip().startswith("<!-- Generated by javadoc") and line.strip() != "<!-- Generated by javadoc -->" :
                contents[i] = "<!-- Generated by javadoc -->"
                modified = True
                break
        if modified :
            f.seek(0)
            f.truncate()
            f.writelines(contents)
    return modified

if __name__ == "__main__" :
    websiteRoot = sys.argv[1]
    baseUrl = sys.argv[2]

    os.chdir(websiteRoot)

    allFiles = []
    for root, dirs, files in os.walk(".") :
        for f in files :
            if len(f) >= 5 and ".html" == f[-5:] :
                allFiles.append(os.path.join(root, f))

    count = 0
    for f in allFiles :
        if tidy(f) :
            count += 1

    print("::set-output name=modified-count::" + str(count))
    
    
