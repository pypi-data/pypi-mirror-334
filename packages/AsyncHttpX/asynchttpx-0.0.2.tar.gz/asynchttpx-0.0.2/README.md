# AsyncHttpX Library

**AsyncHttpX Library** is a high-performance, asynchronous HTTP client built on top of the powerful [httpx](https://www.python-httpx.org/) library. Designed for developers who need a robust and flexible way to make HTTP requests in Python, this library extends `httpx` with enhanced features such as request retries, connection pooling, automatic response parsing, and built-in support for common authentication mechanisms.

## Features

- **Asynchronous Support**: Built on top of the `httpx` library, making it fully asynchronous and optimized for high-performance applications.
- **Automatic Response Parsing**: Automatically parses JSON, XML, or other common response types.
- **Request Retries**: Configurable retries for failed requests, ensuring reliability in case of transient issues.
- **Connection Pooling**: Efficient management of HTTP connections to optimize performance.
- **Authentication Support**: Built-in support for basic authentication, bearer tokens, and other common mechanisms.
- **Customizable**: Easily extendable and customizable for your specific HTTP client needs.

## Installation

You can install the `AsyncHttpX` library using `pip`:

```bash
pip install AsyncHttpX

```