import os
import django
import json
from django.core.serializers import serialize
from django.apps import apps

# ✅ Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatroom.settings")  # Replace with your project name
django.setup()

# ✅ Get all models in the project
all_models = [model for model in apps.get_models()]

data = {}
for model in all_models:
    model_name = model._meta.model_name
    try:
        data[model_name] = json.loads(serialize('json', model.objects.all()))
    except Exception as e:
        print(f"Error serializing {model_name}: {e}")

# ✅ Save the data with UTF-8 encoding
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ Data exported successfully!")
