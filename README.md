# Open city profile

## Summary

Open city profile is used to store common information (name, contact information, areas of interests, ...) about the citizens of the city of Helsinki.

When a citizen is using a service which is connected to the profile, the service can query for the citizen's information from the profile so that the citizen doesn't have to enter all of their data every time it is needed. The services may also provide a better user experience using the profile's data, for example by returning more relevant search results based on the citizen's interests.

The same data may also be queried by the employees of the city of Helsinki while performing their daily duties, for example using the administrative functions of Venepaikka service.

Open city profile is implemented using Django and it provides a GraphQL API.

## Development with Docker

1. Create `.env` environment file

2. Set the `DEBUG` environment variable to `1`

3. Run `docker-compose up`

4. Run migrations if needed: 
    * `docker exec profile-backend python manage.py migrate`

5. Create superuser if needed: 
    * `docker exec -it profile-backend python manage.py createsuperuser`
    
6. Import relevant Helsinki regions if needed:

    * `docker exec profile-backend python manage.py geo_import finland --municipalities`
    * `docker exec profile-backend python manage.py geo_import helsinki --divisions`
    * `docker exec profile-backend python manage.py mark_divisions_of_interest`
  
7. Run the server:
    * `docker exec -it profile-backend python manage.py runserver 0:8000`


## Development without Docker

### Install pip-tools

* Run `pip install pip-tools`

### Creating Python requirements files

* Run `pip-compile requirements.in`
* Run `pip-compile requirements-dev.in`

### Updating Python requirements files

* Run `pip-compile --upgrade requirements.in`
* Run `pip-compile --upgrade requirements-dev.in`

### Installing Python requirements

* Run `pip-sync requirements.txt requirements-dev.in`

### Database

To setup a database compatible with default database settings:

Create user and database

    sudo -u postgres createuser -P -R -S open_city_profile  # use password `open_city_profile`
    sudo -u postgres createdb -O open_city_profile open_city_profile

Allow user to create test database

    sudo -u postgres psql -c "ALTER USER open_city_profile CREATEDB;"

### Import administrative divisions

In order to have the relevant Helsinki regions run the following commands:

* `python manage.py geo_import finland --municipalities`
* `python manage.py geo_import helsinki --divisions`
* `python manage.py mark_divisions_of_interest`


### Daily running

* Set the `DEBUG` environment variable to `1`.
* Run `python manage.py migrate`
* Run `python manage.py runserver 0:8000`

## Running tests

* Set the `DEBUG` environment variable to `1`.
* Run `pytest`.

## Issue tracking

* [Github issue list](https://github.com/City-of-Helsinki/open-city-profile/issues)
* [Jira backlog](https://helsinkisolutionoffice.atlassian.net/secure/RapidBoard.jspa?rapidView=23&projectKey=OM&view=planning)

## Builds

Currently no automated builds.

## Environments

Test environment: https://profile-api.test.hel.ninja/profile-test/graphql/

## API documentation

* [Generated GraphiQL documentation](https://profile-api.test.hel.ninja/profile-test/graphql/)

## Contributing

Make your changes and create a pull request. If your PR isn't getting approved, contact kuva-open-city-profile-developers@googlegroups.com.
