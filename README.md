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
#### POST: https://container.domain.com/api/v1.0/<collection>
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




