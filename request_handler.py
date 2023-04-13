import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_all_styles, get_all_orders, get_all_sizes, get_single_metal
from views import get_single_metal, get_single_style, get_single_order, get_single_size
from views import create_metal, create_order, create_size, create_style
from views import update_metal, update_order, update_size, update_style
from views import delete_metal, delete_order, delete_size, delete_style

# This is a class which inherits from another class.
# A class is like a container for functions that work together.
# That purpose is to respond to HTTP requests from a client.

class HandleRequests(BaseHTTPRequestHandler):
    '''handles fetch functions'''

    def parse_url(self, path):
        '''splitting string. If the path is "/metals/1", the resulting list will have "" at index 0, "metals" at index 1, and "1" at index 2.'''
        # Just like splitting a string in JavaScript. If the
        # path is "/metals/1", the resulting list will
        # have "" at index 0, "metals" at index 1, and "1"
        # at index 2.

        path_params = path.split('/')
        resource = path_params[1]
        id = None

        #Try to get the item at index 2
        try:
            #convert the string '1' to the integer 1 this is new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass #no route parameter exists: /metals
        except ValueError:
            pass
        return(resource, id)

    def do_GET(self):
        """Handles GET requests to the server """
        
        response = {} #default response empty dictionary

        #parsing url to capture tuple

        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)

                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {'message': 'That metal is out of stock'}

            else:
                self._set_headers(200)
                response = get_all_metals()

        if resource == "orders":
            if id is not None:
                response = get_single_order(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {'message': 'This order does not exist'}
            
            else:
                self._set_headers(200)
                response = get_all_orders()
        
        if resource == "sizes":
            if id is not None:
                response = get_single_size(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {'message': 'That size is impossible'}
            
            else:
                self._set_headers(200)
                response = get_all_sizes()
        
        if resource == "styles":
            if id is not None:
                response = get_single_style(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {'message': 'that style is not available'}
            
            else:
                response = get_all_styles()
        #this sends a json format string as a response
        self.wfile.write(json.dumps(response).encode())

        #method on class that overrides parent method handles posts

    def do_POST(self):
        """Handles POST requests to the server """

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        #convert json string to python dictionary
        post_body = json.loads(post_body)
        #parses the url
        (resource, id) = self.parse_url(self.path)
        #intialize new items

        
        new_style = None
        new_resource = None


        if resource == 'orders':
            if 'timestamp' in post_body:
                self._set_headers(201)
                new_resource = create_order(post_body)
            else: 
                self._set_headers(400)
                new_resource = {'message': f'{"please add a time" if "timestamp" not in post_body else ""}'}

            
            self.wfile.write(json.dumps(new_resource).encode())

        
        if resource == 'metals':
            if 'metal' in post_body and 'price' in post_body:
                self._set_headers(201)
                new_resource = create_metal(post_body)
           
            else:
                self._set_headers(400)
                new_resource = {
                'message': f'{"please enter a metal" if "metal" not in post_body else ""}{"please enter a price" if "price" not in post_body else ""}'
            }
                self.wfile.write(json.dumps(new_resource).encode())

        
        if resource == 'sizes':
            if 'carets' in post_body and 'price' in post_body:
                self._set_headers(201)
                new_resource = create_size(post_body)
            
            else:
                self._set_headers(400)
                new_resource = {
                    'message': f'{"please enter carets" if "carets" not in post_body else ""}{"please enter a price" if "price" not in post_body else ""}'
                }
            
            self.wfile.write(json.dumps(new_resource).encode())

        new_style = None
        if resource == 'styles':
            if 'style' in post_body and 'price' in post_body:
                self._set_headers(201)
                new_resource = create_style(post_body)
            else:
                self._set_headers(400)
                new_resource = {
                    'message': f'{"please enter style" if "style" not in post_body else ""}{"please enter a price" if "price" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_resource).encode())
        

    def do_PUT(self):
        """Handles PUT requests to the server """
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == 'orders':
            update_order(id, post_body)
        self.wfile.write(''.encode())

        if resource == 'metals':
            update_metal(id, post_body)
        self.wfile.write(''.encode())

        if resource == 'sizes':
            update_size(id, post_body)
        self.wfile.write(''.encode())

        if resource == 'styles':
            update_style(id, post_body)
        self.wfile.write(''.encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == 'orders':
            delete_order(id)
        self.wfile.write(''.encode())

        if resource == 'metals':
            delete_metal(id)
        self.wfile.write(''.encode())

        if resource == 'sizes':
            delete_size(id)
        self.wfile.write(''.encode())

        if resource == 'styles':
            delete_style(id)
        self.wfile.write(''.encode())




# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
