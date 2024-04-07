## Setup [Linux]

- Install the platformio extension in VS Code.
- Add udev rules for supported boards/devices:  
    1. `curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules`
    2. `sudo service udev restart`
    3.
    Ubuntu/Debian users may need to add own “username” to the “dialout” group if they are not “root”, doing this issuing:
    ```
    sudo usermod -a -G dialout $USER
    sudo usermod -a -G plugdev $USER
    ```
    Similarly, Arch users may need to add their user to the “uucp” group:
    ```
    sudo usermod -a -G uucp $USER
    sudo usermod -a -G lock $USER
    ```
    4. Logout for user changes to take effect. In some cases, a reboot might even be needed (e.g. in my case, the CP210X UART driver was only registered after a reboot.)
