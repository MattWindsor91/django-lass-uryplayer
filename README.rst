=====================
django-lass-uryplayer
=====================

``django-lass-uryplayer`` is the *URY Player* service, or rather the
models and views that make it work.  It provides models and views for
podcasts, attachments between podcasts and other models, and methods
to group podcasts into streams (*channels*).

Licence
=======

In short: 2-clause BSD or GPL version 2, take your pick.

``django-lass-metadata``, as a spin-off from the *LASS* project, is
licensed under the GNU General Public License version 2.  However, as
it was comprised entirely of code solely written by URY and/or code
not under licence, the original author decided to dual-license under
GPLv2 and the FreeBSD 2-clause license.

Usage
=====

Documentation is coming soon (there are docstrings in the actual code,
but nothing much else).

Future changes
==============

The metadata app currently contains some common patterns mixins and
functions from the *LASS* project that could do with being further
separated into another reusable app.

The multitudinous ways of accessing metadata from metadata subjects
should probably be condensed into one or two methods.
