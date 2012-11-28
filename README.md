# PyMTT #

PyMTT is a command-line text generator. It allows you to render [Jinja2](http://jinja.pocoo.org/)
templates using context created from pure Python modules or shell environment
variables. Primary usage is config generation for deployment.

PyMTT was inspired by Oleg Mamontov's [MTT](http://svn.mamontov.net/svn/mtt/),
but uses Python, not Perl.

## Example usage ##

    export DJANGO_SETTINGS_MODULE=settings_test
    pymtt -e -d -b config.py ~/template.proto ~/template

This command creates context from `settings_test` Django module (-d switch),
overwrites it with `config.py` and finally overwrites context with environment
variables if any (-e switch). Then uses context to render `template` out of
`template.proto`.

## Installation ##

	pip install -e 'git+https://github.com/pklemenkov/pymtt.git#egg=pymtt'
