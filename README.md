# mongo-api
## HTTP API front end for Mongo DB

### To get all collections:
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

## Collections are created automatically if they don't exist

### To post to a collection:
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
   "_id": "5c71d199e9fe9b0021041152",
   "acknowledged": true
}
```

### To ALL data from collection
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

### To specific data from collection
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

### To specific data from collection by ID
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

### To Delete specific ITEM
#### DELETE  https://container.domain.com/api/v1.0/TEST_COLLECTION?_id=5c71d7fc39fe6b0021441353
#### RESPONSE:
```json
{
  "n": 1,
  "ok": 1
}
```
n = number of items modified (in this case deleted)

### To Delete specific entire collection
#### DELETE  https://container.domain.com/api/v1.0/collections?collection=TEST_COLLECTION
#### RESPONSE:
```json
{
"RESULT": "Collection TEST_COLLECTION Deleted"
}
```


