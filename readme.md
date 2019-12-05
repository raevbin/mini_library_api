# Mini Library

*author Evgeny Bobin*

This project is implemented as an API using the Django Rest Framework.

## SETTINGS
in the file pro/pro/settings.py


## Installation
> docker-compose build
> docker-compose up

After a successful launch, the service is available at http://localhost:8000/api-v1/


## DOCUMENTATION


OPTIONS /api-v1/books/

    Returns a description of types and supported formats

    responses:
      200: OK
				  {
					  "name": "Book List",
					  "description": "",
					  "renders": [
						  "application/json",
						  "text/html"
					  ],
					  "parses": [
						  "application/json",
						  "application/x-www-form-urlencoded",
						  "multipart/form-data"
					  ],
					  "actions": {
						  "POST": {
							  "url": {
								  "type": "field",
								  "required": false,
								  "read_only": true,
								  "label": "Url"
							  },
							  "id": {
								  "type": "integer",
								  "required": false,
								  "read_only": true,
								  "label": "ID"
							  },
							  "author": {
								  "type": "string",
								  "required": true,
								  "read_only": false,
								  "label": "Author",
								  "max_length": 100
							  },
							  "name": {
								  "type": "string",
								  "required": true,
								  "read_only": false,
								  "label": "Name",
								  "max_length": 200
							  },
							  "reader": {
								  "type": "field",
								  "required": false,
								  "read_only": false,
								  "label": "Reader"
							  },
							  "reader_name": {
								  "type": "field",
								  "required": false,
								  "read_only": true,
								  "label": "Reader name"
							  }
						  }
					  }
					}


GET /api-v1/books/   [?page={pageNum}&reader={readerID}]

    Returns a list of books

    parameters:
        query:
            page = <int> Page number. Optional parameter. Default number of items per page: 10
            reader = <int> readerID. Optional parameter

    responses:
			200: OK
				"application/json"

						{
							"count": <int>,
							"next": <url str>,
							"previous": <url str>,
							"results": [
								{
									"url":<str>,
									"id": <int>,
									"author": <str>,
									"name": <str>,
									"reader": <int>,
									"reader_name":<str>
								},
								...
							]
						}


POST /api-v1/books/

    Adding a book

    parameters:
        body:  ("application/x-www-form-urlencoded")
            author = <str> Required field
            name = <str> Book title. Required field
            reader = <int> reader ID. Optional parameter

    responses:
			200: OK
				"application/json"

					{
					  "url":<str>,
					  "id": <int>,
					  "author": <str>,
					  "name": <str>,
					  "reader": <int>,
					  "reader_name":<str>
					}

			400: Bad Request
				"application/json"

					{
						<nameField>: [
							"This field may not be blank."
						],
						.....
					}



GET /api-v1/books/{bookID}/

    Detailing a copy of a book

    parameters:
			path:
				bookID: <int> Required parametr

    responses:
			200: by analogy with POST /api-v1/books/

			404: Not Found
				"application/json"

				{
					"detail": "Not found."
				}




DELETE   /api-v1/books/{bookID}/

    Delete existing record

    parameters:
			path:
				bookID: <int> Required parametr

    responses:
			204: No Content  (Record deleted successfully)

			404: by analogy with GET /api-v1/books/{bookID}/




PUT /api-v1/books/{bookID}/

    Updating an existing record

    parameters:
			path:
				bookID: <int> Required parametr

			body:  ("application/x-www-form-urlencoded")
				author = <str> Required field
				name = <str> Book title. Required field
				reader = <int> reader ID. Optional parameter

    responses:
			404: by analogy with GET /api-v1/books/{bookID}/
			400: by analogy with  POST /api-v1/books/


GET /api-v1/books/export.csv

    Returns a book list file
    Columns in file:
        	bid ; author ; name ; rid ; reader


OPTIONS /api-v1/readers/

    Returns a description of types and supported formats

    responses:
		  200: OK
			"application/json"
			{
				"name": "Reader List",
				"description": "",
				"renders": [
					"application/json",
					"text/html"
				],
				"parses": [
					"application/json",
					"application/x-www-form-urlencoded",
					"multipart/form-data"
				],
				"actions": {
					"POST": {
						"url": {
							"type": "field",
							"required": false,
							"read_only": true,
							"label": "Url"
						  },
						"id": {
							"type": "integer",
							"required": false,
							"read_only": true,
							"label": "ID"
						},
						"name": {
							"type": "string",
							"required": true,
							"read_only": false,
							"label": "Name",
							"max_length": 200
						}
					}
				}
			}


GET /api-v1/readers/   [?page={pageNum}]

    Returns a list of readers

    parameters:
			query:
				page = <int> Page number. Optional parameter. Default number of items per page: 10

    responses:
			200: OK
				"application/json"

					{
						"count": <int>,
						"next": <url str>,
						"previous": <url str>,
						"results": [
							{
								"url": <str>,
								"id": <int>,
								"name": <str>
							},
							...
						]
					}


POST /api-v1/readers/

    Adding a reader

    parameters:
			body:  ("application/x-www-form-urlencoded")
				name = <str> Reader name. Required field

    responses:
			200: OK
				"application/json"

						{
							"url": <str>,
							"id": <int>,
							"name": <str>,
						}

			400: by analogy with  POST /api-v1/books/



GET /api-v1/readers/{readerID}/

    Detailing a copy of a reader

    parameters:
			path:
				readerID: <int> Required parametr

    responses:
			200: by analogy with POST /api-v1/books/

			404: by analogy with GET /api-v1/books/{bookID}/


PUT /api-v1/readers/{readerID}/

    Updating an existing record

    parameters: by analogy with  POST /api-v1/readers/

    responses:
			200: by analogy with POST /api-v1/books/

			404: by analogy with GET /api-v1/books/{bookID}/

			400: by analogy with  POST /api-v1/books/



DELETE /api-v1/readers/{readerID}/

    Delete existing record

    parameters:
			path:
				readerID: <int> Required parametr

    responses:
			204: No Content  (Record deleted successfully)

			404: by analogy with GET /api-v1/books/{bookID}/

			423: record LOCKED
				 "application/json"

				{
					"detail": "not delete. that object is associated with others",
					"result": [
						{
							"url": <str>,
							"id": <int>,
							"author": <str>,
							"name": <str>,
							"reader": <int>,
							"reader_name":<str>
					 },
					 .......
				}
