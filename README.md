# km-show-pages

Tools for discovering html pages in Keyman keyboards that don't load properly in WebKit2

## Included tools

`km-show-page` is a little tool that loads the provided html file with WebKit2. In case the file
doesn't load properly a message is printed. When passing `--close` it will automatically close.

`show-pages` finds all html files in the `release` subdirectory of the given directory and calls
`km-show-pages` on each. The list of html files that WebKit2 can't load is written to
`/tmp/show-pages.output`.
