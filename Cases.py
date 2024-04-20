import os

class base_case(object):
    '''Parent for case handlers'''

    Listing_Page = '''\
<html>
<body>
    <ul>
        {0}
    </ul>
    <p>TODO: file upload area</p>
</body>
</html>
'''

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def list_dir(self, handler, full_path):
        try:
            entries = os.listdir(full_path)
            if handler.path != "/":
                bullets = ['<li><a href="{0}/{1}">{1}</a></li>'.format(handler.path, e) for e in entries if not e.startswith('.')]
            else:
                bullets = ['<li><a href="{0}">{0}</a></li>'.format(e) for e in entries if not e.startswith('.')]

            page = self.Listing_Page.format('\n'.join(bullets)).encode("utf-8")
            handler.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
            handler.handle_error(msg)
        
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented.'
    
    def act(self, handler):
        assert False, 'Not implemented'

class case_no_file(base_case):
    '''File or directory does not exist'''

    def test(self, handler):
        return not os.path.exists(handler.full_path)
    
    def act(self, handler):
        raise Exception("'{0}' not found".format(handler.path)) # TODO: ServerException

class case_existing_file(base_case):
    '''File exists'''

    def test(self, handler):
        return os.path.isfile(handler.full_path)
    
    def act(self, handler):
        self.handle_file(handler, handler.full_path)

class case_directory(base_case):
    '''Serve listing for a directory'''
    
    def test(self, handler):
        return os.path.isdir(handler.full_path) and not os.path.isfile(self.index_path(handler))
    
    def act(self, handler):
        self.list_dir(handler, handler.full_path)

class case_always_fail(base_case):
    '''Base case if nothing else worked'''

    def test(self, handler):
        return True

    def act(self, handler):
        raise Exception("Unknown object '{0}'".format(handler.path)) # TODO: ServerException