### Installation
## Follow these steps to set up and run the script with your device:

- Generate a certificate for authentication following the androidtvremote2 documentation and save it to a known location.

- Configure your config.json file with the IP address of your Android TV Stick, the path to the certificate, and the path to the command file. Alternatively, you can directly pass these parameters as command line arguments when running the script.

- To run the script using a configuration file, use the following command in your terminal:


```python your_script.py /path/to/config.json```
Replace /path/to/config.json with the path to your configuration file.

Alternatively, you can run the script by directly passing the required parameters as command line arguments:

```python your_script.py 100.100.100.100 /path to certificate/cert.pem /path to commands_file/commands_file.json```
Where:

100.100.100.100 is the IP address of your Android TV Stick (arg1).
/path to certificate/certificate.crt is the path to your authentication certificate (arg2).
/path to commands_file/commands_file.json is the path to your file containing the commands to execute (arg3).

This flexibility allows you to quickly switch between different configurations or devices without modifying the config file.




KEYCODE_DPAD_UP: Navigation up button on the D-pad.
KEYCODE_DPAD_DOWN: Navigation down button on the D-pad.
KEYCODE_DPAD_LEFT: Navigation left button on the D-pad.
KEYCODE_DPAD_RIGHT: Navigation right button on the D-pad.
KEYCODE_DPAD_CENTER or KEYCODE_ENTER: Select or enter button.
KEYCODE_BACK: Back button.
KEYCODE_HOME: Home button, usually brings you back to the home screen.
KEYCODE_MENU: Menu button, often brings up a menu in apps.
KEYCODE_VOLUME_UP: Increase the volume.
KEYCODE_VOLUME_DOWN: Decrease the volume.
KEYCODE_POWER: Power button, may turn the device on or off.

C:\Python310\python.exe android_tv_remote_run.py --commands_file commands_file.json --ip 45 --cert dfd
C:\Python310\python.exe android_tv_remote_run.py -c config.json