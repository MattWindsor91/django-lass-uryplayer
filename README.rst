====================
django-lass-metadata
====================

``django-lass-metadata`` is the generic metadata system used by
*LASS*, the Django-based website system that powers the University
Radio York web presence.

It provides a few models and functions that make adding arbitrary,
key-value format metadata to existing models through a minimum of
additional overhead.

The main design decision was to provide metadata in a way that could
be extended at the key level without changing the database structure
and would easily be accessible from database-using applications
outside of Django; as such, it may not be the best solution for new
Django-specific projects.  Always read the label.

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
