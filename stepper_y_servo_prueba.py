import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

angulo = int(input("Introduce el angulo de elevacion: ") )
angulo_corregido = angulo + 10
print("Angulo de Elevacion:",angulo)

azimut = int(input("Introduce el azimut: ") )
azimut_calculo = azimut * 3200//360
print("Azimut:", azimut)

duration = int(input("Introduce el tiempo de duracion: ") )


#Movimiento del azimut ingresado
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)

mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output


GPIO.output(EN_pin,GPIO.LOW) 
mymotortest.motor_go(True, "1/16" , azimut_calculo, .0005, False, .05) 
    
GPIO.cleanup() 

def angle_to_percent (angle) :
    if angle > 190 or angle < 0 :
        return False
    
    start = 2.5
    end = 12.5
    ratio = (end - start)/180 

    angle_as_percent = angle * ratio

    return start + angle_as_percent


GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False) 

#Use pin 12 for PWM signal
pwm_gpio = 12
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

#Posición Inicial 0°
pwm.start(angle_to_percent(0))
time.sleep(1)

#Posición ingresada 
pwm.start(angle_to_percent(angulo_corregido))
time.sleep(5)

#Regresa a la posición 0°
pwm.start(angle_to_percent(0))
time.sleep(1)
pwm.stop()
GPIO.cleanup()

#Retorno del Azimut
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)

mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
GPIO.setup(EN_pin,GPIO.OUT) 


GPIO.output(EN_pin,GPIO.LOW) 
mymotortest.motor_go(False, "1/16" , azimut_calculo, .0005, False, .05) 
    
GPIO.cleanup() 

