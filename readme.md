# Code Streak

Code streak is a simple django app that helps you keep a track of your programming, through github.

## Installation

#### Prerequisites
* python 3.5 (untested with other versions)
* django-allauth (0.27.0) for the user's github username (although you can supply that yourself)
* django itself (1.9.9)
* huey (1.2.2)
* pushbullet.py (0.10.0)
* requests (2.12.4)

#### Clone
When you have all of those, drop the app into your project clone the extendless branch (master extends a template). 
Drop it in your proje ct.

#### Configuration

project/project/settings.py:

    INSTALLED_APPS += [
        'codestreak.apps.CodestreakConfig'
    ]

project/project/urls.py:

    urlpatterns += [
        url(r'^codestreak/', include('codestreak.urls', namespace="codestreak")),
    ]

project/settings_local.py: (it is good practice to keep all api keys outside of your git tree. mine are in a file called settings_local)

    PUSHBULLET_KEY = "MYKEYHERE"

Specify in `codestreak_acceptedevent` in the database which events you want to count as a success.
Events are defined here: [Event Types & Payloads](https://developer.github.com/v3/activity/events/types/)

A good place to start is with `PushEvent`, `PullRequestEvent`, and `CreateEvent`


## Planned:

-[ ] reduce dependencies

## Usage

Go to /codestreak with a github account attached to your allauth user to register. Start commiting!

## Contributing

This was made as an hour code challenge. It is currently hosted [here](www.hattiechocolateday.com/codestreak).
It is feature sparse by design. It's not even designed to work with timezones. If you want to add a feature:

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.