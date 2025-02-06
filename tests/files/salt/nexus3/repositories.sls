{% from tpldir + "/map.jinja" import nexus with context %}

{% for repository, data in nexus['repositories'].items() %}
repositories_{{ repository }}:
  nexus3_repositories.present:
    - name: {{ repository }}
  {% for item in data %}
    - {{ item }}
  {% endfor %}
{% endfor %}

remove_unwanted-hosted_repo:
  nexus3_repositories.absent:
    - name: unwanted-hosted