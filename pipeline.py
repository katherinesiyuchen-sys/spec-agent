from groq import Groq
import json

client = Groq()  

def spec_to_tasks(spec: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""You are a senior software engineer breaking down a feature spec into dev tasks.

Given this spec: {spec}

Return ONLY a JSON array of tasks, each with:
- title: short task name
- description: what needs to be done
- acceptance_criteria: how you know it's done
- effort: small / medium / large

No preamble, no markdown, just raw JSON."""
            }
        ]
    )
    
    tasks = json.loads(response.choices[0].message.content)
    return tasks


def review_tasks(spec: str, tasks: list):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""You are a senior engineer reviewing a task breakdown.

Original spec: {spec}

Task list:
{json.dumps(tasks, indent=2)}

Review this task list and return ONLY a JSON object with:
- missing_tasks: list of important tasks that were missed
- ambiguous_tasks: list of task titles that need clearer acceptance criteria
- overall_quality: good / needs_work / poor
- summary: 1-2 sentence verdict

No preamble, no markdown, just raw JSON."""
            }
        ]
    )
    
    review = json.loads(response.choices[0].message.content)
    return review


def run_pipeline(spec: str):
    print(f"📋 Spec: {spec}\n")
    
    print("🔨 Generating tasks...")
    tasks = spec_to_tasks(spec)
    
    print("🔍 Reviewing tasks...")
    review = review_tasks(spec, tasks)
    
    print("\n--- TASKS ---")
    for task in tasks:
        print(f"\n✅ {task['title']} [{task['effort']}]")
        print(f"   {task['description']}")
        print(f"   Done when: {task['acceptance_criteria']}")
    
    print("\n--- REVIEW ---")
    print(f"Quality: {review['overall_quality']}")
    print(f"Summary: {review['summary']}")
    
    if review['missing_tasks']:
        print(f"Missing: {', '.join(review['missing_tasks'])}")
    if review['ambiguous_tasks']:
        print(f"Ambiguous: {', '.join(review['ambiguous_tasks'])}")


run_pipeline("Build a login page with email and Google OAuth")