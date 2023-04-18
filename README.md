# unmask-mastermind

Clone this repository

```bash
git clone https://github.com/Cloudburst-E/unmask-mastermind.git
```

Navigate to the directory of the cloned repo

```bash
cd unmask-mastermind
```

### Set up the repo
---

#### Create a python virtual environment

- macOS

```bash
python3 -m venv venv
```

- Windows

```bash
python -m venv venv
```

#### Activate the virtual environment

- macOS

```bash
. venv/bin/activate
```

- Windows (in Bash, NOT Powershell)

```bash
source venv/Scripts/activate
```

#### Install the project in editable mode

```bash
pip install -e ".[dev]"
```

---

## Run scripts

To run the profiling:
Include SSH_PKEY, DB_USERNAME, and DB_PASS variable assignment in the .env file,
which correspond to SSH private key, database username, and database password.

```bash
export $(cat .env | xargs)
```

### Run the channels profiling pipeline:
   
```bash
run/run_channels_profiling.py
```
   
### Run the users profiling pipeline:

```bash
run/run_users_profiling.py
```

## Testing and Coverage

We use pytest as our testing framework and coverage to measure code coverage.

To run the tests:

```bash
pytest
```

To generate a coverage report:

```bash
coverage run -m pytest
coverage report
```

You can also use coverage html command to generate HTML files that you can view in a web browser.

## Git Large File Storage (Git LFS)

All files in [`data/`](data/) are stored with `lfs`.

To initialize Git LFS:

```bash
git lfs install
```

```bash
git lfs track data/**/*
```

To pull data files, use

```bash
git lfs pull
```

## Synchronize with the repo

Always pull the latest code first

```bash
git pull
```

Make changes locally, save. And then add, commit and push

```bash
git add [file-to-add]
git commit -m "update message"
git push
```

# Best practice

## Coding Style

We follow [PEP8](https://www.python.org/dev/peps/pep-0008/) coding format.
The most important rules above all:

1. Keep code lines length below 80 characters. Maximum 120. Long code lines are NOT readable.
1. We use snake_case to name function, variables. CamelCase for classes.
1. We make our code as DRY (Don't repeat yourself) as possible.
1. We give a description to classes, methods and functions.
1. Variables should be self explaining and just right long:
   - `implied_volatility` is preferred over `impl_v`
   - `implied_volatility` is preferred over `implied_volatility_from_broker_name`

## Do not

1. Do not place .py files at root level (besides setup.py)!
1. Do not upload big files > 100 MB.
1. Do not upload log files.
1. Do not declare constant variables in the MIDDLE of a function
