{% from tpldir + "/map.jinja" import nexus with context %}

{% for user, data in nexus['users'].items() %}
user_{{ user }}:
  nexus3_users.present:
    - name: {{ user }}
  {% for item in data %}
    - {{ item }}
  {% endfor %}
{% endfor %}

remove_unwanted_user:
  nexus3_users.absent:
    - name: unwanted-user