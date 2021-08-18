# canercharm

## Description

A little charmed operator for Caner to play, hack and break.

## Usage

TODO: Provide high-level usage, such as required config or relations


## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests


## Build

   $ charmcraft pack

## deploy

   $ juju deploy ./canercharm.charm --resource httpbin-image=whatever/httpbin

## watch

   $ watch -n1 --color juju status --color

### set the log level to DEBUG for the development model

   $ juju model-config logging-config="<root>=WARNING;unit=DEBUG"

Have the `juju debug-log` and `watch` running all the time to keep track of things

## kubectl

   $ kubectl -n development get pods

   $ kubectl -n development describe pod canercharm-0

(canercharm-0 <- 0 index is because we have only 1 unit of the application)