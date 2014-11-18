sandworm
========

exec/grader playground

Setup
=====

currently just a simple angular app with tornado backend

  1. run with:
    ```shell
    cd grader/
    python server.py
    ```
    
  2. go to [localhost:8000](http://0.0.0.0:8080/)

  3. run tests (in the another shell) with:
    ```shell
    cd grader/
    protractor test/protractor_conf.js
    ```