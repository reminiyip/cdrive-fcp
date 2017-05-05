#### Usage
- Setup settings.py
  - `Download the settings.py file and open it.` 
  - `Link: https://drive.google.com/open?id=0BzdascQ9kP5rOUVEYmtCcDJhdTg`
  - `Substitude the xxx values using your own keys and secrets`
  - `Put the updated settings.py file in cdrive-fcp/cdrive_fcp`

- Install dependencies
  - `pip3 install django Pillow social-auth-app-django python-social-auth`   

- Run server
  - `cd <project-root>`  
  - `python3 manage.py runserver`  

- Errors
  - If errors showing missing libraries, run `pip3 install <missing-library>`

Open the browser, go to `localhost:8000`.

#### Structure

###### URL Patterns

```
# admin

/admin/                                                  <- admin page


# general

/homepage/                                               <- includes profile, featured games, recommendations, genres
/genre/:id/                                              <- VIEW games in specific genres
           game/:id/                                     <- VIEW game
                    reviews/                             <- VIEW reviews
                    review/new/                          <- review CRUD actions (for members already purchased the game)
                           :id/
                               edit/
                               remove/
                    tag/:name/add/                       <- tag CREATE action; <redirect>
                    add_to_cart/                         <- ADD game to cart; <redirect>
          ?filter=platform+platform+...                  <- filter genre games by platforms; <redirect>
          
/tag/:name/                                              <- VIEW games with specific tags
          ?filter=platform+platform+...                  <- filter tagged games by platforms; <redirect>

/cart/:id/                                               <- VIEW cart
          payment/                                       <- payment page
                  done/                                  <- finish payment; <redirect>
          remove/:game_id/                               <- REMOVE game from cart; <redirect>
          assign_rewards?game=game_id&value=rewards      <- assign rewards to specific games; <ajax>

/purchase_history/                                       <- VIEW purchase history


# account (refer to django.contrib.auth & social_django)

/register/
/login/
/logout/
/password_change/
                 done/
/password_reset/
                done/
/reset/done/
/oauth/
/profile/:id/                                           <- VIEW profile
             edit/                                      <- EDIT cart
```

###### Project Directory

```
cdrive-fcp/
           # project
           cdrive-fcp/
                      :manage urls & settings
                      templatetags/
                                    :globally usable template filters
                      utils/
                                    :utility functions
       
           # apps
           core/
                      :login, registration, password recovering, etc.
                      :browse/edit profile, browse rewards, purchase history, etc.
                      :browse cart content, payment page, etc.
           game/
                      :browse homepage, genre, games, tagged games, etc.
       
           # others
           media/     :database related images or other media objects
           static/
                      :static files (css, js, img, lib, etc.)
           templates/
                      :global templates
           dev_docs/
                      :documentation during development stage
```

#### Account

###### Admin

```
Run `python3 manage.py createsuperuser` for one, or use the default:

Username: cdriveadmin
Password: cdriveadmin
Email: admin@example.com
```

###### User

Go to `/register/` and sign up for one.

#### Notes

- `index.html` pages under `<app>/templates/` are for architecture setup & testing purpose only.
- All emails will be redirected to console.
- For FaceBook logins, it may fail because the app holder needs to grant privilege to testers. Ask us for help if needed.


