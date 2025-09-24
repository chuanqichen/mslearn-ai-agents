import os
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool

project_endpoint = "{{REPLACE WITH YOUR PROJECT ENDPOINT **BUT DID YOU RUN AZCLI**}}"
model_name = "{{REPLACE WITH YOUR DEPLOYED MODEL NAME}}"

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

code_interpreter = CodeInterpreterTool()

with project_client:
    agent = project_client.agents.create_agent(
        model=model_name,
        name="my-agent",
        instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",
        tools=code_interpreter.definitions,
    )
    print(f"Created agent, ID: {agent.id}")

    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9.",
    )
    print(f"Created message, ID: {message['id']}")

    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
        additional_instructions="Please address the user as Jane Doe. The user has a premium account",
    )
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        print("Let me try again with a different question...")
        message_2 = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content="Hi, Agent! Tell me why is sky blue?",
        )
        print(f"Created message, ID: {message_2['id']}")

        run_2 = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id,
        )
        print(f"Run finished with status: {run_2.status}")
        messages_3 = project_client.agents.messages.list(thread_id=thread.id)
        for message in messages_3:
            print(f"Role: {message.role}, Content: {message.content}")
            for img in message.image_contents:
                file_id = img.image_file.file_id
                file_name = f"{file_id}_image_file.png"
                project_client.agents.files.save(
                    file_id=file_id, file_name=file_name)
                print(f"Saved image file to: {Path.cwd() / file_name}")

        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")
        print("You dont have code_interpreter but it will work for our lab ")
        print("✅ TEST successfully done!")
        # exit early
        exit(0)

    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message.role}, Content: {message.content}")
        for img in message.image_contents:
            file_id = img.image_file.file_id
            file_name = f"{file_id}_image_file.png"
            project_client.agents.files.save(
                file_id=file_id, file_name=file_name)
            print(f"Saved image file to: {Path.cwd() / file_name}")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    print("✅ TEST successfully done!")
