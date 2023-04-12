import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_all_styles, get_all_orders, get_all_sizes, get_single_metal
from views import get_single_metal, get_single_style, get_single_order, get_single_size
from views import create_metal, create_order, create_size, create_style
from views import update_metal, update_order, update_size, update_style
from views import delete_metal, delete_order, delete_size, delete_style


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """parses"""
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
        
        response = {} #default response

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
            
            else:
                response = get_all_orders()
        
        if resource == "sizes":
            if id is not None:
                response = get_single_size(id)
            
            else:
                response = get_all_sizes()
        
        if resource == "styles":
            if id is not None:
                response = get_single_style(id)
            
            else:
                response = get_all_styles()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
        
        new_order = None
        if resource == 'orders':
            new_order = create_order(post_body)
        self.wfile.write(json.dumps(new_order).encode())

        new_metal = None
        if resource == 'metals':
            new_metal = create_metal(post_body)
        self.wfile.write(json.dumps(new_metal).encode())

        new_size = None
        if resource == 'sizes':
            new_size = create_size(post_body)
        self.wfile.write(json.dumps(new_size).encode())

        new_style = None
        if resource == 'styles':
            new_style = create_style(post_body)
        self.wfile.write(json.dumps(new_style).encode())
        

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
