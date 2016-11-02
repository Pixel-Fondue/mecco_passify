#python

# Floor It

import modo

TAG = "FLOR"

PRODUCT_GLOC = "product_group"
FLOOR_GLOC = "floor_group"

product_grp = None
floor_grp = None

for i in modo.Scene().iterItems():
	if i.hasTag(TAG):
		if i.getTags()[TAG] == PRODUCT_GLOC:
			product_grp = i
		if i.getTags()[TAG] == FLOOR_GLOC:
			floor_grp = i

	if product_grp != None and floor_grp != None:
		break

if product_grp == None:
	product_grp = modo.Scene().addItem('groupLocator')
	product_grp.name = PRODUCT_GLOC
	product_grp.setTag(TAG, PRODUCT_GLOC)

if floor_grp == None:
	floor_grp = modo.Scene().addItem('groupLocator')
	floor_grp.name = FLOOR_GLOC
	floor_grp.setTag(TAG, FLOOR_GLOC)
