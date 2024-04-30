# Mqtt Client

This Mqtt client Publisher and Analyzer which will iteratively publish number message incrementally by following the controller. In addition, it will also receive some information from $SYS topic which maybe using on analyzing data.

## Requirement

This gopher client application was testing on `Window` . Please read through the dependency below.
Make sure you have installed these dependencies:

* `Python` 3
* `WireShark` for communication tracking
* `Mqtt broker` which can be locally, public or cloud
* `Paho mqtt python module`

## Run the application

This application was build and execute on Window 11.

Run steps

1. Open the COMP3310-assignment3-code which contain `n_analyzer.py` and `n_controller.py`.

2. Open the terminal on this location.

3. Run the application:

```sh
  > python n_controller.py
```

run the controller first, imagine that it's already on the broker. Then

```sh
  > python n_analyzer.py
```

run the analyzer.

4. Input the desired instance, delay, and QoS level. Then wait for the result.

5. If you want to test with friend broker and publisher only change the broker ip and execute only `n_analyzer.py`.

```sh
  analyzer.connect("broker.emqx.io", 1883) # replace the "broker.emqx.io" with your friend broker ip in n_analyzer.py
```

6. If your friends ask you for testing his analyzer only run the `n_controller.py`.

