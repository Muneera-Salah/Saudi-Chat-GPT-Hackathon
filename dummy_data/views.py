import os
from django.shortcuts import render
from .forms import GenerateDummyForm

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import http.client
import json
from requests import request
from decouple import config

HEADERS = {
        'Content-Type': 'application/json',
        'customer-id': '1905674446',
        'x-api-key': config('APIKKEY')
        }

CONN = http.client.HTTPSConnection("experimental.willow.vectara.io")

def generate_dummy_1(field_name_1):
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
  CONN.request("POST", "/v1/chat/completions", payload, HEADERS)
  res = CONN.getresponse()
  data = res.read()
  result = data.decode("utf-8")
  json_object = json.loads(result)
  res = json_object['choices'][0]['message']['content']

  data = [el.strip()[2:].strip() for el in res.split('\n')[2:]]

  return data

def generate_dummy_2(field_name_2):
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
  CONN.request("POST", "/v1/chat/completions", payload, HEADERS)
  res = CONN.getresponse()
  data = res.read()
  result = data.decode("utf-8")
  json_object = json.loads(result)
  res = json_object['choices'][0]['message']['content']

  data = [el.strip()[2:].strip() for el in res.split('\n')[2:]]

  return data

def index (request):
  template_name = "index.html"
  context = {
    'table_headers':'',
    'results':'',
  }
  field_name_1 = ''
  field_name_2 = ''

  if request.method == 'POST':
    form = GenerateDummyForm(request.POST)
    
    if form.is_valid():
      field_name_1 = form.cleaned_data['field_name_1']
      field_name_2 = form.cleaned_data['field_name_2']
      table_headers = zip(field_name_1, field_name_2)

      data_1=generate_dummy_1(field_name_1)    
      data_2=generate_dummy_2(field_name_2) 

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
    context.update ({
      'form': form
    })
  return render(request, template_name, context)