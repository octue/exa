# Exa 

An example of how to trigger Octue services from a django webserver, allowing you to put a paywall, permissions, auth, throttling, schedulers or other stage gates / triggers between the outside world and your scientific data services.

## Purpose

### Working to improve Octue's communications architecture

Exa is a basic django webserver, utilising [`django-twined`](https://github.com/octue/django-twined) to interface between django and the octue services in your GCP project.

The main reason for us building Exa is as a demonstration of our communications architecture, allowing us to run load tests to improve communications and stability of the way in which we deploy and communicate with Octue services.

This with a view to working with GCP and support partners to improve our Architecture. [Click here to see a full introduction of the issues this repository demonstrates.](https://docs.google.com/presentation/d/1o_4xok7SwdPyxxnAS_XFUNNSaRWcgaAxj5aO0sSu5mE/edit?usp=sharing)

### Demonstration of Django on GCP

Exa is a basic django webserver, utilising [`django-gcp`](https://github.com/octue/django-gcp) to manage django storage and events on GCP in a serverless way.

Together, the `terraform` directory, the `server.settings`, and the `.github/workflows/cd.yml` files provide a complete working example of how to run django in a serverless cloud environment on GCP, and all the infrastructure required to do so.

Feel free to use this as an example of how to use django on GCP, even without `django-twined` and the octue service aspects.
