from flask import Flask, request
from flask_restful import Api, Resource, reqparse, marshal_with, fields, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# SQlite Db config.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///device.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["FLASK_ENV"] = 'development'
db = SQLAlchemy(app)

class DeviceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    mac_address = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"Device.__class__<{self.model}, {self.type}, {self.mac_address}>"

db.create_all()

item_for_put = reqparse.RequestParser()
item_for_put.add_argument("model", type=str, help="The model is empty but a required feild", required=True)
item_for_put.add_argument("type", type=str, help="The type is empty but a required feild", required=True)
item_for_put.add_argument("mac_address", type=str, help="The mac_address is empty but a required feild", required=True)


item_for_patch = reqparse.RequestParser()
item_for_patch.add_argument("model", type=str, help=None)
item_for_patch.add_argument("type", type=str, help=None)
item_for_patch.add_argument("mac_address", type=str, help=None)

resource_fields = {
    'id': fields.Integer,
    'model': fields.String,
    'type': fields.String,
    'mac_address': fields.String
}

class Device(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = DeviceModel.query.filter_by(id=id).first()
        if result is None:
            abort(404, message="Device not found...")
        return result, 200

    @marshal_with(resource_fields)
    def put(self, id):
        args = item_for_put.parse_args()
        result = DeviceModel.query.filter_by(id=id).first()
        if result:
            abort(404, message="Item already exists...")
        device = DeviceModel(id=id, model=args['model'], type=args['type'], mac_address=args['mac_address'])
        print(device)
        db.session.add(device)
        db.session.commit()
        return device, 201

    @marshal_with(resource_fields)
    def patch(self, id):
        args = item_for_patch.parse_args()
        device = DeviceModel.query.filter_by(id=id).first()
        print("Inside Patch", device)
        if device is None:
            abort(404, message="Device not found. Use put request.")

        if args['model']:
            device.model = args['model']
        if args['type']:
            device.type = args['type']
        if args['mac_address']:
            device.mac_address = args['mac_address']

        db.session.commit()

        return {"message": "Patched successfully!"}

    def delete(self, id):
        item_to_delete = DeviceModel.query.filter_by(id=int(id)).first()
        print("Inside delete",item_to_delete)
        if item_to_delete is None:
            abort(405, message = f"Item with id: {id} doesn't exist.")
        db.session.delete(item_to_delete)
        db.session.commit()
        print("Deleted")
        return {"message": f"Item with id: {id} successfully deleted."}, 204

api.add_resource(Device, '/api/<int:id>')

@app.route('/')
def index():
    return "API to collect Device Info."

if __name__ == '__main__':
    app.run(debug=True)
