[SCENE_RECIPE]

NAME: urban rail canyon
SCENE_TYPE: dense city rail / tram corridor / elevated transit action environment
MOOD_TAGS:
- compressed
- urban
- wet
- industrial
- cinematic
- high-perspective-pressure

CORE_OBJECT_SET:
- rail track
- tram car or train car
- building facade
- window grid
- transit signage glyph panel
- cable bundle
- glass reflection panel

OPTIONAL_OBJECTS:
- overhead gantry
- platform edge
- signal light
- service ladder
- guardrail
- warning panel
- rain puddle / wet reflection strip
- distant bridge or overpass
- creature frame or action foreground object when fantasy is involved

LAYOUT_PATTERNS:
- lock a primary depth axis first: rails, tram body, roof seams, and corridor edges should share the same vanishing direction
- use building facades as left/right vertical planes, not random dark texture
- place signage on buildings, gantries, platform edges, or tram/station surfaces with visible mounts
- route cable bundles along walls, gantries, or overhead planes; do not let them float across empty air unless they attach at both ends
- use glass panels and windows as lower-contrast depth rhythm, not equal-brightness clutter
- reserve a clear lane around the main figure’s face, hands, and silhouette

FOCAL_SUPPORT:
- rails and tram roof act as scale and motion anchors
- building facades compress the subject and increase pressure
- signage and glyph panels provide small accent blocks and worldbuilding
- glass and wet metal catch controlled highlights that point back to the focal subject
- cables can frame or guide the eye but should not overpower anatomy or vehicle scale

DENSITY_RULES:
- highest density at side-plane architecture, cable routes, rail hardware, and non-focal signage clusters
- medium density on tram roof/body, nearby windows, and selected glass panels
- lowest density around the face, hands, weapon grip, support contact, and key silhouette gaps
- if detail starts to hide scale, remove decorative texture before removing rails, tram box, facade planes, or support contact

LIGHTING_IMPLICATIONS:
- wet rails, tram roof, and glass panels create long aligned highlights along the depth axis
- signage adds tiny cyan/green/red accent blocks but should stay subordinate to the main focal hierarchy
- building facades often sit in dark mid/low values, with edge glints defining plane changes
- hard backlight can separate figure, tram, and creature/foreground frame from the city mass

STYLE_VARIATIONS:
- realistic: stronger rail hardware, window modules, sign mounts, grime, and believable distance haze
- anime simplified: fewer objects, clearer rail/tram/facade silhouettes, controlled signage blocks
- cyberpunk: stronger neon signs, glass reflections, cable density, and wet surfaces
- gothic urban fantasy: darker vertical slabs, harsher white cuts, creature or cloak frames, and reduced readable signage
- redjuice-inspired: sharp variable line, dark architectural planes, tiny surgical accent glyphs, and face-first density control

RELATED_OBJECT_CARDS:
- illustration-library/object_cards/urban/rail_track.md
- illustration-library/object_cards/transport/tram_car.md
- illustration-library/object_cards/urban/building_facade.md
- illustration-library/object_cards/urban/window_grid.md
- illustration-library/object_cards/urban/transit_signage_glyph_panel.md
- illustration-library/object_cards/industrial/cable_bundle.md
- illustration-library/object_cards/urban/glass_reflection_panel.md
- illustration-library/object_cards/industrial/warning_panel.md
- illustration-library/object_cards/urban/roadside_guardrail.md

SOURCE_NOTES:
- Recipe built as a reusable environment pack for rail / tram / city corridor scenes after scale and perspective issues in dense action compositions
- Intended to prevent generic background texture by requiring plane-aware object placement and shared perspective

CONFIDENCE: high

LAST_UPDATED: 2026-04-24

[/SCENE_RECIPE]
