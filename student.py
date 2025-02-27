#!/usr/bin python3
from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 79.5
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        
    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit),
                "sq": ("square", self.square),
                "w": ("wall", self.wall),
                "b": ("box", self.box),
                "t": ("swerve box", self.box_swerve),
                "m": ("maze nav", self.maze_1)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''
    
    def g_fwd (self, amount = 5):
      start_time = time.time()
      start_heading = self.get_heading()
      while time.time() < start_time + amount:
        turn = self.get_heading() - start_heading
        self.fwd(left = 80 - turn, right = 80 + turn)
      self.stop()
      
    def square(self):
      self.servo(2500)
      
    def dance(self):
        """A higher-ordered algorithm to make your robot dance"""
        # TODO: check to see if it's safe before dancing
        if self.safe_to_dance():
          self.fwd()
          time.sleep(2)
          self.stop()
          
          self.right()
          time.sleep(3)
          self.stop()
          
          self.left()
          time.sleep(2)
          self.stop()
    
    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe """
        for x in range(4):
          self.scan()
          for value in self.scan_data: 
            if self.scan_data[value] < 300:
              print ("don't dance")
              return False
          self.turn_by_deg(90)
        
        print ("safe to dance")
        return True
    
    def wall(self):
      while True:
        self.fwd()
        self.servo(self.MIDPOINT)
        time.sleep(.1)
        self.read_distance()
        if self.read_distance() < 500:
          self.stop()
          self.turn_by_deg(175)

    def box(self):
      while True: 
        self.fwd()
        self.servo(self.MIDPOINT)
        time.sleep(.1)
        self.read_distance()
        if self.read_distance() < 250:
          self.stop()
          self.servo(800)
          right_distance = self.read_distance()
          self.servo(2200)
          left_distance = self.read_distance()
          
          if left_distance > right_distance:
            self.left()
            time.sleep(0.85)
            self.stop()
            
            self.fwd()
            time.sleep(1)
            self.stop()

            self.right()
            time.sleep(.85)
            self.stop()
            
            self.fwd()
            time.sleep(1)
            self.stop()
            
          elif right_distance > left_distance:
            self.right()
            time.sleep(0.85)
            self.stop()
            
            self.fwd()
            time.sleep(1)
            self.stop()

            self.left()
            time.sleep(.85)
            self.stop()
            
            self.fwd()
            time.sleep(1)
            self.stop()
          
    def box_swerve(self):
      self.LEFT_DEFAULT = 60
      self.RIGHT_DEFAULT = 60
      while True: 
        self.g_fwd(.1)
        self.servo(self.MIDPOINT)
        c_distance = self.read_distance()
        self.servo(800)
        time.sleep(.3)
        r_distance = self.read_distance()
        self.servo(2200)
        time.sleep(.3)
        l_distance = self.read_distance()

        if c_distance < 300 or r_distance < 300 or l_distance < 300:
          self.stop()
          if l_distance > r_distance:
            self.fwd(left=20, right= 50)
            time.sleep(2)
            self.fwd(left=50, right=20)
            time.sleep(2)
          
          elif r_distance > l_distance:
            self.fwd(left=50, right= 20)
            time.sleep(2)
            self.fwd(left=20, right=50)
            time.sleep(2)
        
    def maze_1(self):
      self.LEFT_DEFAULT = 59.5
      self.RIGHT_DEFAULT = 60
      
      while True:
        self.fwd()
        self.servo(self.MIDPOINT)
        time.sleep(.1)
        self.read_distance()
        if self.read_distance() < 100:
          self.stop()
          self.servo(500)
          time.sleep(.3)
          rt_distance = self.read_distance()
          self.servo(2500)
          time.sleep(.3)
          lt_distance = self.read_distance()
          
          if lt_distance > rt_distance:
            self.turn_by_deg(-68)
            self.stop()
          elif rt_distance > lt_distance:
            self.turn_by_deg(72)
            self.stop()
          
    def shake(self):
        """ Another example move """
        self.deg_fwd(720)
        self.stop()

    def example_move(self):
        """this is an example dance move that should be replaced by student-created content"""
        self.right() # start rotating right
        time.sleep(1) # turn for a second
        self.stop() # stop
        self.servo(1000) # look right
        time.sleep(.25) # give your head time to move
        self.servo(2000) # look left

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 25):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        
        # TODO: build self.quick_check() that does a fast, 3-part check instead of read_distance
        while self.read_distance() > 250:  # TODO: fix this magic number
            self.fwd()
            time.sleep(.01)
        self.stop()
        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  

    