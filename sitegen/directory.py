# Directory preparation tools for the sitegen site structure.

import os
import sys
from sitegen import settings
from sitegen import publish

'''
This module contains the procedures for creating and managing the site's 
directory structure upon creation or content updates.

Classes are:

 - IndexMaker: makes index.html files for blog directories
 - TagMaker: makes the /tags/ index according to the blog posts categories
 - DirMaker: makes the initial directory structure on the website.

For the sake of clarity, this is the target implementation of the site:

/ Site root
|
|--| index.html -> rendered home page
|--| index.md -> contents for the home page
|--| pubdate -> date when the page was published (YYYY-MM-DD)
|--| description (optional) -> to use with meta description tag
|
|------ /page1 -> directory for page1 (about, privacy policy, contact, etc)
|--------| index.html -> rendered page for page1
|--------| index.md -> contents for page1
|--------| pubdate -> date when the page was published
|--------| description (optional)
|
 ...
|
|------ /blog -> blog article index
|---------| index.html
|---------| pubdate
|---------| description (optional)
|
|------------- /post1
|----------------| index.html -> rendered page for blog post1 
|----------------| index.md -> contents for blog post1
|----------------| pubdate -> date when the post was published
|----------------| categories (optional) -> tags of the post
|----------------| description (optional)
|
 ...
|
|------------ /tags -> Tag index for blog
|----------------- /tag1 -> Article index for tag1
| etc
| 
'''

class IndexMaker:
    '''
    Creates the blog index from a collection of files defined in settings.BLOG
    '''
    def __init__(self):
        # Do we need a startup routine?
        self.startdir = settings.PUBDIR

class DirMaker:
    '''
    Creates the site structure for the first run.

    Alternatively, updates the entire website's pages template without touching
    the content.
    '''
    def __init__(self):
        self.startdir = settings.PUBDIR

    def init(self, force=False):
        '''
        Build site structure from zero.
        '''
        if os.path.isdir(self.startdir):
            print("[INFO] Site root directory already exists.")
        else:
            try:
                print("[INFO] Creating site root directory...")
                os.mkdir(self.startdir)
            except PermissionError:
                print("[ERROR] Could not create site root due to permission error.")
                print("Make sure you have write permissions on this directory and try again.")
                sys.exit(1)

        os.chdir(self.startdir)
        
        # If the directory is empty 
        if len(os.listdir('.')) == 0:
            print("[INFO] Creating directory structure from zero...")
        else:
            if force:
                print("[WARNING] Recreating directory structure from zero...")
                # There has got to be a better way to do this, but...
                os.system('rm -rf *')
            else:
                print("[ERROR] Site structure is not empty. Not touching this.")
                print("Will not recreate structure unless force=True is set")
                print("(note that this would delete *everything* here)")
                print("Please recheck where you'd like to build the site.")
                sys.exit(1)

        os.mkdir(settings.BLOG)
        print("[INFO] Created %s subdirectory." % settings.BLOG_SUBDIR)

        # TODO: do we create the tags directory now?

        print("[INFO] Creating site page directories...")
        # each 'page' is a tuple like: (title, url)
        for page in settings.SITE_PAGES:
            os.mkdir(page[1])
            os.chdir(page[1])

            with open('title', 'w') as ptitle:
                ptitle.write(page[0])
            with open('index.md','w') as index:
                index.write("Edit here your page's content in *MarkDown*")

            print("[INFO] Created page '%s'" % page[0])

            os.chdir('..')
        
        # put some content on the website's root to "bootstrap" it:
        os.chdir(settings.PUBDIR)
        with open('index.md','w') as index:
            index.write('''# Welcome to your new site!

We just created a structure with the following directories:
            ''')
            for page in settings.SITE_PAGES:
                index.write('''
 - [%s](/%s)
                ''' % (page[0], page[1]) )
            index.write('''
Your blog is located [here](%s).
            ''' % settings.BLOG_SUBDIR)
            index.write('''
To get started, edit out the template to your taste and edit the index.md files

Yours,

The Sitegen Team
            ''')
        print("[INFO] Homepage created.")
        with open('index.md', 'r') as index:
            print(index.read())

    def updatetemplate(self):
        '''
        Updates the template for the entire site without altering the content

        TODO
        '''


