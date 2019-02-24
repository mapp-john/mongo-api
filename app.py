import os,json
from bson.errors import *
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, jsonify, request

##########################################
#
# Flask App Config
app = Flask(__name__)
app.url_map.strict_slashes = False # Disable redirecting on POST method from /star to /star/
#
# PyMongo Configuration
client = MongoClient(
    username=os.environ['MONGODB_USER'],
    password=os.environ['MONGODB_PASSWORD'],
    host=os.environ['MONGODB_PORT_27017_TCP_ADDR'],
    authSource=os.environ['MONGODB_DATABASE']
)
#
database = (os.environ['MONGODB_DATABASE'])
db = client[database]
#
# Test Connection
print(db)
print(db.collection_names())

##########################################
# Functions
#
# Convert String ID to BSON ID
def IDtoBSON(JSON):
    # Convert IDs for items in dict
    if type(JSON) == type(dict()):
        for key,value in JSON.items():
            if key == '_id':
                value = ObjectId(value)
                JSON[key] = value
        return JSON
    # Convert IDs for items in list
    elif type(JSON) == type(list()):
        for item in JSON:
            for key,value in item.items():
                if key == '_id':
                    value = ObjectId(value)
                    item[key] = value
        return JSON
    else:
        raise TypeError('Expected dict() or list()')
#
#
# Convert BSON ID to String ID
def IDtoSTR(JSON):
    # Convert IDs for items in dict
    if type(JSON) == type(dict()):
        for key,value in JSON.items():
            if key == '_id':
                ID = JSON['_id'].__str__()
                JSON.update({'_id': ID})
        return JSON
    # Convert IDs for items in list
    elif type(JSON) == type(list()):
        for item in JSON:
            for key,value in item.items():
                if key == '_id':
                    ID = item['_id'].__str__()
                    item.update({'_id': ID})
        return JSON
    else:
        raise TypeError('Expected dict() or list()')
#
#
##########################################
# Routes
#
# Collections Processes
@app.route('/api/v1.0/collections', methods=['GET','POST','PUT','PATCH','DELETE'])
def collections():
    args = request.args.to_dict()
    
    # GET ALL COLLECITONS
    if request.method == 'GET':
        # return collections
        result = db.collection_names()

        return jsonify({'collections': result})

    # DELETE ITEMS
    elif request.method == 'DELETE':
        # If Collection in Args, Delete
        if len(args) ==1 and 'collection' in args:
            collection = args['collection']
            try:
                db[collection].drop()
                result = {'RESULT': 'Collection '+collection+' Deleted'}
            except Exception as e:
                result = {'ERROR': str(e) }
                return jsonify(result), 400

            return jsonify(result)
        elif len(args) > 1:
            result = {'ERROR': 'Only one URL argument allowed'}
            return jsonify(result), 400
        else:
            result = {'ERROR': 'Must provide "collection" in URL argument to delete items'}
            return jsonify(result), 400

    # Default Else
    else:
        result = {'ERROR': 'Only GET and DELETE methods allowed'}
        return jsonify(result), 400

