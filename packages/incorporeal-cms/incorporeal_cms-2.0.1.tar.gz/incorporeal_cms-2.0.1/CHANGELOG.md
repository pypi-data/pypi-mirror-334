# CHANGELOG

Included is a summary of changes to the project, by version. Details can be found in the commit history.

## v2.0.1

### Improvements

* The `Image` tag in Markdown files no longer requires the full URL to be specified. Now `Config.BASE_HOST` is
  prepended to the tag value, which should be the full path to the image.
* `.files` are skipped when copying files to the SSG output directory.

## v2.0.0

### Features

* The project has been rewritten as a static site generator. This is of course a larger change than one line, so see the
  commit involved for the nitty gritty.
* Notably, this means I am now --- yes :( --- shipping some JavaScript, to handle the style switching, which is all
  client-side now.
* CHANGELOG.md added.
