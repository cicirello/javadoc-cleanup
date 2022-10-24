#!/usr/bin/env -S python3 -B
#
# javadoc-cleanup: Github action for tidying up javadocs
# 
# Copyright (c) 2020-2022 Vincent A Cicirello
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
import re

def tidy(filename, baseUrl, extraBlock, jd) :
    """The tidy function does the following:
    1) Removes any javadoc timestamps that were inserted by javadoc despite using the
    notimestamp option.
    2) Adds the meta viewport tag to improve browsing javadocs on mobile browsers.
    3) Adds the canonical link (if that option was chosen).

    Keyword arguments:
    filename - The name of the file, including path.
    baseUrl - The url of the documentation site
    extraBlock - A string containing an additional block to insert into the head of
        each page (e.g., can be used for links to favicons, etc).
    """
    modified = False
    generatedByJavadoc = False
    if baseUrl != None :
        canonical = '<link rel="canonical" href="{0}">\n'.format(urlstring(filename, baseUrl))
    with open(filename, 'r+') as f :
        redirected = False
        needsViewport = True
        generatedByJavadoc = False
        contents = f.readlines()
        for i, line in enumerate(contents) :
            if line.strip() == "<head>" :
                headIndex = i
            elif jd.isJavadocGenerated(line.strip()) :
                generatedByJavadoc = True
                if jd.hasTimestamp(line.strip()) :
                    contents[i] = jd.removeTimestamp(line.strip()) 
                    modified = True
            elif generatedByJavadoc and jd.isViewportDeclaration(line.strip()) :
                needsViewport = False
            elif generatedByJavadoc and jd.isRedirect(line.strip()) :
                redirected = True
            elif line.strip().find("</head>") >= 0 :
                break
        if generatedByJavadoc and contents[headIndex+1].strip() != "<!-- GitHub action javadoc-cleanup -->" :
            j = 1
            contents.insert(headIndex+j, "<!-- GitHub action javadoc-cleanup -->\n")
            j += 1
            if redirected :
                # For redirected pages, such as in case of Java Platform Module System modules,
                # direct search engines to noindex, but to follow.
                contents.insert(headIndex+j, '<meta name="robots" content="noindex, follow">\n')
                j += 1
            if baseUrl != None and not redirected:
                # only insert canonical URL if page is not a redirect
                contents.insert(headIndex+j, canonical)
                j += 1
            if needsViewport :
                contents.insert(headIndex+j, '<meta name="viewport" content="width=device-width, initial-scale=1">\n')
                j += 1
            if extraBlock != None :
                if extraBlock=="" or extraBlock[-1] != "\n" :
                    extraBlock = extraBlock + "\n"
                contents.insert(headIndex+j, extraBlock)
                j += 1
            contents.insert(headIndex+j, "<!-- End javadoc-cleanup block -->\n")
            modified = True
        if modified :
            f.seek(0)
            f.truncate()
            f.writelines(contents)
    return modified

def urlstring(f, baseUrl) :
    """Forms a string with the full url from a filename and base url.
    
    Keyword arguments:
    f - filename
    baseUrl - address of the root of the website
    """
    if f[0]=="." :
        u = f[1:]
    else :
        u = f
    if len(u) >= 11 and u[-11:] == "/index.html" :
        u = u[:-10]
    elif u == "index.html" :
        u = ""
    if len(u) >= 1 and u[0]=="/" and len(baseUrl) >= 1 and baseUrl[-1]=="/" :
        u = u[1:]
    elif (len(u)==0 or u[0]!="/") and (len(baseUrl)==0 or baseUrl[-1]!="/") :
        u = "/" + u
    return baseUrl + u

class JavadocDetector :
    """An instance of this class is used to detect if a line of the html file
    contains the comment that indicates it is generated by Javadoc."""

    __slots__ = [ "_withVersion",
                  "_noVersion",
                  "_javadocGeneratedComment",
                  "_viewportCheck",
                  "_redirect_script",
                  "_redirect_refresh"
                ]

    def __init__(self) :
        self._withVersion = re.compile("<!--\s+[Gg]enerated by javadoc\s+\(.+\)\s+-->", flags=re.A)
        self._noVersion = re.compile("<!--\s+[Gg]enerated by javadoc\s+-->", flags=re.A)
        self._javadocGeneratedComment = re.compile("<!--\s+[Gg]enerated by javadoc", flags=re.A)
        self._viewportCheck = re.compile("<meta\s+.+viewport", flags=re.A)
        self._redirect_refresh = re.compile("<meta\s+http-equiv=\"Refresh\"", flags=re.A)
        self._redirect_script = re.compile("<script\s+.+window\.location\.replace", flags=re.A)

    def isRedirect(self, s) :
        """Checks if a string is a redirect.

        Keyword arguments:
        s - the string to check
        """
        return self._redirect_script.match(s) != None or self._redirect_refresh.match(s) != None

    def isViewportDeclaration(self, s) :
        """Checks if a string is a meta viewport declaration.
        
        Keyword arguments:
        s - the string to check
        """
        return self._viewportCheck.match(s) != None

    def isJavadocGenerated(self, s) :
        """Checks if a string is a javadoc generated marker.

        Keyword arguments:
        s - the string to check
        """
        return self._javadocGeneratedComment.match(s) != None

    def hasTimestamp(self, s) :
        """Checks if a string is a javadoc generated marker containing a timestamp.

        Keyword arguments:
        s - The string to check
        """
        return self.isJavadocGenerated(s) and self._noVersion.match(s) == None and self._withVersion.match(s) == None

    def removeTimestamp(self, s) :
        """Assumes that the given string is the Javadoc generated comment, and removes
        any timestamp that may be present.

        Keyword arguments:
        s - The string to remove a timestamp from, assumed to be a valid marker of beginning of javadoc generated code.
        """
        end = s.find(")")
        if end >= 0 :
            return s[:end+1] + " -->\n"
        else :
            return "<!-- Generated by javadoc -->\n"

def set_outputs(names_values) :
    """Sets the GitHub Action outputs.

    Keyword arguments:
    names_values - Dictionary of output names with values
    """
    if "GITHUB_OUTPUT" in os.environ :
        with open(os.environ["GITHUB_OUTPUT"], "a") as f :
            for name, value in names_values.items() :
                print("{0}={1}".format(name, value), file=f)
    else : # Fall-back to deprecated set-output for non-updated runners
        for name, value in names_values.items() :
            print("::set-output name={0}::{1}".format(name, value))

if __name__ == "__main__" :
    websiteRoot = sys.argv[1]
    baseUrl = sys.argv[2].strip()
    extraBlock = sys.argv[3] if len(sys.argv[3]) > 0 else None
    
    if not baseUrl.startswith("http") :
        baseUrl = None

    os.chdir(websiteRoot)

    allFiles = []
    for root, dirs, files in os.walk(".") :
        for f in files :
            if len(f) >= 5 and ".html" == f[-5:] :
                allFiles.append(os.path.join(root, f))

    jd = JavadocDetector()

    count = 0
    for f in allFiles :
        if tidy(f, baseUrl, extraBlock, jd) :
            count += 1
    
    set_outputs({"modified-count" : count})
    
    
