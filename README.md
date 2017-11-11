# pyinfo
This library collect all the info for python environment you are running and optionally display them as html page or on terminal for cli program.
It could be considered like a python equivalent of phpinfo for php language.



## Usage as standalone command
```bash

~ # python -m pyinfo
============== System information ==============
     Python version: 3.6.3
         OS Version: Linux 4.13.11-1-ARCH
         Executable: /usr/bin/python3
         Build Date: Oct 24 2017 14:48:20
           Compiler: GCC 7.2.0
         Python API: 1013
...

```

## Usage via python code
```python
import pyinfo

# get the information as object
info = pyinfo.python_info()

# The info dictionary contains all info grouped by topic
# info = {
#    'System information': { ... },
#    'Python internals': { ... },
#    'OS internals': { ... },
#    'Environment variables': { ... },
#    'Database support': { ... },
#    'Compression and archiving': { ... },
#    'Socket': { ... },
#    'Multimedia support': { ... },
#    'Copyright'
# }

print(info['Socket']['Hostname'])
# > 3.6.3


# you can even retrieve the text or html versions
text_info = pyinfo.info_as_text()
print(text_info)

with open('/tmp/pyinfo.html', 'w') as f:
    f.write(pyinfo.info_as_html())

```

## As standalone WSGI app
```python
def application(environ, start_response):
    import pyinfo

    output = pyinfo.info_as_html()

    start_response('200 OK', [('Content-type', 'text/html')])
    return [output]
```

## Mount into WSGI application

Eg. using flask
```python
# myapp.py

from flask import Flask

app = Flask(__name__)

@app.route('/pyinfo')
def info():
    import pyinfo
    return pyinfo.info_as_html()
```

# or in webapp2 app
```python
from webapp2 import WSGIApplication, Route

app = WSGIApplication([
  Route('/pyinfo', handler='pyinfo.wsgi')
])
```


# CREDITS

This library is based on the great work made by [@branneman](https://gist.github.com/branneman/951825).
