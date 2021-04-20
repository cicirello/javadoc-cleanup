# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-04-20

### Added
* This changelog.
  
### Changed
* Various improvements to documentation, specifically to the example
  workflows.

### Deprecated

### Removed

### Fixed

### CI/CD
* Enabled CodeQL code scanning on all push/pull-request events.


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

