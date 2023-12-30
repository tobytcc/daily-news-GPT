# Setup Instructions

To get started with the project, please follow the steps below:

1. **Install Rust:**  
    Before installing the Python packages, ensure you have Rust installed. This is required for some of the dependencies.

    Install Rust by visiting https://rustup.rs/ and following the instructions.

3. **Clone the Repository:**  
    If you haven't already, clone the repository to your local machine and go into it
    ```bash
    git clone https://github.com/tobytcc/daily-news-GPT.git
    cd daily-news-GPT
    ```

3. **Setup a Virtual Environment:**  
    It's a good practice to create a virtual environment for your Python projects to ensure dependencies do not interfere with each other.

   - **For macOS/Linux:**
     ```bash
     python -m venv env
     source env/bin/activate
     ```

   - **For Windows (Command Prompt):**
     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```

     After this, next time you work with the project, only the second line is necessary for both windows and mac.  
     (```source env/bin activate``` and ```env/Scripts/activate```)

4. **Checkout to the Appropriate Branch:**  
    If you're planning to view the changes in my branch in your local env:
    ```bash
    git pull origin kevin_webscraping
    git checkout -b [your_new_branch_name]
    ```

    Alternatively, if the PR to the master has been approved and merged, you can pull the latest changes from the master:
    ```bash
    git pull origin master
    git checkout -b [your_new_branch_name]
    ```

5. **Install Python Dependencies:**  
    Navigate to the project directory and install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

6. **Setup Pre-commit:**  
    I think it will be best to use pre-commit hooks to ensure code quality. It checks for simple stuff like file formatting. Though there are 2 major pre-commit hooks I've decided to use: mypy and pylint  
    mypy: static type checker  
    pylint: good code practice checker, e.g. variable names or function, class, and module docstrings  
    <br>
    To set it up:
    ```bash
    pre-commit install
    ```

    To run your code amongst all of these checks, simply do:  
    ```bash
    pre-commit run --all-files
    ```
    or on individual files:
    ```bash
    pre-commit run --files <insert filepath1> <insert optional filepath2> ...
    ```

    Note: If you  need to bypass the pre-commit checks when committing, you can use the --no-verify flag with your git commit command:
    ```bash
    git commit -m "comments" --no-verify
    ```
    this will commit while ignoring pre-commit checks.  


This guide is made with help of GPT
