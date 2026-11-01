# Creator audio library (Google Drive index)

The creator's full audio library lives in **Google Drive**: about 5,700 SFX and 400 music tracks, several GB in total. It is **not stored in git**. This folder holds:

- `catalog.json`: one entry per file (Drive `id`, `name`, `folder`, `kind` = sfx/music, `dur` in seconds when known, `kit` = repo path if it's already local).
- `fetch.mjs`: search the catalog and download single files on demand.

## Usage (run from a project folder)

```bash
node ../../assets/library/fetch.mjs search riser --kind sfx          # find sounds
node ../../assets/library/fetch.mjs search --kind music --folder motivational
node ../../assets/library/fetch.mjs folders --kind music             # list genres
node ../../assets/library/fetch.mjs get <id> --to assets             # download into this project
```

**Check `assets/sfx/` first.** The most-used sounds are already in the repo: see `assets/sfx/MANIFEST.md`, and the creator's starter kit is in `assets/sfx/kit/`.

## Sources

| # | Drive folder | What's in it |
|---|---|---|
| 1 | https://drive.google.com/drive/folders/1P-_8mPTYp-viA_VL1jbq07HhzD1mvk6x | SFX monster pack, music library by genre, reel BGM, `sound effect important 2.0` (→ starter kit) |
| 2 | https://drive.google.com/drive/folders/1yczqC7xbnb7BA6C7Q10rrC29Zdbq3_9D | 10 sounds (charge, deep bass, flash, risers, snap…) → starter kit |
| 3 | https://drive.google.com/drive/folders/1ef54jgBKat0-7nYcT79cz48sqt-Sxb2H | `20+ Sound Effects.mp4`: another creator's 48s pack-preview reel (overlapping, labelled). Reference only, not usable as clips |

Excluded from the catalog: `.DS_Store`, `.sfk` peak files, and `SFX one click download pack 3.9 GB download.zip` (folder 1 root, a zipped copy of the pack).

The folders must stay shared as **Anyone with the link → Viewer**, or `fetch.mjs get` will fail.

## Licensing ⚠️

- `ES_…` tracks are **Epidemic Sound** and `… Artlist` tracks are **Artlist**. They are only cleared for monetized posts while the publishing account holds an active subscription with that service. Confirm before using them in a published video.
- The SFX packs come from mixed sources (Pixabay, Mixkit, SoundSnap-style naming, YouTube creator packs). Treat them as the creator's responsibility to clear.

## SFX categories

| Folder | Files |
|---|---|
| (root) | 11 |
| Action Sound | 98 |
| Alarm & Chime | 36 |
| Ambience | 15 |
| Animals | 54 |
| Arcade Noises | 10 |
| Beep | 196 |
| Bell | 63 |
| Bugs | 38 |
| Button | 277 |
| Camera | 42 |
| Chime | 284 |
| Cinematic hub | 216 |
| Clicks | 27 |
| Construction & Tools | 56 |
| Crowd & People | 7 |
| Digital | 27 |
| ESFX | 16 |
| Electric | 32 |
| Epic Cinematic Trailer Impact - Pack 2 | 5 |
| Evolve Audio - Epic Drama SFX | 10 |
| Evolve Audio - Essential Transitions FREE | 6 |
| Explosions | 25 |
| FW sounds | 30 |
| Fart | 22 |
| Feeling | 6 |
| Fire & Fireworks | 28 |
| Firearms | 20 |
| Food | 8 |
| Games | 17 |
| Gear | 147 |
| Glitch | 89 |
| Hits | 47 |
| Horn | 20 |
| Insta Reel background music/audio murse/Ping Boom Major_Minor | 12 |
| Insta Reel background music/audio murse/Risers Deep Breath Major_Minor | 12 |
| Keyboard & Mouse | 53 |
| Logo Animation | 5 |
| Mechanical | 10 |
| Meme SFX | 89 |
| Miscellaneous | 5 |
| Money | 11 |
| Musical | 96 |
| Negative | 411 |
| Notifications | 302 |
| Paper Sound Effects | 29 |
| Percussion | 232 |
| Phone | 1 |
| Positive | 126 |
| Ringtones | 58 |
| Risers | 25 |
| Sci-Fi | 118 |
| Sports | 2 |
| Swishes | 16 |
| Switch | 168 |
| Swoosh | 34 |
| Tone | 20 |
| Transition Sound Effects | 142 |
| Ui Sound | 32 |
| Vehicles | 58 |
| Vibes | 6 |
| Water | 44 |
| Whoosh | 193 |
| Wind | 24 |
| build up | 16 |
| clock | 8 |
| error | 2 |
| i  phone | 17 |
| knife | 5 |
| liquid | 5 |
| other | 30 |
| pen click | 6 |
| pop | 14 |
| shining | 3 |
| sound effect important 2.0 | 84 |
| wooshes | 58 |
| z_Other | 1175 |

## Music by genre

Lengths are listed only for tracks that were downloaded while the catalog was being built. Run `search` to get the ids.

### Adventure (31)

- andalucia-max-ll-musicbed-licensed — 3:38
- ES_A Fly on the Wall - Raymond Grouse — 1:52
- ES_A Million Upheavals - Edgar Hopp — 2:46
- ES_A True Hero - Edgar Hopp — 3:59
- ES_Across the Ocean - Bonnie Grace — 2:07
- ES_Allegiances - Hampus Naeselius — 2:13
- ES_Apollo - Dream Cave — 2:21
- ES_Can_t Dampen My Spirit - Adriel Fair — 2:27
- ES_Conquest - Dragon Tamer (1) — 2:39
- ES_Crank It - Sage Oursler — 2:02
- ES_Crusaders - Adriel Fair — 1:43
- ES_Forever to Run - Howard Harper-Barnes — 2:34
- ES_Globetrotter - Adriel Fair — 2:03
- ES_Highland Hymn - Bonnie Grace — 3:08
- ES_Keep Close to the Guide - Philip Ayers — 2:21
- ES_Knight_s Templar - Adriel Fair — 1:34
- ES_Look _ See - Max Anson — 1:52
- ES_Medieval Adventure - Bonnie Grace — 2:01
- ES_On a Hunt - Philip Ayers — 2:01
- ES_Peacekeepers - Dream Cave — 2:06
- ES_Plains of Illeyneth - Dragon Tamer — 3:13
- ES_Playing With Thunder - Max Anson — 2:01
- ES_Ropes Away - Adriel Fair — 1:43
- ES_Skilled In The Arts - Yi Nantiro — 2:13
- ES_The Eye of the Storm - Edward Karl Hanson — 1:55
- ES_The Traveller - Christoffer Moe Ditlevsen — 2:53
- ES_Truce No More - Dream Cave — 1:56
- ES_Valley of Drakes - Dragon Tamer — 2:02
- ES_Victory Theme - Max Anson (1) — 2:05
- ES_Victory Theme - Max Anson — 2:05
- galway-clover by c.k.-martin Artlist — 2:59

### Alternative (26)

- big-shot-instrumental-irontom-musicbed-licensed — 3:39
- call-me-the-west-irontom-musicbed-licensed — 3:15
- cheers by rex-banner Artlist — 1:56
- ES_(Stay) True (Instrumental Version) - Lars Eriksson — 3:32
- ES_A Most Violent Man - Lofive — 3:00
- ES_Baby Don_t Care - Mike Stringer — 1:51
- ES_Cassandra, I Really Know You - Marc Torch — 1:44
- ES_Illusion (Instrumental Version) - Coma Svensson — 2:53
- ES_Just Say When - The Grateful 7 — 1:56
- ES_Smokey Goodbye - Modal Youth — 2:27
- ES_The End of Me - Gaillardia — 2:46
- ES_The Whole Nine Yards - Another Notion — 1:59
- ES_We_re Not the Same (GOOD SONG) Audio Extracted_1 — 0:01
- ES_We_re Not the Same (GOOD SONG) — 2:15
- filthy-instrumental-moony-musicbed-licensed — 2:39
- full-moon-instrumental-irontom-musicbed-licensed — 3:12
- keep-movin-along---no-lead-vocals by milano Artlist — 2:08
- let-em-talk-instrumental-lone-waves-musicbed-licensed — 3:06
- loverboy-instrumental-irontom-musicbed-licensed — 3:38
- never-wanted-your-love-instrumental-nevada-wild-musicbed-licensed — 3:23
- perfect-day-for-a-party by custommelody Artlist — 1:51
- rush-hour by dan-zeitune Artlist — 2:31
- the-gemberzee-instrumental-lovedrug-musicbed-licensed — 3:34
- way-back-when-before---instrumental-version by con-davison Artlist — 3:45
- we’ll-keep-running---instrumental-version by to-the-valley Artlist — 2:51
- when-a-dickhead-dies-instrumental-irontom-musicbed-licensed — 2:50

### Ambient (30)

- boot-sequence by jimmy-svensson Artlist — 1:56
- ES_A Closer Look - Charles Holme — 2:00
- ES_And Behold - Awlee — 4:09
- ES_Atlas Light - Farrell Wooten — 2:21
- ES_Cold War Games - Gabriel Lewis — 2:21
- ES_Detector - Max Anson — 1:46
- ES_Digital Future - Christoffer Moe Ditlevsen — 2:18
- ES_Divine Comedy - Oh the City — 3:11
- ES_Enter the Realm of Shadows - Christoffer Moe Ditlevsen — 3:02
- ES_Feeling New - Max Anson — 1:58
- ES_Floating Variables - Isaac Larson — 0:33
- ES_Forest Sunrise - Marten Moses — 1:50
- ES_Formations - Van Sandano — 3:26
- ES_In Cinemas - Pulsed — 1:55
- ES_In Obscurity Lies the Gate - Christoffer Moe Ditlevsen — 2:46
- ES_Leaving Traces - Gettz G — 2:29
- ES_Path to the Abyss - Christoffer Moe Ditlevsen — 2:42
- ES_Tension 2 - Fredrik Ekstrom — 1:42
- ES_Thirty-Fourth Window - Heath Cantu — 1:46
- ES_Trembling Anticipation - Dream Cave — 1:57
- ES_True Stories - Farrell Wooten — 1:46
- father-son-makeup-and-vanity-set-musicbed-licensed — 7:14
- fearful-continuity by josh-mccausland Artlist (1) — 2:14
- first-try by neon-ridge Artlist — 4:00
- free-radicals by stanley-gurvich Artlist — 4:41
- into-the-storm---no-drums by ian-post Artlist — 2:24
- k.i.t.t.-vs.-k.a.r.r by ian-post Artlist — 1:21
- mayhem by ian-post Artlist — 1:25
- the-harvest by dan-mayo Artlist — 5:03
- unknown-darkness by jimmy-svensson Artlist — 3:40

### Chamber Music (12)

- ES_A Delightful Evening - Francis Wells — 1:32
- ES_A Swallow_s Escape - Fabien Tell — 1:36
- ES_Errands - Fabien Tell — 1:41
- ES_Fly Baby Fly - Fabien Tell (1) — 1:39
- ES_Highest Gear - Brightarm Orchestra — 1:35
- ES_Life in Pieces - Howard Harper-Barnes — 3:10
- ES_Refined Enlightenment - Howard Harper-Barnes — 2:23
- ES_Rememberance - Fabien Tell (1) — 1:35
- ES_Sudden Escape - Brightarm Orchestra — 1:43
- ES_We Must Be Prepared - Brightarm Orchestra — 1:53
- immaterial by anbr Artlist — 4:10
- run-with-the-wolves by ardie-son Artlist — 2:04

### Classical (15)

- ES_A Brand New Sunset (Modern Version) - Joe E. Lee — 2:12
- ES_Agrumes - Ch@ntarelle — 2:48
- ES_Fly Baby Fly - Fabien Tell — 1:39
- ES_Kinderszenen, Op. 15_ No. 1, A Curious Story - Traditional — 1:52
- ES_Paidias Pledge - Golden Anchor — 2:30
- ES_Run and Hide - Philip Ayers — 2:04
- ES_Suite Bergamasque, L. 75_ III_ Clair De Lune (Intro) - Traditional — 2:08
- ES_The Barber of Seville - Traditional — 1:42
- ES_The Farewell Serenade - Howard Harper-Barnes — 2:02
- ES_The Nutcracker Op. 71, TH.14 _ Act 2 - No. 12D Trepak (Russian Dance) - Traditional — 1:05
- ES_William Tell Overture - Traditional — 1:05
- farewell by maya-belsitzman--matan-ephrat Artlist — 1:56
- rain by anbr Artlist — 2:19
- the-day-before by maya-belsitzman--matan-ephrat Artlist (1) — 1:48
- this-way by biba-dupont Artlist — 1:42

### Clock Timed (3)

- ES_Abandoned Houses - Wendel Scherer — 1:54
- ES_In Timely Manner - Guy Copeland — 1:49
- ES_It Is Set - Wendel Scherer — 1:58

### Drones (4)

- ES_Did They Lose Us - Experia — 1:50
- ES_Hidden Output - Ethan Sloan — 1:43
- ES_Natural Cause - Ethan Sloan — 1:45
- ES_Radiant Shore - Cobby Costa — 1:59

### Drum N bass (8)

- ES_Catrine - Power Druid — 2:37
- ES_Monologue - Splasher! — 2:25
- ES_Now - AGST — 2:49
- ES_Paradigm - Raccy — 3:08
- ES_Paralysed - AGST — 3:53
- ES_Wanna Go Back - Squiid — 2:51
- ES_You Give Me Feelings - House Of Say — 3:30
- ES_Zanobi - Catiso — 2:39

### Eccentric (38)

- ES_A Cradle Song - Mary Riddle — 2:25
- ES_A Faint Touch - Ethan Sloan — 1:52
- ES_Afternoon Tea Galore - Magnus Ringblom — 1:56
- ES_Afternoon Tea In Polynesia 3 - Martin Gauffin — 2:15
- ES_Appeased Soundscape 03 - August Wilhelmsson — 2:04
- ES_Beach Grave - DJ DENZ The Rooster — 3:46
- ES_Caught in the Net - Jon Bjork — 1:34
- ES_Cinematic Latin Flavours 2 - Magnus Ringblom — 2:09
- ES_Coconut Monkey - Anders Ekengren — 1:32
- ES_Crossing States 3 - Magnus Ringblom — 2:13
- ES_Dangerous Fling - Alexandra Woodward — 2:15
- ES_Dizzy Mind - Stationary Sign — 2:02
- ES_Duck Confit - Alexandra Woodward — 2:05
- ES_Festive Riot - Harper Rey — 2:03
- ES_Goofy Moments 17 - Magnus Ringblom — 2:01
- ES_Hangover Weekend - Stationary Sign — 2:11
- ES_High Heels Walkabout 1 - Magnus Ringblom — 1:53
- ES_Latin Orchestra 2 - Magnus Ringblom — 2:07
- ES_Lawnmower Trouble - Stationary Sign — 2:06
- ES_Mambo Lounge 9 - Martin Gauffin — 2:21
- ES_Mario Paint — 1:52
- ES_Morning After 1 - Magnus Ringblom — 2:11
- ES_National Anthem Sweden 8 - Traditional — 1:42
- ES_Odd Coincidence - Kikoru — 2:06
- ES_Playful Mischief - Josef Falkenskold — 1:50
- ES_Second Toe To The Left 3 - Peter Sandberg — 1:57
- ES_Simple Pleasantries 1 - Gavin Luke — 2:10
- ES_Sneaking Into the Kitchen - Arthur Benson — 2:04
- ES_The Juice Jam - Arthur Benson — 2:54
- ES_The King of Thieves - Christoffer Moe Ditlevsen — 2:29
- ES_The Kook - Marc Torch — 2:12
- ES_Tiptoeing 2 - Valdemar Hansen — 2:08
- ES_Tongue Twister - White Bones — 1:58
- ES_Trainee Day - Stationary Sign — 2:04
- ES_Whacky Theater 4 - Magnus Ringblom — 2:01
- ES_Whimsical And Playful 2 - Gavin Luke — 2:20
- ES_Wives Club 4 - Gunnar Johnsén — 2:16
- ES_Work These Shoes - Medite — 2:12

### Experimental (15)

- boom-clap-instrumental-chair-model-musicbed-licensed — 2:40
- chocolate-brownie---instrumental-version by ian-post Artlist — 3:11
- drift-instrumental-peached-musicbed-licensed — 3:30
- entertain-you-instrumental-bronze-radio-return-musicbed-licensed — 3:37
- ES_Dot. - Real Heroes — 2:14
- ganga-sun---instrumental-version by omri-smadar Artlist — 5:22
- healthier-instrumental-moony-musicbed-licensed — 2:33
- hey-you-instrumental-chair-model-musicbed-licensed — 2:29
- hot-for-a-min---instrumental-version by captain-qubz Artlist — 2:59
- id-rather-cry---instrumental-version by jane--the-boy Artlist — 2:56
- nonsense by raw Artlist — 3:24
- poolside-retreat by marc-robillard Artlist — 1:32
- rue-de-jaffa---instrumental-version by a.m.-beef Artlist — 3:30
- we-the-ones-with-oohs-ahhs-instrumental-mf-graves-musicbed-licensed — 3:11
- what-ya-want-instrumental-hipz-musicbed-licensed — 2:28

### Extra (1)

- ES_Accident Scene - SFX Producer — 0:45

### Funk (3)

- ES_My Rama Dama Doo - Sven Lindvall
- ES_Rain Checking - OTE
- ES_The Setup - Gerhard Feng

### Funny (33)

- (LOW) puddles
- cat-walk by roie-shpigler Artlist
- ES_A Dolphin Serenade - Josef Bel Habib
- ES_A Tiny Tumble - Josef Falkenskold (1)
- ES_Bathtub - Ballpoint
- ES_Be Nice Twice - Mac Taboel
- ES_Becoming Mr Bossa - Redeemin_
- ES_Bird Watching - Justnormal
- ES_Bop_It_-_Jules_Gaia
- ES_Bringing the Groove - Arthur Benson
- ES_Bubble Bee - The Fly Guy Five
- ES_Feeling_Alright_-_Gavin_Luke
- ES_Flying Pillows - Mike Franklyn
- ES_Go After Them! - Harry Edvino
- ES_I Could Stay Forever (Modern Version) - Joe E. Lee
- ES_Incidental Encounter - Arthur Benson
- ES_It_s Not Me - Arthur Benson
- ES_Jubilation_-_Jules_Gaia
- ES_Mama_Swing_-_Lucas_Pittman
- ES_Midnight_Swing_-_Jules_Gaia
- ES_Muffin Cuffin - Martin Klem
- ES_People Falling Down - Arthur Benson
- ES_Simple Pleasantries - Arthur Benson
- ES_Skipping Class - Birdies
- ES_The Director - Stationary Sign
- ES_When the Final Bell Rings - Mike Franklyn
- ES_Wild_Slide_-_Jules_Gaia
- ES_Yellow Light - Arthur Benson
- on-the-tip-of-my-toes by roie-shpigler Artlist
- quick-party-before-the-end-of-the-world by francesco-dandrea Artlist
- the-kings-parade by francesco-dandrea Artlist
- wag-the-tail by roie-shpigler Artlist
- white-russian-rag by the-bottlesnakes Artlist

### Happy (14)

- ES_A Tiny Tumble - Josef Falkenskold
- ES_African Food Truck - Sahara Skylight
- ES_Day at the Fair - The Fly Guy Five
- ES_Dime a Dozen - Esme Cruz
- ES_Forest Bugs - Stationary Sign
- ES_In the Name of Z - Real Heroes
- ES_Pigeons on a Train - Harry Edvino
- evermore-feat-jordan-critz-roary-musicbed-licensed
- flight-hannah-parrott-musicbed-licensed
- Lie In The Sun
- March of Toys
- oasis by milano Artlist
- temptation---instrumental-version by ride-free Artlist
- wannabe---instrumental-version by g9 Artlist

### Jazz (3)

- ES_Common Language - Vendla
- ES_Eye - Hara Noda
- ES_Yurei - Sugoi

### Jungle (7)

- Energetic Percussion by Infraction [No Copyright Drum Music]   The Rhythm
- ES_Encountering the Unknown - Zauana
- ES_Hidden and Ready - Zauana
- ES_In the Amazonas - Kikoru
- ES_Snake Trails - Experia
- ES_Through Deep Forests - Experia
- ES_When Warriors Align - Zauana

### Master plan (5)

- come-in-instrumental-kaina-musicbed-licensed
- continent by anbr Artlist
- jane-austens-fight-club-steven-gutheinz-musicbed-licensed
- solving-puzzles-alistair-sung-musicbed-licensed
- TV Drama Theme

### Motivational (17)

- avengers (artlist)
- ES_And The Sky Shall Unfold 1 - Johannes Bornlöf
- ES_Army of Angels - Edgar Hopp
- ES_Dungeon - Dream Cave
- ES_First Shooter - Bonnie Grace
- ES_On a Hunt - Philip Ayers
- ES_One Last Battle - Edgar Hopp
- ES_Power Squad - Adriel Fair
- ES_Roaming the Island - Adriel Fair
- ES_Tense Excitement 1 - Johannes Bornlöf
- ES_Termination 1 - Johannes Bornlöf
- ES_Termination 2 - Johannes Bornlöf
- ES_The Crew - Adriel Fair
- ES_Treasure Hunter 5 - Johannes Bornlöf
- ES_Unstoppable 3 - Johannes Bornlöf
- ES_Watchdogs - Jo Wandrini
- vortex by shahead-mostafafar Artlist

### Mystery (18)

- ES_Ancient Discoveries - Gabriel Lewis
- ES_Backdoor Exit - Max Anson
- ES_Carabiner - Max Anson
- ES_Commando - Max Anson
- ES_Desert Mirage - Colors of Illusion
- ES_Destiny Unfolds - Max Anson
- ES_Detective Work - V.V. Campos
- ES_Electric Spark - Sight of Wonders
- ES_Follow Every Move - Radio Night
- ES_In the Outskirts of Buenos Aires - Harper Rey
- ES_It_s Not Me - Arthur Benson
- ES_Mysterious Madeleine - Lucas Pittman
- ES_Mystery Box - Stationary Sign
- ES_Mystical Tension - Dream Cave
- ES_Nothing Can Conquer Us Now - Christian Andersen
- ES_Private Detective - Ch@ntarelle
- ES_The Unveiling - Christoffer Moe Ditlevsen
- ES_Through Space and Time - Etienne Roussel

### Pop (21)

- anthem-of-a-quirky-hipster by rex-banner Artlist (1)
- better-than-ever-instrumental-lady-bri-musicbed-licensed
- breaking-out-instrumental-prty-anml-musicbed-licensed
- ES_Being Nostalgic - FLYIN
- ES_Don_t Bore Me Alberto! - Harry Edvino
- ES_Mexican Standoff - Walt Adams
- ES_New Dawn Is Rising (Instrumental Version) - Stonekeepers
- ES_New Location - FLYIN
- ES_Silver Bullet - Elliot Holmes
- ES_Slap Act - White Bones
- ES_Upbeat Electronic Pop (Indie Pop Version) - Gavin Luke
- ES_Zoot Suit - Elliot Holmes
- freewheel by rex-banner Artlist (1)
- i-feel-free-instrumental-jamie-lono-musicbed-licensed (1)
- i-got-it-instrumental-juliet-roberts-musicbed-licensed
- locktup---instrumental-version by lone-wild Artlist
- move-your-body by rocknstock Artlist (1)
- ready-to-go-instrumental-louis-ii-musicbed-licensed
- solid-gold-instrumental-goldenface-musicbed-licensed
- solid-gold-with-oohs-ahhs-instrumental-goldenface-musicbed-licensed
- work-feat-kvlvnv-instrumental-cass-xq-musicbed-licensed

### Quirky (7)

- ES_A Tiny Tumble - Josef Falkenskold (1)
- ES_Extra Fries - The Fly Guy Five
- ES_Healthy Throat - Martin Landstrom
- ES_How to Tango
- ES_It_s Not Me - Arthur Benson
- ES_Out of Order - The Fly Guy Five
- ES_When the Cats Away - The Fly Guy Five

### Retro (8)

- a-moon-walk---instrumental-version by yehezkel-raz Artlist
- do-you-instrumental-kena-musicbed-licensed
- ES_Agent Getaway - Elliot Holmes
- ES_Bubble Beam - Soara
- ES_Kind of Real - Soara
- ES_Megapixel - Lasse Lyx
- lemon-popsicle by randy-sharp Artlist
- starsky by alex-keren Artlist

### Sad (21)

- calm-mind-(feat.-harshini-iyer)---no-lead-vocals by prashant-naidu Artlist
- Domine
- ES_A Common Memory - Trevor Kowalski
- ES_A Whisper In The Dark - Gavin Luke
- ES_Burned Letters - Johannes Bornlof
- ES_Can You Hear Me - Breathing Tides
- ES_Ether - Jakob Ahlbom
- ES_Exile - Lo Mimieux
- ES_Like Home - Jakob Ahlbom
- ES_Miss Everything (Instrumental Version) - Mindme
- ES_Onthou - Ever So Blue
- ES_Sad News - Emily Rubye
- ES_Secrets of the Earth - Lama House
- ES_Shadowman_s Waltz - Franz Gordon
- ES_Spring Queen - Dew Of Light
- ES_Stay (Wide Open) (Instrumental Version) - Loving Caliber
- ES_Valleys - Harbours _ Oceans
- ES_Whisper of the Pines - Howard Harper-Barnes
- Life
- The Bannered Mare
- Winter

### Samba (13)

- ES_Balcony Music - Timothy Infinite
- ES_Bateria Brasileira - Redeemin_
- ES_HEIST MUSIC - NIGHTCAP
- ES_Music Box - Rachel Meyer
- ES_Samba Amigo - Tiki Tiki
- ES_Samba del Sol - El Equipo Del Norte
- ES_Samba No Pe - Ruben Cortes
- ES_Samba Party - Tiki Tiki
- ES_Samba Piano - El Equipo Del Norte
- ES_Samba Triste (Instrumental Version) - Clara Mendes
- ES_Samba Vibes - Riverworn
- ES_The Music Box - Ave Air
- ES_Turtleneck Music - Sarah, the Illstrumentalist

### Spy (4)

- (MEIDUM) Spy Action Detective
- cant-stop-with-oohs-ahhs-instrumental-reagan-james-musicbed-licensed
- ES_A Deal With the Devil - White Bones
- ES_Spy - spring gang

### Suspense (1)

- ES_Charged - Alec Slayne

### background music (12)

- Caleb Arredondo Feeling Blue — 1:47
- Echo Sax End Looped by Caleb Arredondo — 5:05
- Flawed Mangoes Dramamine Visualizer — 3:25
- Kendrick Lamar(Instrumental) - Eduardo — 4:35
- Le Monde — 2:14
- Mary J. Blige - Family Affair ( Instrumental ) — 3:35
- Nightcrawler (Instrumental) — 1:00
- SAE4 Elveda — 2:46
- synthwave goose blade runner 2049 — 3:48
- UNTIL I FOUND YOU - Stephen Sanchez & Em Beihold (Karaoke Version) — 3:06
- VØJ Narvent Memory Reboot 4K Music Video — 3:56
- WhatsApp Video 2025-05-07 at 3.21.03 PM (1) — 2:45

### edits bgm (4)

- Lindsey Stirling Carol of the Bells Official Music Video — 3:06
- Ogryzek EMPIRE Slowed — 1:55
- OGRYZEK GLORY SLOWED REVERB — 2:29
- VØJ x Narvent Memory Reboot Slowed — 3:56

### other Music (29)

- Late Night Snack - Gunnar Olsen
- mixkit-aggressive-beast-roar-13
- mixkit-big-fire-spell-burning-1332
- mixkit-cinematic-drama-anticipation-795
- mixkit-cinematic-glass-hit-suspense-677
- mixkit-cinematic-orchestra-chaos-639
- mixkit-cinematic-transition-swoosh-heartbeat-trailer-488
- mixkit-cinematic-tunnel-reverb-woosh-1486
- mixkit-classic-alarm-995
- mixkit-clock-countdown-bleeps-916
- mixkit-crickets-and-insects-in-the-wild-ambience-39
- mixkit-eating-crispy-cookies-122
- mixkit-epic-orchestra-transition-2290
- mixkit-fast-laptop-keyboard-typing-1392
- mixkit-fast-small-sweep-transition-166
- mixkit-game-show-suspense-waiting-667
- mixkit-keyboard-typing-1386
- mixkit-light-rain-loop-2393
- mixkit-little-birds-singing-in-the-trees-17
- mixkit-rain-and-thunder-storm-2390
- mixkit-sad-game-over-trombone-471
- mixkit-swallowing-a-water-drink-in-the-throat-150
- mixkit-tick-tock-clock-timer-1045
- mixkit-vacuum-swoosh-transition-1465
- New Tires - Silent Partner
- Not For Nothing - Otis McDonald
- Shoulder Closures - Gunnar Olsen
- The Charmer_s Call - Hanu Dixit
- Tropic Fuse - French Fuse
