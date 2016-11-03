#python

# Compy

# Add to Background pass
# Remove from Background pass

# Add to Foreground pass
# Remove from Foreground pass

# Add to [Aux] pass
# Remove from [Aux] pass
# Delete [Aux] pass
# ... (FCL)

# Add new pass

# Auto-Add Changes to Pass (Warning!)
# Apply Changes
# Discard Changes

# Convert to Shadow Catcher
# Add Shadow Choke

# Define Background Outputs
# Define Foreground Outputs
# Define [Aux] Outputs... (FCL)

# Define Output Location
# Define Output Pattern

# Preview Foreground
# Preview Background
# Preview Full Image

# Render All

# Remove Compy from Scene


import modo

TAG = "FLOR"

PRODUCT_GLOC = "product_group"
FLOOR_GLOC = "floor_group"
PASS_GROUP = "floor_passes"

product_grp = None
floor_grp = None
pass_grp = None

for i in modo.Scene().iterItems():
    if i.hasTag(TAG):
        if i.getTags()[TAG] == PRODUCT_GLOC:
            product_grp = i
        if i.getTags()[TAG] == FLOOR_GLOC:
            floor_grp = i
        if i.getTags()[TAG] == PASS_GROUP:
            pass_grp = i

    if None not in (product_grp, floor_grp, pass_grp):
        break

if product_grp == None:
    product_grp = modo.Scene().addItem('groupLocator')
    product_grp.name = PRODUCT_GLOC
    product_grp.setTag(TAG, PRODUCT_GLOC)

if floor_grp == None:
    floor_grp = modo.Scene().addItem('groupLocator')
    floor_grp.name = FLOOR_GLOC
    floor_grp.setTag(TAG, FLOOR_GLOC)

if pass_grp == None:
    pass_grp = modo.Scene().addItem('group')
    pass_grp.setTag('GTYP','render')
    pass_grp.name = PASS_GROUP
    pass_grp.setTag(TAG, PASS_GROUP)

for i in modo.Scene().selected:
    if i.isLocatorSuperType():
        i.setParent(floor_grp)


scn_svc = lx.service.Scene ()
type_shader = scn_svc.ItemTypeLookup (lx.symbol.sITYPE_DEFAULTSHADER)
type_mesh = scn_svc.ItemTypeLookup (lx.symbol.sITYPE_MESH)

scn_sel = lxu.select.SceneSelection ()

scene = lx.object.Scene (scn_sel.current ())
mesh_item = scene.AnyItemOfType (type_mesh)
shader_item = scene.ItemAdd (type_shader)

shd_gph = lx.object.ItemGraph (scene.GraphLookup (lx.symbol.sGRAPH_SHADELOC))
shd_gph.AddLink (mesh_item, shader_item)

# TODO: include radius for floor shadows and reflections

#layout.createOrClose cookie:GraphEditor open:? layout:{Graph Editor Palette_layout} title:{@frame.vpgraph@@0@} width:1080 height:325 persistent:1 style:palette
