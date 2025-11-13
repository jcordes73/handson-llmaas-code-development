"""
AI-Powered Task Manager Application
A simple Flask web application for managing tasks with AI-generated suggestions.

Students will complete the missing functions using Continue.dev AI assistant.
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
    # TODO: Implement this function to return all tasks
    # Return tasks sorted by creation date (newest first)
    # Each task should include: id, title, description, status, created_at, priority
    pass


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.
    Expected JSON body: { "title": "Task title", "description": "Task description", "priority": "medium" }
    """
    # TODO: Implement this function to create a new task
    # 1. Get JSON data from request
    # 2. Validate that title is provided
    # 3. Create a new task with: id, title, description, status='pending', created_at, priority
    # 4. Add task to the tasks list
    # 5. Return the created task with status code 201
    pass


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task.
    Expected JSON body: { "title": "Updated title", "description": "Updated description", "status": "completed", "priority": "high" }
    """
    # TODO: Implement this function to update a task
    # 1. Find the task by task_id
    # 2. Update the task fields that are provided in the request
    # 3. Return the updated task
    # 4. Return 404 if task not found
    pass


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task by ID.
    """
    global tasks

    # TODO: Implement this function to delete a task
    # 1. Find the task by task_id
    # 2. Remove it from the tasks list
    # 3. Return success message
    # 4. Return 404 if task not found
    pass


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

    # TODO: Implement this function to get AI suggestions
    # 1. Create a prompt for the AI model asking for task improvement suggestions
    #    Example: "Given this task: [title and description], suggest 3 concrete next steps or improvements"
    # 2. Call the call_ai_model() function with the prompt
    # 3. Return the AI's response
    # 4. Handle any errors from the AI model call
    pass


@app.route('/api/tasks/analyze', methods=['POST'])
def analyze_tasks():
    """
    Use AI to analyze all tasks and provide insights.
    Expected JSON body: { "analysis_type": "priority" | "completion" | "overview" }
    """
    # TODO: Implement this function to analyze tasks using AI
    # 1. Get analysis_type from request JSON
    # 2. Create a prompt based on analysis_type:
    #    - "priority": Ask AI to suggest which tasks should be prioritized
    #    - "completion": Ask AI to estimate completion timeline
    #    - "overview": Ask AI to provide a summary of all tasks
    # 3. Include relevant task information in the prompt
    # 4. Call the call_ai_model() function
    # 5. Return the analysis results
    pass


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
    # TODO: Implement this function to call the AI model
    # 1. Create headers with Authorization token:
    #    headers = {
    #        "Content-Type": "application/json",
    #        "Authorization": f"Bearer {AI_API_TOKEN}"
    #    }
    # 2. Create the request payload with:
    #    - model: AI_MODEL_NAME
    #    - messages: [{"role": "user", "content": prompt}]
    #    - max_tokens: max_tokens
    #    - temperature: 0.7
    # 3. Make a POST request to AI_MODEL_URL with headers and JSON payload
    # 4. Extract and return the response text from: response.json()['choices'][0]['message']['content']
    # 5. Handle connection errors and return appropriate error messages
    # 6. Add timeout of 30 seconds to the request
    pass


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
