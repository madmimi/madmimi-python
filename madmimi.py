# Released into the Public Domain by tav <tav@espians.com>

"""MadMimi API Client."""

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from urllib import quote, urlencode
from urllib2 import urlopen

try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    try:
        import cElementTree as ElementTree
    except ImportError:
        try:
            from xml.etree import ElementTree
        except ImportError:
            from elementtree import ElementTree

# ------------------------------------------------------------------------------
# A Client For The MadMimi API
# ------------------------------------------------------------------------------

DEFAULT_CONTACT_FIELDS = '"first name","last name","email","tags"'

class MadMimi(object):
    """
    The client is straightforward to use:

      >>> mimi = MadMimi('user@foo.com', 'account-api-key')

    You can use it to list existing lists:

      >>> mimi.lists()
      <lists>
        <list subscriber_count="712" name="espians" id="24245"/>
        <list subscriber_count="16" name="family" id="76743"/>
        <list subscriber_count="0" name="test" id="22103"/>
      </lists>

    Delete any of them:

      >>> mimi.delete_list('test')

    Create new ones:

      >>> mimi.add_list('ampify')

    Add new contacts:

      >>> mimi.add_contact(['Tav', 'Espian', 'tav@espians.com'])

    Subscribe contacts to a list:

      >>> mimi.subscribe('tav@espians.com', 'ampify')

    See what lists a contact is subscribed to:

      >>> mimi.subscriptions('tav@espians.com')
      <lists>
        <list subscriber_count="1" name="ampify" id="77461"/>
      </lists>

    And, of course, unsubscribe a contact from a list:

      >>> mimi.unsubscribe('tav@espians.com', 'ampify')

      >>> mimi.subscriptions('tav@espians.com')
      <lists>
      </lists>

    """

    base_url = 'http://madmimi.com/'

    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key

    def get(self, method, **params):
        params['username'] = self.username
        params['api_key'] = self.api_key
        url = self.base_url + method + '?' + urlencode(params)
        return urlopen(url).read()

    def post(self, method, **params):
        url = self.base_url + method
        params['username'] = self.username
        params['api_key'] = self.api_key
        return urlopen(url, urlencode(params)).read()

    def lists(self, as_xml=True):
        response = self.get('audience_lists/lists.xml')
        if as_xml:
            return response
        tree, lists = ElementTree.ElementTree(), {}
        tree.parse(StringIO(response))
        for elem in list(tree.getiterator('list')):
            lists[elem.attrib['name']] = elem.attrib['id']
        return lists

    def add_list(self, name):
        return self.post('audience_lists', name=name)

    def delete_list(self, name):
        return self.post('audience_lists/%s' % quote(name), _method='delete')

    def add_contacts(self, contacts_data, fields=DEFAULT_CONTACT_FIELDS):
        output = [fields]
        out = output.append
        for contact in contacts_data:
            line = []
            contact = contact + ['contactmanager']
            for field in contact:
                if '"' in field:
                    field = field.replace('"', '""')
                line.append('"%s"' % field)
            out(','.join(line))
        csv = '\n'.join(output)
        return self.post('audience_members', csv_file=csv)

    def add_contact(self, contact_data, fields=DEFAULT_CONTACT_FIELDS):
        return self.add_contacts([contact_data], fields)

    def subscribe(self, email, list):
        return self.post('audience_lists/%s/add' % quote(list), email=email)

    def unsubscribe(self, email, list):
        return self.post('audience_lists/%s/remove' % quote(list), email=email)

    def subscriptions(self, email):
        return self.get('audience_members/%s/lists.xml' % quote(email))

    # Unfortunately, accessing a CSV export of the list membership only works
    # through the web interface and doesn't work over the API, so you can't find
    # out who the subscribers for a given list are.
    def subscribers(self, list=None, list_id=None):
        if not list_id:
            list_id = self.lists(as_xml=False)[list]
        return self.get('exports/audience/%s.csv' % list_id)
