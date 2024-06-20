import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("API_KEY")

# Configure the Google Generative AI with API key
genai.configure(api_key=os.environ["API_KEY"])

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def create_dockerfile(service_name):
    # Generate Dockerfile content using the Gemini API
    prompt = f"""
    Write a Dockerfile with the following specifications:
    * Base image: Ubuntu latest
    * Service to run: {service_name} (e.g., FTP server, web server, mail server)
    * Ensure the service starts properly.

    **Assumptions:**
    * The Dockerfile should be minimal, including only essential instructions for setting up the {service_name} environment.
    * Avoid using unnecessary commands like `COPY` or `ADD` for copying application code or configuration files since there are no configuration files present.
    * Use package managers like `apt-get` for installing required dependencies.
    * Configuration and setup specific to {service_name} should be handled within the Dockerfile.

    **Exclusions:**
    * Do not include unnecessary instructions for directories or configurations that are not explicitly required by {service_name}.
    * Exclude placeholders or comments that are not directly related to the setup of {service_name}.
    Provide the Dockerfile content without leading and trailing dockerfile markers.
    """
    
    response = model.generate_content(prompt)
    content = response.text
    lines = content.split('\n')
    lines_to_write = lines[1:-1]
    new_content = '\n'.join(lines_to_write)
    # Write the content to a Dockerfile
    file_path = 'Dockerfile'
    with open(file_path, 'w') as file:
        file.write(new_content)
    
    print(f'Content written to {file_path}')

def build_and_run_container(port):
    try:
        # Build the Docker image from the Dockerfile
        build_command = ["docker", "build", "-t", "custom_service_image", "."]
        subprocess.run(build_command, check=True)
        
        # Run the Docker container
        run_command = ["docker", "run", "-d", "-p", f"{port}:{port}", "custom_service_image"]
        container_id = subprocess.check_output(run_command).decode('utf-8').strip()
        
        print(f"Container started with ID: {container_id}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    service_name = input("Enter the service name (ftp, web server, mail server): ").strip().lower()
    port = input("Enter the desired port for the service: ").strip()
    
    if not service_name or not port:
        print("Service name and port are required.")
    else:
        create_dockerfile(service_name)
        build_and_run_container(port)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         service_name = request.form['service_name'].strip().lower()
#         port = request.form['port'].strip()
        
#         if not service_name or not port:
#             flash("Service name and port are required.")
#             return redirect(url_for('index'))
        
#         create_dockerfile(service_name)
#         container_id = build_and_run_container(port)
        
#         if "error" in container_id.lower():
#             flash(f"An error occurred: {container_id}")
#         else:
#             flash(f"Container started with ID: {container_id}")
        
#         return redirect(url_for('index'))
    
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(debug=True)