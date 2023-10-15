# states based on pillar data
{% from tpldir + "/map.jinja" import nexus with context %}

{% for blobstore, data in nexus['blobstores'].items() %}
create_blobstore_{{ blobstore }}:
  nexus3_blobstores.present:
    - name: {{ blobstore }}
  {% for item in data %}
    - {{ item }}
  {% endfor %}
{% endfor %}

remove_unwanted-blobstore:
  nexus3_blobstores.absent:
    - name: unwanted-blobstore