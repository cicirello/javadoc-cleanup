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


import unittest
import tidyjavadocs as tidy
import os

class TestTidyjavadocs(unittest.TestCase) :

    javadocWithTimestamp = """<!DOCTYPE HTML>
<!-- NewPage -->
<html lang="en">
<head>
<!-- Generated by javadoc (11.0.8) on Wed Sep 23 09:20:01 EDT 2020 -->
<title>Overview (Some Java Library.....)</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="stylesheet.css" title="Style">
<link rel="stylesheet" type="text/css" href="jquery/jquery-ui.css" title="Style">
<script type="text/javascript" src="script.js"></script>
<script type="text/javascript" src="jquery/jszip/dist/jszip.min.js"></script>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils.min.js"></script>
<!--[if IE]>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils-ie.min.js"></script>
<![endif]-->
<script type="text/javascript" src="jquery/jquery-3.3.1.js"></script>
<script type="text/javascript" src="jquery/jquery-migrate-3.0.1.js"></script>
<script type="text/javascript" src="jquery/jquery-ui.js"></script>
</head>
<body>
The body of the javadocs....
</body>
</html>
"""

    javadocWithoutTimestamp = """<!DOCTYPE HTML>
<!-- NewPage -->
<html lang="en">
<head>
<!-- Generated by javadoc -->
<title>Overview (Some Java Library.....)</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="stylesheet.css" title="Style">
<link rel="stylesheet" type="text/css" href="jquery/jquery-ui.css" title="Style">
<script type="text/javascript" src="script.js"></script>
<script type="text/javascript" src="jquery/jszip/dist/jszip.min.js"></script>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils.min.js"></script>
<!--[if IE]>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils-ie.min.js"></script>
<![endif]-->
<script type="text/javascript" src="jquery/jquery-3.3.1.js"></script>
<script type="text/javascript" src="jquery/jquery-migrate-3.0.1.js"></script>
<script type="text/javascript" src="jquery/jquery-ui.js"></script>
</head>
<body>
The body of the javadocs....
</body>
</html>
"""

    javadocAlreadyCleanedUp = """<!DOCTYPE HTML>
<!-- NewPage -->
<html lang="en">
<head>
<!-- GitHub action javadoc-cleanup -->
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- End javadoc-cleanup block -->
<!-- Generated by javadoc -->
<title>Overview (Some Java Library.....)</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="stylesheet.css" title="Style">
<link rel="stylesheet" type="text/css" href="jquery/jquery-ui.css" title="Style">
<script type="text/javascript" src="script.js"></script>
<script type="text/javascript" src="jquery/jszip/dist/jszip.min.js"></script>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils.min.js"></script>
<!--[if IE]>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils-ie.min.js"></script>
<![endif]-->
<script type="text/javascript" src="jquery/jquery-3.3.1.js"></script>
<script type="text/javascript" src="jquery/jquery-migrate-3.0.1.js"></script>
<script type="text/javascript" src="jquery/jquery-ui.js"></script>
</head>
<body>
The body of the javadocs....
</body>
</html>
"""

    expectedJavadoc = javadocAlreadyCleanedUp

    javadocAlreadyCleanedUpCanon = """<!DOCTYPE HTML>
<!-- NewPage -->
<html lang="en">
<head>
<!-- GitHub action javadoc-cleanup -->
<link rel="canonical" href="https://TESTING.1.2.3/testcase.html">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- End javadoc-cleanup block -->
<!-- Generated by javadoc -->
<title>Overview (Some Java Library.....)</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="stylesheet.css" title="Style">
<link rel="stylesheet" type="text/css" href="jquery/jquery-ui.css" title="Style">
<script type="text/javascript" src="script.js"></script>
<script type="text/javascript" src="jquery/jszip/dist/jszip.min.js"></script>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils.min.js"></script>
<!--[if IE]>
<script type="text/javascript" src="jquery/jszip-utils/dist/jszip-utils-ie.min.js"></script>
<![endif]-->
<script type="text/javascript" src="jquery/jquery-3.3.1.js"></script>
<script type="text/javascript" src="jquery/jquery-migrate-3.0.1.js"></script>
<script type="text/javascript" src="jquery/jquery-ui.js"></script>
</head>
<body>
The body of the javadocs....
</body>
</html>
"""

    expectedJavadocCanon = javadocAlreadyCleanedUpCanon

    nonJavadoc = """<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=utf-8>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="title" content="Page title....">
</head>
<body>
The body of the javadocs....
</body>
</html>
"""

    expectedNonJavadoc = nonJavadoc

    def test_removetimestamp(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.javadocWithTimestamp)
        tidy.tidy("testcase.html")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedJavadoc)
        os.remove("testcase.html")

    def test_notimestamp(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.javadocWithoutTimestamp)
        tidy.tidy("testcase.html")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedJavadoc)
        os.remove("testcase.html")

    def test_alreadycleanedup(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.javadocAlreadyCleanedUp)
        tidy.tidy("testcase.html")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedJavadoc)
        os.remove("testcase.html")

    def test_nonJavadoc(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.nonJavadoc)
        tidy.tidy("testcase.html")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedNonJavadoc)
        os.remove("testcase.html")

    def test_urlstring(self) :
        filenames = [ "./a.html",
                      "./index.html",
                      "./subdir/a.html",
                      "./subdir/index.html",
                      "./subdir/subdir/a.html",
                      "./subdir/subdir/index.html",
                      "./aindex.html",
                      "./subdir/aindex.html",
                      "/a.html",
                      "/index.html",
                      "/subdir/a.html",
                      "/subdir/index.html",
                      "/subdir/subdir/a.html",
                      "/subdir/subdir/index.html",
                      "/aindex.html",
                      "/subdir/aindex.html",
                      "a.html",
                      "index.html",
                      "subdir/a.html",
                      "subdir/index.html",
                      "subdir/subdir/a.html",
                      "subdir/subdir/index.html",
                      "aindex.html",
                      "subdir/aindex.html"
                      ]
        base1 = "https://TESTING.FAKE.WEB.ADDRESS.TESTING/"
        base2 = "https://TESTING.FAKE.WEB.ADDRESS.TESTING"
        expected = [ "https://TESTING.FAKE.WEB.ADDRESS.TESTING/a.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/a.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/aindex.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/aindex.html"
                     ]
        for i, f in enumerate(filenames) :
            self.assertEqual(expected[i%len(expected)], tidy.urlstring(f, base1))
            self.assertEqual(expected[i%len(expected)], tidy.urlstring(f, base2))

    def test_removetimestamp_canon(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.javadocWithTimestamp)
        tidy.tidy("testcase.html", "https://TESTING.1.2.3/")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedJavadocCanon)
        os.remove("testcase.html")

    def test_notimestamp_canon(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.javadocWithoutTimestamp)
        tidy.tidy("testcase.html", "https://TESTING.1.2.3/")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedJavadocCanon)
        os.remove("testcase.html")

    def test_alreadycleanedup_canon(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.javadocAlreadyCleanedUp)
        tidy.tidy("testcase.html", "https://TESTING.1.2.3/")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedJavadocCanon)
        os.remove("testcase.html")

    def test_alreadycleanedupcanon_canon(self) :
        with open("testcase.html", "w") as testfile :
            testfile.write(TestTidyjavadocs.javadocAlreadyCleanedUpCanon)
        tidy.tidy("testcase.html", "https://TESTING.1.2.3/")
        with open("testcase.html", "r") as testfile :
            self.assertEqual(testfile.read(), TestTidyjavadocs.expectedJavadocCanon)
        os.remove("testcase.html")

