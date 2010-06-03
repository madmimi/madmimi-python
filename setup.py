#!/usr/bin/env python
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""MadMimi setup script."""

__author__ = 'jordan.bouvier@analytemedia.com (Jordan Bouvier)'
__maintainer__ = 'jordan.bouvier@analytemedia.com (Jordan Bouvier)'

from distutils.core import setup



setup(
    name='MadMimi',
    version='1.0',
    author='tav',
    author_email='tav@espians.com',
    maintainer='Jordan Bouvier',
    maintainer_email='jordan.bouvier@analytemedia.com',
    url='http://developer.madmimi.com/',
    description='Python client for Mad Mimi',
    long_description='A simple python client for Mad Mimi.',
    classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Topic :: Communications :: Email',
            'Topic :: Communications :: Email :: Mailing List Servers',
            'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    py_modules=['madmimi', 'madmimi_test']
)