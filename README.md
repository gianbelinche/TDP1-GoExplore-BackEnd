# ACP1-firenbn

Repositorio para el backend del proyecto GoExplore de la materia Taller de Desarrollo de Proyectos I en FIUBA.


## API

### Develop: http://localhost:{PORT}/api/
### Production: http:///api/

## Docker

You can easily get goexplore API up by running

```
docker build -t goexplore .
docker run -d --name goexplore-container -p 8080:8080 goexplore

```

## Virtual Env (Optional)

- Install virtualenv

- Create virtual env

```bash
virtualenv acp1 --python=python3
```

- Activate env

```bash
source acp1/bin/activate
```

- To deactivate run

```bash
deactivate
```


## Install

- Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

or

```bash
pip install poetry
```

- Check enviroment variables

- Install dependencies

```
poetry install
```


## Run the server

One commands is given in order to simplify server execution:

```bash
make start-server
```

* Will start a server.

Host and port on which the server will run can be specified by using two variables on  `start-server`:

```bash
make start-server PORT=4000 HOST=127.0.0.1
```

If not specified, port will be defaulted to 4000 and host to 0.0.0.0

