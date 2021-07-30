# Project review report

Project name: "values-conv.py"  
Project urls: https://github.com/Ratgor/values-conv  
Reviewer: Aliaksandr Tsurko  
Review date: 2021-07-27  

Review aim: find out what is ok and what can be improved, to have points for discussion at the candidate interview.  

---

# Table of contents

1. project planning issues  
2. project architecture issues  
3. project operations issues  
4. project technology issues  

---

# Project planning issues


---

* 1.1 Project business requirements do not fixed

* 1.2 Project technical requirements do not fixed

Despite the project is free-of-charge and open-source,  
the business goal and target audience should be specified (business requirements)  
to elicitate technical requirements (functional and non-functional)  
  
Without technical requirements it's hard to say what the project should do (and should not),  
what should (not) be tested, what should (not) be improved, which priority the backlog tasks have.  

---

* 1.3 Seems that the tool can (and should) be multilingual

* 1.4 Seems that the project description should have a bit of SEO

It refers to lack of requirements touching to target audience.  

Originally, it has been done for one representative of artisans group  
who were working with some culture- and language-specific communities.

A proper description in sense of search optimization  
could lead more interested persons to this project.

More people -> more feedback, fresh requirements, and further development.

---

# Project architecture issues  

---

* 2.1 The lack of technical and user documentation is obvious

That means the project is currently hard to maintain, and hard to use.  

The only justification is it has been done by one person for another one.    

This cannot go on.  
The first what we should do after (and even starting from) requirements elicitation and analysis - write the docs, make them clear and keep up-to-date.  
Otherways no effective project usage, maintenance and further development will be possible.

(This should include architecture docs and working principle/algorithms of the app too)

* 2.2 UI should have button to call/show docs or help

* 2.3 The docs should include instructions how to add or edit conversion formulas

* 2.4 The docs should include instructions how to make configuration of the app

* 2.5 The docs should include knowledge base about measurement units

* 2.6 UI should have separate buttons to save/load settings and printable conversion results

Currently, the converter app has a mix of code and settings functionality.  
That means adding new conversions can be done only via the source code editing. That is a bad practice.  
At the same time the app architecture is oriented to loading them from settings files. That is a good practice.  

* 2.7 project files structure

* 2.8 deployment and delivery docs

The project was designed as offline tool with support of Windows and Linux.
It has two delivery options available for each OS:  
running as a script or as a portable executable.

Currently, docs on building and delivery are not provided.  
They should include system and python environment requirements,  
build and deploy configuration and instructions, links to repositories.

In addition, virtual environment files (e.g. pipfile or requirements.txt)  
and bundle config files (for pyinstaller) may be provided.

Those files, including embedded docs, configs, user configs, printable results, and others  
should require improved directory structure and embedding into the project and config.

* 2.9 architecture enhancements and new features

The app architecture should be reworked and split to multiple parts:  

Currently all is packed to the UI. That is a bad practice.  
UI should be an independent module. That will be good practice.

Logging is not provided but is strongly recommended.  

Config files processing should be extracted to one file.  

Files and path operations should be extracted to one file.  

Conversions (evaluation) module. 
This can be packed together with conversion docs in separate python package and published on PyPI.
In addition, implementing this as microservice with CLI and REST API for this package could be considered.

Auto-update feature should be considered too.

Translations module (with loading translations from files).

Database module (to keep settings and conversion results),  
with import/export from files. 

Conversion settings editor.  
Currently, the text editor shows only printable results.  
It will be nice to have possibility to edit settings directly from the app,  
and provide integrated to the editor hints for that.

---

# Project operations issues  

---

* 3.1 automated tests should be added

I prefer pytest tool for making tests.  

The fixed requirements, especially to the APIs of the app ant its modules,  
should be provided to make the test coverage. 

e.g. there is a requirement so save and load profiles and conversion results by a person name as the file name.  
The fulfillness of this requirement should be checked with a specific test.

In ideal, that means that list of requirements from SA and BA should be integrated in CI/CD and reports.

* 3.2 code style should be reviewed
 
PEP8 recommendations could be considered as a starting point  
to determine code style and codes standard guide for the project.

Inline and docstrings comments should be used.  
(I prefer NumPY docstring style, compatible with Sphinx)

Static code analysis tools (like fleke8 and pylint) may be added to the tests,  
and configured to selected code standards.

Naming in the code is not always clear. 
I tends to be self-documented, but does not reach this everywhere.

e.g. `self.title_lbl` can be clarified as `self.app_title_label`,  

`self.top_sep` can be clarified as `self.top_separator`,  

`self.text` can be clarified as `self.text_field`,  

`person_settings` stands for `person_metrics`,  

and the code 
```python
for person in self.person_settings:
    try:
        local_values_dict[person['id']] = float(person['value'])
    except:
        pass
```  

actually, iterates over metrics for one person only, except the person’s name,  
thus, may be refactored as 
```python 
for metric in self.person_metrics:
    if metric['id'] != 'name':
        try:
            person_metrics_dict[metric['id']] = float(person['value'])
        except:
            strings.append( f"Parson metric {metric['id']} has wrong input string format: {person['value']}\n")
```

* 3.3 CI/CD should be considered

That touches auto-builds for portable releases and auto updates for both delivery options.
If the python module for PyPI should be published, that should be included in the automated cycle.
Automated test should be included in it too.

---

# Project technology issues 

---

* 4.1 current code is simple and more-less fits in current requirements

We have no special requirements for performance and security,  
and we provide only basic functionality (like offline Proof-of-Concept)

In that case using only embedded python modules seems a plus,
(e.g. tkinter, logging, configparser, sqlite, etc.)

* 4.3 importing all is not a good practice, if you do not control all the namespace

e.g. `from tkinter import *` may be replaced with `import tkinter as tk`

* 4.3 use pathlib and f-strings for combining file pathes

e.g. instead of 
```python
import os

file_name = os.path.join(os.getcwd(), person_name + '.txt')

if not os.path.isfile(file_name):
```

we may use 
```python
from pathlib import Path

file_name = Path.cwd() / f"{person_name}.txt"

if not file_name.is_file():
```

* 4.4 the function `def recalculate(self):` should be refactored

because: 

4.4.1 it doesn't reload metric values from the input forms,  
thus, works with the default values only

4.4.2 it is a mix of conversion template, evaluations, print layout and text field update.  
that should be separate functions with clear names.  
(a function name should correspond to the action it does)  

4.4.3 conversion template files, that has been mentioned earlier as conversion settings files, 
should be introduced. we may try to use jinja templates engine for that or make our own solution.

4.4.4 Currently, any unsupervised code can be executed from the conversion templates, that is unsafe.  
Best approach - to describe all possible evaluation as a conversions language in docs,  
and write a parser and evaluation engine for it.  
