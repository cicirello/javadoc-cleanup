# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-05-26

### Added
  
### Changed

### Deprecated

### Removed

### Fixed

### CI/CD


## [1.3.0] - 2021-05-26

### Added
* Ability to insert a user-defined block into the head of each javadoc page. The
  motivation of this was for the purpose of adding the ability to insert links to
  a favicon for the site. But exactly what is needed for this can vary greatly from
  one site to the next. This new feature is not limited to this use-case. It can be
  used to insert anything that is valid in the head of an html page into every
  javadoc generated page.
  
### Changed
* Changed tag used to pull base docker image from `latest` to `3` (the current
  latest major release tag) to ensure we don't accidentally pick up breaking 
  changes in future releases of base image.
* Refactored existing code to improve maintainability.


## [1.2.1] -2021-05-06

### Changed
* Various improvements to documentation, specifically to the example
  workflows.

### CI/CD
* Introduced major version tag.
* Enabled CodeQL code scanning on all push/pull-request events.
* Added integration testing to all push/pull-request events.

### Other
* Added changelog.


## [1.2.0] - 2020-10-15

### Added
* Now includes option to also generate and insert canonical URLs in head of each javadoc page.

### Changed
* Example workflows now assume Maven for running workflows, but can easily be adapted 
  to any other method of running javadoc.

## [1.1.0] - 2020-9-24

### Changed
* Switched to smaller docker base image, 
  [pyaction-lite](https://github.com/cicirello/pyaction-lite), to speed up action loading
* Updated example workflows in README

## [1.0.1] - 2020-9-23

### Fixed
* Minor bug fix: javadoc-cleaner is now prevented from 
  modifying non-javadoc html files, if any are present.

## [1.0.0] - 2020-9-22

### Added
* Initial release features improved browsing of javadocs on mobile devices.

