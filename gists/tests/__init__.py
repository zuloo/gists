# Copyright (c) 2012 <Jaume Devesa (jaumedevesa@gmail.com)>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from gists.utils import GithubFacade
import os
import json


class MockFacade(GithubFacade):

    def __init__(self, username, credential):
        super(MockFacade, self).__init__(username, credential)
        current_dir = os.path.abspath(os.path.split(__file__)[0])
        self.fixtures_dir = os.path.join(current_dir, 'fixtures')

    def request_list_of_gists(self, username):
        pass

    def request_list_starred_gists(self, username):
        pass

    def request_gist(self, id_gist):
        return True, self._load('request_gist_' + id_gist + '.gist')

    def create_gist(self, payload):
        pass

    def update_gist(self, payload):
        pass

    def delete_gist(self, id_gist):
        pass

    def list_authorizations(self):
        pass

    def fork_gist(self, gist_id):
        pass

    def star_gist(self, gist_id):
        pass

    def unstar_gist(self, gist_id):
        pass

    def authorize(self, payload):
        pass

    def _load(self, filename):
        path = os.path.join(self.fixtures_dir, filename)
        with open(path, 'r') as f:
            data = f.read()
        return json.loads(data)
