#!/bin/bash

ZINSTANCE=~/Plone/zinstance
I18NDUDE=$ZINSTANCE/bin/i18ndude

# Flush the english (transifex source language) po files
# If we don't do this, new *-manual translations won't be synced.

> en/LC_MESSAGES/bika.wine.po

# Remove generated files

find . -name "*.mo" -delete
rm bika.wine.pot 2>/dev/null

touch i18ndude.pot
$I18NDUDE rebuild-pot --pot i18ndude.pot --exclude "build" --create bika.wine ..
msgcat --strict --use-first bika.wine-manual.pot i18ndude.pot > bika.wine.pot
$I18NDUDE sync --pot bika.wine.pot */LC_MESSAGES/bika.wine.po
rm i18ndude.pot

# Compile *.mo

for po in `find . -name "*.po"`; do msgfmt -o ${po/%po/mo} $po; done

