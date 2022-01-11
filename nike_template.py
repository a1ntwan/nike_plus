from yaml import load, FullLoader
from shutil import rmtree
from os import mkdir
from jinja2 import Template

with open('vars.yml') as fd:
    file_data = load(fd, Loader=FullLoader)

for host in file_data:
    rmtree(host, ignore_errors=True)
    mkdir(host)

tm = Template('''---
version: "3.9"
services:
  builder:
    build: .
    <<: &img
        image: nike/plus
{%- for host, data in file_data.items() %}
  {{ host }}:
    <<: *img
    environment:
      URL: "{{ data.url }}"
      EMAIL: "{{ data.email }}"
      PASS: "{{ data.password }}"
      SIZE: "{{ data.size }}"
      CVV: "{{ data.cvv }}"
      USER_AGENT: "{{ data.user_agent }}"
      PROXY: "{{ data.proxy }}"
      YEAR: "{{ data.time.split(' ')[0].split('-')[0] | int }}"
      MONTH: "{{ data.time.split(' ')[0].split('-')[1] | int }}"
      DAY: "{{ data.time.split(' ')[0].split('-')[2] | int }}"
      HOUR: "{{ data.time.split(' ')[1].split(':')[0] | int }}"
      MINUTE: "{{ data.time.split(' ')[1].split(':')[1] | int }}"
      SECOND: "{{ data.time.split(' ')[1].split(':')[2] | int }}"
    command: python3 sneakers.py
    restart: on-failure:5
    volumes:
      - ./host{{ loop.index }}:/sneakers/logs
      - .:/screen
{%- endfor %}
''')

msg = tm.render(file_data=file_data)

with open('docker-compose.yml', 'w') as dc_file:
    dc_file.write(msg)

print(msg)
