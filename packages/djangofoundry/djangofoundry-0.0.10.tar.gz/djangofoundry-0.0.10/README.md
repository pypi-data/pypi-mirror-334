# DjangoFoundry

DjangoFoundry is a Python library which intends to expedite the development process by creating a few classes your code can inherit from.

## Do I need another framework?

No. You don't. This is entirely unnecessary for your project, but it includes tools that help me bootstrap my work, so I'm releasing it. Feel free to modify it to your needs, or ignore this project altogether. 

## Installation

To install DjangoFoundry, use pip:

```bash
pip install djangofoundry
```

## Features

DjangoFoundry includes classes to manage aspects of a Django application, such as:

- Generic controllers to inherit from including JSON and memory monitoring.
- A library of exceptions.
- Progress tracking with the ProgressStates, ProgressBar, and ChildProgressBar classes.
- Hook and waypoint management.
- Template rendering for specific use-cases, such as creating db models.
- Matching engine for handling tasks like OCR.
- Utility mixins for dealing with dirty fields, hookable objects, and param handling.
- Simplified JSON encoding with the JSONEncoder class.
- Model, queryset, and serializer management for data handling.
- Readthedocs documentation
- Finish pylint / prospector cleanup
- Github actions
- Easy access to various apis

## Sample Cases

Bootstrapping a new django project

```bash
python src/djangofoundry/scripts/app/bootstrap.py
```

Consider a scenario where you are processing a set of items, and you want to display a progress bar to indicate the progress of the task. 

```python
    total_items = items_to_process.count()
    processed_items = 0
    for item in items_to_process:
        processed_items += 1
        progress = (processed_items / total_items) * 100
        # Now you have to manually handle this progress information
```

With DjangoFoundry, we can remove some of the boilerplate:

```python
    progress_bar = ProgressBar(total=items_to_process.count())
    for item in items_to_process:
        progress_bar.advance()
        # DjangoFoundry handles the progress tracking for you.
```

We can use querysets to calculate statistics like the median:
```python
median_value = Model.objects.values_list('field_name', flat=True).median()
filtered = Model.objects.filter(field_name__gte=median_value - deviation, field_name__lte=median_value + deviation)
```

With DjangoFoundry, most of that goes away:
```python
filtered = Model.objects.filter_median('field_name', deviation)
```

We can find correlations in the data as well:
```python
correlated_fields = Model.objects.find_correlated_fields('field_name', threshold)
```

Scripts are included to start up, monitor, and manage various processes, including django and a postgres db. 
```python
python scripts/db.py start
```

It also includes an alpha version of a "GPT-4 linter", which scans your python files, sends them to the openai api to ask for feedback, and saves that feedback to a diff file. No embeddings are passed, so this will only be of so much help. An openai api key is needed: a sample-settings.yaml is provided to copy
```python
python scripts/lint.py --help
```

## About the Author
DjangoFoundry is developed by Jess Mann. For any queries, suggestions, or feedback, feel free to reach out.

## Contributing
Contributions to DjangoFoundry are always welcome. If you find a bug or have a suggestion for improvement, please open an issue. Pull requests are also welcome.

## Testing
The unit tests work in my environment, but haven't been adapted to work without django. This will be done when I have a moment. 

## TODO
* Script to bootstrap django/angular project with a single command. 
* Unit tests should work independent of django env
* Expand app startup script to check for common env problems
* requirements.txt and other setup
* Opinionated dependencies fail gracefully
* Script to create new controller/url/angular components with a single command
* Standard pages (memory management, etc)
* Standard way to tie in jinja generated code into admin ui

## License
DjangoFoundry is released under the [BSD 3-Clause License](LICENSE.md).