class TagMaker:
    '''
    An object that creates and handles the tag detection and structure.
    '''

    def __init__(self):
        self._taglist = []
        self.tagrelation = []

    def get_taglist(self):
        return self._taglist

    def detect_tags(self):
        '''
        Detect tags in the BLOG directory by reading the 'categories' files
        in each post, and squashing duplicates.
        '''
        os.chdir(settings.BLOG)

        raw_list = ''        
        for item in os.walk('.'):
            if 'categories' in item[2]:
                ind = item[2].index('categories')
                catfile = item[0] + '/' + item[2][ind]
                with open(catfile, 'r') as cats:
                    raw = cats.read()
                    raw_list += raw
                
                # Make the relation between tags and posts:
                raw_tags = raw.split("\n")
                raw_tags.pop()

                with open(item[0] + '/' + 'index.md', 'r') as post:
                    raw = post.read()
                    title = raw.split("\n")[0][2:]
                self.tagrelation.append((item[0][2:], raw_tags, title))

        # Raw list populated with all tag material. Remove duplicates
        for line in raw_list.split('\n'):
            if line not in self._taglist:
                self._taglist.append(line)

        # Remove empty category from end of stack:
        self._taglist.pop()
        os.chdir('../')

    def build_dir(self):
        '''
        Makes the tag directory with links for each tagged post.
        '''
        if self._taglist == []:
            raise OSError("your tag list is empty. Please run detect_tags()")

        # suck template data into this variable. ALWAYS copy from now on
        raw_content = ''
        with open(settings.TEMPLATE, 'r') as template:
            raw_content = template.read()

        # Nuke the directory of /tags/ if it exists, rebuild anew.
        os.chdir(settings.BLOG)
        if os.path.isdir("tags/"):
            print("Directory /tags/ exists. Rebuilding...")
            res = os.system("rm -rf tags/")
            if res != 0:
                raise OSError("could not delete tags directory.")
            else:
                os.mkdir("tags/")
        else:
            print("Building directory /tags/...")
            os.mkdir("tags/")
        os.chdir('..')

        for tag in self._taglist:
            # Begin work:
            # TODO: a way to remove everything before creating
            tagdir = settings.BLOG + 'tags/' + tag
            os.mkdir(tagdir)
            os.chdir(tagdir)

            postlist = []
            for item in self.tagrelation:
                if tag in item[1]:
                    postlist.append((item[0], item[2]))

            pagetitle = "Posts tagged '%s'" % tag
            filler = """# All posts tagged with '%s':
""" % tag
            for post in postlist:
                filler += """
 - [%s](/%s)
""" % (post[1], BLOG + post[0])

            filler += '''
[Back to all tags](../)
'''

            cont = markdown(filler)
            with open('index.html', 'w') as index:
                index.write(raw_content % 
                    (pagetitle, cont))
            print("***Built directory under tag '%s'" % tag)
            os.chdir('../../../')
            # tag pages are now built.

        # Now build the "tag index" under /blog/tags
        os.chdir(BLOG + '/tags/')
        pagetitle = "All content tags"
        filler = """# Conteúdo por tags

Atualmente, todos os nossos posts estão distrubuídos nas seguintes *tags*:

"""
        for directory in os.listdir('.'):
            filler += """ - [%s](/%s)
""" % (directory, BLOG + '/tags/' + directory)
        
        cont = markdown(filler)
        with open('index.html', 'w') as index:
            index.write(raw_content % 
                (pagetitle, cont))

        print("***Built tag index page.")
        os.chdir('../../')
