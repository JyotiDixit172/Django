# Error 1: Import "rest_framework.decorators" could not be resolved

## Section 1: Problem

`api/views.py` showed a squiggle on line 1 and the editor reported `reportMissingImports`, even though Django REST Framework was installed.

```
Import "rest_framework.decorators" could not be resolved
```

## Section 2: Environment

1. macOS, Cursor editor
2. Python 3.9.6 inside `.venv`
3. Django 4.2.30, djangorestframework 3.16.1
4. Workspace root: `Django`, project folder: `first-django-project` (venv sits one level below the root)
5. Language server: basedpyright (Cursor does not use Pylance)

## Section 3: Root cause

1. Cursor runs basedpyright, so Pylance steps did not apply.
2. The workspace root was `Django`, while `.venv` lives inside `first-django-project`, so the editor never found the venv.
3. The `python` file in `.venv/bin` is a symlink to Apple's Command Line Tools Python, so the interpreter picker rejected it as invalid.
4. The code was never broken. The import ran fine in the terminal.

## Section 4: Step 1, Confirm the code and install are fine

1. A bare `python -c` import fails with `ImproperlyConfigured` because no Django settings are loaded. This is expected and not a real error.
2. Run the import with settings loaded:

```
DJANGO_SETTINGS_MODULE=config.settings python -c "from rest_framework.decorators import api_view; print('ok')"
```

3. It prints `ok`, so the problem is only the editor.
4. In a new terminal without `(.venv)`, `pip` is not found. Use the venv python directly:

```
.venv/bin/python -m pip list | grep -i django
```

5. Output shows Django 4.2.30 and djangorestframework 3.16.1, so the venv is intact.

## Section 5: Step 2, Identify the language server

1. Hover over the error in `views.py`.
2. The message ends with `basedpyright(reportMissingImports)`, which shows the editor uses basedpyright, not Pylance.

## Section 6: Step 3, Approaches that did not work

1. Selecting the interpreter through the picker (Browse, or typing the path). It failed with "Selected file is not a valid Python interpreter" because the venv `python` symlink resolves to Apple's Python.
2. Setting `python.defaultInterpreterPath`. It only applies on first load and caused a "could not be resolved" warning.
3. A leftover `python-envs.defaultEnvManager` setting pushed the picker toward system Python.
4. Pasting config into `rest_framework/__init__.py`. Never edit files inside `.venv`.

## Section 7: Step 4, The fix

1. Create `pyrightconfig.json` in the `Django` root, next to `.vscode`:

```json
{
  "venvPath": "first-django-project",
  "venv": ".venv"
}
```

2. Reduce `Django/.vscode/settings.json` to a single entry:

```json
{
  "python.analysis.extraPaths": [
    "${workspaceFolder}/first-django-project/.venv/lib/python3.9/site-packages"
  ]
}
```

3. Save both files.
4. Press Cmd+Shift+P and run **Developer: Reload Window**.
5. Open `views.py`. The squiggle on line 1 is gone.

## Section 8: Step 5, Verify the project

1. Confirm `INSTALLED_APPS` in `config/settings.py` includes:

```python
'rest_framework',
'api',
```

2. Activate the venv and run the Django check:

```
source .venv/bin/activate
python manage.py check
```

3. Output: `System check identified no issues (0 silenced).`

## Section 9: Quick checklist for next time

1. Hover over the error to see which language server is used.
2. Confirm the code runs in the terminal with the venv active.
3. Put `pyrightconfig.json` in the workspace root with `venvPath` and `venv`.
4. Do not rely on the interpreter picker if the venv python is a symlink.
5. Never paste config into files inside `.venv`.
6. Activate the venv with `source .venv/bin/activate` in every new terminal.