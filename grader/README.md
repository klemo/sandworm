sandworm: grader
========

setup
=====

currently just a simple angular app with tornado backend


  0. install python, mongo and stuff from requirements.txt (pip install -r requirements.txt)

  1. load test db:
    ```shell
    cd grader/
    python utils.py --fixtures
    ```

  2. run with:
    ```shell
    python server.py
    ```
    
  3. go to [localhost:8080](http://0.0.0.0:8080/)

  4. run tests (in the another shell) with:
    ```shell
    cd grader/
    protractor test/protractor_conf.js
    ```