Notes from Autumn Rogers (80kv) class visit

* drum tree
	* design considerations
		* hate standing behind a drum machine or table
		* looking for something standalone, stands on its own
		* raspberry pi generates audio using supercollider
		* want some kind of variation in rhythm without too much interaction
			* ability to write custom algorithm for behaviour
		* took the part of her brain that conceptualizes rhythm and turned it into an object
		* scale of  instrument creates a gravitas
		* arms detach for transport
			* PVc pipe for main frame
		* sound design
			* kick, snare, hihat, 2 toms
			* mostly noise based
				* actually uses samples
				* maybe the noise is mostly due to bitcrushing (or zoom?)
	* algorithmically generating a rhythm
		* weighted probabilities for how probable a note will be on a step
			* weighted for rock rhythm
			* 16 steps / 1 measure
			* weightings are set per sensor
			* plays a base  pattern for 3-bars then generates a new pattern with currently selected weighting
				* only plays new pattern for one bar, then goes to base pattern
			* after 4-16 bars randomly changes base pattern
		* 3 nodes per branch
		* strings optionally attach to nodes to remember which node is active
		* inmost node has fewest notes, outermost has more notes
	* turn swing on with a switch
	* potentiometer for bitcrushing
		* compensate for lower bitrates
	* how to control tempo?
		* pads start stop, tap tempo, trigger additional sample
	* when are probabilities set?
	* visual feedback
		* leds when branch is active
		* strings to indicate active node
	* what would she change if she were to do it again
		* robustness
* gloves
	* design considerations
		* gloves are super obvious design
			* visually strong design
			* sci-fi / cyberpunk
				* exposed wires
				* leds
				* lasers on arms of drum tree
		* something that will allow for interative with another instrument while also using gloves
			* (originally guitar)
		* totally wireless
			* receiver and processing inside drum tree
		* single system allows gloves and drum tree to interact
		* each album uses a new mapping /synthesis
	* mechaincal design
		* sintra - expandable foam for costume design
			* heat up to make moldable
		* elastic straps
			* rings with snaps for fingers
			* zipper for forearm
			* velcro on neck
	* visual aesthetic
	* sensing
		* 4 flex sensors on left hand
		* imu on right hand
	* sound design
	* mapping
		* IMU mappings
			* BNO055 9-dof sensor
			* IMU sends out XYZ in degrees
				* absolute orientation
			* arm pitch to frequency (y-axis)
			* z-axis / fine grained control (roll)
				* good for delicate control
			* x-axis: difficult to be precise (yaW)
				* good for dramatic statements, requires big arm motions
			* use mouse to try out mappings
				* then plug in glove 
			* binary trigger by flicking arm
				* if acceleratino exceeds threshold
					* debounce to prevent retriggering
					* IMU sends out
				* leds light up to indicate state
			* mostly uses ptich roll yaw
				* more complex signals are hard to use in performance, too complex
				* requires practice to keep all these signals in your head
			* flex sensor is analog
				* converts to binary signal / continuous is too hard to keep track off
					* indicates if finger bent or not
				* uses of flex:
					* turn on synthesizers, or effects
					* or can modify parameters
					* use boolean logic to combine finger signals (16 possible states)
					* 
		* able to manipulate sample from drum tree
		* able to select fx for harp
			* distortion, reverb, dry
			* manual switch on glove
		* sample transformation
			* y-axis pitch
			* z-axis length of sample slice
			* x-axis where in sample slice begins
		* IMU intialization
			* X-axis calibrates to zero when system is powered on
			* when performance starts by ‘demonstrating’ by doing simple obvious motions
		* likes to go through 3 different iterations to get to final form
		* likes building things physically, less interested in digital manufacturing