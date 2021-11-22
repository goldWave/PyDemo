from wsgiref.simple_server import make_server

def application(environ, start_response):
	start_response('201 Not found', [('Content-Type', 'text/html')])
	return [b'<h1>Hello, web!</h1>']

def demo_app(environ,start_response):
    from io import StringIO
    stdout = StringIO()
    print("Hello world!", file=stdout)
    print(file=stdout)
    h = sorted(environ.items())
    for k,v in h:
        # print(k,'=',repr(v), file=stdout)
        pass
    start_response("200 OK", [('Content-Type','text/plain; charset=utf-8')])
    return [stdout.getvalue().encode("utf-8")]

httpd = make_server('', 9999, demo_app)
print('start http: 9999')
httpd.serve_forever()