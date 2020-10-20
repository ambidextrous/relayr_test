# Product comparison service task

A service that helps the end customer to decide which website or retail shop
they can use to buy their product by comparing data from different providers.

Service details:

* Language: Python (8.5)
* Framework: `tornado`
* Format: REST API
* Documentation: OpenAPI web-page 
* Pulls from:
  * LRU Cache dictionary
  * Sqlite3 database instance
  * (Dummy) external APIs
* Accepts push via:
  * Batch processing CLI 
  * REST API endpoint

# Instructions

## Running

Start by `cd`ing into the directory containing this `README.md`.

To build a docker image of this app, run:
```bash
docker image build -t aidan_butler_relayr_test .
```
To run the container on port 8889, run:
```bash 
docker run -p 8889:8888 -d aidan_butler_relayr_test
```
To read the OpenAPI documentation, go to: 
* http://localhost:8889/v0.1/docs

To test the API running on the container, go to:
* http://localhost:8889/v0.1/product?category=Canines&product=coyotee
* http://localhost:8889/v0.1/product?category=Canines
* http://localhost:8889/v0.1/product?product=coyotee
* http://localhost:8889/v0.1/product

To test the to create and delete a new product, run the following in sequence
```bash
curl -d "product=owl&supplier=DavesPets" -X GET localhost:8889/v0.1/product
curl -d "product=owl&description=wise&price=3&supplier=DavesPets&product_rating=0.98&category=Birds" -X PUT localhost:8889/v0.1/product
curl -d "product=owl&supplier=DavesPets" -X GET localhost:8889/v0.1/product
curl -d "product=owl&supplier=DavesPets" -X DELETE localhost:8889/v0.1/product
curl -d "product=owl&supplier=DavesPets" -X GET localhost:8889/v0.1/product
```

## Testing

To run the automated unit tests locally, `cd` into the directory containing this `README.md`, then run:
```bash
export PYTHONPATH="${PYTHONPATH}:<path/to/directory/containing/this/README.md>"
pytest tests/
```

# Explanation

## Main task
* Service should provide an endpoint that accepts product name and category 
as a search options and returns a list of product info that matches it.
  * Done: service provides a `v0.1/product` REST endpoint with `GET` (search),
  `PUT` (create/update) and `DELETE` (delete) methods. OpenAPI documentation
  for the service can be found at the `v0.1/docs` endpoint.
* The service should support multiple data sources for importing new products 
to the service data base (push, pull, batch data import, ….).
  * Done: the service allows for push operations via the `GET` and `DELETE` methods
  for the `v0.1/product` endpoint; pull operations from external APIs have not 
  been implemented, but are mocked in the product handler; batch push operations
  are implemented via a command line interface allowing for the operations
  `add_products`, `add_suppliers` and `add_supplier_products` using JSONL files.
  (this batch operation CLI is invoked at application start-up to add test data to the application database)
* Please select one data source to implement. However, your code should be flexible 
and allow for introducing new data sources.
  * Done: see above
* The solution should be documented but should also be understandable (try to follow 
SOLID and clean code principles).
  * That's for you to judge: I've tried to give the app a sensible structure,
  name things sensibly and include documentation where necessary.
* Performance and test cases are important.
  * All blocking I/O operations are carried out asynchronously (and where possible
  in parallel) so as to aid performance. Unit tests for the handler's core functionality
  and caching system are included. Manual tests using Postman and `curl` we carried
  out during development.  
* The system should be easy to scale and maintain.
  * The system is dockerized so as to facilitate scaling via services such as Heroku

## Bonus points
* Delivering the solution running on container based env such as docker.
  * Done: instructions for building, running and testing a docker image of the 
  app included below.
* Assume there is an AI service that uses customer reviews for different products 
and provides recommendations on product providers, so you need to return the 
search result ranked based on result from recommendation service.
  * Done: SQL search results returned from the database are ordered by their 
  `combined_rating` ((`supplier_rating` + `product_rating`)/2) score.
* The service should be of high availability 
  * Done: the service is designed to return up-to-date search results sourced 
  from external parties as quickly as possible (using caching) and to ensure that
  slower requests requiring I/O operations (such as accessing the database or 
  external APIs are non-blocking).
  The service is written using the asynchronous Python `tornado` web framework; 
  when a search for a particular `product` and `category` combination is entered, 
  the handler first checks to see if the results are stored in a size-limited 
  cache of recent searches; if the results are not found in that cache, the 
  handler then queries the database to see if they can be found there; if no 
  results are found in either the cache or the database, or if the results found 
  are older than a configured time delta (e.g. 24 hours) the app then hits a list
  of (mocked) external APIs to see if results can be found.
  
## Limitations
The following are things that are missing from the app, either because they seemed
beyond the scope of the requirements of the task or because I did not have time. Given
more time to work on the project, I would add:
* End-to-end and integration tests, including full database creation and teardown
* Improved unit test coverage
* Security
* Authentication
* Pagination for results
* Inclusion of a production level database, e.g. PostgreSQL instead of SQLite
