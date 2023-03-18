from django.shortcuts import render
from .forms import GenerateDummyForm

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import http.client
import json
from requests import request

HEADERS = {
        'Content-Type': 'application/json',
        'customer-id': '1905674446',
        'x-api-key': 'zqt_cZZIzncr3qQYrfNyK-xnsqkQL0quDshqCb9gzA'
        }


CONN = http.client.HTTPSConnection("experimental.willow.vectara.io")

def generate_dummy_1(request, field_name_1):
  result = {}
  payload = json.dumps({
  "model": "gpt-3.5-turbo",
  "messages": [
      {
      "role": "user",
      "content": f"generate a list 5 saudi of {field_name_1} in arabic"
      # "content": f"generate fake list of saudi school name in arabic"
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

def generate_dummy_2(request, field_name_2):
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
    'mylist':'',
  }

  if request.method == 'POST':
    form = GenerateDummyForm(request.POST)
    
    if form.is_valid():
      field_name_1 = form.cleaned_data['field_name_1']
      field_name_2 = form.cleaned_data['field_name_2']
      data_1=generate_dummy_1(request, field_name_1)    
      data_2=generate_dummy_2(request, field_name_2) 
      mylist = zip(data_1, data_2)
      form = GenerateDummyForm()
      context = {
          'mylist': mylist,
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