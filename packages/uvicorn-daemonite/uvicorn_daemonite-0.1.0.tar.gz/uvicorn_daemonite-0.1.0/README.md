# UVICORN Deamonite

Allows you to start/stop/restart ASGI/WSGI servers as daemons without needing
to know any commandline arguments or using screen. Add the following to your
flask/fastapi service.

```
if __name__ == "__main__":
  UvicornDaemonite(
    name="my_app",
    description="Does do canonic pythionic things.",
    port="6969",
    log_level="info").start()
```

**name** has to be the same as the name of your main file. The rest should be
self explanatory.

After adding und making your my_app.py executable type:

```
  ./my_app.py
```

for more info about parameters.

## Full FastAPI example

The following code has to be in a file **main.py**, the Daemonite name has
to be **main** in this case.

```
#!/usr/bin/python
from fastapi import FastAPI
from uvicorn_daemonite import Daemonite

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":                                                                     
  Daemonite(
    name="main",
    description="Does do canonic pythionic things.",
    port="6969",
    log_level="info").start()
```

## Future

I might add code so that info shows memory utilization.

## Warning

I know nothing about python, and I think its a pile of dung as a language. Has
some nice libraries though, so I have to make life bearable for myself. The
code in this lib might be very bad or unideomatic. Deal with it.

## License

LGPL 3.0 or later
