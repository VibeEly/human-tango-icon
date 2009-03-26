#!/usr/bin/env python

# Copyright (c) 2008 Patryk Zawadzki <pzawadzki@gnome.org>
# Contributor   2008 Patrick Niklaus <marex@compiz-fusion.org>
# Based on an idea and Ruby script by Jakub Steiner
#
# Licensed under LGPL v3+ (http://www.gnu.org/copyleft/lesser.html)

from xml.dom.minidom import parse
import os
import sys

INKSCAPE = 'inkscape'
CONVERT = 'convert'
SRC = './svg'

def renderIt(template):
	print 'Rendering %s...' % template
	doc = parse(template)
	groups = doc.getElementsByTagName('g')
	layers = [g for g in groups if g.parentNode.tagName == 'svg']
	tmp = None
	for l in layers:
		plate = None
		for s in l.getElementsByTagName('g'):
			if 'plate' in s.getAttribute('inkscape:label'):
				style = s.parentNode.getAttribute('style')
				if 'display:none' not in style:
					plate = s
					break
		if plate:
			if not tmp:
				dirname = u'tmp'
				if not os.path.exists(dirname):
					os.makedirs(dirname)
				tmp = u'%s/%s.png' % (dirname, template.split(u'/')[-1].replace(u'.svg', u''))
				cmd = u'%s -z -e "%s" "%s"' % (INKSCAPE, tmp, template)
				os.system(cmd)
			# if no plate is found, it could be a drawing aid, skip it
			context = 'unknown'
			icon_name = 'unknown'
			for t in plate.getElementsByTagName('text'):
				if t.getAttribute('inkscape:label') == 'context':
					context = t.getElementsByTagName("tspan")[0].childNodes[0].data.strip()
				elif t.getAttribute('inkscape:label') == 'icon-name':
					icon_name = t.getElementsByTagName("tspan")[0].childNodes[0].data.strip()
			sizes = plate.getElementsByTagName('rect')
			for s in sizes:
				rectid = s.getAttribute('id')
				width = s.getAttribute('width')
				height = s.getAttribute('height')
				x = s.getAttribute("x")
				y = s.getAttribute("y")
				dirname = u'%sx%s/%s' % (width, height, context)
				if not os.path.exists(dirname):
					os.makedirs(dirname)
				fname = u'%sx%s/%s/%s.png' % (width, height, context, icon_name)
				cmd = u'convert %s -gravity NorthWest -crop %sx%s+%s+%s %s' % (tmp, width, height, x, y, fname)
				os.system(cmd)

if __name__ == '__main__':
	args = sys.argv[1:]
	if args:
		for a in args:
			renderIt(a)
	else:
		for root, dirs, files in os.walk(SRC):
			for f in files:
				if os.path.splitext(f)[1] == '.svg':
					renderIt(os.path.join(root, f))
