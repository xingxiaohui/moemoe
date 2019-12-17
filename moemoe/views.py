from moemoe import app


@app.route('/')
def index():
    return 'Hello moemoe！'

