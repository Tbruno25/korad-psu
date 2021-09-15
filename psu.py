import sys
from serial import Serial

psu_path = "/dev/ttyACM0"

def _send(func, decode=True):
    """
    Decorator for sending a command to the power supply.
    """

    def wrapper(*args, **kwargs):
        cmd = f"{func(*args, **kwargs)}\r".encode()
        try:
            with Serial(psu_path, baudrate=9600, timeout=0.1) as p:
                p.write(cmd)
                response = p.readline()
                if response:
                    try:
                        return float(response.decode())
                    except ValueError:
                        binary_str = bin(
                            int.from_bytes(response, byteorder=sys.byteorder)
                        )
                        return binary_str
        except Exception as e:
            print(f"PSU send failed: {e}")

    return wrapper


@_send
def _get_status():
    """
    Returns 8bit message.
    """
    return "STATUS?"


@_send
def get_current(channel: int, realtime: bool = False):
    """
    Returns either the programmed setting or a realtime reading for channel.
    """
    return f"I{('SET','OUT')[realtime]}{channel}?"


@_send
def set_current(channel: int, value: float):
    """
    Sets current on channel to the value.
    """
    return f"ISET{channel}:{value}"


@_send
def get_voltage(channel: int, realtime: bool = False):
    """
    Returns either the programmed setting or a realtime reading for channel.
    """
    return f"V{('SET','OUT')[realtime]}{channel}?"


@_send
def set_voltage(channel: int, value: float):
    """
    Sets voltage on channel to the value.
    """
    return f"VSET{channel}:{value}"


@_send
def set_mode(mode: int):
    """
    Sets the power supply mode to: [0]NORMAL | [1]SERIAL | [2]PARALLEL
    """
    return f"TRACK{mode}"


@_send
def set_ocp(state: bool):
    """
    Sets the overcurrent protection state.
    """
    return f"OCP{state}"


def get_output():
    return int(_get_status()[7])


@_send
def set_output(state: bool):
    """
    Sets the output state.
    """
    return f"OUT{int(state)}"


@_send
def get_id():
    """
    Returns the ID.
    """
    return "*IDN?"


if __name__ == "__main__":
    pass
