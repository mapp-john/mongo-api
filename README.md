# mongo-api
## HTTP API front end for Mongo DB

## Get all collections:
#### GET: https://container.domain.com/api/v1.0/collections
#### RESPONSE: 
```json
{
  "collections": [
    "COLLECTION_ONE" 
    "COLLECTION_TWO" 
    "COLLECTION_THREE"
  ]
}
```



## Post single item to a collection:
*Collections are created automatically if they don't exist*
#### POST: https://container.domain.com/api/v1.0/TEST_COLLECTION
```json
{
  "type": "type_a",
  "version": "version_1"
}
```
#### RESPONSE: 
```json
{
   "_id": "5c71d69939fe6b0021441352",
   "acknowledged": true
}
```
**_id** = *ID of item created*



## Retrieve ALL data from collection:
#### GET https://container.domain.com/api/v1.0/TEST_COLLECTION
#### RESPONSE:
```json
[
  {
    "_id": "5c71d69939fe6b0021441352",
    "type": "type_a",
    "version": "version_1"
  },
  {
    "_id": "5c71d7fc39fe6b0021441353",
    "type": "type_b",
    "version": "version_2"
  }
]
```



## Retrieve specific data from collection by key:
#### GET https://container.domain.com/api/v1.0/TEST_COLLECTION?type=type_a
#### RESPONSE:
```json
[
  {
    "_id": "5c71d69939fe6b0021441352",
    "type": "type_a",
    "version": "version_1"
  }
]
```



## Retrieve specific data from collection by ID:
#### GET https://container.domain.com/api/v1.0/TEST_COLLECTION?_id=5c71d7fc39fe6b0021441353
#### RESPONSE:
```json
[
  {
    "_id": "5c71d7fc39fe6b0021441353",
    "type": "type_b",
    "version": "version_2"
  }
]
```



## Delete specific item by ID:
#### DELETE  https://container.domain.com/api/v1.0/TEST_COLLECTION?_id=5c71d7fc39fe6b0021441353
#### RESPONSE:
```json
{
  "n": 1,
  "ok": 1
}
```
**n** = *number of items modified (in this case deleted)*



## Delete specific entire collection:
#### DELETE  https://container.domain.com/api/v1.0/collections?collection=TEST_COLLECTION
#### RESPONSE:
```json
{
"RESULT": "Collection TEST_COLLECTION Deleted"
}
```



## Bulk item creation:
#### POST: https://container.domain.com/api/v1.0/TEST_COLLECTION/bulk
```json
[
  {
    "type": "type_a",
    "version": "version_1"
  },
  {
    "type": "type_b",
    "version": "version_2"
  }
]
```
#### RESPONSE: 
```json
{
  "acknowledged": true,
  "inserted_ids":    [
    {"_id": "5c72292f39fe6b0021441354"},
    {"_id": "5c72292f39fe6b0021441355"}
  ]
}
```



## Update single item by ID:
*Must provide ID in Post Data*
#### PATCH: https://container.domain.com/api/v1.0/TEST_COLLECTION
```json
{
  "_id":"5c72292f39fe6b0021441354",
  "version": "version_1.5"
}
```
#### RESPONSE: 
```json
{
  "RESULT": "Object updated"
}
```



## Replace single item by ID:
*Must provide ID in Post Data*
*All data in item will be replaced with data sent*
#### PATCH: https://container.domain.com/api/v1.0/TEST_COLLECTION
```json
{
  "_id":"5c72292f39fe6b0021441354",
  "type": "type_a",
  "version": "version_1.5",
  "status": "down"
}
```
#### RESPONSE: 
```json
{
  "RESULT": "Object updated"
}
```
