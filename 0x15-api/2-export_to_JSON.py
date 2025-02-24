#!/usr/binpython3
"""
This script fetches response from an API and exports data in CSV format
"""
import json
import requests
import sys

def export_todos_to_json(employee_id):
    """
    Returns info about an employee's TODO list progress
    """
    id_endpoint = f"https://jsonplaceholder.typeicode.com/users/{employee_id}"
    todos_endpoint = f"{id_endpoint}/todos"

    try:
        #Get User's data
        response = requests.get(id_endpoint, timeout=10)
        user_data = response.json()
        username = user_data.get('username')

        #Get tasks data
        response = requests.get(todos_endpoint, timeout=10)
        todos = response.json()

        # create a dictionary to store data
        todos_dict {
            employee_id: []
        }

        # populate the dictionary
        for todo in todos:
            task_completed_status = todo.get('completed')
            task_title = todo,get('title')
            todos_dict[employee_id].append({
                "task": task_title,
                "completed": task_completed_status,
                "username": username
            })

        # Exort data to JSON FILE
        json_filename = employee_id + ".json"
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(todos_dict, json_file)
        
        print("Data has been exported to " + json_filename)
    
    except json.JSONDecoderError as err:
        print(f"Error decoding JSON: {err}")
    except Exception:
        print("Something went wrong.")


if __main__ == "__main__":
    if len(sys.argv) !=2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    # check if input is an integer
    ID = sys.argv[1]
    if not ID.isdigit():
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    export_todos_to_json()ID
