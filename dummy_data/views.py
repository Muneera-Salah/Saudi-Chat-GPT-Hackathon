import os
from django.shortcuts import render
from .forms import GenerateDummyForm

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import http.client
import json
import re

from requests import request
from decouple import config

HEADERS = {
    'Content-Type': 'application/json',
    'customer-id': '1905674446',
    'x-api-key': config('APIKKEY')
}

CACHE = {}


def get_connection():
    conn = http.client.HTTPSConnection("experimental.willow.vectara.io")
    return conn


def generate_dummy_1(field_name_1):
    # chcek if it's cached
    if field_name_1 in CACHE:
        return CACHE[field_name_1], None

    result = {}
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f"generate a list 5 saudi of {field_name_1} in arabic"
            }
        ]
    })
    conn = get_connection()
    conn.request("POST", "/v1/chat/completions", payload, HEADERS)
    res = conn.getresponse()
    data = res.read()
    result = data.decode("utf-8")
    json_object = json.loads(result)
    res = json_object['choices'][0]['message']['content']

    final_data = []

    for el in res.split('\n'):
        if el == "":
            continue
        tmp = re.sub(r'\d*\..', '', el)
        final_data.append(tmp.strip())

    CACHE[field_name_1] = final_data

    return final_data


def generate_dummy_2(field_name_2):
    # chcek if it's cached
    if field_name_2 in CACHE:
        return CACHE[field_name_2], None

    result = {}
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f"generate a list 5 saudi of {field_name_2} in arabic"
            }
        ]
    })
    conn = get_connection()
    conn.request("POST", "/v1/chat/completions", payload, HEADERS)
    res = conn.getresponse()
    data = res.read()
    result = data.decode("utf-8")
    json_object = json.loads(result)
    res = json_object['choices'][0]['message']['content']

    final_data = []

    for el in res.split('\n'):
        if el == "":
            continue
        tmp = re.sub(r'\d*\..', '', el)
        final_data.append(tmp.strip())

    CACHE[field_name_2] = final_data

    return final_data


def index(request):
    template_name = "index.html"
    context = {
        'table_headers': '',
        'results': '',
    }
    field_name_1 = ''
    field_name_2 = ''

    if request.method == 'POST':
        form = GenerateDummyForm(request.POST)

        if form.is_valid():
            field_name_1 = form.cleaned_data['field_name_1']
            field_name_2 = form.cleaned_data['field_name_2']
            table_headers = zip(field_name_1, field_name_2)

            data_1 = generate_dummy_1(field_name_1)
            data_2 = generate_dummy_2(field_name_2)

            results = zip(data_1, data_2)

            form = GenerateDummyForm()
            context = {
                'table_header': table_headers,
                'results': results,
                'form': form
            }
        else:
            form = GenerateDummyForm()
    else:
        form = GenerateDummyForm()
        context.update({
            'form': form
        })
    return render(request, template_name, context)
