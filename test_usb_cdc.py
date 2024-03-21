import usb_cdc

def read_serial(serial):
    available = serial.in_waiting
    text = ""
    while available:
        raw = serial.read(available)
        text = raw.decode("utf-8")
        available = serial.in_waiting
    return text

# main
buffer = ""
# usb_cdc.enable(console=True, data=False) #
serial = usb_cdc.console
while True:
    buffer += read_serial(serial)
    if buffer.endswith(">"):
        # strip line end
        input_line = buffer[:-1]
        # clear buffer
        buffer = ""
        # handle input
        print(input_line)
