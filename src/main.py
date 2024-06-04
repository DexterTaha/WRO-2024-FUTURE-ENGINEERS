import cv2
import time
import numpy as np
import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient
from utils import *

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
HUB_NAME = "Acting Hub"

Px = 0.0264583333  # Pixel to cm conversion
Focal_distance = 3  # Approx
Signal_size = 10  # in cm
Weight = 5
Object_size = int(100 * 0.3)

l = 640
b = 480


async def main():
    main_task = asyncio.current_task()

    def handle_disconnect(_):
        print("Hub was disconnected.")
        if not main_task.done():
            main_task.cancel()

    ready_event = asyncio.Event()

    def handle_rx(_, data: bytearray):
        if data[0] == 0x01:
            payload = data[1:]
            if payload == b"rdy":
                ready_event.set()
            else:
                print("Received:", payload)

    device = await BleakScanner.find_device_by_name(HUB_NAME)

    if device is None:
        print(f"could not find hub with name: {HUB_NAME}")
        return

    async with BleakClient(device, handle_disconnect) as client:
        await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)

        async def send(data):
            await ready_event.wait()
            ready_event.clear()
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + data,
                response=True
            )

        print("Start the program on the hub now with the button.")

        cap = cv2.VideoCapture(0)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, l)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, b)

        camera_task = asyncio.create_task(camera_loop(cap, send))

        # Keep the event loop running until all tasks are completed
        await asyncio.gather(camera_task)  # Add more tasks here if needed

async def camera_loop(cap, send):
    lap_number = 0
    order = 0
    while True:
        start = time.time()

        ret, frame = cap.read()
        if not ret:
            print("Error reading frame")
            break


        if lap_number != 3:
            image = frame


        Signal_img = frame.copy()
        Wall_img = frame.copy()

        # Call signal_detection function to detect signals and determine direction to turn
        Signal_img, Signal_data = signal_detection(frame, Signal_size, Weight, Object_size, Focal_distance, Px, l)
        data = Signal_data
        print(data)
        if order == 0:
            # Detect signals and determine the direction to turn
            Signal_img, Signal_data = signal_detection(frame, Signal_size, Weight, Object_size, Focal_distance, Px, l)
            data = Signal_data
            print(data)

            if data[0] == 1:
                if data[1] == 0:
                    if data[4] < 15:
                        print("LEFT")
                        await send(b"rev")

                else:
                    if data[4] < 15:
                        print("left")
                    else:
                        print("Centered")
            elif data[0] == 0:
                if data[1] == 0:
                    if data[4] < 15:
                        print("RIGHT")
                        await send(b"fwd")

                else:
                    if data[4] < 15:
                        print("RIGHT")
                    else:
                        print("Centered")
            else:
                print("0")
            order += 1

        elif order == 1:
            # Detect lanes and determine the angle to turn
            Wall_img, Wall_data, Wall_angle = wall_detection(image, l, b, 6)
            data = Wall_data
            angle = Wall_angle
            angle += 10
            print(data, angle)
            if data == "R":
                print("LEFT")
                await send(angle)
            elif data == "L":
                print("RIGHT")
                await send(angle)
            elif data == "F":
                print("Wall")
            elif data == "N":
                print("Nothing")
            order -= 1

        # Resize Signal_img and Wall_img to be smaller
        small_height = b // 3
        small_width = l // 3
        Signal_img_small = cv.resize(Signal_img, (small_width, small_height))
        Wall_img_small = cv.resize(Wall_img, (small_width, small_height))

        # Create a composite image
        composite_image = np.zeros((b, l + small_width, 3), dtype=np.uint8)
        composite_image[:b, :l] = frame
        composite_image[:small_height, l:] = Signal_img_small
        composite_image[small_height:2 * small_height, l:] = Wall_img_small

        # Display the composite image
        cv.imshow("Composite Image", composite_image)

        end = time.time()
        print("FPS :", 1 / (end - start))

        # Check for keypress
        key = cv.waitKey(1)
        if key == ord("q"):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())

