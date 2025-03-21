from flask import Flask, json, Response, request


api = Flask(__name__)


@api.route('/artist/1234', methods=['GET'])
@api.route('/artist/004608ab-3793-4758-a43f-4c7c875e95a3', methods=['GET'])
def get_artist_1234():
    if request.url.find('release-groups') > 0:
        return json.dumps({'release-groups': [
            {'id': '8d2c022e-91c7-40d1-ac31-1b91e8e453ed'},
            {'id': '4f1e0d22-2557-4e37-901f-2dc6eaa6d16f'}]})
    else:
        return json.dumps({'name': 'Victimized'})

# '8acde982-ed94-4731-95f1-d797d6b5394e', 'e00fc180-5c1f-4f72-b01c-3f538fcfeaae', '04d67265-1a49-47f7-8af9-8adf00aafaa8'


@api.route('/artist/2345', methods=['GET'])
@api.route('/artist/e86bdd24-9b46-4606-bfdc-66a98cefe932', methods=['GET'])
def get_artist_2345():
    if request.url.find('release-groups') > 0:
        return json.dumps({'release-groups': [
            {'id': '8acde982-ed94-4731-95f1-d797d6b5394e'},
            {'id': 'e00fc180-5c1f-4f72-b01c-3f538fcfeaae'},
            {'id': '04d67265-1a49-47f7-8af9-8adf00aafaa8'},
            {'id': 'e3122d32-d2a6-4131-a5ee-4817a162608d'}
        ]})
    else:
        return json.dumps({'name': 'Res Sacra Misa'})


@api.route('/', methods=['GET'])
def get_index():
    print(request.data)
    return Response("", status=200, mimetype='application/json')


if __name__ == '__main__':
    api.run(port=3000)
