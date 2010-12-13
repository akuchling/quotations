#!/usr/bin/env python

import sys, re, rfc822, time, os, string
import StringIO
import rst_html

wwwdir = os.path.join(os.environ['HOME'], 'files', 'www')
rootdir = os.path.join(wwwdir, 'sites/quotations.amk.ca')

MONTHS = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
          7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

HOME_NAME = "quotations.amk.ca"
TREE_INFO = {
  HOME_NAME: '/',
}

# Types for the different kinds of entries in a LinkList
HEADING = 1
LINK = 2
DEADLINK = 3

def isURL(href):
    "Return true if a string seems to be a URL"
    # Has it got a :// in it?
    if string.find(href, '://') != -1: return 1

    # mailto:whoever is an annoying exception
    elif href.startswith('mailto:'): return 1
    else:
        return 0
    
class LinkList (list):
    """Class containing a list of links and titles.  Predicates:
    isHeading(index) -- is it a heading?  then you can call heading()
    isLink(index) -- is it a live link? then you can call linkText/linkHref()
    isDeadLink(index) -- is it a link to this page? then you can call linkText()

    Accessor functions:
    heading(index) -- can only call if isHeading(index) is true
    linkText(index) -- text of link (only if isLink or isDeadLink is true)
    linkHref(index) -- HREF to which link is pointing

    It's not a linked list; it's a list of links.
    """

    def __init__(self, otherlinks, filename):
        """Apply various bits of magic to the otherlinks specs."""

        # The list is kept as a list of tuples.  A 2-tuple containing
        # (type code, string) is a heading or text inclusion; links
        # are 3-tuples containing (type, linkText, linkHref).  The
        # link is dead if linkHref == None

        filename = filename + 'ml'
        
        # Assume the base text consists of a bunch of <LI> items,
        # with <H3>...</H3> items in between.
        # Change each of these into a table cell.

        s = otherlinks
        heading_pat = re.compile(r'\s*<h3>(.*?)</h3>', re.I | re.S)
        link_pat = re.compile(r"[\s\n]*<li>(.*?)(<li>|<h3>|$)", re.I|re.M|re.S)
        href_pat = re.compile(r'<a href="?([^<>"]*)"?\s*>(.*?)</a>', re.S | re.I)
        pos = 0
        s = string.strip(s)
        while (pos < len(s)):
            m = heading_pat.match( s, pos)
            if m:
                t= (HEADING, m.group(1))
                self.append( t )
                pos = m.end()
                continue
            m = link_pat.match( s, pos)
            if m:
                pos = m.start(2)
                t = m.group(1)
                m2 = href_pat.search( m.group(1) )
                href, text = m2.group(1, 2)

                # Figure out whether the HREF URL points to this file; if so,
                # it's a dead link.
                
                href_target = href
                if isURL(href_target):
                    # It's a URL of some sort, so it should never be dead
                    # (unless you're fully specifying your own hostname in
                    # the URL; this seems unlikely)
                    pass
                else:
                    if href_target in ("", "./") or href_target[-1:] == '/':
                        href_target = href_target + "index.html"
                    if href_target[0] == '/':
                        href_target = os.path.join(rootdir, href_target[1:])
                    else:
                        # It might be some sort of relative URL, so we figure
                        # out what directory we're in, and join the href to
                        # that path
                        p1 = os.path.dirname(filename)
                        p1 = os.path.join(p1, href_target)
                        href_target = os.path.normpath(p1)
                        
                # Now actually do the comparison
                if href_target == filename:
                    href = None
                    self.append( (DEADLINK, text, href) )
                else:
                    self.append( (LINK, text, href) )
            else:
                raise RuntimeError, "Can't handle text in links"

    def isHeading(self, index):
        return self[index][0] == HEADING
    def isLink(self, index):
        return self[index][0] == LINK
    def isDeadLink(self, index):
        return self[index][0] == DEADLINK
    
    def heading(self, index):
        if not self.isHeading(index):
            raise ValueError, "Index %s is not a heading" % (index,)
        return self[index][1]
    def linkText(self, index):
        if not (self.isLink(index) or self.isDeadLink(index)):
            raise ValueError, "Index %s is not a link" % (index,)
        text = self[index][1].replace(' ', '&nbsp;')
        return text
    def linkHref(self, index):
        if self.isDeadLink(index):
            raise ValueError, "Index %s is a dead link" % (index,)
        if not self.isLink(index):
            raise ValueError, "Index %s is not a link" % (index,)
        return self[index][2]

