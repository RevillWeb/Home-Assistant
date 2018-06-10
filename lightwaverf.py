"""
homeassistant.components.light.lightwave
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Richie Schuster - LightwaveRf Lights - 08/05/2018

"""
#import 
import logging
import random
import sys
import pika
import voluptuous as vol

#import light info
from homeassistant.components.light import (ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, PLATFORM_SCHEMA)
#import schema known light config
from homeassistant.const import (CONF_NAME, CONF_ID, CONF_LIGHTS, CONF_SWITCHES)
#import validation
import homeassistant.helpers.config_validation as cv
from entities.light import LWRFLight
from entities.switch import LWRFSwitch

#Requirements
REQUIREMENTS = ['pika==0.11.2']

#set brightness support
SUPPORT_LIGHTWAVE = (SUPPORT_BRIGHTNESS)

#logger?
_LOGGER = logging.getLogger(__name__)

#set defaults incase of user error
DEFAULT_LIGHTS_NAME = 'LightwaveRF Lights'
DEFAULT_SWITCHES_NAME = 'LightwaveRF Switches'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 15672
DEFAULT_STATE = False
DEFAULT_RFLINK = '255.255.255.255'

#assign non known config
#rabbitmq
CONF_RABBITHOST = 'rabbithost'
CONF_RABBITQUE = 'rabbitque'
CONF_RABBITUNAME = 'rabbituname'
CONF_RABBITPASS = 'rabbitpass'
CONF_RABBITPORT = 'rabbitport'
CONF_RFLINK = 'rflink'

#validate user config
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_RABBITHOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_RABBITPORT, default=DEFAULT_PORT): cv.port,
    vol.Required(CONF_RABBITQUE): cv.string,
    vol.Required(CONF_RABBITUNAME): cv.string,
    vol.Required(CONF_RABBITPASS): cv.string,
    vol.Optional(CONF_LIGHTS, default=[]):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ID): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_LIGHTS_NAME): cv.string,
                vol.Optional(CONF_RFLINK, default=DEFAULT_RFLINK): cv.string,
            })
        ])
    vol.Optional(CONF_SWITCHES, default=[]):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ID): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_SWITCHES_NAME): cv.string,
                vol.Optional(CONF_RFLINK, default=DEFAULT_RFLINK): cv.string,
            })
        ])
})

#import user config from yaml    
def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Setup LightwaveRF devices """
    rabbithost = config.get(CONF_RABBITHOST)
    rabbitport = config.get(CONF_RABBITPORT)
    rabbitque = config.get(CONF_RABBITQUE)
    rabbituname = config.get(CONF_RABBITUNAME)
    rabbitpass = config.get(CONF_RABBITPASS)
    devices = []
    lights = config[CONF_LIGHTS]
    for light in lights:
        deviceid = light[CONF_ID]
        name = light[CONF_NAME]
        rflink = light[CONF_RFLINK]
        device = LWRFLight(name, DEFAULT_STATE, deviceid, rflink, rabbithost, rabbitport, rabbitque, rabbituname, rabbitpass)
        devices.append(device)
    switches = config[CONF_SWITCHES]
    for switch in switches:
        deviceid = switch[CONF_ID]
        name = switch[CONF_NAME]
        rflink = switch[CONF_RFLINK]
        device = LWRFSwitch(name, DEFAULT_STATE, deviceid, rflink, rabbithost, rabbitport, rabbitque, rabbituname, rabbitpass)
        devices.append(device)    
    
    add_devices(devices)