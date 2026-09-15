# Code Reviewer

Code Reviewer is a Python command-line tool that uses the Google Gemini API to review code changes and report potential bugs, security issues, performance problems, and code quality concerns.

## Features

- Review staged Git changes locally.
- Audit an individual source file.
- Run automatically with GitHub Actions.
- Review pull requests and pushes to the `main` branch.
- Detect bugs, security issues, performance problems, and style issues.

## Requirements

- Python 3.11 or newer
- Git
- A Google Gemini API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/miguelromorsk06/Code-Reviewer.git
cd Code-Reviewer
```

### 2. Create a virtual environment

#### Linux and macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

## Configure the Gemini API key

Create a Gemini API key using [Google AI Studio](https://aistudio.google.com/apikey).

For local use, create a file named `.env` in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your real API key.

Never commit your `.env` file or expose your API key in the source code. The `.env` file is already excluded by `.gitignore`.

## Local usage

### Review staged Git changes

First, stage the files you want to review:

```bash
git add path/to/file.py
```

Then run the reviewer:

```bash
python main.py
```

The program analyzes the staged Git diff and reports:

- File name
- Approximate line number
- Severity
- Category
- Explanation
- Suggested fix

Example:

```text
[HIGH] app.py (line ~24)
Category: security
User input is used without validation.
Suggestion: Validate and sanitize the input before processing it.
```

If there are no staged changes, the program reports that there is no diff to review.

### Audit an entire file

To perform a broader audit of an individual file, run:

```bash
python main.py --audit path/to/file.py
```

Audit mode evaluates areas such as:

- Readability
- Maintainability
- Architecture
- Complexity
- Security
- Performance
- Error handling
- Testing
- Scalability
- Code quality

## GitHub Actions

The project includes a GitHub Actions workflow located at:

```text
.github/workflows/code-review.yml
```

The workflow runs when:

- A pull request is opened.
- A pull request is updated.
- A pull request is reopened.
- A commit is pushed directly to `main`.
- It is started manually from GitHub Actions.

### Configure the GitHub secret

Before using GitHub Actions, add your Gemini API key as a repository secret:

1. Open your repository on GitHub.
2. Go to **Settings**.
3. Open **Secrets and variables**.
4. Select **Actions**.
5. Click **New repository secret**.
6. Set the name to:

```text
GEMINI_API_KEY
```

7. Paste your Gemini API key as the value.
8. Save the secret.

The workflow uses this secret without exposing it in the logs.

## Recommended Pull Request workflow

GitHub Actions runs after a push has already reached GitHub. Therefore, Actions cannot prevent a direct push to `main`.

The recommended workflow is to use a separate branch and a Pull Request.

### 1. Create a branch

```bash
git switch -c my-change
```

### 2. Make your changes

Modify the project files as required.

### 3. Commit your changes

```bash
git add .
git commit -m "Describe the change"
```

### 4. Push the branch

```bash
git push -u origin my-change
```

### 5. Create a Pull Request

On GitHub:

1. Open your repository.
2. Click **Compare & pull request**.
3. Select `main` as the base branch.
4. Select `my-change` as the compare branch.
5. Click **Create pull request**.

GitHub Actions will run automatically.

## Protect the main branch

To prevent unreviewed code from being merged into `main`:

1. Open the repository on GitHub.
2. Go to **Settings**.
3. Open **Rules** or **Branches**.
4. Create a ruleset or branch protection rule for `main`.
5. Enable:

```text
Require a pull request before merging
Require status checks to pass before merging
```

Select the Code Reviewer GitHub Actions check as a required status check.

With this configuration:

```text
Push to a working branch
        |
        v
Create a Pull Request
        |
        v
GitHub Actions runs the review
        |
        +--> Review passes: merge allowed
        |
        +--> Review fails: merge blocked
```
## Add the reviewer to another repository

To use this reviewer in another GitHub repository, create the following file in the target repository:

```text
.github/workflows/code-review.yml
```

Paste this workflow into that file:

```yaml
name: Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

  push:
    branches:
      - main
      - master

  workflow_dispatch:

