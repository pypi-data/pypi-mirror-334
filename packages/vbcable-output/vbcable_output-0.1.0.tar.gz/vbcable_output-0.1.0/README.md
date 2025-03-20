# vbcable_output

This package outputs audio to the VBCable virtual audio device.   
https://vb-audio.com/Cable/

## Installation

You can install the package using pip:

```
pip install vbcable_output
```

## Usage
```python
import vbcable_output

# Play the given data at the specified rate.
vbcable_output.play(data, rate)

# Wait for the sound to finish playing.
vbcable_output.wait()

# Check if the VB-CABLE is installed.
vbcable_output.is_vbcable_installed() => bool
```

## Parameters
    data: The audio data you want to play.
    rate: The sample rate of the audio.

## License
MIT License. See the LICENSE file for details.