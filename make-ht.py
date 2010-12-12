
import re, sys, os

initial_dir = os.getcwd()
file = sys.argv[1]
os.chdir(file)

titles = {'doctor-who': 'Doctor Who Quotes',
          'comics': 'Comic Book Quotes',
          'hp-lovecraft':'H.P. Lovecraft Quotes',
          'housing-bubble':'Housing Bubble Quotes',
          'neil-gaiman':'Neil Gaiman Quotes',
          'python-quotes':'Python Quotes',
          'quotations':'Commonplace Book',
          'shakespeare': 'Quotes from William Shakespeare',
          'sherlock-holmes': 'Quotes from Conan Doyle\'s Sherlock Holmes',
          }

keywords = {'doctor-who':'DW, Doctor Who, drwho, rec.arts.drwho,'
                         'William Hartnell, Patrick Troughton, Jon Pertwee,'
                         'Tom Baker, Peter Davison, Colin Baker, '
                         'Sylvester McCoy, Paul McGann, TARDIS, time travel',
            'comics':'comics, Shade, Enigma, Peter Milligan, '
                     'Doom Patrol, Grant Morrison, '
                     'Sandman Mystery Theater',
            'neil-gaiman':'Sandman, Neil Gaiman, Dream, Death, Endless, '
                          'Books of Magic, Dreaming, dreams, Morpheus',
            'hp-lovecraft':'HPL, Howard Phillips Lovecraft, Cthulhu mythos, '
                          'Necronomicon',
            'shakespeare':'William Shakespeare, Shakespearian, Bard of Avon, '
                          '',
            'sherlock-holmes': 'Sherlock Holmes, Sir Arthur Conan Doyle, '
                               'Watson',
            'python-quotes': ('open source, free software, python, '
                              'software engineering, software development'),
            'quotations':'commonplace book, collection',
            }

related_links = {
    'hp-lovecraft':"""
    <p>I wrote up <a href="/conceit/quoting-hpl.html">some thoughts about finding quotations</a> in HPL's works.
    
    <p>My accounts of the two most recent Necronomicon conventions
    are available from <a href="/writing/">my writing page</a>.
    
    <p>Consult the excellent <a
href="http://www.hplovecraft.com">H.P. Lovecraft Archive</a> for 
a detailed and high-quality archive of Lovecraftian information.
    """,
    "sherlock-holmes": """<p>For a master list of Holmesian information
    on the Web, consult <a href="http://www.sherlockian.net">Sherlockian.net</a>.  

    <p><a href="http://e.1asphost.com/sherlockholmes/">The Sherlock Holmes Chronicles</a> 
    provides the full text of the Conan Doyle stories and tools
    for exploring the texts such as full-text search and a concordance.
    """,
    'neil-gaiman': """
    <p>Gaiman's official Web site is at <a
    href="http://www.neilgaiman.com">www.neilgaiman.com</a>.  The
    primary fan-maintained site is <a
    href="http://www.holycow.com/dreaming/">The Dreaming</a>.
    """
    }

def write_related_links (output):
    return
    if related_links.has_key(file):
        output.write('<hr><h3>Related Links</h3>')
        output.write(related_links[file])

    cc_license = open(os.path.join(initial_dir, 'cc.html'), 'r')
    output.write(cc_license.read())
    cc_license.close()

        
def output_filename(pageno):
    if pageno == 1: return 'index'
    else:           return '%i' % pageno

        
separator_pat = re.compile('^NEW FILE (\d+)/(\d+)')

output = None ; total=1
while 1:
    line = sys.stdin.readline()
    if line == "": break
    m = separator_pat.match(line)
    if m is None:
        output.write(line)
    else:
        page, total = m.group(1,2)
        page = int(page) ; total = int(total)
        if output is not None:
            if page == 2:
                write_related_links(output)
            output.close()
        output = open(output_filename(page)+'.ht', 'w')
        title = titles[file]
        output.write("Title: %s, page %i of %i\n" % (title, page, total))
        output.write('stylesheet: /css/quotations.css\n')
        if page == 1 and keywords.has_key(file):
            output.write('Keywords: quotations, quotes, %s, %s\n'
                         % (title, keywords[file]) )

        # Write Meta: header with LINK elements
        links = ""
        if page > 1:
            links += ('<link rel="Prev" href="%s.html" />' %
                      output_filename(page-1) )
        if page < total:
            links += ('<link rel="Next" href="%s.html" />' %
                      output_filename(page+1) )
            
        output.write("Meta: %s\n" % links)
            
        if file == 'robertson-davies':
            output.write('palette: gold\n')
        elif file == 'python-quotes':
            output.write("""Other-links: <h3>Other Software Quotes</h3>
<li><a href="ftp://ftp.icce.rug.nl/pub/unix/linuxcookie.data">Linux Cookies</a>
<li><a href="http://www.cs.yale.edu/~perlis-alan/quotes.html">Alan Perlis</a>
<li><a href="http://www.perl.com/CPAN/authors/id/GBACON/lwall-quotes.txt.gz">Larry Wall</a>
""")
        output.write('\n')
        
# end while
    
if output is not None: 
    output.close()

total = int(total)

# Write the links.h file
link = open('links.h', 'w')

link.write("<H3>Other&nbsp;Formats</H3>\n")
link.write("""<li><a href="../%s.txt">ASCII</a>
<li><a href="../%s.ft">Fortune</a>
<li><a href="../%s.xml">XML</a>
""" % ((file,)*3) )

link.write("""<H3>Other&nbsp;Collections</H3>
<LI><A HREF="../comics/">Comics</A>
<LI><A HREF="../quotations/">Commonplace&nbsp;book</A>
<LI><A HREF="../doctor-who/">Doctor&nbsp;Who</A>
<LI><A HREF="../neil-gaiman/">Neil&nbsp;Gaiman</A>
<LI><A HREF="../peter-greenaway/">Peter&nbsp;Greenaway</A>
<LI><A HREF="../hp-lovecraft/">H.P.&nbsp;Lovecraft</A>
<LI><A HREF="../python-quotes/">Python</A>
<LI><A HREF="../shakespeare/">Shakespeare</A>
<LI><A HREF="../sherlock-holmes/">Sherlock&nbsp;Holmes</A>
""")

link.close()

if os.path.islink('index.html'):
    os.unlink('index.html')

f=open('.htaccess', 'w')
f.write("""RedirectPermanent /%s/1.html http://quotations.amk.ca/%s/\n""" % (file, file))
f.close()

