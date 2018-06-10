from homeassistant.helpers.entity import Entity

class LWRFSwitch(Entity):
    """ LRF SOcket """
    def __init__(self, name, state, deviceid, rflink, rabbithost, rabbitport, rabbitque, rabbituname, rabbitpass):
        self._rabbithost = rabbithost
        self._rabbitport = rabbitport 
        self._rabbitque = rabbitque
        self._rabbituname = rabbituname
        self._rabbitpass = rabbitpass
        self._deviceid = deviceid
        self._rflink = rflink
        self._name = name
        self._state = state

    @property
    def should_poll(self):
        """ No polling needed for a demo light. """
        return False        
        
    @property
    def name(self):
        """ Returns the name of the device if any. """
        return self._name
        
    @property
    def rabbithost(self):
        """ Returns the host of the device if any. """
        return self._rabbithost
        
    @property
    def rabbitport(self):
        """ Returns the name of the device if any. """
        return self._rabbitport
        
    @property
    def rabbitque(self):
        """ Returns the que of the device if any. """
        return self._rabbitque
        
    @property
    def rabbituname(self):
        """ Returns the username of the device if any. """
        return self._rabbituname
        
    @property
    def rabbitpass(self):
        """ Returns the password of the device if any. """
        return self._rabbitpass

    @property
    def brightness(self):
        """ Brightness of this light between 0..255. """
        return self._brightness
    
    @property
    def deviceid(self):
        """ The Lightwave Device ID """
        return self._deviceid
    
    @property
    def is_on(self):
        """ True if device is on. """
        return self._state

    def send_command(self, msg):
        credentials = pika.PlainCredentials(self._rabbituname, self._rabbitpass)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self._rabbithost, self._rabbitport, '/', credentials))
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=self._rabbitque, body=msg)
        connection.close()

    def turn_on(self, **kwargs):
        """ Turn the device on. """
        self._state = True

        msg = '%s|666, !%sF1|Turn On|%s ' % (self._rflink, self._deviceid, self._name)
        self.send_command(msg)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """ Turn the device off. """ 
        msg = "%s|666, !%sF0|Turn Off|%s " % (self._rflink, self._deviceid, self._name)
        self.send_command(msg)
        self._state = False
        self.schedule_update_ha_state()