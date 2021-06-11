
==============
pibooth-qrcode
==============

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-qrcode`` is a plugin for the `pibooth`_ application.

It adds the display of a custom qrcode at the print and wait state

Install
-------

::

    $ pip3 install pibooth-qrcode

Configuration
-------------

Here below the new configuration options available in the `pibooth`_ configuration.
**The keys and their default values are automatically added to your configuration after first** `pibooth`_ **restart.**

.. code-block:: ini

    [QRCODE]
    # Prefix URL for the QR code
    prefix_url = https://github.com/pibooth/pibooth

    # Use only one URL for all photos (one QR code linking to the album)
    unique_url = True

    # QR code foreground color
    foreground = (255, 255, 255)

    # QR code background color
    background = (0, 0, 0)

    # QR code offset according to location
    offset = (20, 40)

    # QR code location on 'wait' state: topleft, topright, bottomleft, bottomright, midtop-left, midtop-right, midbottom-left, midbottom-right
    wait_location = bottomleft

    # QR code location on 'print' state: topleft, topright, bottomleft, bottomright, midtop-left, midtop-right, midbottom-left, midbottom-right
    print_location = bottomright

.. note:: Edit the configuration by running the command ``pibooth --config``.

Locations
---------

Here is the possible QR code location at screen:

.. image:: https://raw.githubusercontent.com/pibooth/pibooth-qrcode/master/docs/images/locations.png
   :align: center
   :alt: Locations

Example
-------

Here is an example of the rendering you can get with this plugin on the wait screen:

.. image:: https://raw.githubusercontent.com/pibooth/pibooth-qrcode/master/docs/images/screenshot.png
   :align: center
   :alt: Example screenshot

.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth-qrcode.svg
   :target: https://pypi.org/project/pibooth-qrcode
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth-qrcode?color=purple
   :target: https://pypi.org/project/pibooth-qrcode
   :alt: PyPi downloads
