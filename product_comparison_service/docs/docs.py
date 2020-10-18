DOCS="""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Swagger UI</title>
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui.css" >
  <style>
    html
    {
      box-sizing: border-box;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
    }
    *,
    *:before,
    *:after
    {
      box-sizing: inherit;
    }
    body {
      margin:0;
      background: #fafafa;
    }
  </style>
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-bundle.js"> </script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-standalone-preset.js"> </script>
<script>
window.onload = function() {
  var spec = {"swagger": "2.0", "info": {"description": "Coding test project for Relayr.", "version": "0.1", "title": "Product Comparison Service", "contact": {"email": "butleraidan@gmail.com"}}, "host": "localhost:8888", "basePath": "/v0.1/", "tags": [{"name": "product", "description": "Products", "externalDocs": {"description": "Products", "url": "localhost:8888/product"}}], "schemes": ["http"], "paths": {"/product": {"get": {"tags": ["product"], "summary": "Search products by name and category", "description": "Multiple status values can be provided with comma separated strings", "operationId": "searchProduct", "produces": ["application/json"], "parameters": [{"name": "product", "type": "string", "in": "query", "description": "Name of product to filter by", "required": false, "collectionFormat": "multi"}, {"name": "category", "type": "string", "in": "query", "description": "Category of product to filter by", "required": false, "collectionFormat": "multi"}], "responses": {"200": {"description": "successful operation", "schema": {"type": "array", "items": {"$ref": "#/definitions/Product"}}}}}, "put": {"tags": ["product"], "summary": "Upsert product", "description": "Creates or updates a product for a supplier", "operationId": "upsertProduct", "produces": ["application/json"], "parameters": [{"name": "product", "type": "string", "in": "query", "description": "Name of product", "required": true, "collectionFormat": "multi"}, {"name": "category", "type": "string", "in": "query", "description": "Category of product", "required": true, "collectionFormat": "multi"}, {"name": "description", "type": "string", "in": "query", "description": "Description of product", "required": true, "collectionFormat": "multi"}, {"name": "price", "type": "number", "in": "query", "description": "Price of product", "required": true, "collectionFormat": "multi"}, {"name": "supplier", "type": "string", "in": "query", "description": "Supplier of product at given price", "required": true, "collectionFormat": "multi"}, {"name": "product_rating", "type": "number", "in": "query", "description": "Real value in range [0,1]", "required": false, "collectionFormat": "multi"}], "responses": {"200": {"description": "successful operation", "schema": {"type": "array", "items": {"$ref": "#/definitions/Upsert"}}}, "400": {"description": "bad request"}}}, "delete": {"tags": ["product"], "summary": "Deletes a product for supplier", "description": "", "operationId": "deleteProduct", "produces": ["application/json"], "parameters": [{"name": "product", "type": "string", "in": "query", "description": "Name of product to filter by", "required": false, "collectionFormat": "multi"}, {"name": "category", "type": "string", "in": "query", "description": "Category of product to filter by", "required": false, "collectionFormat": "multi"}], "responses": {"200": {"description": "successful operation", "schema": {"type": "array", "items": {"$ref": "#/definitions/Deletion"}}}, "400": {"description": "bad request"}}}}}, "definitions": {"Product": {"type": "object", "properties": {"success": {"type": "boolean"}, "search_results": {"type": "object", "properties": {"product": {"type": "string"}, "description": {"type": "string"}, "category": {"type": "string"}, "price": {"type": "string"}, "supplier": {"type": "string"}, "product_rating": {"type": "number"}, "supplier_rating": {"type": "number"}, "combined_ratng": {"type": "number"}, "last_updated": {"type": "string"}}}}}, "Upsert": {"type": "object", "properties": {"success": {"type": "boolean"}, "upsert": {"type": "object", "properties": {"product": {"type": "string"}, "description": {"type": "string"}, "category": {"type": "string"}, "price": {"type": "string"}, "supplier": {"type": "string"}, "product_rating": {"type": "number"}, "last_updated": {"type": "string"}}}}}, "Deletion": {"type": "object", "properties": {"success": {"type": "boolean"}, "upsert": {"type": "object", "properties": {"product": {"type": "string"}, "supplier": {"type": "string"}}}}}}};
  // Build a system
  const ui = SwaggerUIBundle({
    spec: spec,
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout"
  })
  window.ui = ui
}
</script>
</body>
</html>"""
