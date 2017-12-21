Tool for performing long-running computations

TODO: dockerize everything so it can be deployed on Docker Cloud

## Current local setup
Install the dependencies in virtualenv, remember to activate it in all the terminal windows
```
$ docker-compose up
```
In another terminal window
```
$ ./manage.py migrate
$ ./manage.py createsuperuser --username admin --email admin@admin.com
$ ./manage.py register
$ ./manage.py runserver
```
In another terminal window
```
$ ./manage.py runobservers
```
In another terminal window
```
$ ./manage.py runlistener
```
In another terminal window
```
$ celery -A modeling worker --queues=ordinary,hipri --loglevel=info
```

To run the process with `reSDK`
```
pip install resdk
```
In Python shell
```python
In [1]: import res

In [2]: res = resdk.Resolwe(url='http://localhost:8000', username='admin', password='...')

In [3]: paths1 = res.run('pathways-predictor', input={'model': 'e_coli_core', 'product': 'ethanol', 'n_pathways': 1})

In [4]: paths1.update()

In [5]: paths1.status
Out[5]: 'PR'

In [6]: paths1.update()

In [7]: paths1.status
Out[7]: 'OK'
```
You can see the results of the local runs in `data/data` directories