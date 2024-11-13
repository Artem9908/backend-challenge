from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor

def instrument():
    DjangoInstrumentor().instrument()
    CeleryInstrumentor().instrument()
