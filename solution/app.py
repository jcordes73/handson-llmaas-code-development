"""
AI-Powered Task Manager Application
A simple Flask web application for managing tasks with AI-generated suggestions.

This is the COMPLETE SOLUTION with all functions implemented.
"""

from flask import Flask, render_template, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

# In-memory storage for tasks (in production, use a database)
tasks = []
task_counter = 1

# AI Model Configuration
AI_MODEL_URL = os.getenv('AI_MODEL_URL', 'http://localhost:8000/v1/chat/completions')
AI_MODEL_NAME = os.getenv('AI_MODEL_NAME', 'granite-3.0-8b-instruct')
AI_API_TOKEN = os.getenv('AI_API_TOKEN', '')


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks.
    Returns a JSON array of all tasks.
    """
    # Sort tasks by creation date (newest first)
    sorted_tasks = sorted(tasks, key=lambda x: x['created_at'], reverse=True)
    return jsonify(sorted_tasks), 200


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.
    Expected JSON body: { "title": "Task title", "description": "Task description", "priority": "medium" }
    """
    global task_counter

    # Get JSON data from request
    data = request.get_json()

    # Validate that title is provided
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    # Create a new task
    task = {
        'id': task_counter,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'priority': data.get('priority', 'medium')
    }

    # Increment counter and add to tasks
    task_counter += 1
    tasks.append(task)

    return jsonify(task), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task.
    Expected JSON body: { "title": "Updated title", "description": "Updated description", "status": "completed", "priority": "high" }
    """
    # Find the task by task_id
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Get update data
    data = request.get_json()

    # Update only provided fields
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'status' in data:
        task['status'] = data['status']
    if 'priority' in data:
        task['priority'] = data['priority']

    return jsonify(task), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task by ID.
    """
    global tasks

    # Find the task by task_id
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Remove from tasks list
    tasks.remove(task)

    return jsonify({'message': 'Task deleted successfully'}), 200


@app.route('/api/tasks/<int:task_id>/suggest', methods=['POST'])
def suggest_improvements(task_id):
    """
    Use AI to suggest improvements or next steps for a task.
    This endpoint calls the AI model to generate suggestions.
    """
    # Find the task
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Create prompt for AI model
    prompt = f"""Given this task:

Title: {task['title']}
Description: {task['description']}
Priority: {task['priority']}
Status: {task['status']}

Please provide 3 specific, actionable next steps or improvements to help complete this task effectively."""

    try:
        # Call AI model
        suggestions = call_ai_model(prompt, max_tokens=300)
        return jsonify({'suggestions': suggestions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/analyze', methods=['POST'])
def analyze_tasks():
    """
    Use AI to analyze all tasks and provide insights.
    Expected JSON body: { "analysis_type": "priority" | "completion" | "overview" }
    """
    # Get analysis type from request
    data = request.get_json()
    analysis_type = data.get('analysis_type', 'overview')

    # Format tasks for the prompt
    task_list = []
    for task in tasks:
        task_info = f"- [{task['priority'].upper()}] {task['title']}"
        if task['description']:
            task_info += f": {task['description']}"
        task_info += f" (Status: {task['status']})"
        task_list.append(task_info)

    task_summary = "\n".join(task_list) if task_list else "No tasks available."

    # Create prompt based on analysis type
    prompts = {
        'priority': f"""Here are my current tasks:

{task_summary}

Based on the priorities and descriptions, which tasks should I focus on first and why? Provide a recommended order with brief reasoning.""",

        'completion': f"""Here are my current tasks:

{task_summary}

Estimate roughly how long these tasks might take to complete and suggest an order for tackling them to be most efficient.""",

        'overview': f"""Here are my current tasks:

{task_summary}

Provide a brief overview and insights about this task list. What patterns do you notice? Any suggestions for better task management?"""
    }

    # Get the appropriate prompt
    prompt = prompts.get(analysis_type, prompts['overview'])

    try:
        # Call AI model
        analysis = call_ai_model(prompt, max_tokens=500)
        return jsonify({'analysis': analysis}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def call_ai_model(prompt, max_tokens=500):
    """
    Helper function to call the AI model API.

    Args:
        prompt (str): The prompt to send to the AI model
        max_tokens (int): Maximum tokens in the response

    Returns:
        str: The AI model's response text

    Raises:
        Exception: If the API call fails
    """
    # Create headers with Authorization token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AI_API_TOKEN}'
    }

    # Create the request payload
    payload = {
        'model': AI_MODEL_NAME,
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'max_tokens': max_tokens,
        'temperature': 0.7
    }

    try:
        # Make POST request to AI model with headers
        response = requests.post(
            AI_MODEL_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        # Extract and return the response text
        result = response.json()
        return result['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to call AI model: {str(e)}")


@app.route('/health')
def health():
    """Health check endpoint for OpenShift."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'tasks_count': len(tasks)
    })


if __name__ == '__main__':
    # Run the Flask app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
