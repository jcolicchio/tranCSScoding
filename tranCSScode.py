def hashFromRGB(r, g, b):
	r = hex(r)[2:4]
	if len(r) < 2:
		r = "0"+r
	g = hex(g)[2:4]
	if len(g) < 2:
		g = "0"+g
	b = hex(b)[2:4]
	if len(b) < 2:
		b = "0"+b
	return "#"+r+g+b

def hashAtFrameXY(frame, x, y):
	r, g, b = frame.getpixel((x, y))
	return hashFromRGB(r, g, b)

def cssFromFrameWithScale(frame, scale):
	frame = frame.resize((int(frame.size[0]*scale), int(frame.size[1]*scale)), Image.NEAREST)
	out = "background:"+hashAtFrameXY(frame, 0, 0)+";box-shadow:"
	
	pixels = frame.size[0]*frame.size[1]
	notfirst = False
	threshold = 250 # 255 is no threshold
	for i in range(1, pixels):
		x = i % frame.size[0]
		y = i // frame.size[0]
		r, g, b = frame.getpixel((x, y))
		if r < threshold and g < threshold and b < threshold:
			if notfirst:
				out += ","
			else:
				notfirst = True
			out += str(x)+"px "+str(y)+"px"+hashAtFrameXY(frame, x, y)
		

	return out

#todo: some math to determine min distinguishable percent sig figs

def cssFromFramesWithFPSAndScale(frames, frameRate, scale):
	frameRepeat = 240//frameRate # ensure it always has a "click time" of 1/30
	frameCount = len(frames) # 481
	duration = frameCount/float(frameRate) # 481 seconds
	percentPerFrame = 10000/(frameCount*frameRepeat)/100.0 # 0.02079 %
	
	line = cssFromFrameWithScale(frames[0], scale)
	out = "<html><head><style>.scale{-webkit-transform:scale("+str(1.0/scale)+");width:1px;margin:"+str(int(1.0/scale))+"px;}.apng{width:1px;height:1px;"+line+";-webkit-animation:apngframes "+str(duration)+"s infinite} @-webkit-keyframes apngframes {"
	
	outfile = open(sys.argv[1]+'.html', 'w')
	outfile.write(out)
	outfile.flush()
	for i in range(1,frameCount):
		out = ""
		if frameRepeat > 1:
			out = str(percentPerFrame*(i*frameRepeat-1))+"%{"+line+"}"
		line = cssFromFrameWithScale(frames[i], scale)
		out += str(percentPerFrame*i*frameRepeat)+"%{"+line+"}"

		print("done with frame "+str(i))
		outfile.write(out)
		outfile.flush()
	out += "}</style></head><body><div class='scale'><div class='apng'></div></div></body></html>"
	outfile.write(out)
	outfile.close()

import sys, os
from PIL import Image, ImageSequence
im = Image.open(sys.argv[1]+'.gif')
frames = [frame.copy().convert('RGB') for frame in ImageSequence.Iterator(im)]
# now frameData is a list of frame objects which can be called getpixel((x,y)) on

cssFromFramesWithFPSAndScale(frames, 12, float(sys.argv[2]))
