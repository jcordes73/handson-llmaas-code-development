# Solution Guide for Module 05

This document contains reference implementations for all incomplete functions in `app.py`. These solutions can be shared with students after they complete the exercise or used by instructors for reference.

## Function 1: `get_tasks()`

```python
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks.
    Returns a JSON array of all tasks.
    """
    # Sort tasks by creation date (newest first)
    sorted_tasks = sorted(tasks, key=lambda x: x['created_at'], reverse=True)
    return jsonify(sorted_tasks), 200
```

**Key Points:**
- Uses Python's `sorted()` with a lambda function to sort by `created_at`
- `reverse=True` gives newest first
- Returns JSON with status 200

## Function 2: `create_task()`

```python
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
```

**Key Points:**
- Must declare `global task_counter` to modify it
- Validates title exists before proceeding
- Uses `.get()` with defaults for optional fields
- Returns status 201 (Created) for successful creation
- Uses `.isoformat()` for datetime serialization

## Function 3: `update_task()`

```python
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
```

**Key Points:**
- Finds task by iterating through the list
- Returns 404 if not found
- Only updates fields that are present in the request (partial updates)
- Uses `in data` to check for field presence

**Alternative Solution (more concise):**
```python
# Update only provided fields
for field in ['title', 'description', 'status', 'priority']:
    if field in data:
        task[field] = data[field]
```

## Function 4: `delete_task()`

```python
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
```

**Key Points:**
- Must declare `global tasks` to modify the list
- Finds and removes in separate steps for clarity
- Returns success message, not the deleted task

**Alternative Solution (list comprehension):**
```python
global tasks
initial_length = len(tasks)
tasks = [t for t in tasks if t['id'] != task_id]

if len(tasks) == initial_length:
    return jsonify({'error': 'Task not found'}), 404

return jsonify({'message': 'Task deleted successfully'}), 200
```

## Function 5: `call_ai_model()`

```python
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
```

**Key Points:**
- Creates headers with Authorization Bearer token for API authentication
- Follows OpenAI chat completion API format
- Includes timeout to prevent hanging requests
- Uses `raise_for_status()` to catch HTTP errors
- Extracts content from nested JSON structure
- Re-raises with descriptive error message

## Function 6: `suggest_improvements()`

```python
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
```

**Key Points:**
- Creates a clear, structured prompt with all task context
- Uses try-except to handle AI model errors gracefully
- Returns 500 (Internal Server Error) for AI failures
- Limits tokens to 300 for concise suggestions

**Prompt Engineering Tips:**
- Be specific: "3 specific, actionable next steps"
- Provide context: Include all relevant task fields
- Set expectations: "to help complete this task effectively"

## Function 7: `analyze_tasks()`

```python
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
```

**Key Points:**
- Supports three different analysis types with different prompts
- Formats tasks in a readable list format for the AI
- Handles empty task list gracefully
- Uses dictionary to map analysis types to prompts
- Falls back to 'overview' for unknown analysis types

**Enhancement Ideas:**
- Add task count and completion percentage to prompt
- Include timestamps for time-based analysis
- Filter completed vs. pending tasks differently

## Testing the Complete Application

### Manual Testing Checklist

1. **Create Tasks**
   - Try with all required fields
   - Try with only title (should work)
   - Try without title (should return 400 error)
   - Test all priority levels

2. **Get Tasks**
   - Verify newest tasks appear first
   - Check JSON format is correct

3. **Update Tasks**
   - Update individual fields
   - Update multiple fields at once
   - Try updating non-existent task (should return 404)

4. **Delete Tasks**
   - Delete existing task
   - Try deleting non-existent task (should return 404)

5. **AI Suggestions**
   - Test with different task types
   - Verify suggestions are relevant
   - Check error handling when AI model is unavailable

6. **AI Analysis**
   - Test all three analysis types
   - Verify with different task sets
   - Check with empty task list

### Automated Testing (Optional Enhancement)

Students could add these pytest tests:

```python
def test_create_task():
    response = client.post('/api/tasks', json={
        'title': 'Test Task',
        'priority': 'high'
    })
    assert response.status_code == 201
    assert response.json['title'] == 'Test Task'

def test_create_task_missing_title():
    response = client.post('/api/tasks', json={})
    assert response.status_code == 400

def test_get_tasks():
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)
```

## Common Student Mistakes

1. **Forgetting `global` declarations**
   - Symptom: Variables don't update
   - Fix: Add `global task_counter` or `global tasks`

2. **Not handling missing data**
   - Symptom: KeyError exceptions
   - Fix: Use `.get()` with defaults

3. **Incorrect JSON extraction**
   - Symptom: AI responses not showing
   - Fix: Verify path `['choices'][0]['message']['content']`

4. **No error handling**
   - Symptom: App crashes on AI failures
   - Fix: Wrap AI calls in try-except

5. **Wrong HTTP status codes**
   - Created should be 201, not 200
   - Not found should be 404
   - Server errors should be 500

## Extension Activities

For advanced students who finish early:

1. **Add task filtering**: Filter by priority or status
2. **Add task search**: Search by title/description
3. **Add batch operations**: Complete all tasks at once
4. **Add task categories/tags**: Organize tasks better
5. **Add due dates**: Track task deadlines
6. **Persist to database**: Use SQLite or PostgreSQL
7. **Add user authentication**: Flask-Login integration
8. **Add task history**: Track all changes to tasks
9. **Improve AI prompts**: More sophisticated prompt engineering
10. **Add streaming responses**: Stream AI responses for better UX
