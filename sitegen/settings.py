# Core settings of sitegen

import os

# Should debug messages be printed to stdout?
DEBUG = True

# Absolute path to the template file.
TEMPLATE = '/home/vman/Programs/web/sitegen/template.html'

# -- Site structure -- #

# Path to where the site should be published (put in production):
PUBDIR = '/home/vman/Programs/web/sitegen/testsite/'

# "Static" pages of the site (i.e. root pages)
# Add them as tuples in the format of ("page title", "URL"):
SITE_PAGES = [
    ('About this site', 'about'),
    ('Get in touch', 'contact'),
    ('Privacy Policy', 'privacy'),
]

# What's the name of the "blog" subfolder of the site?
# This will be appended to PUBDIR
BLOG_SUBDIR = 'blog/'
BLOG = PUBDIR + BLOG_SUBDIR

# -- /Site structure -- #
