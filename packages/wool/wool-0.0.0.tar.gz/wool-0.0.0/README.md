# WorkerPool

WorkerPool is a native Python package for transparently executing tasks in a horizontally scalable, distributed network of agnostic worker processes. Any picklable async function or method can be converted into a task with a simple decorator and a client connection.

## Installation

### Using pip

To install the package using pip, run the following command:

```sh
pip install git+https://github.com/conradbzura/workerpool.git
```

### Cloning from GitHub

To install the package by cloning from GitHub, run the following commands:

```sh
git clone https://github.com/yourusername/workerpool.git
cd workerpool
pip install .
```

## Usage

### CLI Commands

WorkerPool provides a command-line interface (CLI) for managing the worker pool.

To list the available commands:

```sh
workerpool --help
```

#### Start the Worker Pool

To start the worker pool, use the `up` command:

```sh
workerpool up --host <host> --port <port> --authkey <authkey> --breadth <breadth> --depth <depth> --max-size <max_size> --max-idle <max_idle> --module <module>
```

- `--host`: The host address (default: `localhost`).
- `--port`: The port number (default: `0`).
- `--authkey`: The authentication key (default: `b""`).
- `--breadth`: The number of worker processes (default: number of CPU cores).
- `--depth`: The depth of the worker pool (default: `1`).
- `--max-size`: The maximum work queue size (optional).
- `--max-idle`: The maximum idle time before shutting down (optional).
- `--module`: Python module containing workerpool task definitions to be executed by this pool (optional, can be specified multiple times).

#### Stop the Worker Pool

To stop the worker pool, use the `down` command:

```sh
workerpool down --host <host> --port <port> --authkey <authkey>
```

- `--host`: The host address (default: `localhost`).
- `--port`: The port number (required).
- `--authkey`: The authentication key (default: `b""`).

#### Ping the Worker Pool

To ping the worker pool, use the `ping` command:

```sh
workerpool ping --host <host> --port <port> --authkey <authkey>
```

- `--host`: The host address (default: `localhost`).
- `--port`: The port number (required).
- `--authkey`: The authentication key (default: `b""`).

#### Retry a Task

To retry a task, use the `retry_task` command:

```sh
workerpool retry_task --host <host> --port <port> --authkey <authkey> <task-ref>
```

- `--host`: The host address (default: `localhost`).
- `--port`: The port number (optional).
- `--authkey`: The authentication key (default: `b""`).
- `<task-ref>`: The reference ID of the task to retry.

### Sample Python Application

Below is an example of how to create a WorkerPool client connection, decorate an async function using the `remote` decorator, and execute the function remotely:

Module defining remote tasks:
`tasks.py`
```python
import asyncio
from workerpool import remote, WorkerPool


# Create a WorkerPool client connection
def get_client():
    client = WorkerPool.Client(
        address=("localhost", 5000), authkey=b"deadbeef"
    )
    client.connect()
    return client


# Decorate an async function using the `remote` decorator
@remote(get_client)
async def sample_task(x, y):
    await asyncio.sleep(1)
    return x + y
```

Module executing remote workflow:
`main.py`
```python
import asyncio
from tasks import sample_task


# Execute the decorated function
async def main():
    result = await sample_task(1, 2)
    print(f"Result: {result}")


asyncio.new_event_loop().run_until_complete(main())
```
To run the demo, first start a worker pool specifying the module defining the tasks to be executed:
```bash
cd demo
export PYTHONPATH=$PYTHONPATH:$PWD
workerpool -vvvv up -p 5000 -a deadbeef -b 1 -m tasks
```
Next, in a separate terminal, execute the application defined in main.py and, finally, stop the worker pool:
```bash
python main.py
workerpool down -p 5000 -a deadbeef
```

## License

This project is licensed under the Apache License Version 2.0.
