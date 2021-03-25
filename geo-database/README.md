# Geo DataBase Class Notes

## Creation of the PostgreSQL docker container

```
## Download the official repository
$ docker pull mdillon/postgis

## Container execution with a Postgresql instance
$ docker run --name postgresql -p 5480:5432 -e POSTGRES_PASSWORD=postgres -d mdillon/postgis
```

## Container docker database

> Creation of the PGAdmin4 docker container (Graphical User Interface):

```
## Download the official repository
$ docker pull dpage/pgadmin4

## Container execution with a PGAdmin instance
$ docker run --name pgadmin4 -p 16543:80 -e PGADMIN_DEFAULT_EMAIL,PGADMIN_DEFAULT_PASSWORD=abner.anjos@fatec.sp.gov.br,postgres -d dpage/pgadmin4
```

> Creation of the PostgreSQL and PGAdmin4 (Graphical User Interface) docker container by default with Docker Compose:

```
$ docker-compose up -d postgresql pgadmin4
```

**Obs.:** You will need to install the tool (docker-compose)[https://docs.docker.com/compose/] and don't forget to register the PostgreSQL database server to use the PGAdmin4 graphical interface with the necessary credentials.
