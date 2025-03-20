Requests-Stdin
=============================================================================

Requests-Stdin is a transport adapter for use with the `Requests`_ Python
library to allow stdin input access via stdin:\/\/ URLs.

To use:

.. code-block:: python

    import requests
    from requests_stdin import StdinAdapter

    s = requests.Session()
    s.mount('stdin://', StdinAdapter())

    resp = s.get('stdin://some_prompt')

Features
-----------------------------------------------------------------------------

- Will read stdin input
- Might set a Content-Length header
- That's about it

Contributing
-----------------------------------------------------------------------------

Contributions welcome! Feel free to open a pull request against
https://github.com/huakim/requests-stdin

License
-----------------------------------------------------------------------------

To maximise compatibility with Requests, this code is licensed under the Apache
license. See LICENSE for more details.

.. _`Requests`: https://github.com/kennethreitz/requests
