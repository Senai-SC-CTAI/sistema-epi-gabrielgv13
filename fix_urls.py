import os
import re

# Define the replacements
replacements = {
    r"{% url 'app_dashboard' %}": "{% url 'dashboard:app_dashboard' %}",
    r"{% url 'app_users' %}": "{% url 'colaboradores:app_users' %}",
    r"{% url 'app_users_create' %}": "{% url 'colaboradores:app_users_create' %}",
    r"{% url 'app_users_edit' %}": "{% url 'colaboradores:app_users_edit' %}",
    r"{% url 'app_users_delete' %}": "{% url 'colaboradores:app_users_delete' %}",
    r"{% url 'app_items' %}": "{% url 'equipamentos:app_items' %}",
    r"{% url 'app_items_create' %}": "{% url 'equipamentos:app_items_create' %}",
    r"{% url 'app_items_edit' %}": "{% url 'equipamentos:app_items_edit' %}",
    r"{% url 'app_items_delete' %}": "{% url 'equipamentos:app_items_delete' %}",
    r"{% url 'app_requests' %}": "{% url 'emprestimos:app_requests' %}",
    r"{% url 'app_requests_create' %}": "{% url 'emprestimos:app_requests_create' %}",
    r"{% url 'app_requests_edit' %}": "{% url 'emprestimos:app_requests_edit' %}",
    r"{% url 'app_requests_delete' %}": "{% url 'emprestimos:app_requests_delete' %}",
    r"{% url 'app_requests_return' %}": "{% url 'emprestimos:app_requests_return' %}",
    r"{% url 'app_history' %}": "{% url 'historico:app_history' %}",
    r"{% url 'app_reports' %}": "{% url 'relatorios:app_reports' %}",
}

# Process all HTML files in core/templates
templates_dir = "core/templates"
for filename in os.listdir(templates_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(templates_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated: {filename}")

print("All templates updated successfully!")
