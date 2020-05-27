====================
pibooth-qrcode
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-qrcode`` is a plugin for the `pibooth <https://github.com/pibooth/pibooth>`_
application.

Pibooth plugin to generate a QR code to access to the final the picture

Install
-------

::

    $ pip3 install pibooth-qrcode


Configuration
-------------

This is the extra configuration options that can be added in the ``pibooth``
configuration):

.. code-block:: ini

    [QRCODE]
    # Enable qr code
    activate = True
    
    # Generate new link by photo with basename and photo name
    by_photo = False
    
    # The qr code basename of URL or unique URL(if by_photo=False)
    url = 
    
    # The qr code color to fill and background
    color = ("black", "white")

.. note:: Edit the configuration by running the command ``pibooth --config``.


.. |PythonVersions| image:: https://img.shields.io/badge/python-2.7+ / 3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 2.7+/3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth-qrcode.svg
   :target: https://pypi.org/project/pibooth-qrcode
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth-qrcode?color=purple
   :target: https://pypi.org/project/pibooth-qrcode
   :alt: PyPi downloads
