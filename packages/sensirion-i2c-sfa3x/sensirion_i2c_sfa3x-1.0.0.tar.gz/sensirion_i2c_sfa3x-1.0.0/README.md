# Python I2C Driver for Sensirion SFA3X

This repository contains the Python driver to communicate with a Sensirion SFA3X sensor over I2C.

<img src="https://raw.githubusercontent.com/Sensirion/python-i2c-sfa3x/master/images/sfa3x.png"
    width="300px" alt="SFA3X picture">


Click [here](https://sensirion.com/products/catalog/SEK-SFA30) to learn more about the Sensirion SFA3X sensor.



The default I²C address of [SFA3X](https://sensirion.com/products/catalog/SFA30) is **0x5D**.



## Connect the sensor

You can connect your sensor over a [SEK-SensorBridge](https://developer.sensirion.com/sensirion-products/sek-sensorbridge/).
For special setups you find the sensor pinout in the section below.

<details><summary>Sensor pinout</summary>
<p>
<img src="https://raw.githubusercontent.com/Sensirion/python-i2c-sfa3x/master/images/sfa3x-pinout.png"
     width="300px" alt="sensor wiring picture">

| *Pin* | *Cable Color* | *Name* | *Description*  | *Comments* |
|-------|---------------|:------:|----------------|------------|
| 1 | red | VDD | Supply Voltage | 3.15V to 5.5V
| 2 | black | GND | Ground |
| 3 | green | SDA | I2C: Serial data input / output |
| 4 | yellow | SCL | I2C: Serial clock input |
| 5 | blue | SEL | Interface select | Pull to GND to select I2C (leaving it floating selects UART)


</p>
</details>


## Documentation & Quickstart

See the [documentation page](https://sensirion.github.io/python-i2c-sfa3x) for an API description and a
[quickstart](https://sensirion.github.io/python-i2c-sfa3x/execute-measurements.html) example.


## Contributing

### Check coding style

The coding style can be checked with [`flake8`](http://flake8.pycqa.org/):

```bash
pip install -e .[test]  # Install requirements
flake8                  # Run style check
```

In addition, we check the formatting of files with
[`editorconfig-checker`](https://editorconfig-checker.github.io/):

```bash
pip install editorconfig-checker==2.0.3   # Install requirements
editorconfig-checker                      # Run check
```

## License

See [LICENSE](LICENSE).