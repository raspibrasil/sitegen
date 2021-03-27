#
# Publishing tools to build a page or blog post.
#

import os
import sys
import datetime

from sitegen import settings

try:
    from markdown import markdown
except ImportError:
    print("[ERROR] Module 'markdown' not found. Please install it via pip with:")
    print("    pip install markdown")
    sys.exit(1)

class Publisher:
    def __init__(self, article=False, draft=False):
        self.article = article
        self.draft = draft
        self.startdir = os.path.realpath('.')

        # Carry your own copy of the TEMPLATE_FIELDS variable
        self.fields = settings.TEMPLATE_FIELDS
        try:
            with open(settings.TEMPLATE, 'r') as tmpl:
                self.template_contents = tmpl.read()
        except FileNotFoundError:
            print("[ERROR] Could not open template file '%s'" % settings.TEMPLATE)
            print("Please correct its location in the settings")
            sys.exit(1)


    def publish(self, page):
        # change to directory of the page to publish:
        os.chdir('/'.join(os.path.realpath(page).split('/')[:-1]))
        
        try:
            with open('index.md', 'r') as index:
                raw_content = index.read()

        except FileNotFoundError:
            print("[ERROR] Could not open 'index.md'")
            print("Please make sure the file exists to publish it.")
            sys.exit(1)

        # For the page title, either read from a file named 'title' or get the
        # first line of the post:
        try:
            with open('title', 'r') as title:
                pagetitle = title.read()
        except FileNotFoundError:
            pagetitle = raw_content.split('\n')[0][2:]
            print("[INFO] No title file given. Using your first line: %s" % pagetitle)
        self.fields['title'] = pagetitle

        # Same for the meta description tag. If there's a file, read it:
        try:
            with open('description', 'r') as desc:
                description = desc.read()
        except FileNotFoundError:
            description = pagetitle

        self.fields['description'] = description

        # For categories, default to uncategorized:
        try:
            with open('categories', 'r') as catfile:
                cats = catfile.read()
                categories = cats.split('\n')
                categories.pop()

        except FileNotFoundError:
            print("[INFO] No categories file found for %s. Defaulting to 'uncategorized'" % page)
            categories = ['uncategorized']

        # For date, if not specified, default to today, and write it as such:
        try:
            with open('pubdate', 'r') as pd:
                pubdate = pd.read()
        except FileNotFoundError:
            print("[INFO] No pubdate specified. Assuming it's 'today'")
            pubdate = datetime.datetime.now().strftime("%Y-%m-%d")
            with open('pubdate', 'w') as pd:
                pd.write(pubdate)

        # Obtaining the golden "canonical link:"
        pathraw = page.split('/')
        pathraw.reverse()
        pathraw.pop() # get rid of the publish directory page 
        pathraw.reverse()

        path = "/".join(pathraw[:-1])
        self.fields['canonical'] = settings.DOMAIN + path

        # Write to the template:
        if self.article:
            raw_content += '''
Published on %s

Filed under: ''' % pubdate

            for cat in categories:
                raw_content += "[%s](/blog/tags/%s)" % (cat, cat)

        self.fields['content'] = markdown(raw_content)
        
        # This looks more organized!
        final = self.template_contents.format(**self.fields)
        if settings.DEBUG:
            print("[DEBUG] Printing the contents of the page:")
            print(final)

        with open('index.html', 'w') as index:
            index.write(final)
        print("*** Page published")
        os.chdir(self.startdir)

