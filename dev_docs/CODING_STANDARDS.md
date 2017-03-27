#### Coding Standards

[Django](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) coding standards.  
If doubts, refer to [Python](https://google.github.io/styleguide/pyguide.html) coding standards.  
[SQL](http://www.sourceformat.com/pdf/sql-coding-standard-sqlserver.pdf) coding standards.

##### Common Coding Standard Examples

###### Import: break long lines

```
from django.http.response import (
    Http404, HttpResponse, HttpResponseNotAllowed, StreamingHttpResponse,
    cookie,
)
```

###### Template: spaces

`{{ foo }}` instead of `{{foo}}`

###### View: 'request' instead of 'req'

```
def my_view(request, foo):
    # ...
```

###### Model

- Field name: all lowercase, underscores

```
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
```

- Inner class: appear AFTER fields; blankline

```
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'people'
```

###### Other namings

`module_name`  
`package_name`  
`ClassName`  
`method_name`  
`ExceptionName`  
`function_name`  
`GLOBAL_CONSTANT_NAME`  
`global_var_name`  
`instance_var_name`  
`function_parameter_name`  
`local_var_name`
