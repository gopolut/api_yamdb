import http.client


def check_web_server(host, port, path):
    h = http.client.HTTPConnection(host, port)   
    h.request('GET', path)
    resp = h.getresponse()

    print('HTTP Response:')
    print('  status=', resp.status)
    print('  status=', resp.reason)
    print('HTTP Headers: ')

    for hdr in resp.getheaders():
        print('  %s: %s' % hdr)

    print('Lines in code:')
    for lines in resp.readlines():
        print('  ', lines)


host_info = {
    'host': '127.0.0.1',
    'port' : 8000,
    'path': '/polls/'
}


check_web_server(**host_info)
