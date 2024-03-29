# -*- coding: utf-8 -*-

from gpiozero import OutputDevice, InputDevice, DistanceSensor
import gpiozero
import time

class Ultrasonic():
    """ Initialize Ultrasonic sensor 
        See <https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering> for pin numbering
        params echo_pin int: pin number for echo (input); int will translate pin number to GPIO number
        params trigger_pin int: pin number for trigger (output); int will translate pin number to GPIO number
    """
    def __init__(self, echo_pin=None, trigger_pin=None, pin_factory=None):
        if (not trigger_pin or not echo_pin):
            raise Exception("Trigger OR Echo pin is missing; need this pin to initialize ultrasonic sensor!")
        
        self._trigger = OutputDevice(trigger_pin, pin_factory=pin_factory, initial_value=False)
        self._echo = InputDevice(echo_pin, pin_factory=pin_factory, pull_up=False)
        # NOTE: better to pull-down the echo pin, to prevent some noise from using the same VCC pin
        self._sound_speed = 34300
        # when it detect distance below this threshold, means vehicle is passing the gate
        self._distance_threshold = 140
        print("initialize ultra")
    
    def set_sound_speed(self, sound_speed=34300):
        """ Sound speed traveling through the air is around 343m/s (on 20°C), 
            use this method to change them, when needed 
            (most of the time, it's not needed)
        """
        self._sound_speed = sound_speed

    def set_distance_threshold(self, distance_threshold=140):
        """ Set distance threshold for detecting vehicle passing the sensor
            params distance_threshold int: distance threshold on centimeter
        """
        self._distance_threshold = distance_threshold

    def distance(self) -> int:
        """ Get distance from sensor to object """
        # clear trigger
        self._trigger.off()
        time.sleep(0.01)

        self._trigger.on()
        # let trigger on for 0.01 milliseconds
        time.sleep(0.00001)
        self._trigger.off()

        start_time = time.time()
        stop_time = time.time()
        while self._echo.value == 0:
            start_time = time.time()
        
        while self._echo.value == 1:
            stop_time = time.time()
        
        # time difference when sound is traveling through air
        time_passed = stop_time - start_time
        # multiply with how fast sound traveled through the air (roughly 343m/s)
        # and divide by 2 to know the distance of the object in cm
        return round((time_passed * self._sound_speed) / 2, 2)

    def is_vehicle_pass(self) -> bool:
        """ Check if vehicle is passing the sensor """
        start_time = time.time()
        
        exit_condition = False
        start_time = False
        end_time = False
        while not exit_condition:
            distance = self.distance()
            if distance < self._distance_threshold and not start_time:
                start_time = time.time()
                print(distance)

            elif distance > self._distance_threshold and start_time:
                end_time = time.time()
                return True

            if int(end_time - start_time) > 30:
                # when it's already 30 seconds, just force it to close the gate then
                return True
            time.sleep(1)

        return True
