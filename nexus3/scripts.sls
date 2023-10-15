{% from tpldir + "/map.jinja" import nexus with context %}

# nexus3_scripts require the groovy script api to be enabled
http://localhost:8081:
  nexus3_scripts.base_url

# create tasks based on dictionary from pillars
{% for task, data in nexus['tasks'].items() %}
task_{{ task }}:
  nexus3_scripts.task:
    - name: {{ task }}
    - typeId: {{ data['typeId'] }}
    - taskProperties: {{ data['taskProperties'] }}
    - cron: {{ data['cron'] }}
  {% if data['setAlertEmail'] is defined %}
    - setAlertEmail: {{ data['setAlertEmail'] }}
  {%endif %}
{% endfor %} 