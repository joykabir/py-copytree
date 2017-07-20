
py-copytree
===========

[![Build Status][travis-badge]][travis]

A slightly better implementation python [copytree] that copies recursively source contents to a destination.

Features
--------------------------------------------------
* Destination path is created automatically if it does not exists
* Possible to specify force flag to overwrite destination contents
* Possible to specify which files to copy and not to copy to destination

How it works
-------------
The function takes six arguments. Positional arguments - src and dest -are mandatory. Third positional argument `ignore` takes a function which takes list of items to ignore by using `ignore_patterns` function. The same `ignore` also accepts list of items to copy by using
`include_patterns` function. Specify true to copy symlinks. If force is set to true, destination contents will be overwritten.

```
ignore_patterns() example
-------------------------

copy_tree(src, dest, ignore=ignore_patterns('*.pyc', '*.class'), force=False)

include_patterns() example
--------------------------

copy_tree(src, dest, ignore=include_patterns('*.py', '*.sh'), symlink=True, force=True)

```

Test and lint
--------------

The function is unit tested (not fully covered) and ran through pylint.


Acknowledgements
-----------------
https://stackoverflow.com/a/35161407

License
-------
[MIT License]

[Zia Kab]: http://joykabir.github.io/
[MIT License]: LICENSE.md
[travis-badge]: https://travis-ci.org/joykabir/copytree.svg?branch=develop
[travis]: https://travis-ci.org/joykabir/copytree
[copytree]: https://docs.python.org/2/library/shutil.html
