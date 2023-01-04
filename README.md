HowTo
=====

Prepare environmenent
---------------------

```shell
$ python3 -m venv env
$ source env/bin/activate
```


Make distribution source package
--------------------------------

Activate environment and execute next command

```shell
(env) $ python setup.py sdist
```

the `dist` folder will be created with JofemarVending package inside.

Installation
------------

Make distribution package copy it into raspberry and run pip install, for example

```shell
$ pip install 'Deputany bot-1.0.0.tar.gz'
```

