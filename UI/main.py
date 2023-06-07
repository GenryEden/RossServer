import sys
from loguru import logger as lg
from flask import Flask, render_template, url_for, redirect, request
from collections import namedtuple

sys.path.append("../")

import Model
from ServerDescriptor import OutputProto

app = Flask(__name__)

servers = Model.ServersModel("127.0.0.1")
servers.add_sound("../sounds/")
servers.run()

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html', servers=servers.get_descriptors())


@app.route('/add_message', methods=['POST'])
def add_message():
    filtered_cameras = (request.form['filtered_cameras'])
    filtered_cameras_set = set(map(int, filtered_cameras.split()))
    for i in filtered_cameras_set:
        if i < 0 or i > 128:
            return redirect(url_for('main'))
    port = int(request.form['port'])
    protocol = request.form['protocol']
    lg.debug(f"Got protocol {protocol}")
    if port < 0 or port > 65536:
        return redirect(url_for('main'))
    for descriptor in servers.get_descriptors().values():
        if descriptor.port == port:
            return redirect(url_for('main'))
    if protocol == "sound":
        for descriptor in servers.get_descriptors().values():
            if descriptor.protocol == OutputProto.SOUND:
                return redirect(url_for('main'))
        servers.add_sound("../sounds/")
    if protocol == "TSL UMD v3.1":
        servers.add_tslumd(port)
    if protocol == "JSON":
        servers.add_json(port)
    if protocol == "ezTSL UMD":
        servers.add_eztslumd(port)
    if protocol == "filtered ezTSL UMD":
        servers.add_filtered_eztslumd(port, filtered_cameras_set)
    if protocol == "filtered TSL UMD":
        servers.add_filtered_tslumd(port, filtered_cameras_set)
    return redirect(url_for('main'))


@app.route('/delete', methods=['POST'])
def delete():
    lg.debug(str(request.form))
    servers.delete_server(int(request.form["servIndex"]))
    return redirect(url_for('main'))


app.run(debug=True)
