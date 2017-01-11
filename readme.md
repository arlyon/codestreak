# Code Streak

Code Streak is a simple django app that helps you keep a track of your commit streak, sending pushbullet
notifications to keep you on track.
## Installation

#### Prerequisites
* python 3.5 (untested with other versions)
* django (1.9.9)
* huey (1.2.2)
* pushbullet.py (0.10.0)
* requests (2.12.4)
* dateutil (2.6.0)

#### Clone

Simply clone the project into your django folder and add the app to your settings, shown below.

#### Configuration

project/project/settings.py:

    INSTALLED_APPS += [
        'codestreak.apps.CodestreakConfig'
    ]

project/project/urls.py:

    urlpatterns += [
        url(r'^codestreak/', include('codestreak.urls'),
    ]

project/settings_local.py: (it is good practice to keep all api keys outside of your git tree. mine are in a file called project/settings_local.py)

    PUSHBULLET_KEY = "MYKEYHERE"

Specify in `codestreak_acceptedevent` in the database which events you want to count as a success.
These are checked at 20:00 and 00:00 local time against each users event history.

Events are defined here: [Event Types & Payloads](https://developer.github.com/v3/activity/events/types/)

A good place to start is accepting `PushEvent`, `PullRequestEvent`, and `CreateEvent`.


## Planned:

- [ ] reduce dependencies
- [ ] allauth (and github) integration

## Usage

Currently the app assumes that `request.user.username` is the user's github username.
Go to /codestreak to register. Start commiting!

## Contributing

This was made as an hour code challenge. It is currently hosted [here](www.arlyon.co/codestreak).
It is feature sparse by design. It's not even designed to work with timezones. If you want to add a feature:

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.