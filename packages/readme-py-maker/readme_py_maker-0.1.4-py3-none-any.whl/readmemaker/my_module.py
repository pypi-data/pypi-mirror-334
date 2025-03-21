import argparse
from github import Github
import os
import nbformat
from nbconvert import PythonExporter
from groq import Groq

def convert_notebook_to_script(notebook_content):
    notebook_node = nbformat.reads(notebook_content, as_version=4)
    exporter = PythonExporter()
    script_content, _ = exporter.from_notebook_node(notebook_node)
    return script_content

def get_bot_response(text, file_name, groq_client):
    original_extension = os.path.splitext(file_name)[1]
    if not original_extension and '_' in file_name:
        parts = file_name.split('_')
        if len(parts) > 0:
            original_extension = '.' + parts[0]
    
    detailed_prompt = f"""I am making a GitHub readme file maker. I will provide you with code from a {original_extension} file, and I need you to write a 100-200 word description for that code. 

    Here is the code of the file: {text}

    Make sure you cover:
    1. What programming language this is
    2. Any module packages or libraries used
    3. The primary purpose of the code
    4. Key functionalities 

    I will combine all descriptions to generate a final readme file. Focus only on describing this specific file's code. Keep your response between 100-200 words."""

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": detailed_prompt}
        ],
        model="llama3-8b-8192",
        max_tokens=1000
    )

    return chat_completion.choices[0].message.content

def get_bot_response_readme(text, groq_client, additional_info, basic_markdown, demo_readme):
    detailed_prompt = f"""I am giving you brief descriptions about each code file in my project. Please create a comprehensive GitHub README.md file using all this information.

    Here are the file descriptions: {text}

    The README should include:
    1. Project title and brief overview
    2. Installation instructions
    3. Usage examples
    4. Code explanations with appropriate code snippets
    5. Project structure
    6. Dependencies

    Format the README with proper Markdown syntax including headers, code blocks, lists, etc. Make it professional, complete, and easy to understand for developers of any level. Add several emojis and proper formatting of text to make it more visually appealing, like adding bold text, italics, headers, etc. Make sure the read me file is visually appealing and easy to read. I am providing you with some syntax examples of markdown language, make sure you use them to make more visually aesthetic. Here it is {basic_markdown}. This is what a demo readme file looks like, you can use this as a reference: {demo_readme}, make sure you stay very close to this.Components like this [![Next.js](https://img.shields.io/badge/Built%20with-Next.js-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
    looks good in the readme file, so make sure you add them. This is additional information you NEED to add to the readme file: {additional_info}"""

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": detailed_prompt}
        ],
        model="llama-3.3-70b-versatile",
        max_tokens=10000
    )

    return chat_completion.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description='Generate a README.md file for a GitHub repository.')
    parser.add_argument('-r', '--repo', required=True, help='GitHub repository in the format "owner/repo"')
    parser.add_argument('-k', '--key', required=True, help='GitHub API key')
    args = parser.parse_args()

    g = Github(args.key)
    repo = g.get_repo(args.repo)

    additional_info = input("Do you want to add any additional information to the README? (y/n): ")
    if additional_info.lower() == 'y':
        additional_info = input("Enter the additional information you want to add: ")
        with open(r'additional_info_ai.txt', 'w', encoding='utf-8') as additional_info_file:
            additional_info_file.write(additional_info)

    groq_client = Groq(api_key=args.key)
    folder_path = r"Readme Maker"
    outside_path = os.path.join(os.getcwd())
    output_folder = folder_path
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    code_extensions = [
        '.py', '.ipynb',
        '.html', '.css', '.js', '.jsx', '.ts', '.tsx',
        '.c', '.cpp', '.h', '.hpp', '.cs',
        '.java', '.kt',
        '.rb', '.php', '.go',
        '.rs', '.swift',
        '.sh', '.bash',
        '.r', '.scala', '.lua', '.pl', '.sql'
    ]

    contents = repo.get_contents("") 

    while contents:
        file_content = contents.pop(0)

        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path)) 

        else:
            file_extension = os.path.splitext(file_content.path)[1].lower()

            if file_extension in code_extensions:
                if file_extension == '.ipynb':
                    try:
                        notebook_content = file_content.decoded_content.decode("utf-8")
                        python_script = convert_notebook_to_script(notebook_content)

                        output_basename = os.path.basename(file_content.path).replace('.ipynb', '')
                        python_file_path = os.path.join(output_folder, output_basename + '.py')
                        with open(python_file_path, 'w', encoding='utf-8') as py_file:
                            py_file.write(python_script)

                        text_file_path = os.path.join(output_folder, output_basename + '.txt')
                        with open(text_file_path, 'w', encoding='utf-8') as text_file:
                            text_file.write(python_script)
                    except Exception as e:
                        print(f"Error processing notebook {file_content.path}: {e}")
                else:
                    try:
                        file_content_text = file_content.decoded_content.decode("utf-8")
                        output_basename = os.path.basename(file_content.path)
                        text_file_path = os.path.join(output_folder, output_basename.replace(file_extension, '.txt'))

                        with open(text_file_path, 'w', encoding='utf-8') as text_file:
                            text_file.write(file_content_text)
                    except UnicodeDecodeError:
                        print(f"Could not decode {file_content.path} as UTF-8, skipping")
                    except Exception as e:
                        print(f"Error processing {file_content.path}: {e}")

    while True:
        text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt') and not f.endswith('_ai.txt')]
        
        for text_file in text_files:
            text_file_path = os.path.join(folder_path, text_file)
            
            with open(text_file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            
            response = get_bot_response(text_content, text_file, groq_client)
            
            text_file_base = text_file.replace('.txt', '')
            ai_text_file_path = os.path.join(folder_path, f"{text_file_base}_ai.txt")
            with open(ai_text_file_path, 'w', encoding='utf-8') as ai_file:
                ai_file.write(f"Response for {text_file}:\n{response}\n\n")
        break

    with open(r'demo_readme.txt', 'r', encoding='utf-8') as readme_file:
        demo_readme = readme_file.read()

    with open(r'basic_markdown.txt', 'r', encoding='utf-8') as readme_file:
        basic_markdown = readme_file.read()

    all_text = ""

    for file_name in os.listdir(folder_path):
        if file_name.endswith('_ai.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                all_text += file.read() + "\n"

    final_response = get_bot_response_readme(all_text, groq_client, additional_info, basic_markdown, demo_readme)

    readme_path = os.path.join(outside_path, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        readme_file.write(final_response)

    print(f"README.md has been created at {readme_path}")

if __name__ == "__main__":
    main()