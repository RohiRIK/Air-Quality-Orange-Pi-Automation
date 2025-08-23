
# Troubleshooting


- **No Sensor Detection**: Check connections and I2C enablement with `sudo i2cdetect -y 0`.

- **Python Import Errors**: Make sure all required Python packages are installed. Run `pip3 install -r requirements.txt` if available.

- **I2C Bus Not Found**: Double-check the I2C device path (e.g., `/dev/i2c-0`). Use `ls /dev/i2c-*` to list available I2C devices.

- **Sensor Data Incorrect or Unstable**: Ensure the sensor is powered correctly and wires are secure. Try a different sensor or cable if possible.

- **Permission Denied on I2C**: Add your user to the `i2c` group: `sudo usermod -aG i2c $USER` and reboot.

- **Network Errors**: Verify internet access and the endpoint URL.

- **Service/API Endpoint Not Responding**: Confirm the server is running and accessible from the device. Test with `curl` or `ping`.

- **Docker Issues**: Ensure `--privileged` and `--device` flags are used, and check Docker logs with `docker logs <container-id>`.

- **Container Fails to Start**: Check for missing Docker privileges or device flags. Review error messages for clues.

- **Permission Issues**: Run Docker commands with `sudo` if needed.
