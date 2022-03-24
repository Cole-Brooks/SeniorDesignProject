import os
import subprocess
import sys

# readPlate:
# returns a tuple containing the plate number followed by the confidence
# takes the path to the image you want to analyze
def readPlate(img):
	# run the command to read the plate
	cmd = 'alpr -n 1 ' + img
	output = subprocess.check_output(cmd, shell=True).decode("utf-8")
	
	# reformat. Keep only the license plate and the confidence
	try:
		plateNum = output[output.index('\n'):output.index('\t')].strip()[2:]
		confidence = float(output[output.index("confidence") + 10:].strip()[2:])
	except:
		print("An error has occurred in reading this plate")
		return ("No Plate Found", -1)

	return (plateNum,confidence)

if __name__ == "__main__":
	args = sys.argv[1:]
	if (len(args) == 0) or (args[0] != "-p"):
		img = "car6.jpg"
	else:
		img = args[1]
	print(readPlate(img))
