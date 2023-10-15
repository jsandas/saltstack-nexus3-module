{% from tpldir + "/map.jinja" import nexus with context %}

{% for role, data in nexus['roles'].items() %}
role_{{ role }}:
  nexus3_roles.present:
    - name: {{ role }}
  {% for item in data %}
    - {{ item }}
  {% endfor %}
{% endfor %}

remove_unwanted-role:
  nexus3_roles.absent:
    - name: unwanted-role