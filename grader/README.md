sandworm: grader
========

Setup
=====

currently just a simple angular app with tornado backend

  0. load test db:
    ```shell
    cd grader/
    python utils.py --fixtures
    ```
  1. run with:
    ```shell
    python server.py
    ```
    
  2. go to [localhost:8080](http://0.0.0.0:8080/)

  3. run tests (in the another shell) with:
    ```shell
    cd grader/
    protractor test/protractor_conf.js
    ```