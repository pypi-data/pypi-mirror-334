Requests-Text
=============

Requests-Text is a transport adapter for use with the `Requests`_ Python
library to allow text under text:\/\/ URLs.

To use:

.. code-block:: python

    import requests
    from requests_text import TextAdapter

    s = requests.Session()
    s.mount('text://', TextAdapter())

    resp = s.get('text://sometext')

Features
--------

- Will open and read text
- Might set a Content-Length header
- That's about it

------------

Contributions welcome! Feel free to open a pull request against
https://github.com/huakim/python-requests-text

License
-------

To maximise compatibility with Requests, this code is licensed under the Apache
license. See LICENSE for more details.

.. _`Requests`: https://github.com/kennethreitz/requests
