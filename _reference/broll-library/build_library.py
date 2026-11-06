"""Build library.json + LIBRARY.md from drive-listing.json and the hand-written notes below.

Run from the repo root after re-listing Drive (see README in LIBRARY.md):
  python3 -I _reference/broll-library/build_library.py

people: "none" = no person or hands only (always safe)
        "A"    = the woman who filmed the pacagen-main batch (long dark hair, white/brown tops)
        "B"    = the Nov-5 creator (long brown hair; green, maroon or blue tops)
Only use a clip showing a person if that person is the speaker of the video you're editing.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

FOLDERS = {
    "pacagen-main": {
        "url": "https://drive.google.com/drive/folders/1Rzp2KmpcLtVEMqLZSZA92K9N5ShiA36Q",
        "about": "Original Pacagen kit: spray, supplement, cleaning/air purifier and general cat B-roll. 4K, cats Salem/Squirrel/Tiger.",
    },
    "pills-symptoms": {
        "url": "https://drive.google.com/drive/folders/1dcrdbOeYrqY_jpALUPfBRYTECSPseL0h",
        "about": "Allergy symptom set: pills, sprays, 3pm fog, dry mouth (person = hands or a woman not on camera elsewhere).",
    },
    "nov5-creator": {
        "url": "https://drive.google.com/drive/folders/1-7sQpKl0AAn6fOKnXBuczjWl4ajC3mjG",
        "about": "Shot by creator B (rehome / two-jobs / alpaca videos): her ragdoll + siamese cats, her kitchen, products on counter.",
    },
}

# path -> (people, description, tags, notes)
N = {
    # ---------------- pacagen-main / SPRAY ----------------
    "✅ALL SPRAY B-ROLL/bottle": ("none", "Spray bottle hand-held, label turning to camera", "spray product hero label", ""),
    "✅ALL SPRAY B-ROLL/bottle in front of cat": ("none", "Hand holds spray next to a tabby asleep on white bedding; from ~10s the bottle leaves and it's just the sleeping cat", "spray cat sleeping bed calm ending", "@0.3 bottle+cat; @10 cat only (great final shot)"),
    "✅ALL SPRAY B-ROLL/box back & side": ("none", "Spray box back and side panels in hand", "spray box packaging", ""),
    "✅ALL SPRAY B-ROLL/boxes": ("none", "Spray boxes front, logo visible", "spray box packaging brand", "used for 'that's where Pacagen came in'"),
    "✅ALL SPRAY B-ROLL/creator with box": ("A", "Woman A holding the spray box", "spray box person", "person A"),
    "✅ALL SPRAY B-ROLL/logo on box": ("none", "Close-up of the Pacagen logo on the box", "brand logo", ""),
    "✅ALL SPRAY B-ROLL/pouring from bag": ("none", "Pouring stabilizing solution from the pouch into the bottle", "spray mixing activate setup", ""),
    "✅ALL SPRAY B-ROLL/pouring powder": ("none", "Pouring WhiskerBlock powder into the bottle", "spray mixing activate powder", ""),
    "✅ALL SPRAY B-ROLL/screwing spray": ("none", "Screwing the sprayer head onto the bottle", "spray setup", ""),
    "✅ALL SPRAY B-ROLL/shaking bottle": ("none", "Shaking the bottle (mostly a plant/wall in frame, weak)", "spray shake activate", "weak framing"),
    "✅ALL SPRAY B-ROLL/spray bottle": ("none", "Bottle held against a green tiled wall", "spray product", ""),
    "✅ALL SPRAY B-ROLL/spray bottle 1": ("none", "Hand raises bottle in a sunny bedroom", "spray product bedroom", ""),
    "✅ALL SPRAY B-ROLL/spray on guest bed": ("none", "Bottle held over a guest bed, label clear", "spray bed guest 98% bedding", "@1"),
    "✅ALL SPRAY B-ROLL/spraying bed": ("A", "Woman A spraying a bed", "spray bed bedding", "person A"),
    "✅ALL SPRAY B-ROLL/spraying carpet entryway": ("A", "Woman A spraying the entryway carpet", "spray carpet floor", "person A"),
    "✅ALL SPRAY B-ROLL/spraying cat tree": ("none", "Hand sprays a cat tree by a window", "spray cat tree environment", "@1.4 hands only"),
    "✅ALL SPRAY B-ROLL/spraying cat tree 2": ("none", "Empty cat tree by a window, then a hand sprays it", "cat tree things they touch spray", "@0.3 before the spray appears"),
    "✅ALL SPRAY B-ROLL/spraying closeup": ("none", "Close-up hand spraying near a door, visible mist", "spray mist closeup environment", "@0.2"),
    "✅ALL SPRAY B-ROLL/spraying coffee table": ("A", "Woman A spraying around a coffee table", "spray furniture", "person A"),
    "✅ALL SPRAY B-ROLL/spraying couch": ("A", "Empty couch for ~3s, then woman A walks in and sprays it", "couch furniture spray", "@0-3 empty (user found it 'plain'); @7.6 spraying (person A)"),
    "✅ALL SPRAY B-ROLL/spraying desk chair": ("A", "Woman A spraying a white desk chair", "spray chair", "person A"),
    "✅ALL SPRAY B-ROLL/spraying dining chairs": ("A", "Woman A spraying dining chairs", "spray chairs", "person A"),
    "✅ALL SPRAY B-ROLL/spraying pillows": ("A", "Woman A spraying pillows on a bed", "spray pillows bedding", "person A"),
    "✅ALL SPRAY B-ROLL/spraying scratcher": ("A", "Spraying a cat scratcher post (woman A's arm/body in frame)", "spray scratcher cat", "person A"),
    "✅ALL SPRAY B-ROLL/spraying sheets": ("A", "Woman A spraying white bed sheets", "spray sheets bedding", "person A"),
    "✅ALL SPRAY B-ROLL/spraying stairs": ("A", "Woman A spraying carpeted stairs, face visible at end", "spray stairs carpet", "person A"),
    "✅ALL SPRAY B-ROLL/spraying stools": ("A", "Woman A spraying bar stools", "spray stools", "person A"),
    "✅ALL SPRAY B-ROLL/spraying sunlight": ("none", "Spray in sunlight over a bed with a visible mist cloud", "spray mist neutralize 98%", "@3.2"),
    "✅ALL SPRAY B-ROLL/unboxing": ("none", "Unboxing the spray kit on a table", "spray unboxing kit", ""),
    "✅ALL SPRAY B-ROLL/unscrewing bottle": ("none", "Unscrewing the bottle cap", "spray setup", ""),
    # ---------------- pacagen-main / SUPPLEMENT ----------------
    "✅ALL SUPPLEMENT B-ROLL/back of supplement": ("none", "Back label of the supplement jar", "supplement label ingredients", ""),
    "✅ALL SUPPLEMENT B-ROLL/cats eating": ("none", "Cats eating from plates", "supplement cats eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/cats eating 2": ("none", "Cats eating from plates", "supplement cats eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/cats eating 3": ("none", "Two cats eating from metal plates on a wooden table", "cats eating multi-cat three cats", "@1"),
    "✅ALL SUPPLEMENT B-ROLL/cats eating tiger+squirrel": ("none", "Tiger and Squirrel eating side by side", "cats eating multi-cat", ""),
    "✅ALL SUPPLEMENT B-ROLL/eating": ("none", "Cat eating close", "supplement cat eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/eating + supplement": ("none", "Cats eating with the jar beside the plates", "supplement drug-free eating jar", "@1"),
    "✅ALL SUPPLEMENT B-ROLL/eating closeups": ("none", "Close-ups of cats eating", "supplement eating closeup", ""),
    "✅ALL SUPPLEMENT B-ROLL/eating full plates": ("none", "Cats at full plates", "supplement eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/empty plates": ("none", "Empty licked plates", "supplement picky finished", ""),
    "✅ALL SUPPLEMENT B-ROLL/food + supplement": ("none", "Plate of food with the supplement", "supplement food", ""),
    "✅ALL SUPPLEMENT B-ROLL/hero shot": ("none", "Supplement jar hero shot", "supplement product hero", ""),
    "✅ALL SUPPLEMENT B-ROLL/IMG_0451.MOV": ("none", "Long supplement/cat clip (88s), not reviewed in detail", "supplement", "review before use"),
    "✅ALL SUPPLEMENT B-ROLL/jar in front of cats eating": ("none", "Jar in the foreground, cats eating behind", "supplement jar eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/open jar in front of cats eating": ("none", "Open jar in front, cats eating behind", "supplement jar eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/opening jar + scoop": ("none", "Opening the jar and taking the scoop out", "supplement scoop open", ""),
    "✅ALL SUPPLEMENT B-ROLL/opening supplement": ("none", "Opening the supplement jar", "supplement open", ""),
    "✅ALL SUPPLEMENT B-ROLL/placing plates + supplement on counter": ("none", "Plates and jar placed on the counter", "supplement setup", ""),
    "✅ALL SUPPLEMENT B-ROLL/pouring food + supplement": ("none", "Pouring food then supplement (110s)", "supplement food pour", ""),
    "✅ALL SUPPLEMENT B-ROLL/putting supplement in food": ("none", "Scoop of supplement onto food on a metal plate", "supplement scoop how it works topper", "@16"),
    "✅ALL SUPPLEMENT B-ROLL/salem near food": ("none", "Plate with topped food on a mat, hand sets it down", "supplement food setting", ""),
    "✅ALL SUPPLEMENT B-ROLL/scoop+ supplement": ("none", "Scoop beside the jar", "supplement scoop", ""),
    "✅ALL SUPPLEMENT B-ROLL/scooper": ("none", "The included scooper", "supplement scoop dose", ""),
    "✅ALL SUPPLEMENT B-ROLL/scooping powder on food": ("none", "Scooping powder onto food (80s)", "supplement scoop topper", ""),
    "✅ALL SUPPLEMENT B-ROLL/scooping supplement": ("none", "Scooping from the jar", "supplement scoop", ""),
    "✅ALL SUPPLEMENT B-ROLL/setting food down": ("none", "Setting a plate down", "supplement feeding", ""),
    "✅ALL SUPPLEMENT B-ROLL/setting food down + cats eating": ("none", "Plate set down, cats come and eat", "supplement feeding eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/squirrel + tiger finishing food": ("none", "Two cats finishing their food", "supplement eating finished", ""),
    "✅ALL SUPPLEMENT B-ROLL/squirrel eating leftovers": ("none", "Squirrel eating leftovers", "supplement eating", ""),
    "✅ALL SUPPLEMENT B-ROLL/squirrel licking plate": ("none", "Cat licking a clean plate", "supplement picky eater loves it", ""),
    "✅ALL SUPPLEMENT B-ROLL/supplement": ("none", "Supplement jar", "supplement product", ""),
    "✅ALL SUPPLEMENT B-ROLL/supplement +empty plate": ("none", "Jar next to an empty plate", "supplement finished", ""),
    "✅ALL SUPPLEMENT B-ROLL/supplement dining table": ("none", "Jar on a dining table", "supplement product", ""),
    "✅ALL SUPPLEMENT B-ROLL/supplement in front of bed": ("none", "Hand holds the jar in front of a bed", "supplement product CTA", "@3"),
    "✅ALL SUPPLEMENT B-ROLL/supplement in front of cat": ("none", "Hand holds the jar next to a tabby lying on a blanket", "supplement switch reveal cat", "@1"),
    "✅ALL SUPPLEMENT B-ROLL/supplement in front of plates": ("none", "Jar in front of plates", "supplement", ""),
    "✅ALL SUPPLEMENT B-ROLL/supplement lid open": ("none", "Jar with lid open", "supplement open", ""),
    "✅ALL SUPPLEMENT B-ROLL/supplement+scoop": ("none", "Jar with the scoop", "supplement scoop", ""),
    "✅ALL SUPPLEMENT B-ROLL/tigerino eating": ("none", "Tiger eating", "supplement eating", ""),
    # ---------------- pacagen-main / CLEANING ----------------
    "✅CLEANING_AIR PURIFIERS B-ROLL/2 air purifiers": ("none", "Two air purifiers running", "tried everything air purifier", "@0.5"),
    "✅CLEANING_AIR PURIFIERS B-ROLL/air purifier 2": ("none", "Air purifier close", "air purifier", ""),
    "✅CLEANING_AIR PURIFIERS B-ROLL/laundry": ("none", "White sheet going into a washer", "washing bedding laundry", "@6.8"),
    "✅CLEANING_AIR PURIFIERS B-ROLL/laundry 2": ("none", "Laundry", "washing bedding laundry", "not reviewed in detail"),
    "✅CLEANING_AIR PURIFIERS B-ROLL/laundry 3": ("A", "Laundry with woman A in a different outfit", "laundry", "person A"),
    "✅CLEANING_AIR PURIFIERS B-ROLL/room air purifier": ("A", "Room air purifier, ends on a face close-up", "air purifier", "ends on face"),
    "✅CLEANING_AIR PURIFIERS B-ROLL/sweeping": ("none", "Sweeping the floor", "cleaning tried everything", "@2"),
    '✅CLEANING_AIR PURIFIERS B-ROLL/sweeping floor': ('A', 'Woman A sweeping a wood floor', 'cleaning sweeping tried everything', 'person A'),
    '✅CLEANING_AIR PURIFIERS B-ROLL/vaccuming 3': ('A', 'Woman A vacuuming a room', 'vacuuming cleaning tried everything', 'person A'),
    '✅CLEANING_AIR PURIFIERS B-ROLL/vacuuming': ('A', 'Woman (purple pajamas) vacuuming the kitchen', 'vacuuming cleaning', 'person (other woman); HDR'),
    '✅GENERAL CAT B-ROLL/2 cats eating treat': ('none', 'Hand feeds a treat stick to two tabbies on a bed', 'cats treat multi-cat', 'hands only'),
    '✅GENERAL CAT B-ROLL/2 cats on bed pets': ('A', 'Woman petting two cats on a white bed', 'petting cats bed', 'person'),
    '✅GENERAL CAT B-ROLL/2 cats on cat tree': ('none', 'Two tabbies on a white cat tree', 'cat tree multi-cat places they spend time', 'HDR'),
    '✅GENERAL CAT B-ROLL/bed': ('A', 'Woman lying in bed with a tabby, selfie angle', 'sleeping with cat bed', 'person; HDR'),
    '✅GENERAL CAT B-ROLL/creator & squirrel cuddles': ('A', 'Woman lying on a bed cuddling a tabby, top-down', 'cuddles payoff', 'person'),
    '✅GENERAL CAT B-ROLL/cuddling tiger bed hoodie': ('A', 'Woman (pink hoodie) cuddling a tabby in bed', 'sleep with cat payoff', 'person; HDR'),
    '✅GENERAL CAT B-ROLL/cuddling with squirrel': ('A', 'Woman asleep in bed with a tabby, sunlight', 'sleep with cat payoff bedroom', 'person; HDR'),
    '✅GENERAL CAT B-ROLL/grooming on bed': ('none', 'Tabby licking/grooming on a bed', 'grooming saliva Fel d 1 skin oils', 'great for saliva lines'),
    '✅GENERAL CAT B-ROLL/guest room squirrel': ('A', 'Woman on a guest bed holding a tabby (orange blanket)', 'guest room visit', 'person'),
    '✅GENERAL CAT B-ROLL/guest room squirrel 1': ('A', 'Woman reading on a guest bed, cat beside', 'guest room visit', 'person'),
    '✅GENERAL CAT B-ROLL/kneading': ('none', 'Tabby kneading a blanket', 'kneading cat cosy', 'HDR'),
    '✅GENERAL CAT B-ROLL/kneading w sweater': ('none', 'Tabby in a sweater on a bed', 'cat cute', 'HDR'),
    '✅GENERAL CAT B-ROLL/petting + kneading': ('none', 'Hands pet a tabby kneading a blanket', 'petting saliva skin oils', 'hands only; HDR'),
    '✅GENERAL CAT B-ROLL/pov pets w squirrel': ('none', 'POV hand petting a tabby on bedding', 'petting skin oils', 'hands only'),
    '✅GENERAL CAT B-ROLL/pov tiger pets': ('none', 'POV hand petting a tabby on a bed', 'petting', 'hands only'),
    '✅GENERAL CAT B-ROLL/reading on bed w cats': ('A', 'Woman reading in bed with two cats (97s)', 'payoff sleep bedroom living with cats', 'person'),
    '✅GENERAL CAT B-ROLL/salem': ('none', 'Black cat rolling on the floor (starts on red frame)', 'black cat', 'start after 1.5s; HDR'),
    '✅GENERAL CAT B-ROLL/salem & squirrel outside': ('none', 'Black cat and tabby on a patio', 'cats outside', 'off-topic'),
    '✅GENERAL CAT B-ROLL/salem + squirrel': ('none', 'Black cat and tabby in sweater outside by a wall', 'cats outside', 'off-topic; HDR'),
    '✅GENERAL CAT B-ROLL/salem closeup bed': ('none', 'Black cat close-up against a striped blanket', 'black cat close', 'HDR'),
    '✅GENERAL CAT B-ROLL/salem in hoodie street': ('A', 'Woman holds a black cat in a hoodie outside', 'cat outside', 'person; off-topic; HDR'),
    '✅GENERAL CAT B-ROLL/salem in jacket': ('A', 'Woman (pink hoodie) holding a black cat', 'cat person', 'person; HDR'),
    '✅GENERAL CAT B-ROLL/salem on bed': ('none', 'Black cat lying on a floral bed', 'cat bed bedding', 'duplicate names exist'),
    '✅GENERAL CAT B-ROLL/salem on bed pets': ('A', 'Woman petting a black cat on a floral bed', 'petting bed', 'person'),
    '✅GENERAL CAT B-ROLL/salem on couch': ('none', 'Black cat on a couch, close', 'cat couch furniture', 'HDR'),
    '✅GENERAL CAT B-ROLL/salem pets tiger on bed': ('A', 'Woman petting two cats on a floral bed, wide', 'petting bed', 'person'),
    '✅GENERAL CAT B-ROLL/salem sleeping': ('none', 'Black cat asleep on carpet', 'cat sleeping carpet', 'HDR'),
    '✅GENERAL CAT B-ROLL/salem sleeping chair': ('none', 'Black cat asleep on a chair, very close', 'cat sleeping', 'close/blurry'),
    '✅GENERAL CAT B-ROLL/sleeping on carpet': ('none', 'Tabby asleep in sun on a rug', 'cat sleeping carpet floor', 'HDR'),
    '✅GENERAL CAT B-ROLL/squirrel': ('none', 'Tabby close by a window', 'cat close', 'HDR'),
    '✅GENERAL CAT B-ROLL/squirrel & salem on carpet': ('none', 'Two cats lying on a rug by a door', 'cats carpet floor multi-cat', 'HDR'),
    '✅GENERAL CAT B-ROLL/squirrel biscuits': ('none', 'Tabby kneading a blanket', 'kneading cosy', 'dark'),
    '✅GENERAL CAT B-ROLL/squirrel bow tie': ('none', 'Tabby in a bow tie sitting', 'cat cute', 'HDR'),
    '✅GENERAL CAT B-ROLL/squirrel grooming outside': ('none', 'Tabby grooming outside on concrete', 'grooming', 'off-topic'),
    '✅GENERAL CAT B-ROLL/squirrel in sweater': ('none', 'Tabby in a sweater on a fluffy bed', 'cat cute bed', 'HDR'),
    '✅GENERAL CAT B-ROLL/squirrel making biscuits': ('none', 'Tabby kneading a blanket', 'kneading', 'dark'),
    '✅GENERAL CAT B-ROLL/squirrel napping on bed': ('none', 'Tabby napping on a bed', 'cat sleeping bed bedding', 'duplicate names exist'),
    '✅GENERAL CAT B-ROLL/squirrel on sheets': ('none', 'Tabby lying on white sheets', 'cat bedding sheets', 'HDR; duplicate names exist'),
    '✅GENERAL CAT B-ROLL/squirrel pets': ('A', 'Woman lying on a bed petting a tabby', 'petting bed', 'person; HDR'),
    '✅GENERAL CAT B-ROLL/squirrel sleeping blanket': ('none', 'Tabby asleep on a white blanket', 'cat sleeping bedding', 'calm ending'),
    '✅GENERAL CAT B-ROLL/tiger & salem on bed': ('none', 'Tabby and black cat lying on a floral bed', 'cats bed multi-cat bedding', 'duplicate names exist'),
    '✅GENERAL CAT B-ROLL/tiger & squirrel on table': ('none', 'Two cats sitting on a dining table', 'cats table furniture', 'HDR'),
    '✅GENERAL CAT B-ROLL/tiger cat tree': ('none', 'Tabby lying on a white cat tree', 'cat tree places they spend time', 'HDR'),
    '✅GENERAL CAT B-ROLL/tiger grooming on bed': ('none', 'Tabby grooming on a floral bed', 'grooming saliva bed', ''),
    '✅GENERAL CAT B-ROLL/tiger in hoodie bed': ('A', 'Woman (pink hoodie) in bed with a tabby', 'sleep with cat', 'person; HDR'),
    '✅GENERAL CAT B-ROLL/tiger in living room': ('none', 'Tabby walking across a living room rug', 'cat living room', 'HDR'),
    '✅GENERAL CAT B-ROLL/tiger king': ('none', 'Tabby in a king costume on a bed', 'cat cute costume', 'off-tone'),
    '✅GENERAL CAT B-ROLL/tiger on bed': ('none', 'Tabby lying on a floral bed', 'cat bed', ''),
    '✅GENERAL CAT B-ROLL/tiger on couch': ('none', 'Tabby curled on a couch, hand with blanket', 'cat couch', 'HDR'),
    '✅GENERAL CAT B-ROLL/tiger on sheets': ('none', 'Tabby on white sheets by a headboard', 'cat bed sheets', 'HDR'),
    '✅GENERAL CAT B-ROLL/tiger outside': ('none', 'Tabby lying on a patio', 'cat outside', 'off-topic'),
    '✅GENERAL CAT B-ROLL/tiger pets on bed': ('A', 'Woman petting a tabby on a floral bed', 'petting', 'person'),
    '✅GENERAL CAT B-ROLL/tiger sleeping': ('none', 'Tabby asleep belly-up, close', 'cat sleeping cosy', ''),
    '✅GENERAL CAT B-ROLL/tiger tie': ('none', 'Tabby wearing a tie on a cat tree', 'cat cute', 'HDR'),
}

NOV5 = {
    "Air filter.MOV": ("none", "White air purifier then cats on a cat tree by a clock", "air purifier cat tree", ""),
    "back side of package supplement.mov": ("none", "Hand turns the supplement jar, spray behind", "supplement label", ""),
    "backside of package 2.mov": ("none", "Spray box back: 'Inside this Pack' (WhiskerBlock powder, solution, founder video QR)", "how it works science box WhiskerBlock", "used for 'how it works' CTA"),
    "cat by window moving around.mov": ("none", "Siamese on a window bed, jumps down", "cat window home", ""),
    "Cat eating .mov": ("none", "Fluffy ragdoll eating from a bowl on a tray", "cat eating", ""),
    "Cat eating the supplements .mov": ("none", "Siamese eating, supplement jar beside bowl", "supplement eating jar", ""),
    "cat eating.MOV": ("none", "Ragdoll at the food tray, several bowls", "cat eating multi-cat bowls", "@1"),
    "Cat hair everywhere grabbing the hair.MOV": ("none", "Hand pinches cat hair out of a fuzzy cat bed", "cat hair everywhere places cats have been", "@1"),
    "cat in house - filler video.mov": ("none", "White ragdoll on a sunny couch", "cat couch furniture", "@0.3"),
    "Cat locked out waiting.MOV": ("none", "Siamese walks around a door, carpet", "cat locked out bedroom door", ""),
    "Cat next to supplement while eating.mov": ("none", "Siamese eating, jar beside", "supplement eating jar", ""),
    "Cat waiting at door.MOV": ("none", "Siamese waiting at a doorway", "cat door bedroom", ""),
    "Grooming on bed.mov": ("none", "Grey ragdoll grooming on a bed", "cat grooming saliva skin oils", "@1"),
    "Lint rolling Cat hair.MOV": ("B", "Creator B (green top) lint-rolling cat hair off herself", "cat hair lint roll allergies cleaning", "person B"),
    "rag doll by window .mov": ("none", "Ragdoll by window, then walks past a cat tree", "cat home", ""),
    "ragdoll hide.mov": ("none", "Ragdoll hiding under a trampoline", "cat home", ""),
    "showing each product.mov": ("B", "Creator B (green top) holds up each product at the counter", "products spray box CTA", "@3.5 refill box (person B)"),
    "showing product on counter.mov": ("none", "Pan across spray, pouch, boxes and jar on the counter", "product lineup Pacagen CTA", "@0.4"),
    "showing product on counter 2.mov": ("none", "Close pan across pouch, box, jar", "product lineup Pacagen", ""),
    "showing the back side of package 1.mov": ("none", "Back of spray box: Step 1 Activate / 2 Neutralize / 3 Relax & Repeat", "how it works steps science", ""),
    "supplement side view.mov": ("none", "Hand turns the supplement jar", "supplement product", ""),
    "whisker block powder.mov": ("none", "Hand holds the WhiskerBlock powder packet", "WhiskerBlock science protein powder", ""),
}
IMG = {  # nov5 IMG_* by number (first matching id is used if duplicates)
    "IMG_0102": ("none", "Spray box back 'Inside this Pack' in hand", "how it works box", ""),
    "IMG_0107": ("B", "Creator B in kitchen setting out three bowls", "multi-cat feeding", "person B"),
    "IMG_0112": ("B", "Tall cat tree, creator B at edge", "cat tree", "person B at edge"),
    "IMG_0113": ("none", "Siamese on a window ledge over a cat bed", "cat window", ""),
    "IMG_0114": ("none", "Siamese on a sunny windowsill next to the spray bottle", "spray cat environment targets", "@1"),
    "IMG_0122": ("none", "Siamese playing with a feather toy", "cat playing", ""),
    "IMG_0123": ("none", "Siamese lying with a feather toy", "cat playing", ""),
    "IMG_0124": ("none", "Siamese playing with toys on carpet", "cat playing", ""),
    "IMG_0126": ("none", "Siamese eating, supplement jars beside", "supplement eating", ""),
    "IMG_0127": ("none", "Grey ragdoll in a black box bed", "cat", ""),
    "IMG_0130": ("none", "Grey ragdoll lying belly-up on a white blanket", "cat bedding blanket", "@0.5"),
    "IMG_0131": ("none", "Hand pets a grey ragdoll on bedding", "cat petting saliva skin oils", "@2"),
    "IMG_0132": ("none", "Grey ragdoll sitting on a bed", "cat bed", ""),
    "IMG_0133": ("none", "Grey ragdoll on a bed, close", "cat bed", ""),
    "IMG_0134": ("none", "Arm pets ragdoll on bed", "cat petting", ""),
    "IMG_0135": ("none", "Ragdoll lying on a quilted bed", "cat bed", ""),
    "IMG_0136": ("none", "Hand pets ragdoll lying on bed", "cat petting", ""),
    "IMG_0137": ("none", "Ragdoll on bed, room wide", "cat bed", ""),
    "IMG_0138": ("none", "Grey ragdoll close-up staring at camera on bed", "cat closeup Fel d 1 protein", "@0"),
    "IMG_0139": ("none", "Arm pets ragdoll on bed", "cat petting", ""),
    "IMG_0140": ("none", "Ragdoll on bed, sits up", "cat bed", ""),
    "IMG_0141": ("none", "Ragdoll on bed, varied angles", "cat bed", ""),
    "IMG_0144": ("none", "Hand in a hair-covered cat bed", "cat hair", ""),
    "IMG_0145": ("B", "Creator B (green top) brushing off cat hair", "cat hair", "person B"),
    "IMG_0146": ("B", "Creator B lint rolling", "cat hair lint", "person B"),
    "IMG_0147": ("none", "Siamese walks a wall shelf then cat tree", "cat shelf places they spend time", "@5 (cat fully on shelf)"),
    "IMG_0148": ("none", "Siamese on a wall shelf", "cat shelf", ""),
    "IMG_0149": ("none", "Siamese on a wall shelf, close", "cat shelf", ""),
    "IMG_0150": ("none", "Siamese on a cat tree by a clock, then wall bed", "cat tree", ""),
    "IMG_0151": ("none", "Food and water bowls on a tray", "cat bowls feeding", ""),
    "IMG_0152": ("none", "Air purifier close", "air purifier", ""),
    "IMG_0153": ("none", "Air purifier then cats on cat tree", "air purifier cat tree", ""),
    "IMG_0154": ("none", "Siamese, then air purifier", "air purifier cat", ""),
    "IMG_0161": ("none", "Siamese around a door", "cat door", ""),
    "IMG_0162": ("none", "Siamese walking by a door", "cat door", ""),
    "IMG_0164": ("none", "Siamese in a doorway", "cat door", ""),
    "IMG_0165": ("B", "Creator B on the couch: siamese jumps up, she reads with the cat beside her (88s)", "payoff relaxed couch living with cat CTA", "@60 reading with cat (person B)"),
    "IMG_0169": ("none", "Feeding tray with many bowls", "multi-cat feeding three diets", ""),
    "IMG_0170": ("none", "Grey ragdoll walks toward camera past the food tray", "cat adopted walking", "@0.5"),
    "IMG_0171": ("none", "Ragdoll eating from a bowl on a tray", "cat eating", ""),
    "IMG_1108": ("B", "Creator B (maroon top) spraying a pouf/play-couch", "spray furniture breaks down allergen", "HDR: tone-map. person B"),
    "IMG_1109": ("B", "Creator B spraying a sectional couch", "spray couch", "HDR? check. person B"),
    "IMG_1110": ("B", "Creator B spraying the sectional couch", "spray couch routine", "HDR: tone-map. person B"),
    "IMG_8761": ("none", "Fluffy cat at the food tray", "cat eating", ""),
}
PILLS = {
    "3pm fog_confused": ("none", "Tired, foggy woman at a laptop (not a speaker so far)", "3pm fog tired drowsy pills toll", "@1 or @14.5; HDR-free"),
    "allergy pills": ("none", "Hand holds an allergy pill bottle", "antihistamine pills 2,200", "@0.2"),
    "annoyed taking pills": ("none", "Opening a pill box, taking a pill", "pills six years antihistamine", "@0.3, @12"),
    "allergy sprays": ("none", "Hand compares nasal sprays", "nasal spray not working", "@2.5"),
    "dry mouth_drinking water": ("none", "Drinking water", "dry mouth", "@1"),
    "TALKING HEAD _ SCRIPT": (None, None, None, None),  # not B-roll
}


def main():
    listing = json.load(open(os.path.join(HERE, "drive-listing.json")))
    lib, seen = [], set()
    for folder, files in listing.items():
        for fid, path in files:
            name = path.strip()
            key = (folder, name)
            dup = key in seen
            seen.add(key)
            if folder == "pacagen-main":
                info = N.get(name)
            elif folder == "pills-symptoms":
                info = PILLS.get(name)
            else:
                info = NOV5.get(name)
                if info is None and name.startswith("IMG_"):
                    info = IMG.get(name.split(".")[0])
            if info and info[0] is None:
                continue
            people, desc, tags, notes = info if info else ("?", "NOT REVIEWED - make a contact sheet before using", "", "")
            lib.append({"folder": folder, "path": name, "id": fid, "duplicate_name": dup,
                        "people": people, "description": desc, "tags": tags, "notes": notes})
    json.dump({"folders": FOLDERS, "clips": lib}, open(os.path.join(HERE, "library.json"), "w"), indent=1, ensure_ascii=False)

    md = ["# B-roll library", "",
          "Every Pacagen B-roll clip on Google Drive, with what it shows, so a new session can plan without downloading.",
          "Download only the clips you pick: `python3 -I _reference/broll-library/fetch_broll.py <out_dir> <id-or-name> ...`", "",
          "**people:** `none` = no person / hands only (always safe) · `A` = a woman from the pacagen-main batch (not the Nov-5 speaker; the description says who) · "
          "`B` = the Nov-5 creator (rehome / two-jobs / alpaca speaker). Use a person clip only if that person is the speaker.",
          "**@N** = good in-point in seconds. **HDR** clips must be tone-mapped (see the ugc-meta-edit skill).", ""]
    for folder, meta in FOLDERS.items():
        rows = [c for c in lib if c["folder"] == folder]
        md += [f"## {folder}", "", f"{meta['about']}  ", f"Drive: {meta['url']}", "",
               "| clip | people | shows | tags | notes | id |", "|---|---|---|---|---|---|"]
        for c in rows:
            md.append(f"| {c['path']}{' (dup)' if c['duplicate_name'] else ''} | {c['people']} | {c['description']} | "
                      f"{c['tags']} | {c['notes']} | `{c['id']}` |")
        md.append("")
    open(os.path.join(HERE, "LIBRARY.md"), "w").write("\n".join(md))
    unrev = sum(1 for c in lib if c["people"] == "?")
    print(f"{len(lib)} clips, {unrev} not yet reviewed")


main()
