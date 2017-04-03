#### References

- [Our Coding Standards](https://github.com/pyliaorachel/cdrive-fcp/blob/master/dev_docs/CODING_STANDARDS.md)
- [Sample Projects](https://github.com/django/djangoproject.com)
- [Django Reusable Apps](http://django-reusable-app-docs.readthedocs.io/en/latest/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/en/)
- [Login Tutorial](https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html)
- [Password Reset](https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html)

#### Usage

`pip install django-registration`  
`python manage.py runserver`

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
                    /tag/:name/add                <- members purchased the game; redirect
                    /add_to_cart/                 <- redirect
/tag/:name

/cart/:id
          /payment
          
/register
/login
/logout
/password_reset
          /done

/profile
          /edit
/purchase_history

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

#### Account

###### Admin

```
Use 'createsuperuser' for one, or use:

Username: cdriveadmin
Password: cdriveadmin
Email: admin@example.com
```

###### User

```
Go to /register for one, or use:

Username: sampleuser
Password: thisisapassword
Email: sample@example.com
```
