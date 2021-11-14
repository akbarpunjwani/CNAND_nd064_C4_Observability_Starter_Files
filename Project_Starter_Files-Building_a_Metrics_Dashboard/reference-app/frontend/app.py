import logging
from flask import Flask, render_template, request

from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from random import randint
from time import sleep

app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

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

tracer = init_tracer('frontendapp-service')

@app.route('/')
def homepage():
    with tracer.start_span('sleep-b4-render') as span:
        sleep(randint(1,10))
    return render_template("main.html")

if __name__ == "__main__":
    app.run()