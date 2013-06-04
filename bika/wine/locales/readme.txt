bika.wine i18n
=============

Edit the first few lines of updatelocales.sh, then open a terminal and run

    $ ./updatelocales.sh

This will

1. Create bika.wine.pot, and scan for all messages in the "bika.wine" domain.
These are  identified by using domain="bika.wine" in templates, and by scanning
for _() calls in python code.  Import bika.lims.bikaMessageFactory as _

2. Override messages in bika.wine.pot with those found in bika.wine-manual.pot

3. Use i18ndude to synchronise bika.wine.pot with */LC_MESSAGES/bika.wine.po

4. Create plone.pot, and scan the bika/wine/profiles folder for all messages
in the "plone" domain.

5. Override messages in the default plone.app.locales "plone" domain with
those found in plone-manual.pot

Recompile (requires gettext/msgfmt) all *.mo files
