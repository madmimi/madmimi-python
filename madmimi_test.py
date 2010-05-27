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

"""Test suite for PyMadMimi.

    These tests run against a mock object. It is possible that these tests
will pass and interaction with Mad Mimi will still fail if they change their
API.
"""

__author__ = 'jordan.bouvier@analytemedia.com (Jordan Bouvier)'

from mock import Mock
from nose.tools import with_setup
from nose import tools
import datetime
import unittest
from urllib import urlencode
from urllib import quote
from urlparse import urlparse
import yaml

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

import madmimi



class MadMimiTest(unittest.TestCase):
    
    def setUp(self):
        """Setup fixture."""
        
        # Test Values
        self.email = 'test@test.com'
        self.api_key = '23890889df8909fs09s09'
        self.promotion = 'Test Promotion'
        self.recipient = 'john@doe.com'
        self.recipient_name = 'John Doe'
        self.subject = 'Test Mailing'
        self.sender = 'mimiuser@doe.com'
        self.audience_lists = [(1, 'Dinosaur', '71056')]
        self.list_name = 'PyMadMimi Test List'
        self.body = {'abc': 123}
        self.expected_args = {
            'username': self.email,
            'api_key': self.api_key
        }
        
        self.mimi = madmimi.MadMimi(self.email, self.api_key)
        self.mimi.urlopen = Mock()
        
    
    def test_lists(self):
        """Test that expected url is fetched for getting a list."""
        
        self.mimi.urlopen.return_value = generate_lists(self.audience_lists)
        lists = self.mimi.lists()
        
        args = urlencode({'username': self.email, 'api_key': self.api_key})
        expected_url = ('%saudience_lists/lists.xml?%s'
                % (self.mimi.base_url, args))
        self.mimi.urlopen.assert_called_with(expected_url)
    
    def test_lists_dict(self):
        """Test that lists are properly parsed into a dictionary."""
        
        self.mimi.urlopen.return_value = generate_lists(self.audience_lists)
        lists = self.mimi.lists(as_xml=False)
        self.assertEqual(type(lists), dict)
    
    def test_add_list(self):
        """Test that an add list request is properly formatted."""
        
        self.mimi.add_list(self.list_name)
        expected_url = '%saudience_lists' % self.mimi.base_url
        self.expected_args['name'] = self.list_name
        expected_args = urlencode(self.expected_args)
        self.mimi.urlopen.assert_called_with(expected_url, expected_args)
    
    def test_delete_list(self):
        """Test that a delete list request is properly formatted."""
        
        self.mimi.delete_list(self.list_name)
        expected_url = '%saudience_lists/%s' % (
                self.mimi.base_url, quote(self.list_name))
        self.expected_args['_method'] = 'delete'
        expected_args = urlencode(self.expected_args)
        self.mimi.urlopen.assert_called_with(expected_url, expected_args)
    
    def test_add_contacts(self):
        """Test that adding contacts results in a properly formatted post."""
        
        contact_fields = [('first_name', 'last_name', 'email')]
        contacts_data = [('John', 'Doe', 'john@doe.com'),
                ('Jane', 'Doe', 'jane@doe.com')]
        self.mimi.add_contacts(contacts_data, fields=contact_fields)
        
        expected_url = '%saudience_members' % self.mimi.base_url
        expected_csv = ('"(\'first_name\', \'last_name\', \'email\')"\r\nJohn'
                ',Doe,john@doe.com\r\nJane,Doe,jane@doe.com\r\n')
        
        called_url = self.mimi.urlopen.call_args[0][0]
        called_args = parse_qs(urlparse(self.mimi.urlopen.call_args[0][1])[2])
        called_username = called_args['username'][0]
        called_api_key = called_args['api_key'][0]
        called_csv_file = called_args['csv_file'][0]
        
        self.assertEqual(expected_url, called_url)
        self.assertEqual(called_username, self.email)
        self.assertEqual(called_api_key, self.api_key)
        self.assertEqual(called_csv_file, expected_csv)
    
    def test_subscribe(self):
        """Test that subscribe results in a properly formatted post."""
        
        response = self.mimi.subscribe(self.recipient, self.list_name)
        expected_url = '%saudience_lists/%s/add' % (
                self.mimi.base_url, quote(self.list_name))
        self.expected_args['email'] = self.recipient
        expected_args = urlencode(self.expected_args)
        
        self.mimi.urlopen.assert_called_with(expected_url, expected_args)
    
    def test_unsubscribe(self):
        """Test that unsubscribe results in a properly formatted post."""
        
        self.mimi.unsubscribe(self.recipient, self.list_name)
        expected_url = '%saudience_lists/%s/remove' % (
                self.mimi.base_url, quote(self.list_name))
        self.expected_args['email'] = self.recipient
        expected_args = urlencode(self.expected_args)
        self.mimi.urlopen.assert_called_with(expected_url, expected_args)
    
    def test_subscriptions(self):
        """Test that subscriptions results in a properly formatted url."""
        
        expected_response = ('<lists>\n  <list subscriber_count='
                '"0" name="Test List" id="94522"/>\n</lists>\n')
        self.mimi.urlopen.return_value = StringIO()
        self.mimi.urlopen.return_value.write(expected_response)
        self.mimi.urlopen.return_value.seek(0)
        
        response = self.mimi.subscriptions(self.recipient)
        expected_args = urlencode(self.expected_args)
        expected_url = '%saudience_members/%s/lists.xml?%s' % (
                self.mimi.base_url, quote(self.recipient), expected_args)
        
        self.assertEqual(expected_response, response)
        self.mimi.urlopen.assert_called_with(expected_url)
    
    def test_send_message(self):
        """Test that send_message results in a properly formatted post."""
        
        expected_response = '12341234'
        self.mimi.urlopen.return_value = StringIO()
        self.mimi.urlopen.return_value.write(expected_response)
        self.mimi.urlopen.return_value.seek(0)
        
        response = self.mimi.send_message(self.recipient_name, self.recipient,
                self.promotion, self.subject, self.sender,
                body=self.body)
        
        expected_url = '%smailer' % self.mimi.secure_base_url
        expected_recipients = '%s <%s>' % (
                self.recipient_name, self.recipient)
        
        called_url = self.mimi.urlopen.call_args[0][0]
        called_args = parse_qs(urlparse(self.mimi.urlopen.call_args[0][1])[2])
        called_username = called_args['username'][0]
        called_api_key = called_args['api_key'][0]
        called_body = called_args['body'][0]
        called_promotion = called_args['promotion_name'][0]
        called_subject = called_args['subject'][0]
        called_sender = called_args['sender'][0]
        called_recipients = called_args['recipients'][0]
        
        self.assertEqual(expected_response, response)
        self.assertEqual(expected_url, called_url)
        self.assertEqual(self.email, called_username)
        self.assertEqual(self.api_key, called_api_key)
        self.assertEqual(self.body, yaml.load(called_body))
        self.assertEqual(self.promotion, called_promotion)
        self.assertEqual(self.subject, called_subject)
        self.assertEqual(self.sender, called_sender)
        self.assertEqual(expected_recipients, called_recipients)
    
    def test_send_message_to_list(self):
        """Test that send_message_to_list results in proper post."""
        
        expected_response = '12341234'
        self.mimi.urlopen.return_value = StringIO()
        self.mimi.urlopen.return_value.write(expected_response)
        self.mimi.urlopen.return_value.seek(0)
        
        response = self.mimi.send_message_to_list(self.list_name, self.promotion,
                self.body)
        
        expected_url = '%smailer/to_list' % self.mimi.secure_base_url
        
        called_url = self.mimi.urlopen.call_args[0][0]
        called_args = parse_qs(urlparse(self.mimi.urlopen.call_args[0][1])[2])
        called_username = called_args['username'][0]
        called_api_key = called_args['api_key'][0]
        called_body = called_args['body'][0]
        called_promotion = called_args['promotion_name'][0]
        called_list_name = called_args['list_name'][0]
        
        self.assertEqual(expected_response, response)
        self.assertEqual(expected_url, called_url)
        self.assertEqual(self.email, called_username)
        self.assertEqual(self.api_key, called_api_key)
        self.assertEqual(self.body, yaml.load(called_body))
        self.assertEqual(self.promotion, called_promotion)
        self.assertEqual(self.list_name, called_list_name)
    
    def test_message_status(self):
        """Test that message_status results in a proper url."""
        
        transaction_id = 1234567
        expected_response = 'sending'
        self.mimi.urlopen.return_value = StringIO()
        self.mimi.urlopen.return_value.write(expected_response)
        self.mimi.urlopen.return_value.seek(0)
        
        response = self.mimi.message_status(transaction_id)
        
        self.expected_args['is_secure'] = True
        args = urlencode(self.expected_args)
        expected_url = '%smailers/status/%s?%s' % (self.mimi.secure_base_url,
                transaction_id, args)
        
        self.assertEqual(expected_response, response)
        self.mimi.urlopen.assert_called_with(expected_url)
    
    def test_supressed_since(self):
        """Test that supressed_since results in a proper url."""
        
        date = datetime.datetime.now()
        self.mimi.supressed_since(date)
        
        expected_url = '%saudience_members/suppressed_since/%s.txt?%s' % (
                self.mimi.base_url, date.strftime('%s'),
                urlencode(self.expected_args))
        self.mimi.urlopen.assert_called_with(expected_url)
    
    def test_promotion_stats(self):
        """Test that promotion_stats results in a proper url."""
        
        self.mimi.promotion_stats()
        
        expected_url = '%spromotions.xml?%s' % (self.mimi.base_url,
                urlencode(self.expected_args))
        self.mimi.urlopen.assert_called_with(expected_url)
    

def generate_lists(audience_lists):
    """Helper for returning dynamic lists."""
    lists = ['<lists>\n']
    for audience_list in audience_lists:
        lists.append('<list subscriber_count="%s" name="%s" id="%s"/>\n'
                % (audience_list[0], audience_list[1], audience_list[2]))
    
    lists.append('</lists>\n')
    
    response = StringIO()
    response.write(''.join(lists))
    response.seek(0)
    
    return response

