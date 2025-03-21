<h1>Server_3_free_threads</h1>

<p>The WSGI server is based on threads, <br>
which began with experiments on sockets.</p>

><h3 style="color: red;">Important!</h3>
><p>It is supported only on Linux 2.5.44 and later</p>

<ol>the server uses four threads:
    <li><b>accepting_connections</b>, to accept connections</li>
    <li><b>reading_from_socket</b>, to read data from a client socket</li>
    <li><b>sending_to_socket</b>, to send data to a socket</li>
    <li><b>close_client_sock</b>, to close client sockets</li>
</ol>

><h3 style="color: yellow;">Note</h3>
><p>It is recommended to use a python 3.13 or later<br>
>build from the source code, with the GIL disabled,<br> 
>to improve performance.</p>



