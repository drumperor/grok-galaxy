from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_socketio import SocketIO, emit
import json
from grok_galaxy_tamga import GalaksiTamgaGenerator, TamgaError

app = Flask(__name__, static_folder='.', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins='*')
generator = GalaksiTamgaGenerator()
api = Api(app, version='2.0', title='Grok Galaxy API', description='Yıldızlar arası tamga yönetimi', doc='/docs')

tamga_model = api.model('Tamga', {
    'extra_info': fields.String,
    'stars': fields.List(fields.Raw),
    'emotion': fields.String,
    'created_by': fields.String(default='drumperor')
})

@api.route('/api/tamga')
class TamgaResource(Resource):
    @api.expect(tamga_model)
    def post(self):
        try:
            data = api.payload
            tamga = generator.generate_galaksi_tamga(
                data['extra_info'],
                data.get('stars', []),
                data.get('emotion', 'birlik'),
                created_by=data.get('created_by', 'drumperor')
            )
            generator.save_tamga(tamga)
            generator.save_tamga_to_db(tamga)
            for sid, star in tamga['star_connections'].items():
                s2 = dict(star)
                s2['star_id'] = sid
                generator.generate_star_music(s2)
            socketio.emit('tamga_created', {'tamga_id': tamga['tamga_id']})
            return tamga, 201
        except TamgaError as e:
            generator.notify_error(str(e), 'APIError', {'endpoint': '/api/tamga'})
            return {'error': str(e)}, 400

@socketio.on('connect')
def on_connect():
    emit('message', {'data': 'WebSocket bağlantısı kuruldu'})

@app.route('/')
def index():
    """Serve the GUI HTML page"""
    return app.send_static_file('cosmosguiv2.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files"""
    return app.send_static_file(path)

if __name__ == '__main__':
    print('Sunucu başlatılıyor…')
    # Run without reloader and bind to all interfaces
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
