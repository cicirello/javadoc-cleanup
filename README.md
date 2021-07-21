# javadoc-cleanup

[<img alt="cicirello/javadoc-cleanup - Create mobile-friendly documentation sites by post-processing javadocs in GitHub Actions" 
     src="images/javadoc-cleanup.png" width="640">](#javadoc-cleanup)

Check out all of our GitHub Actions: https://actions.cicirello.org/

## About

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/cicirello/javadoc-cleanup?label=Marketplace&logo=GitHub)](https://github.com/marketplace/actions/javadoc-cleanup)
[![build](https://github.com/cicirello/javadoc-cleanup/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/javadoc-cleanup/actions/workflows/build.yml)
[![CodeQL](https://github.com/cicirello/javadoc-cleanup/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cicirello/javadoc-cleanup/actions/workflows/codeql-analysis.yml)
[![License](https://img.shields.io/github/license/cicirello/javadoc-cleanup)](https://github.com/cicirello/javadoc-cleanup/blob/master/LICENSE)
![GitHub top language](https://img.shields.io/github/languages/top/cicirello/javadoc-cleanup)

The javadoc-cleanup GitHub action is a utility to tidy up javadocs prior to deployment to 
an API documentation website, assumed hosted on GitHub Pages. It performs the following
functions:
* Improves mobile browsing experience: It inserts `<meta name="viewport" content="width=device-width, initial-scale=1">` within the `<head>` of each html file that was generated by javadoc.
* Strips out any timestamps inserted by javadoc: The timestamps cause a variety of version control issues for documentation sites maintained in git repositories. Javadoc has an option `-notimestamp` to direct javadoc not to insert timestamps (which we recommend that you also use). However, at the present time there appears to be a bug (in OpenJDK 11's javadoc, and possibly other versions), where the timestamp is not ommitted in the `overview-summary.html` generated by javadoc.
* It is also capable of generating and inserting the canonical URL for each page, of the form `<link rel="canonical" href="https://URL.TO.YOUR.API.DOC.WEBSITE/page.html">`.
* The newest feature enables inserting a user-defined block into the head of each javadoc generated 
  page. For example, if you want to insert a link to your site's favicon, or really anything else that
  is valid in the head of an html file.

The javadoc-cleanup GitHub action is designed to be used 
in combination with other GitHub Actions. For example, it 
does not commit and push the modified javadocs. See 
the [Example Workflows](#example-workflows) for examples of combining
with other actions in your workflow. We also have links to a few projects
that are actively using the javadoc-cleanup action in the 
section [Examples in Other Projects](#examples-in-other-projects).

## Inputs

### `path-to-root`

The path to the root of the website relative to the
root of the repository. The default is `.` which 
is appropriate in cases where you are using a `gh-pages` branch
for your documentation site. If you are instead using this for a GitHub Pages site
in the `docs` directory, then
just pass `docs` for this input.

### `base-url-path`

This is the url to the root of your website. If you provide this 
input, then javadoc-cleanup will generate and insert a canonical 
link for each page in the header, of the 
form: `<link rel="canonical" href="https://URL.TO.YOUR.API.DOC.WEBSITE/page.html">`, 
assuming `base-url-path` equals `"https://URL.TO.YOUR.API.DOC.WEBSITE/"` and 
assuming `page.html` is the relevant filename.

### `user-defined-block`

This input can be used if there is anything else that you want to insert into
the head of every javadoc generated page. For example if you want to insert links
to the site's favicon. Here are a couple examples.

Perhaps you have an favicon.svg in the images directory of the documentation site,
then the following will insert a link to it in the head of every javadoc generated page:

```yml
    - name: Tidy up the javadocs
      uses: cicirello/javadoc-cleanup@v1
      with:
        path-to-root: docs
        user-defined-block: |
          <link rel="icon" href="/images/favicon.svg" sizes="any" type="image/svg+xml">
```

In the above, the `|` is what YAML calls a block scalar, essentially a multiline string.
In the example above, the string itself is only a single line, however, the advantage
of using this syntax is to avoid the need to escape all of the quote characters.

Perhaps there are multiple lines you want to insert into the head of the pages. This next example
shows this using a case where perhaps you have both svg and png versions of your favicon.

```yml
    - name: Tidy up the javadocs
      uses: cicirello/javadoc-cleanup@v1
      with:
        path-to-root: docs
        user-defined-block: |
          <link rel="icon" href="/images/favicon.svg" sizes="any" type="image/svg+xml">
          <link rel="icon" href="/images/favicon.png" type="image/png">
```

Please note that the action does not attempt to check the syntax of your `user-defined-block`.
It simply inserts it verbatim into the head of every javadoc generated page.

## Outputs

### `modified-count`

This output is the count of the number of html pages modified by the action.

## Example Workflows

### Prerequisites of Examples

* The example workflows assume that `javadoc` is run via Maven, and it also
  assumes that Maven's default directory structure is in use (e.g., that 
  output is to a `target` directory). You should put Maven's `target` directory
  in your `.gitignore`. The example workflows include a step that copies the
  generated documentation from Maven's default of `target/site/apidocs` to 
  the `docs` folder (assuming you are serving the documentation via GitHub Pages
  in the `docs` folder).
* Depending upon the version of Java, javadoc may generate multiple zip files
  of its search index, in addition to the JavaScript versions of those very
  search index files. This is true of javadoc for Java 11, although more recent Java
  versions have eliminated the zip files. These zip files are completely unnecessary.
  The documentation will use the `js` versions of these. Additionally, the
  `zip` files are problematic for documentation sites served from a git repository
  because they will appear as if they changed every time javadoc runs, even if
  nothing has actually changed (e.g., due to time-stamping). We strongly recommend 
  that for these reasons you add the five zip files to your `.gitignore`.  They are
  `module-search-index.zip`, `package-search-index.zip`, `type-search-index.zip`, 
  `member-search-index.zip`, and `tag-search-index.zip`. They are functionally 
  unnecessary, as the `.js` counterparts alone are sufficient for javadoc's search to
  work.

### Basic Syntax

You can run the action with a step in yuor workflow like this (assuming that your javadocs 
are in docs directory:

```yml
    - name: Tidy up the javadocs
      uses: cicirello/javadoc-cleanup@v1
      with:
        path-to-root: docs
```

In the above example, the major release version was used, which ensures that you'll
be using the latest patch level release, including any bug fixes, etc. If you prefer,
you can also use a specific version such as with:

```yml
    - name: Tidy up the javadocs
      uses: cicirello/javadoc-cleanup@v1.3.0
      with:
        path-to-root: docs
```


### Example 1: Basic example without canonical links

This example workflow is triggered by a push of java source files.
After setting up java, Maven is used to generate the javadocs, and 
the javadocs are then copied from Maven default target location to the 
docs directory where the GitHub Pages documentation site is assumed hosted. 
After which, the javadoc-cleanup action runs. The workflow then outputs 
the number of modified html pages (for logging purposes). The 
workflow then commits the changes (if any).
This example doesn't push the changes,
but you can easily add a `git push` after the commit, or add another action to handle
that.

```yml
name: docs

on:
  push:
    branches: [ master ]
    paths: [ '**.java' ]

jobs:
  api-website:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout the repo
      uses: actions/checkout@v2

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '11'
        distribution: 'adopt'

    - name: Build docs with Maven
      run: mvn javadoc:javadoc

    - name: Copy to Documentation Website Location
      run: |
        rm -rf docs
        cp -rf target/site/apidocs/. docs

    - name: Tidy up the javadocs
      id: tidy
      uses: cicirello/javadoc-cleanup@v1
      with:
        path-to-root: docs
    
    - name: Log javadoc-cleanup output
      run: |
        echo "modified-count = ${{ steps.tidy.outputs.modified-count }}"
    
    - name: Commit documentation changes
      run: |
        if [[ `git status --porcelain` ]]; then
          git config --global user.name 'YOUR NAME HERE'
          git config --global user.email 'YOUR-GITHUB-USERID@users.noreply.github.com'
          git add -A
          git commit -m "Automated API website updates."
        fi
```

### Example 2: Basic example with canonical links

This example workflow is mostly the same as above, except it also 
generates and inserts canonical links in each javadoc page.

```yml
name: docs

on:
  push:
    branches: [ master ]
    paths: [ '**.java' ]

jobs:
  api-website:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout the repo
      uses: actions/checkout@v2

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '11'
        distribution: 'adopt'

    - name: Build docs with Maven
      run: mvn javadoc:javadoc

    - name: Copy to Documentation Website Location
      run: |
        rm -rf docs
        cp -rf target/site/apidocs/. docs

    - name: Tidy up the javadocs
      id: tidy
      uses: cicirello/javadoc-cleanup@v1
      with:
        base-url-path: https://URL.FOR.YOUR.WEBSITE.GOES.HERE/
        path-to-root: docs
    
    - name: Log javadoc-cleanup output
      run: |
        echo "modified-count = ${{ steps.tidy.outputs.modified-count }}"
    
    - name: Commit documentation changes
      run: |
        if [[ `git status --porcelain` ]]; then
          git config --global user.name 'YOUR NAME HERE'
          git config --global user.email 'YOUR-GITHUB-USERID@users.noreply.github.com'
          git add -A
          git commit -m "Automated API website updates."
        fi
```


### Example 3: Combining with other GitHub actions

This example combines the `javadoc-cleanup` action with other actions. Specifically,
it uses the [cicirello/generate-sitemap](https://github.com/cicirello/generate-sitemap) action 
to generate a sitemap for the documentation website, and the 
[peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request)
action to create a pull request with the changes.  Note that for this example,
the checkout action is called with `fetch-depth: 0` because `generate-sitemap` needs
the complete commit history. This is unnecessary for usage of the `javadoc-cleanup` action
alone.

```yml
name: docs

on:
  push:
    branches: [ master ]
    paths: [ '**.java' ]

jobs:
  api-website:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout the repo
      uses: actions/checkout@v2
      with:
        fetch-depth: 0 

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '11'
        distribution: 'adopt'
    
    - name: Build docs with Maven
      run: mvn javadoc:javadoc

    - name: Copy to Documentation Website Location
      run: |
        rm -rf docs
        cp -rf target/site/apidocs/. docs
    
    - name: Tidy up the javadocs
      id: tidy
      uses: cicirello/javadoc-cleanup@v1
      with:
        path-to-root: docs
        base-url-path: https://URL.FOR.YOUR.WEBSITE.GOES.HERE/
    
    - name: Log javadoc-cleanup output
      run: |
        echo "modified-count = ${{ steps.tidy.outputs.modified-count }}"
    
    - name: Commit documentation changes
      run: |
        if [[ `git status --porcelain` ]]; then
          git config --global user.name 'YOUR NAME HERE'
          git config --global user.email 'YOUR-GITHUB-USERID@users.noreply.github.com'
          git add -A
          git commit -m "Automated API website updates."
        fi

    - name: Generate the sitemap
      id: sitemap
      uses: cicirello/generate-sitemap@v1
      with:
        base-url-path: https://URL.FOR.YOUR.WEBSITE.GOES.HERE/
        path-to-root: docs
        
    - name: Create Pull Request
      uses: peter-evans/create-pull-request@v3.8.2
      with:
        title: "Automated API website updates."
        commit-message: "Automated API documentation website updates."
```

## Examples in Other Projects

If you would like to see examples where the action is actively used, here are a few repositories that 
are actively using the `javadoc-cleanup` action. The table provides a link to repositories using the 
action, and direct links to the relevant workflow as well as to the api documentation sites that result
from the workflow.

| Repository | Workflow | Javadocs |
| :----- | :----- | :----- |
| [Chips-n-Salsa](https://github.com/cicirello/Chips-n-Salsa) | [docs.yml](https://github.com/cicirello/Chips-n-Salsa/blob/master/.github/workflows/docs.yml) | https://chips-n-salsa.cicirello.org/api/ |
| [JavaPermutationTools](https://github.com/cicirello/JavaPermutationTools) | [docs.yml](https://github.com/cicirello/JavaPermutationTools/blob/master/.github/workflows/docs.yml) | https://jpt.cicirello.org/api/ |

## License

The scripts and documentation for this GitHub action are released under
the [MIT License](https://github.com/cicirello/javadoc-cleanup/blob/master/LICENSE).
