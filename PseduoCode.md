Get url from client input
Get port, hostname and path from url
Connect to the server with (port and hostname from url)
Get request method from user input
    * file already takes care of it -> "GET" / "POST"
Make a message
    message = f'{method} {path} HTTP/1.0\r\nHost: {hostname}\r\n\r\n' # {} for var subs
            * Scheme! 
            * hostname: www.example.com
            * method: GET
            * path: /car
            = f'GET /car HTTP/1.0\r\nHost: www.example.com\r\n\r\n'
Send a client message(request) to the webserver
Make a response based on sent request from webserver
    data = recvall()
    * variable data stores webserver response
data = "Status Line\r\nHeaders\r\n\r\nBody(content)" 
    * ex. data = "HTTP/1.1 200 OK\r\nDate: Wed, 08 Feb 2023 17:12:56 GMT\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: 13\r\nServer: ECS (sec/9739)\r\n\r\nHello, world!" 
Get the response code from data in a variable response_code = int
Get headers from data in a variable headers = str
    TODO: ? headers-> str or dict? 
Get body(content) from data in a variable body_content = str
Make a HTTPResponse object with response code and body(content) -> response_obj = HTTPResponse(response_code, body_content)
return HTTPResponse object 
print the response code from the HTTPResponse object -> print(http_response.code) 
print the body(content) from the HTTPResponse object -> print(http_response.body) 

Notes:
payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n' -> complete http request 
url = http://www.google.com/foobar
hostname = 'www.google.com'
Code in Python 3.8.10
You should use the socket library that comes with python

TODOs:
- The httpclient can pass all the tests in freetests.py? 
- HTTP POST can post args? POST(args = None)
- HTTP POST handles at least Content-Type: application/x-www-form-urlencoded
    Haven't specified the Content-Type yet
    What is Content-Type?
    What is application/x-www-form-urlencoded? 
- httpclient can handle 404 requests and 200 requests
    2xx code meaning?
    4xx code meaning?
    3xx code meaning?
    5xx code meaning?
    200 OK 
    404 Not Found

- License your httpclient properly (use an OSI approved license)
    Put your name on it!
- You cannot use a Web Client library except for urllib utils to convert strings to url-encode and query-string format and back
    urllib.request is BANNED
    urllib.parse is OKAY for parsing URLs
    you have to parse headers yourself

- In EClass for this assignment submit a URL to the git repository. I would prefer github for the host.
    Line 1: the git URL
    Line 2: Your CCID
    An example submission looks like this
        https://github.com/youruserid/thisassignment.git 
        yourccid

- To mark your assignment I should be able to type:
    git clone http://github.com/youruserid/thisassignment.git yourccid
    cd yourccid
    python3 freetests.py