#
#
##########################################
#
# Dynamically pull Collection Name from URL
# Individual Processes
@app.route('/api/v1.0/<string:collection>', methods=['GET','POST','PUT','PATCH','DELETE'])
def base(collection):
    args = request.args.to_dict()
    # Reformat Arguments into new dict
    try:
        args = IDtoBSON(args)
    except InvalidId:
        result = {'ERROR': args['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
        return jsonify(result), 400

    # GET ITEMS
    if request.method == 'GET':
        # If ID in Arguments, Search for item
        if len(args) ==1:
            try:
                result = []
                for item in db[collection].find(args):
                    result.append(item) 
            except InvalidId:
                result = {'ERROR': args['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
                return jsonify(result), 400
            # Error if incorrect ID
            if result == []:
                result = {'ERROR': 'Object non-existent'}
                return jsonify(result), 400
            # Convert _id to string
            try:
                result = IDtoSTR(result)
            except InvalidId:
                result = {'ERROR': args['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
                return jsonify(result), 400

            # Return
            return jsonify(result)
        elif len(args) > 1:
            result = {'ERROR': 'Only one URL argument allowed'}
            return jsonify(result), 400

        # return base search all
        result = []
        for item in db[collection].find():
            result.append(item) 
        # Error if incorrect Collection
        if result == []:
            result = {'ERROR': 'Collection non-existent or empty'}
            return jsonify(result), 400

        # Convert _id to string
        result = IDtoSTR(result)

        return jsonify(result)

    # CREATE NEW ITEMS
    elif request.method == 'POST':
        # Pull JSON from HTTP Request
        JSON = request.json
        try:
            result = db[collection].insert_one(JSON)
        except Exception as e:
            print(e)
            result = {'ERROR': str(e) }
            return jsonify(result), 400

        result = {'_id': result.inserted_id,'acknowledged': result.acknowledged }

        # Convert _id to string
        try:
            result = IDtoSTR(result)
        except InvalidId:
            result = {'ERROR': args['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
            return jsonify(result), 400

        # Return
        return jsonify(result), 201

    # REPLACE EXISTING ITEMS
    elif request.method == 'PUT':
        # Pull JSON from HTTP Request
        JSON = request.json
        if '_id' in JSON:
            # Create Filter for Update
            Filter = {'_id': JSON['_id'] }
            try:
                Filter = IDtoBSON(Filter)
            except InvalidId:
                result = {'ERROR': Filter['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
                return jsonify(result), 400

            # Remove ID from JSON
            JSON.pop('_id',None)

            # Update Item
            try:
                result = db[collection].replace_one(Filter, JSON).raw_result
            except Exception as e:
                print(e)
                result = {'ERROR': str(e) }
                return jsonify(result), 400

            # Return Error
            if result['updatedExisting'] == False:
                result = {'ERROR': 'ObjectID non-existent'}
                return jsonify(result), 400

            # Return Result
            elif result['updatedExisting'] == True:
                result = {'RESULT': 'Object updated'}
                return jsonify(result)
            
        else:
            result = {'ERROR': 'Must provide _id for update'}
            return jsonify(result), 400

    # UPDATE EXISTING ITEMS
    elif request.method == 'PATCH':
        # Pull JSON from HTTP Request
        JSON = request.json
        if '_id' in JSON:
            # Create Filter for Update
            Filter = {'_id': JSON['_id'] }
            try:
                Filter = IDtoBSON(Filter)
            except InvalidId:
                result = {'ERROR': Filter['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
                return jsonify(result), 400

            # Remove ID from JSON
            JSON.pop('_id',None)

            # Update Item
            try:
                result = db[collection].update_one(Filter, {'$set': JSON}).raw_result
            except Exception as e:
                print(e)
                result = {'ERROR': str(e) }
                return jsonify(result), 400

            # Return Error
            if result['updatedExisting'] == False:
                result = {'ERROR': 'ObjectID non-existent'}
                return jsonify(result), 400

            # Return Result
            elif result['updatedExisting'] == True:
                result = {'RESULT': 'Object updated'}
                return jsonify(result)
            
        else:
            result = {'ERROR': 'Must provide _id for update'}
            return jsonify(result), 400

    # DELETE ITEMS
    elif request.method == 'DELETE':
        # If ID in Arguments, Search for item
        if len(args) ==1:
            try:
                result = []
                result = db[collection].remove(args)
            except InvalidId:
                result = {'ERROR': args['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
                return jsonify(result), 400
            # Error if incorrect ID
            if result == []:
                result = {'ERROR': 'ObjectID non-existent'}
                return jsonify(result), 400
            # Convert _id to string
            print(result)
            try:
                result = IDtoSTR(result)
            except InvalidId:
                result = {'ERROR': ID +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
                return jsonify(result), 400

            # Return
            return jsonify(result), 204
        elif len(args) > 1:
            result = {'ERROR': 'Only one URL argument allowed'}
            return jsonify(result), 400
        else:
            result = {'ERROR': 'Must provide URL argument to delete items'}
            return jsonify(result), 400

    # Default Else
    else:
        result = {'ERROR': 'Please check API configuration.'}
        return jsonify(result), 400
#
#
# Bulk Processes
@app.route('/api/v1.0/<string:collection>/bulk', methods=['GET','POST','PUT','PATCH','DELETE'])
def bulk(collection):
    args = request.args.to_dict()
    # Reformat Arguments into new dict
    try:
        args = IDtoBSON(args)
    except InvalidId:
        result = {'ERROR': args['_id'] +' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}
        return jsonify(result), 400

    # CREATE NEW ITEMS
    if request.method == 'POST':
        # Pull JSON from HTTP Request
        JSON = request.json
        try:
            result = db[collection].insert_many(JSON)
        except Exception as e:
            print(e)
            result = {'ERROR': str(e) }
            return jsonify(result), 400

        inserted_ids = []
        # Insert IDs as string
        for item in result.inserted_ids:
            inserted_ids.append({'_id': item.__str__()})
        result = {'inserted_ids': inserted_ids,'acknowledged': result.acknowledged }
        
        # Return
        return jsonify(result)

    # Default Else
    else:
        result = {'ERROR': 'Please check API configuration.'}
        return jsonify(result), 400

# Run from all IPs
if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0', port=8080)
