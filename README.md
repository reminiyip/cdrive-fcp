#### References

- [Our Coding Standards](https://github.com/pyliaorachel/cdrive-fcp/blob/master/CODING_STANDARDS.md)
- [Sample Projects](https://github.com/django/djangoproject.com)
- [Django Reusable Apps](http://django-reusable-app-docs.readthedocs.io/en/latest/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/en/)

#### Structure

###### URL

```
/homepage
/genre/:id
          /game/:id
                    /reviews
                    /review                       <- members purchased the game
                           /new
                           /:id
                              /edit
                              /remove
                    /tag/add                      <- members purchased the game
/tag/:name
/purchase_history

/cart/:id
          /payment
          
/register
/login
/recover

/profile
          /edit
          
/admin
```

###### Project

```
cdrive-fcp/
   # project
   cdrive-fcp/
       manage urls & settings
       
   # apps
   core/
       login, registration, password recovering, etc.
       browse/edit profile, browse rewards, purchase history, etc.
       browse cart content, payment page, etc.
   game/
       browse homepage, genre, games, tagged games, etc.
       
   # others
   static/
       static files
   tests/
       test files
   uploads/
       upload files
   templates/
       global templates
   docs/
       documentation
```