def get_full_path ():
    path = os.getcwd()
    path = string.split(path, os.sep)	   # path = ['www', 'root',...]

    # Remove root directory
    index = path.index('quotations.amk.ca')
    root = path[:index+1]
    path = path[index+1:]
    return root, path

def build_tree_info (filename):    
    "Assemble the tree information for this document"

    # First, we need to figure out the path from the root of the
    # tree to this document.  For example, the path might be:
    # ['Home', 'MEMS Tech', 'Patents'].
    # We have to do this the hard way; walk back up 
    # the directory tree, looking for .treeinfo files to tell
    # us the name.
    root, path = get_full_path()
    
    orig_path = path[:]
    tree_path = []
    while len(path) > 0:
        # Check for a .treeinfo file
        try:
            treefile = '/'+string.join(root+path, '/') + '/.treeinfo'
            f = open(treefile, 'r')
            text = string.strip( f.readline() )
            f.close()
        except IOError:	
            text = string.capitalize(path[-1])
        if text != 'skip':
            tree_path = [text] + tree_path 
        path = path[:-1] ; root = root[:-1]

    # tree_path is now something like ['MEMS Tech', 'Deposition', ]
    tree_path = [HOME_NAME] + tree_path
    path = [""] + orig_path

    assert len(tree_path) <= len(path)
    # Now, walk over the two lists
    directory = ""
    for i in range(0, len(path)):
       # Build the directory URL from the path
       url = directory + string.join(path[:i+1], '/')
       if url!='/': url=url+'/'

       # Build a partial tree path
       partial_path = string.join(tree_path[:i+1], ':')
       #               print partial_path, url
       # If there isn't already a path
       if not TREE_INFO.has_key(partial_path):
           TREE_INFO[partial_path] = re.sub('/+', '/', url)
       else:
           pp = TREE_INFO[partial_path]
           while pp and pp[-1] == '/': pp=pp[:-1]
           directory = pp

    if os.path.basename(filename) == 'index.ht':
        tree_path = tree_path[:-1] ; path = path[:-1]

    tree_path = map(string.strip, tree_path)
    if len(tree_path)>0 and tree_path[0] != HOME_NAME: 
        tree_path = [HOME_NAME] + tree_path

    t = ""
    for i in range( len(tree_path) ):
        partial_path = string.join( tree_path[:i+1], ":" )
        #	    print i,tree_path,partial_path,
        url = TREE_INFO[ partial_path ]
        #            print url
        text = tree_path[i]
        t = t + ('<a href="%s">%s</a> &gt;&#160;' % (url, text) )
    print t
    return t

        
def format_linklist(L):
    s = ""
    if len(L) == 0: return ""
    firstHeader = True
    firstLink = True
    for i in range(len(L)):
        if L.isHeading(i):
            if not firstHeader: s += '<br><br>'
            s = ( s + '<span class="link-heading">' +
                  L.heading(i).strip() +
                  ':</span><br>\n' )
            firstLink = 1
        elif L.isDeadLink(i):
            if not firstLink: s = s + '<br>'
            s = (s + '<span class="link-dead">' +
                 L.linkText(i) + "</span>\n")
            firstLink = 0
        elif L.isLink(i):
            if not firstLink: s = s + '<br>'
            s = (s + '<a class="sidebar-link" HREF="%s">%s</a>\n' %
                     (L.linkHref(i), L.linkText(i) ) )
            firstLink = 0
        else:
            assert 0  # This shouldn't happen

        firstHeader = 0
        
    return s 

variable_pat = re.compile('[[](\w*?)[]]')

links_cache = {}

def load_other_links(filename):
    """Read a links.h file, and return a string containing the
    contents. 
    """

    head, tail = os.path.split(filename)
    file = os.path.join(head, "links.h")
    if os.path.exists(file):
        files = [file]
    else:
        files = []

    texts = []
    for file in files:
        if links_cache.has_key(file):
            texts.append(links_cache[file] )
        else:
            f = open(file)
            text = f.read()
            f.close()
            links_cache[ file ] = text
            texts.append(text)

    return '\n'.join(texts)

def parse_links(filename, headers):
    """Given a header name, return a LinkList object representing
    the list of links stored in that header line."""

    links = headers.get('other-links', '')
    fixed_links = load_other_links(filename)
    result = LinkList(links + '\n' + fixed_links, filename)
    return result


