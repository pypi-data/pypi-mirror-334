import sys
import can
import time
import errno
import argparse
import can
from typing import List

from CyberGearDriver import CyberGearMotor, RunMode, CyberMotorMessage

bus: can.Bus
motor: CyberGearMotor
notifier: can.Notifier

DEFAULT_CAN_BITRATE = 1000000


def parse_args(
    args: List[str], description: str = "Connect to the CyberGear driver via CAN bus"
) -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description=description,
    )

    parser.add_argument(
        "-m",
        "--motor-id",
        type=int,
        help="The ID of the motor on the CAN bus",
        default=127,
    )

    parser.add_argument(
        "-c",
        "--channel",
        help=r"Most backend interfaces require some sort of channel. For "
        r"example with the serial interface the channel might be"
        r'"/dev/ttyACM0". With the socketcan interface valid '
        r'channel examples include: "can0", "vcan0".'
        r"(more info: https://python-can.readthedocs.io/en/stable/interfaces.html)",
    )

    parser.add_argument(
        "-i",
        "--interface",
        dest="interface",
        help="""Specify the Python CAN interface to use (for example 'slcan'). See: https://python-can.readthedocs.io/en/stable/interfaces.html""",
        choices=sorted(can.VALID_INTERFACES),
    )

    parser.add_argument(
        "-b",
        "--bitrate",
        dest="bitrate",
        help="""CAN bus communication bitrate""",
        default=DEFAULT_CAN_BITRATE,
        type=int,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="""Verbose output""",
        action=argparse.BooleanOptionalAction,
    )

    if not args:
        parser.print_help(sys.stderr)
        raise SystemExit(errno.EINVAL)
    parsed_args, unknown_args = parser.parse_known_args(args)

    return parsed_args


def connect(
    motor_id: int, interface: str, channel: str, bitrate: int, verbose: bool
) -> CyberGearMotor:
    global bus, motor, notifier

    # Connect to the bus
    bus = can.interface.Bus(
        interface=interface,
        channel=channel,
        bitrate=bitrate,
    )

    # Create function to pass the CyberGear messages to the CAN bus
    def send_message(message: CyberMotorMessage):
        bus.send(
            can.Message(
                arbitration_id=message.arbitration_id,
                data=message.data,
                is_extended_id=message.is_extended_id,
            )
        )

    # Create the motor controller
    motor = CyberGearMotor(motor_id, verbose=verbose, send_message=send_message)

    # Send the CyberGear driver messages received from the CAN bus
    notifier = can.Notifier(bus, [motor.message_received])

    return motor


def main() -> None:
    global bus, motor, notifier

    # Parse command line arguments
    args = parse_args(
        sys.argv[1:], description="Test the CyberGear Operation Control mode"
    )

    # Create the motor controller
    motor = connect(
        motor_id=args.motor_id,
        verbose=args.verbose,
        interface=args.interface,
        channel=args.channel,
        bitrate=args.bitrate,
    )

    # Init motor
    motor.enable()
    motor.mode(RunMode.POSITION)
    motor.set_zero_position()

    motor.set_parameter("limit_spd", 2)
    motor.set_parameter("loc_kp", 30.0)
    # motor.set_parameter("spd_ref", 0.0)

    # Move the motor back and forth
    print("Starting test")
    while True:
        motor.set_parameter("loc_ref", -0.5)
        time.sleep(0.5)
        motor.request_parameter("loc_ref")
        time.sleep(0.5)
        print(f"loc_ref: {motor.params.get('loc_ref')}")
        time.sleep(1)
        motor.set_parameter("loc_ref", 0.5)
        time.sleep(0.5)
        motor.request_parameter("loc_ref")
        time.sleep(0.5)
        print(f"loc_ref: {motor.params.get('loc_ref')}")
        time.sleep(1)

        # motor.request_parameter("limit_spd")
        # time.sleep(1)
        # orig = motor.params.get("limit_spd")
        # print(orig)
        # time.sleep(1)

        # motor.set_parameter("spd_ref", 1.0)
        # time.sleep(1)
        # motor.request_parameter("spd_ref")
        # time.sleep(1)
        # print(motor.params.get("spd_ref"))
        # time.sleep(1)

        # motor.set_parameter("spd_ref", orig)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
        notifier.stop()
        motor.stop()
        bus.shutdown()
