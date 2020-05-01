# epic-auto-free-games

Logs into the Epic Games Store website and grabs the free games for the week.

## You need to set a few Docker environment variables:

- APP_USERNAME: your EPIC account username or email
- APP_PASSWORD: your EPIC account password
- APP_USER_AGENT: set to the same as your desktop browser

## You want to run this daily with something like:

> docker run -it --env APP_USERNAME="yourusername" --env APP_PASSWORD="supersecurepassword" edgard/epic-auto-free-games

## Credits

Based on code from [https://github.com/MasonStooksbury/Free-Games](https://github.com/MasonStooksbury/Free-Games)
