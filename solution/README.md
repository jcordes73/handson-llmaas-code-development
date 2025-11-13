# Exercise 05 - Complete Solution

This directory contains the complete solution for Module 2.2: Building an AI-Powered Application.

## Contents

### `app.py`
The complete, working Flask application with all functions implemented:
- ✅ `get_tasks()` - Retrieve all tasks sorted by creation date
- ✅ `create_task()` - Create new tasks with validation
- ✅ `update_task()` - Update existing tasks (partial updates supported)
- ✅ `delete_task()` - Delete tasks by ID
- ✅ `call_ai_model()` - Helper function to call the AI model API with authentication
- ✅ `suggest_improvements()` - Get AI suggestions for individual tasks
- ✅ `analyze_tasks()` - Analyze all tasks using AI

### `SOLUTIONS.md`
Detailed solution guide with:
- Complete code for each function
- Key implementation points
- Common mistakes to avoid
- Alternative implementations
- Testing checklist
- Extension activities for advanced students

## How to Use This Solution

### As an Instructor
- Use this as a reference implementation
- Share with students after they complete the exercise
- Use code snippets to help students who are stuck
- Demonstrate best practices

### As a Student
- Try to complete the exercise on your own first
- Use this as a reference if you get stuck
- Compare your solution with this one
- Learn from the alternative implementations

## Running the Solution

1. Copy `app.py` to the main exercise directory (replace the incomplete version)
2. Set up environment variables:
   ```bash
   export AI_MODEL_URL="http://granite-instruct-vllm.{user}-ai-models.svc.cluster.local:8000/v1/chat/completions"
   export AI_MODEL_NAME="granite-3.0-8b-instruct"
   export AI_API_TOKEN="your-api-token-here"
   export PORT=8080
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python3.11 app.py
   ```

## Key Features

### Authentication
The solution properly implements Bearer token authentication for API calls to the AI model, ensuring secure communication.

### Error Handling
All endpoints include proper error handling:
- 400 for bad requests (missing required fields)
- 404 for not found resources
- 500 for internal server errors (AI model failures)

### Best Practices
- Uses global declarations where needed
- Implements partial updates for PUT requests
- Returns appropriate HTTP status codes
- Includes proper timeout handling
- Uses type hints in function signatures

## Testing the Solution

See the detailed testing checklist in `SOLUTIONS.md` for comprehensive testing scenarios.

## Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- OpenAI API Reference: https://platform.openai.com/docs/api-reference
- Continue.dev Documentation: https://docs.continue.dev/
