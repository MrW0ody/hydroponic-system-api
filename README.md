# Hydroponic System Management Application

This project aims to develop a simple CRUD application using Django, facilitating the management of hydroponic systems.
Below are the functional requirements and technical specifications:

##Functional Requirements:

### Hydroponic System Management Endpoint:

Allows users to create, read, update, and delete information about their hydroponic systems. Each hydroponic system is
associated with a user (owner). Data validation should adhere to Django REST Framework recommendations.

### Measurement Management Endpoint:

Enables the submission of sensor data (pH, water temperature, TDS) to existing hydroponic systems. Measurements should
be stored in the database.

### Information Retrieval for Systems and Measurements:

Users should be able to retrieve a list of their hydroponic systems. All data retrieval methods should support
filtering (time range, value range) and sorting options. Pagination should be implemented where necessary. Additionally,
users should have the option to fetch details of a specific system with information on the last 10 measurements.

### User Authentication Endpoint:

Incorporates user authorization and authentication.

# Installation

## Make directory for project and enter cd to this directory after clone project cd to project and create .env file example .env file:
        DB_HOST=db
        DB_PORT=5432
        DB_NAME=devname
        DB_USER=devusername
        DB_PASS=devpassword123

## After creation directory and .env file build image:

    docker-compose build


## After this create migrations to database:

    dokcer-compose up -d
    docker-compose app python manage.py migrate
    docker-compose app makemigrations
    docker-compose app python manage.py migrate

## To run tests:

    docker-compose app python manage.py test

## Go to address url:

    127.0.0.1:8000/docs/

## To create user go to address:

    127.0.0.1:8000/user/create

## After creating user create token to authorize user, go to address:

    127.0.0.1:8000//user/token

# Endpoints Hydroponic System API:


### /measurements/:

#### GET:
- **Description:** Retrieve a list of measurements based on specified parameters.
- **Parameters:**
  - `end_date_after` (Optional): Date after which the measurement must have an end date.
  - `end_date_before` (Optional): Date before which the measurement must have an end date.
  - `ordering` (Optional): Field to use for ordering the results.
  - `ph_max` (Optional): Maximum pH value.
  - `ph_min` (Optional): Minimum pH value.
  - `start_date_after` (Optional): Date after which the measurement must start.
  - `start_date_before` (Optional): Date before which the measurement must start.
  - `tds_max` (Optional): Maximum TDS value.
  - `tds_min` (Optional): Minimum TDS value.
  - `temperature_max` (Optional): Maximum temperature.
  - `temperature_min` (Optional): Minimum temperature.
- **Tags:** measurements
- **Security:** tokenAuth
- **Responses:**
  - `200`: List of measurements in JSON format.

#### POST:
- **Description:** Create a new measurement.
- **Tags:** measurements
- **Request Body:** Measurement object in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `201`: Measurement created successfully.

### /measurements/{id}/:

#### GET:
- **Description:** Retrieve details of a single measurement based on ID.
- **Path Parameters:**
  - `id`: Measurement ID.
- **Tags:** measurements
- **Security:** tokenAuth
- **Responses:**
  - `200`: Measurement details in JSON format.

#### PUT:
- **Description:** Update an existing measurement based on ID.
- **Path Parameters:**
  - `id`: Measurement ID.
- **Tags:** measurements
- **Request Body:** New measurement data in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `200`: Updated measurement details.

#### PATCH:
- **Description:** Partially update measurement data based on ID.
- **Path Parameters:**
  - `id`: Measurement ID.
- **Tags:** measurements
- **Request Body:** New partial measurement data in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `200`: Updated measurement details.

#### DELETE:
- **Description:** Delete a measurement based on ID.
- **Path Parameters:**
  - `id`: Measurement ID.
- **Tags:** measurements
- **Security:** tokenAuth
- **Responses:**
  - `204`: No response body.

### /schema/:

#### GET:
- **Description:** Retrieve OpenAPI3 schema for this API. Format can be selected via content negotiation.
- **Parameters:**
  - `format` (Optional): Format of the schema (json or yaml).
  - `lang` (Optional): Language for the schema.
- **Tags:** schema
- **Security:** cookieAuth, basicAuth, or none
- **Responses:**
  - `200`: OpenAPI3 schema in the requested format.

### /systems/:

#### GET:
- **Description:** Retrieve a list of hydroponic systems based on specified parameters.
- **Parameters:**
  - `created_max_after` (Optional): Date after which the system was created.
  - `created_max_before` (Optional): Date before which the system was created.
  - `created_min_after` (Optional): Date after which the system was created.
  - `created_min_before` (Optional): Date before which the system was created.
  - `location` (Optional): Location of the hydroponic system.
  - `ordering` (Optional): Field to use for ordering the results.
  - `updated_max_after` (Optional): Date after which the system was updated.
  - `updated_max_before` (Optional): Date before which the system was updated.
  - `updated_min_after` (Optional): Date after which the system was updated.
  - `updated_min_before` (Optional): Date before which the system was updated.
- **Tags:** systems
- **Security:** tokenAuth
- **Responses:**
  - `200`: List of hydroponic systems in JSON format.

#### POST:
- **Description:** Create a new hydroponic system.
- **Tags:** systems
- **Request Body:** Hydroponic system object in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `201`: Hydroponic system created successfully.

### /systems/{id}/:

#### GET:
- **Description:** Retrieve details of a single hydroponic system along with its latest 10 measurements based on ID.
- **Path Parameters:**
  - `id`: Hydroponic system ID.
- **Tags:** systems
- **Security:** tokenAuth
- **Responses:**
  - `200`: Hydroponic system details with measurements in JSON format.

#### PUT:
- **Description:** Update an existing hydroponic system based on ID.
- **Path Parameters:**
  - `id`: Hydroponic system ID.
- **Tags:** systems
- **Request Body:** New hydroponic system data in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `200`: Updated hydroponic system details.

#### PATCH:
- **Description:** Partially update hydroponic system data based on ID.
- **Path Parameters:**
  - `id`: Hydroponic system ID.
- **Tags:** systems
- **Request Body:** New partial hydroponic system data in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `200`: Updated hydroponic system details.

#### DELETE:
- **Description:** Delete a hydroponic system based on ID.
- **Path Parameters:**
  - `id`: Hydroponic system ID.
- **Tags:** systems
- **Security:** tokenAuth
- **Responses:**
  - `204`: No response body.

### /user/create/:

#### POST:
- **Description:** Create a new user.
- **Tags:** user
- **Request Body:** User object in JSON, URL-encoded form, or form data.
- **Security:** cookieAuth, basicAuth, or none
- **Responses:**
  - `201`: User created successfully.

### /user/me/:

#### GET:
- **Description:** Retrieve details of the authenticated user.
- **Tags:** user
- **Security:** tokenAuth
- **Responses:**
  - `200`: User details in JSON format.

#### PUT:
- **Description:** Update details of the authenticated user.
- **Tags:** user
- **Request Body:** New user data in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `200`: Updated user details.

#### PATCH:
- **Description:** Partially update details of the authenticated user.
- **Tags:** user
- **Request Body:** New partial user data in JSON, URL-encoded form, or form data.
- **Security:** tokenAuth
- **Responses:**
  - `200`: Updated user details.

### /user/token/:

#### POST:
- **Description:** Create a new auth token.
- **Tags:** user
- **Request Body:** Auth token object in URL-encoded form, multipart form data, or JSON.
- **Security:** cookieAuth, basicAuth, or none
- **Responses:**
  - `200`: New auth token created successfully.