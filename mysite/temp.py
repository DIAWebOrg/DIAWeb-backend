from django.db import connection
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def debug_api_key():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM myapp_apikey WHERE id = %s', [6])
        row = cursor.fetchone()
    return row

# Call this function and check if it returns the expected result
debug_result = debug_api_key()
print(debug_result)