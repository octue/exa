# Exa 

An example of how to trigger Octue services from a backend webserver, allowing you to put a paywall, permissions, auth, throttling, schedulers or other stage gates / triggers between the outside world and your data services.

Exa is a basic django webserver, utilising the [django-twined](https://github.com/octue/django-twined) django app to interface between django and the octue services in your GCP project. 

## Purpose

This repository is set up as a demonstration of octue's communications problems, ready for working with GCP to improve architecture.

[Click here to see a full introduction of the issues this repository demonstrated.](https://docs.google.com/presentation/d/1o_4xok7SwdPyxxnAS_XFUNNSaRWcgaAxj5aO0sSu5mE/edit?usp=sharing)

## ...but also

Together, the `terraform` directory, the `server.settings`, and the `.github/workflows/cd.yml` files provide a complete working example of how to run django in a serverless cloud environment on GCP, and all the infrastructure required to do so.

Feel free to use this as an example of how to use django on GCP, even without `django-twined` and the octue service aspects.