def process_file (filename):
    input = open(filename, 'rt')
    headers = rfc822.Message(input)
    headers.rewindbody()
    fn, ext = os.path.splitext(filename)
    output_filename = fn + '.html'
    content_type = headers.get('content-type', None)
    if content_type not in [None, 'text/html', 'text/x-rst']:
        raise RuntimeError("Unknown content-type %r" % content_type)
    is_text = (filename.endswith('.rst') or 
	       content_type == 'text/x-rst')
	
        
    if is_text:
        # Transform using docutils
        from docutils import core, io
        output_file = StringIO.StringIO()
        body = rst_html.process_rst(filename, input.read())

        # Hackery to make the HTML fit into the page better
        body = re.sub('.*<body[^>]*>', '', body)
        body = re.sub('</body>.*', '', body)
        # Transpose <Hn> headers down by 1: <h1> -> <h2>
	#        for i in [5, 4, 3,2,1]:
	#            body = body.replace('h%i>' % i, 'h%i>' % (i+1))
    else:
        body = input.read()

    input.close()

    path = os.getcwd().split('/')
    index = path.index('sites')
    domain = path[index+1]
    template = open(os.path.join(wwwdir, 'sites/quotations.amk.ca/bin/%s.html' % domain), 'rt').read()

    t = time.localtime( os.stat(filename)[8] )
    (date_year, date_month, date_day,
     date_hour, date_minute, date_second) = t[0:6]
    date_month_name = MONTHS[date_month]

    links = parse_links(filename, headers)
    links = format_linklist(links)

    pagelinks = ""
    if 'Page' in headers and 'Total-Page' in headers:
        page_num = int(headers.get('Page'))
        total_pages = int(headers.get('Total-Page'))
        for i in range(1, total_pages+1):
            if i == 1:
                fn = 'index.html'
            else:
                fn = '%i.html' % i
            if i == page_num:
                pagelinks += '<span class="pagenumber">%i</span>' % i
            else:
                pagelinks += '<a class="pagelink" href="%s">[%i]</a>' % (fn,i)
            pagelinks += ' '

    vars = {
        'content' : body,
        'namespaces':headers.get('namespaces', ''),
        'title':headers.get('title', ''),
        'keywords':headers.get('keywords', ''),
        'description':headers.get('description', ''),
        'meta':headers.get('meta', ''),
        'otherlinks': links,
        'date_day': str(date_day),
        'date_year': str(date_year),
        'date_month_name': date_month_name,
        'endif': '[endif]',
        'pagelinks': pagelinks,
        }

    t = time.localtime( os.stat(filename)[8] )
    (vars['date_year'], vars['date_month'], vars['date_day'],
     vars['date_hour'], vars['date_minute'], vars['date_second']) = t[0:6]
    vars['date_month_name'] = MONTHS[vars['date_month']]

    vars['tree_info'] = build_tree_info(filename)
    vars['temporary'] = headers.getheader('temporary') or ''
    vars['rss_link'] = headers.getheaders('RSS-File') or ""
    vars['rdf_link'] = headers.getheaders('RDF-File') or ""
    rss_files = vars['rss_link']
    if rss_files:
        v = ""
        for file in rss_files:
            v += '<link rel="meta" type="application/rss+xml" href="%s" >' % file
        vars['rss_link'] = v
    rdf_files = vars['rdf_link']
    if rdf_files:
        v = ""
        for file in rdf_files:
            v += '<link rel="meta" type="application/rdf+xml" href="%s" >' % file
        vars['rdf_link'] = v

    for hdr in ['description', 'keywords']:
        if vars.get(hdr):
            vars[hdr] = ('<meta name="%s" content="%s" >'
                            % (hdr, vars[hdr]))

    root, urlpath = get_full_path()
    url = os.path.join('/'.join(urlpath)) + '/' + output_filename
    url = url.replace('./', '')
    url = url.lstrip('/')
    url = url.replace('.html', '')
    vars['url'] = url
        
    t = template
    pos = 0
    blocks = []
    while 1:
        m = variable_pat.search(t, pos)
        if m is None: break
        blocks.append(t[pos:m.start()])
        name = m.group(1)
        if vars.has_key(name):
            blocks.append(str(vars[name]))
        else:
            print 'unknown variable:', repr(name)
        pos = m.end()

    blocks.append(t[pos:])
    output = open(output_filename, 'w')
    output.write(''.join(blocks))
    output.close()

    # Set output time
    #ftime = os.stat(filename).st_mtime + 2
    #os.utime(output_filename, (ftime, ftime))
        
if __name__ == '__main__':
    for filename in sys.argv[1:]:
        process_file(filename)