jobs:
  review:
    runs-on: ubuntu-latest

    steps:
      # Check out the repository that will be reviewed.
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Download the reviewer from the Code-Reviewer repository.
      - name: Checkout Code Reviewer
        uses: actions/checkout@v4
        with:
          repository: miguelromorsk06/Code-Reviewer
          ref: main
          path: reviewer

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r reviewer/requirements.txt

      - name: Run AI Code Review
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          BASE_REF: ${{ github.event.pull_request.base.ref }}
          DIFF_BASE: ${{ github.event.before }}
        run: python reviewer/main.py
```

This workflow is required in every repository where you want to use the
reviewer. A workflow stored in `Code-Reviewer` is not automatically applied to
other repositories.

The workflow performs the following actions:

1. Checks out the repository that will be reviewed.
2. Downloads the `Code-Reviewer` project.
3. Installs Python 3.11.
4. Installs the reviewer's dependencies.
5. Runs the AI code review.

The workflow runs when:

- A pull request is opened.
- A pull request is updated.
- A pull request is reopened.
- A commit is pushed to `main`.
- A commit is pushed to `master`.
- The workflow is started manually.

## Configure the Gemini API key

In the target repository, go to:

```text
Settings → Secrets and variables → Actions
```

Create a new repository secret with the exact name:

```text
GEMINI_API_KEY
```

Paste your Gemini API key as the value.

The `Code-Reviewer` repository must be public so that GitHub Actions can
download it. If it is private, the checkout step requires a token with read
access to that repository.

## Recommended Pull Request workflow

GitHub Actions runs after a push has already reached GitHub. Therefore, it
cannot prevent a direct push to `main` or `master`.

The recommended workflow is:

```text
Create a working branch
        ↓
Push the working branch
        ↓
Create a Pull Request
        ↓
GitHub Actions runs the review
        ↓
Merge only if the required checks pass
```

To protect the main branch, configure a branch ruleset in:

```text
Settings → Rules → Rulesets
```

Enable:

- Require a pull request before merging.
- Require status checks to pass before merging.

This prevents reviewed code from being merged into `main` or `master` when the
required GitHub Actions check fails.
## Important limitations

- GitHub Actions cannot undo a push that has already happened.
- A direct push to `main` is already present before GitHub Actions starts.
- A Gemini `503 UNAVAILABLE` error means that the Gemini service is temporarily unavailable.
- If Gemini is unavailable, the workflow may fail and should be retried later.
- The current program prints review findings in the terminal.
- The current program does not automatically create GitHub review comments.
- Findings do not currently fail the workflow automatically based only on their severity.
- Never commit your Gemini API key.

## Project structure

| File | Description |
| --- | --- |
| `main.py` | Main command-line entry point |
| `CallGemini.py` | Sends requests to the Gemini API |
| `DiffGit.py` | Obtains the staged or GitHub Actions Git diff |
| `Promts.py` | Contains the review prompts |
| `ParserJson.py` | Parses Gemini's JSON response |
| `TerminalOutput.py` | Displays review findings |
| `Read_Rutes.py` | Reads files for audit mode |
| `requirements.txt` | Python dependencies |
| `.github/workflows/code-review.yml` | GitHub Actions workflow |

## Troubleshooting

### Gemini API key error

Check that:

- The `.env` file exists in the project root for local use.
- The variable is named exactly `GEMINI_API_KEY`.
- The GitHub secret is also named exactly `GEMINI_API_KEY`.
- The API key is valid.

### No changes are detected

Make sure that your changes are staged:

```bash
git add .
git diff --staged
```

Then run:

```bash
python main.py
```

### Gemini returns a 503 error

A `503 UNAVAILABLE` error usually means that Gemini is temporarily overloaded or unavailable.

Wait a few moments and run the workflow again:

```text
GitHub → Actions → Code-Reviewer → Re-run jobs
```

## License

No license has been specified for this repository yet.