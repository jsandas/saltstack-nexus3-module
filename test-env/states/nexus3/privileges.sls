{% from tpldir + "/map.jinja" import nexus with context %}

{% for privilege, data in nexus['privileges'].items() %}
create_privilege_{{ privilege }}:
  nexus3_privileges.present:
    - name: {{ privilege }}
  {% for item in data %}
    - {{ item }}
  {% endfor %}
{% endfor %}

remove_unwanted-privilege:
  nexus3_privileges.absent:
    - name: unwanted-privilege