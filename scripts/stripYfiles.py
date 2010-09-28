#!/usr/bin/env python
#
# stripYfiles.py
#
# Strip out yFiles extensions from a GraphML file.
#
# yEd is a powerful graphical graph editor that can write out to a 
# GraphML file.  Unfortunately, NetworkX is not able to read files
# created by this tool because they contain an extension to the GraphML 
# format called yFiles.  This script will strip out the yFiles 
# extensions which allows the file to be read into NetworkX using the
# networkx.read_graphml() function.
#
# Matt Shelton <matthew.j.shelton@gmail.com>
#

import os, time
from xml.etree.ElementTree import ElementTree

def recursive_remove(element, keys):
    """Remove all the yFiles elements from the XML structure."""
    if len(element.getchildren()) == 0:
        return

    for child in element.getchildren():
        recursive_remove(child, keys)
        for k in keys:
            if child.attrib.has_key('key') and child.attrib['key'] == k:
                element.remove(child)
                break

def main(argv):
    """Strip all the yFiles extension from the graphml file.

    The yEd graph editor uses a set of extensions called yFiles that are
    not supported by networkx.read_graphml().  This script will strip
    out all of the extensions from the file.
    """
    if len(argv) != 2:
        print "usage:  %s <file.graphml>" % argv[0]
        return 1

    try:
        print "Stripping %s of all yFiles extensions." % argv[1]
        xml = ElementTree(file=argv[1])
        root = xml.getroot()

        # Parse out the yFiles extension IDs.
        keys = []
        for e in xml.findall("{http://graphml.graphdrawing.org/xmlns}key"):
            if e.attrib.has_key("yfiles.type"):
                # This is a yFiles key, record and strip it.
                keys.append(e.attrib['id'])
                root.remove(e)

        # Remove all elements with a 'key' attribute equal to one of the IDs 
        # collected in the step above.
        recursive_remove(root, keys)

        # Backup the original graphml file and write out the new one.
        os.rename(argv[1], "%s.%d" % (argv[1], time.time()))
        xml.write(argv[1])


    except Exception, ex:
        print ex
        return 1

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))

# vim:et:ts=4:sw=4:
