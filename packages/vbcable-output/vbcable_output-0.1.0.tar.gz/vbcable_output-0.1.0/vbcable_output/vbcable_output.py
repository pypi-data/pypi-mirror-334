import sounddevice as sd

class vbcable_output:
    @staticmethod
    def play(data, rate):
        """Play the given data at the specified rate."""
        output_device_name = "CABLE Input"
        output_device_id = vbcable_output._search_output_device_id(output_device_name)
        input_device_id = 0
        sd.default.device = [input_device_id, output_device_id]
        sd.play(data, rate)
        return True

    @staticmethod
    def wait():
        """Wait for the sound to finish playing."""
        sd.wait()
        
    @staticmethod
    def is_vbcable_installed():
        """Check if the VB-CABLE is installed."""
        devices = sd.query_devices()
        for device in devices:
            if "CABLE Input" in device["name"]:
                return True
        return False

    @staticmethod
    def _search_output_device_id(output_device_name, output_device_host_api=0):
        """Search and return the device ID for the output device."""
        devices = sd.query_devices()
        for device in devices:
            is_output_device_name = output_device_name in device["name"]
            is_output_device_host_api = device["hostapi"] == output_device_host_api
            
            if is_output_device_name and is_output_device_host_api:
                return device["index"]

        raise RuntimeError("VB-CABLE is not installed. Please visit https://vb-audio.com/Cable/")
