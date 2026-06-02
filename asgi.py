from app import create_app
from asgiref.wsgi import WsgiToAsgi
import uvicorn
from app.core.config import Config

"""
ASGI Entrypoint wrapping the Flask application.

ARCHITECTURAL RATIONALE FOR ASGI CONVERSION:
Even though we implemented a 100% asynchronous backend stack (using native 'async def' views, 
async services, repositories, and the 'asyncpg' driver), standard Flask natively operates 
under the synchronous WSGI (Web Server Gateway Interface) standard.

THE CONCURRENCY PROBLEM (WSGI / Threading):
Traditional WSGI servers work like a bank with a fixed number of cashiers (thread pool). 
For example, if you have 5 cashiers (5 threads), the server can only process 5 requests at a time. 
The 6th incoming request is blocked and forced to wait in a queue until a thread becomes free. 
This thread-blocking model is highly inefficient under heavy database I/O, leading to resource 
starvation and poor concurrency scaling.

THE SOLUTION (ASGI / Event-Loop):
By wrapping our Flask instance in WsgiToAsgi (from the 'asgiref' package), we adapt the WSGI 
interface to a fully-compliant ASGI application. 

This allows us to run the application on an event-loop-driven ASGI server like Uvicorn. The 
server now works like a highly efficient restaurant waiter (Event Loop). It instantly accepts 
incoming requests, and when waiting for database I/O (which is fully async and non-blocking), 
it yields control to handle subsequent incoming requests instead of blocking a thread. This 
unlocks massive connection scaling, optimal resource utilization, and prevents thread pool 
exhaustion during heavy query execution.
"""

# 1. Instantiate the Flask application factory
flask_app = create_app()

# 2. Wrap WSGI application in high-performance ASGI layer
asgi_app = WsgiToAsgi(flask_app)

if __name__ == "__main__":
    # Run the ASGI app using uvicorn when executed directly
    uvicorn.run("asgi:asgi_app", host="0.0.0.0", port=Config.PORT, reload=Config.DEBUG)
