import requests
import logging
from flask import Flask, render_template, request, jsonify

from flask import json
from werkzeug.exceptions import HTTPException

from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)

import pymongo
from flask_pymongo import PyMongo


trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)

app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'

mongo = PyMongo(app)

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer('backendapp-service')

@app.route('/')
@by_path_counter
def homepage():
    with tracer.start_span('get-python-jobs') as span:
        homepages = []
        res = requests.get('https://jsonplaceholder.typicode.com/todos')
        try:
            span.set_tag('first-tag', len(res.json()))
        except:
            span.set_tag('first-tag', 'len(res.json()) Failed')
        for result in res.json():
            try:
                homepages.append(result['title'])
                a=str(result['title'])[30:]
                span.log_kv({'event':'Site Found', 'value':str(result['title'])})
            except:
                span.log_kv({'event':'Failed URL', 'value':str(result)})
                # return "Unable to get site for %s" % result['company']                
    # return "Hello World"
    return jsonify(homepages)

@app.route('/api1')
@by_path_counter
def my_api1():
    with tracer.start_span('my_api1 | GET1') as span:
        span.set_tag('myown-tag', 'WOW TAG!')
        answer = "Method log_kv has runtime errors"
        a=answer[1000:1010:0]
        for c in answer:
            span.log_kv({'event': 'char-by-char', 'value': str(c)})
    return jsonify(response=answer)

@app.route('/api')
@metrics.do_not_track()
def my_api():
    with tracer.start_span('my_api | GET1') as span:
        span.set_tag('myown-tag', 'WOW TAG!')
        answer = "something NEW"
        for c in answer:
            span.log_kv({'event': 'char-by-char', 'value': str(c)})
    return jsonify(response=answer)

@app.route('/star', methods=['POST'])
@by_path_counter
@metrics.do_not_track()
def add_star():
    with tracer.start_span('add_star | POST') as span:
        star = mongo.db.stars
        name = request.json['name']
        distance = request.json['distance']
        star_id = star.insert({'name': name, 'distance': distance})
        new_star = star.find_one({'_id': star_id })
        output = {'name' : new_star['name'], 'distance' : new_star['distance']}
    return jsonify({'result' : output})

metrics.register_default(by_path_counter)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    app.run()
