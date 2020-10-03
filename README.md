# todobackend-aiohttp

Yet another [todo backend](http://todobackend.com) written in Python 3.5 with aiohttp. Original code [from alec.thoughts import \*](http://justanr.github.io/getting-start-with-aiohttpweb-a-todo-tutorial).

## Usage

```
python3 aiotodo.py
```

## Tests

You can run validate the application with http://www.todobackend.com/specs/.

## Issue

One of the tests does not validate but the following commands would work (used with httpie ):
```
http POST http://localhost:8080/todos/ title="base todo"
http POST http://localhost:8080/tags/ title="associated tag"
http POST http://localhost:8080/todos/1/tags/ id=1
http POST http://localhost:8080/tags/ title="bloh"
http POST http://localhost:8080/todos/1/tags/ id=2
http DELETE http://localhost:8080/todos/1/tags/1
http GET http://localhost:8080/todos/1/tags/
```
Would then give out a list of tags with one entry.