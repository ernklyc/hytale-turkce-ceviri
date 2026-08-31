#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
items.*.name / .description satirlarini sozluk tabanli otomatik ceviren yardimci.
Kullanim:
  python3 sozluk.py taslak      -> pack/.../server.lang'e items bolumu taslagi ekler (### ELLE KONTROL isaretli)
  python3 sozluk.py eksik       -> henuz cevrilmemis item name'leri listeler
Not: Uretilen taslak ELLE gozden gecirilmeli. Dilbilgisi (iyelik ekleri) her zaman dogru olmaz.
"""
import re, sys, pathlib

PROJE = pathlib.Path(__file__).parent
KAYNAK = PROJE / "kaynak" / "Server" / "server.lang"
HEDEF  = PROJE / "pack" / "Server" / "Languages" / "tr-TR" / "server.lang"

# --- Sozluk: tek kelime -> Turkce.  Sira onemli degil, kelime bazli eslesme. ---
SOZLUK = {
  # malzemeler
  "Stone":"Taş","Cobble":"Arnavut Kaldırımı","Cobblestone":"Arnavut Kaldırımı","Brick":"Tuğla",
  "Sandstone":"Kumtaşı","Limestone":"Kireçtaşı","Marble":"Mermer","Basalt":"Bazalt","Slate":"Arduvaz",
  "Shale":"Şist","Chalk":"Tebeşir","Calcite":"Kalsit","Quartzite":"Kuvarsit","Quartz":"Kuvars",
  "Granite":"Granit","Obsidian":"Obsidyen","Clay":"Kil","Gravel":"Çakıl","Sand":"Kum","Dirt":"Toprak",
  "Mud":"Çamur","Snow":"Kar","Ice":"Buz","Soil":"Toprak","Grass":"Çim","Volcanic":"Volkanik",
  "Magma":"Magma","Lava":"Lav","Rock":"Kaya","Ore":"Cevher","Crystal":"Kristal","Gem":"Değerli Taş",
  "Coral":"Mercan","Bone":"Kemik","Wood":"Ahşap","Wooden":"Ahşap","Log":"Kütük","Planks":"Kalas",
  "Plank":"Kalas","Trunk":"Gövde","Branch":"Dal","Roots":"Kök","Root":"Kök","Leaves":"Yaprak",
  "Leaf":"Yaprak","Bamboo":"Bambu","Cactus":"Kaktüs","Vine":"Sarmaşık","Bush":"Çalı","Moss":"Yosun",
  "Mushroom":"Mantar","Sapling":"Fidan","Seed":"Tohum","Seeds":"Tohum","Cloth":"Kumaş","Wool":"Yün",
  "Tree":"Ağaç","Trees":"Ağaç","Plant":"Bitki","Plants":"Bitki","Sprig":"Dalcık","Twig":"Çubuk",
  "Music":"Müzik","Treasure":"Hazine","Loot":"Ganimet","Reward":"Ödül","Prize":"Ödül",
  "Legendary":"Efsanevi","Epic":"Destansı","Rare":"Nadir","Common":"Yaygın","Uncommon":"Az Bulunur",
  "Grass":"Ot","Sand":"Kum","Coral":"Mercan","Kelp":"Yosun","Barnacle":"Midye","Shell":"Kabuk",
  "Leather":"Deri","Fibre":"Lif","Fiber":"Lif","Silk":"İpek","Straw":"Saman","Hay":"Saman",
  "Paper":"Kâğıt","Glass":"Cam","Iron":"Demir","Steel":"Çelik","Bronze":"Bronz","Copper":"Bakır",
  "Gold":"Altın","Silver":"Gümüş","Tin":"Kalay","Zinc":"Çinko","Lead":"Kurşun","Cobalt":"Kobalt",
  "Mithril":"Mithril","Adamantite":"Adamantit","Thorium":"Toryum","Onyxium":"Oniksiyum",
  "Titanium":"Titanyum","Platinum":"Platin","Brass":"Pirinç","Nickel":"Nikel",
  # renkler
  "Red":"Kırmızı","Blue":"Mavi","Green":"Yeşil","Yellow":"Sarı","Orange":"Turuncu","Purple":"Mor",
  "Pink":"Pembe","White":"Beyaz","Black":"Siyah","Grey":"Gri","Gray":"Gri","Brown":"Kahverengi",
  "Cyan":"Turkuaz","Aqua":"Su Yeşili","Azure":"Gök Mavisi","Magenta":"Eflatun","Lime":"Fıstık Yeşili",
  "Teal":"Deniz Mavisi","Gold":"Altın","Golden":"Altın","Dark":"Koyu","Light":"Açık",
  # boyut / bicim tanimlayicilari
  "Small":"Küçük","Medium":"Orta","Large":"Büyük","Big":"Büyük","Tall":"Uzun","Short":"Kısa",
  "Long":"Uzun","Wide":"Geniş","Narrow":"Dar","Thick":"Kalın","Thin":"İnce","Tiny":"Minik",
  "Huge":"Devasa","Giant":"Dev","Full":"Tam","Half":"Yarım","Double":"Çift","Single":"Tekli",
  "Flat":"Düz","Steep":"Dik","Shallow":"Sığ","Steppe":"Bozkır","Hollow":"İçi Boş","Solid":"Dolu",
  "Smooth":"Pürüzsüz","Rough":"Pürüzlü","Polished":"Cilalı","Cracked":"Çatlak","Broken":"Kırık",
  "Ornate":"Süslü","Decorative":"Dekoratif","Plain":"Sade","Simple":"Basit","Fancy":"Şık",
  "Runic":"Rünsel","Ancient":"Kadim","Modern":"Modern","Rustic":"Rustik","Crude":"Kaba",
  "Refined":"Rafine","Reinforced":"Takviyeli","Rounded":"Yuvarlak","Sharp":"Keskin","Curved":"Kavisli",
  "Vertical":"Dikey","Horizontal":"Yatay","Diagonal":"Çapraz","Inner":"İç","Outer":"Dış",
  "Middle":"Orta","Center":"Merkez","Centre":"Merkez","Top":"Üst","Bottom":"Alt","Side":"Yan",
  "Corner":"Köşe","Edge":"Kenar","Base":"Taban","Cap":"Kapak","End":"Uç","Cross":"Çapraz",
  "Young":"Genç","Old":"Yaşlı","Mature":"Olgun","Dead":"Ölü","Dry":"Kuru","Wet":"Islak",
  "Frozen":"Donmuş","Burnt":"Yanmış","Charred":"Kömürleşmiş","Cooled":"Soğumuş","Molten":"Erimiş",
  "Wild":"Yabani","Cooked":"Pişmiş","Raw":"Çiğ","Rotten":"Çürük","Fresh":"Taze","Hanging":"Asılı",
  "Petrified":"Taşlaşmış","Poisoned":"Zehirli","Cursed":"Lanetli","Blessed":"Kutsanmış",
  "Lesser":"Küçük","Greater":"Büyük","Minor":"Küçük","Major":"Büyük","Superior":"Üstün",
  # bicimler / yapi parcalari
  "Block":"Blok","Slab":"Plaka","Stairs":"Merdiven","Stair":"Merdiven","Beam":"Kiriş",
  "Pillar":"Sütun","Column":"Sütun","Post":"Direk","Fence":"Çit","Gate":"Kapı","Door":"Kapı",
  "Trapdoor":"Kapak Kapı","Wall":"Duvar","Roof":"Çatı","Ridge":"Sırt","Slope":"Eğim","Eave":"Saçak",
  "Window":"Pencere","Arch":"Kemer","Pipe":"Boru","Platform":"Platform","Bridge":"Köprü",
  "Ladder":"Merdiven","Stairway":"Merdiven","Rail":"Korkuluk","Railing":"Korkuluk","Panel":"Panel",
  "Tile":"Fayans","Plate":"Levha","Sheet":"Levha","Bar":"Çubuk","Rod":"Çubuk","Chain":"Zincir",
  "Ring":"Halka","Frame":"Çerçeve","Grate":"Izgara","Grille":"Izgara","Lattice":"Kafes",
  "Stalactite":"Sarkıt","Stalagmite":"Dikit","Rubble":"Moloz","Chunk":"Parça","Shard":"Kıymık",
  "Cluster":"Küme","Formation":"Oluşum","Vein":"Damar","Deposit":"Yatak","Boulder":"Kaya Parçası",
  "Cobble":"Arnavut Kaldırımı",
  # esya turleri
  "Sword":"Kılıç","Longsword":"Uzun Kılıç","Shortsword":"Kısa Kılıç","Greatsword":"Pala",
  "Dagger":"Hançer","Daggers":"Hançerler","Knife":"Bıçak","Axe":"Balta","Battleaxe":"Savaş Baltası",
  "Hatchet":"El Baltası","Mace":"Topuz","Club":"Sopa","Hammer":"Çekiç","Warhammer":"Savaş Çekici",
  "Spear":"Mızrak","Lance":"Kargı","Pike":"Kargı","Bow":"Yay","Crossbow":"Arbalet","Arrow":"Ok",
  "Staff":"Asa","Wand":"Değnek","Scepter":"Asa","Rod":"Çubuk","Shield":"Kalkan","Buckler":"Küçük Kalkan",
  "Spellbook":"Büyü Kitabı","Grimoire":"Büyü Kitabı","Tome":"Cilt","Book":"Kitap","Scroll":"Parşömen",
  "Helm":"Miğfer","Helmet":"Kask","Cuirass":"Göğüslük","Chestplate":"Göğüs Zırhı","Breastplate":"Göğüs Zırhı",
  "Gauntlets":"Zırhlı Eldiven","Gauntlet":"Zırhlı Eldiven","Gloves":"Eldiven","Boots":"Bot",
  "Greaves":"Baldır Zırhı","Leggings":"Bacak Zırhı","Pants":"Pantolon","Cloak":"Pelerin","Cape":"Pelerin",
  "Robe":"Cübbe","Tunic":"Tunik","Shirt":"Gömlek","Vest":"Yelek","Belt":"Kemer","Ring":"Yüzük",
  "Amulet":"Muska","Necklace":"Kolye","Pendant":"Madalyon","Trinket":"Takı","Charm":"Tılsım",
  "Pickaxe":"Kazma","Pick":"Kazma","Shovel":"Kürek","Spade":"Bel","Hoe":"Çapa","Sickle":"Orak",
  "Scythe":"Tırpan","Rake":"Tırmık","Saw":"Testere","Chisel":"Keski","Wrench":"İngiliz Anahtarı",
  "Fishing":"Balıkçılık","Rod ":"Olta ","Net":"Ağ","Trap":"Tuzak","Lure":"Yem","Bait":"Yem",
  "Potion":"İksir","Elixir":"İksir","Brew":"İksir","Tonic":"Tonik","Draught":"İçki","Flask":"Şişe",
  "Bottle":"Şişe","Vial":"Fiyol","Bomb":"Bomba","Grenade":"El Bombası","Dynamite":"Dinamit",
  "Bandage":"Bandaj","Salve":"Merhem","Ointment":"Merhem","Poultice":"Lapa","Kit":"Kit",
  "Food":"Yiyecek","Meat":"Et","Wildmeat":"Yaban Eti","Fish":"Balık","Bread":"Ekmek","Cheese":"Peynir",
  "Berry":"Meyve","Berries":"Meyveler","Apple":"Elma","Carrot":"Havuç","Pumpkin":"Balkabağı",
  "Wheat":"Buğday","Corn":"Mısır","Potato":"Patates","Tomato":"Domates","Onion":"Soğan",
  "Stew":"Güveç","Soup":"Çorba","Pie":"Turta","Cake":"Pasta","Jam":"Reçel","Honey":"Bal",
  "Egg":"Yumurta","Milk":"Süt","Butter":"Tereyağı","Flour":"Un","Sugar":"Şeker","Salt":"Tuz",
  "Tiles":"Fayans","Tombstone":"Mezar Taşı","Headstone":"Mezar Taşı","Grave":"Mezar","Urn":"Vazo","Sarcophagus":"Lahit",
  "Beef":"Sığır Eti","Chicken":"Tavuk","Pork":"Domuz Eti","Lamb":"Kuzu Eti","Venison":"Geyik Eti",
  "Grilled":"Izgara","Roast":"Kızarmış","Roasted":"Kızarmış","Fried":"Kızarmış","Baked":"Fırınlanmış",
  "Boiled":"Haşlanmış","Smoked":"Tütsülenmiş","Dried":"Kurutulmuş","Sliced":"Dilimlenmiş",
  "Skewer":"Şiş","Kebab":"Kebap","Salad":"Salata","Popcorn":"Patlamış Mısır","Sandwich":"Sandviç",
  "Dumpling":"Mantı","Noodle":"Erişte","Rice":"Pirinç","Porridge":"Lapa","Biscuit":"Bisküvi",
  "Cookie":"Kurabiye","Muffin":"Kek","Tart":"Turta","Roll":"Rulo","Loaf":"Somun","Bun":"Çörek",
  "Juice":"Meyve Suyu","Wine":"Şarap","Ale":"Bira","Beer":"Bira","Mead":"Bal Şarabı","Cider":"Elma Şarabı",
  "Tea":"Çay","Coffee":"Kahve","Broth":"Et Suyu","Fruit":"Meyve","Vegetable":"Sebze","Vegetables":"Sebze",
  "Nut":"Fındık","Nuts":"Fındık","Grain":"Tahıl","Rye":"Çavdar","Barley":"Arpa","Oat":"Yulaf",
  "Diving":"Dalış","Suit":"Kıyafet","Flippers":"Palet","Goggles":"Gözlük","Heavy":"Ağır","Soft":"Yumuşak",
  "Hard":"Sert","Padded":"Dolgulu","Studded":"Perçinli","Scaled":"Pullu","Plated":"Levhalı",
  "Raven":"Kuzgun","Wolf":"Kurt","Bear":"Ayı","Fox":"Tilki","Hawk":"Şahin","Eagle":"Kartal",
  "Serpent":"Yılan","Dragon":"Ejderha","Lion":"Aslan","Tiger":"Kaplan","Boar":"Yaban Domuzu",
  "Template":"Şablon","Guitar":"Gitar","Lute":"Ut","Drum":"Davul","Flute":"Flüt","Horn ":"Boru ",
  "Fertilizer":"Gübre","Bark":"Ağaç Kabuğu","Scraper":"Kazıyıcı","Capture":"Yakalama","Feed":"Yem",
  "Feedbag":"Yem Torbası","Watering":"Sulama","Can ":"Kabı ","Bell":"Çan","Whistle":"Düdük",
  "Ingredient":"Malzeme","Material":"Malzeme","Resource":"Kaynak","Bag":"Torba","Sack":"Çuval",
  "Pouch":"Kese","Crate":"Kasa","Barrel":"Fıçı","Basket":"Sepet","Pot":"Saksı","Vase":"Vazo",
  "Jar":"Kavanoz","Bucket":"Kova","Cauldron":"Kazan","Anvil":"Örs","Forge":"Ocak","Furnace":"Fırın",
  "Kiln":"Fırın","Oven":"Fırın","Stove":"Ocak","Campfire":"Kamp Ateşi","Torch":"Meşale",
  "Lantern":"Fener","Candle":"Mum","Lamp":"Lamba","Chandelier":"Avize","Brazier":"Mangal",
  "Chest":"Sandık","Container":"Konteyner","Shelf":"Raf","Cabinet":"Dolap","Wardrobe":"Gardırop",
  "Drawer":"Çekmece","Table":"Masa","Desk":"Çalışma Masası","Chair":"Sandalye","Stool":"Tabure",
  "Bench":"Bank","Sofa":"Kanepe","Couch":"Kanepe","Bed":"Yatak","Bedroll":"Yatak Rulosu",
  "Rug":"Halı","Carpet":"Halı","Curtain":"Perde","Banner":"Sancak","Flag":"Bayrak","Sign":"Tabela",
  "Painting":"Tablo","Statue":"Heykel","Bust":"Büst","Trophy":"Kupa","Idol":"Put","Altar":"Sunak",
  "Shrine":"Türbe","Totem":"Totem","Rune":"Rün","Sigil":"Mühür","Emblem":"Amblem","Crest":"Arma",
  "Workbench":"Çalışma Tezgahı","Loom":"Dokuma Tezgahı","Wheel":"Çark","Grindstone":"Bileği Taşı",
  "Recipe":"Tarif","Blueprint":"Plan","Schematic":"Şema","Prefab":"Yapı Taslağı",
  "Portal":"Geçit","Gateway":"Geçit","Teleporter":"Işınlayıcı","Beacon":"İşaret Ateşi","Fragment":"Parça",
  "Spawner":"Doğurucu","Emitter":"Yayıcı","Trigger":"Tetikleyici","Marker":"İşaretçi","Node":"Düğüm",
  "Decoration":"Süs","Deco":"Süs","Ornament":"Süs","Furniture":"Mobilya","Fixture":"Tesisat",
  # varliklar / yerler (ozel adlar - genelde ayni kalir ama sifat olanlar cevrilir)
  "Temple":"Tapınak","Ruins":"Harabe","Ruin":"Harabe","Tomb":"Mezar","Crypt":"Lahit","Dungeon":"Zindan",
  "Tavern":"Han","Inn":"Han","Village":"Köy","Castle":"Kale","Fort":"Hisar","Tower":"Kule",
  "Camp":"Kamp","Outpost":"Karakol","Nest":"Yuva","Hive":"Kovan","Den":"İn","Lair":"İn",
  "Cave":"Mağara","Cavern":"Mağara","Grotto":"Mağara","Mine":"Maden","Quarry":"Taş Ocağı",
  "Civilization":"Uygarlık","Lost":"Kayıp","Forgotten":"Unutulmuş","Fallen":"Düşmüş","Abandoned":"Terk Edilmiş",
  "Human":"İnsan","Kweebec":"Kweebec","Trork":"Trork","Scarak":"Scarak","Feran":"Feran","Klops":"Klops",
  "Outlander":"Diyardışı","Goblin":"Goblin","Skeleton":"İskelet","Zombie":"Zombi","Golem":"Golem",
  "Undead":"Hortlak","Voidspawn":"Boşluk Yavrusu","Void":"Boşluk","Orbis":"Orbis",
  # yaygin ekler
  "of":"—","the":"","and":"ve","with":"ile","for":"için",
  # blok seti / desenler
  "Set":"Set","Sets":"Setler","Pattern":"Desen","Mix":"Karışım","Blend":"Karışım","Mosaic":"Mozaik",
  "Herringbone":"Balıksırtı","Checkered":"Damalı","Striped":"Çizgili","Dotted":"Noktalı",
  # muhtelif
  "Debug":"Hata Ayıklama","Test":"Test","Prototype":"Prototip","Placeholder":"Yer Tutucu",
  "Generic":"Genel","Default":"Varsayılan","Special":"Özel","Custom":"Özel","Basic":"Temel",
  "Advanced":"Gelişmiş","Standard":"Standart","Premium":"Premium","Elite":"Seçkin",
  "Winter":"Kış","Summer":"Yaz","Spring":"İlkbahar","Autumn":"Sonbahar","Fall":"Sonbahar",
  "Holiday":"Bayram","Festive":"Şenlikli","Seasonal":"Mevsimlik","Snowflake":"Kar Tanesi",
  "Water":"Su","Fire":"Ateş","Earth":"Toprak","Air":"Hava","Wind":"Rüzgar","Storm":"Fırtına",
  "Lightning":"Şimşek","Thunder":"Gök Gürültüsü","Frost":"Ayaz","Flame":"Alev","Ember":"Kor",
  "Ash":"Kül","Smoke":"Duman","Steam":"Buhar","Cloud":"Bulut","Mist":"Sis","Fog":"Sis",
  # kumas / lif turleri
  "Cotton":"Pamuk","Linen":"Keten","Woolen":"Yünlü","Canvas":"Branda","Denim":"Kot",
  "Velvet":"Kadife","Satin":"Saten","Burlap":"Çuval Bezi","Hemp":"Kenevir",
  # bitki parcalari
  "Petals":"Taçyaprakları","Petal":"Taçyaprağı","Reeds":"Sazlık","Reed":"Kamış",
  "Flower":"Çiçek","Flowers":"Çiçekler","Blossom":"Çiçek","Fern":"Eğrelti","Ferns":"Eğrelti",
  "Sprout":"Filiz","Sprouts":"Filiz","Shrub":"Çalı","Hedge":"Çit","Ivy":"Sarmaşık",
  "Lily":"Zambak","Rose":"Gül","Tulip":"Lale","Daisy":"Papatya","Poppy":"Gelincik",
  "Nettle":"Isırgan","Thistle":"Devedikeni","Clover":"Yonca","Weed":"Yabani Ot","Weeds":"Yabani Ot",
  "Kelp":"Yosun","Seaweed":"Deniz Yosunu","Algae":"Yosun","Lichen":"Liken",
  "Waterlily":"Nilüfer","Lilypad":"Nilüfer Yaprağı","Pinecone":"Kozalak",
  # kiyafet parcalari
  "Hood":"Başlık","Cowl":"Başlık","Diadem":"Taç","Circlet":"Taç","Crown":"Taç",
  "Bracers":"Kolçak","Bracelets":"Bileklik","Bracelet":"Bileklik","Sash":"Kuşak",
  "Sandals":"Sandalet","Shoes":"Ayakkabı","Slippers":"Terlik","Mask":"Maske","Visor":"Siperlik",
  "Coif":"Başlık","Chestpiece":"Göğüslük","Legguards":"Bacak Zırhı","Legplates":"Bacak Zırhı",
  # agac turleri
  "Oak":"Meşe","Birch":"Huş","Pine":"Çam","Cedar":"Sedir","Spruce":"Ladin","Maple":"Akçaağaç",
  "Willow":"Söğüt","Aspen":"Titrek Kavak","Elm":"Karaağaç","Ash ":"Dişbudak ","Beech":"Kayın",
  "Acacia":"Akasya","Palm":"Palmiye","Mahogany":"Maun","Teak":"Tik","Ebony":"Abanoz",
  "Blackwood":"Karaağaç","Redwood":"Kızılağaç","Goldenwood":"Altınağaç","Darkwood":"Karaağaç",
  "Deadwood":"Ölü Ağaç","Drywood":"Kuru Ağaç","Greenwood":"Yeşil Ağaç","Hardwood":"Sert Ağaç",
  "Lightwood":"Açık Ağaç","Softwood":"Yumuşak Ağaç","Tropicalwood":"Tropik Ağaç","Whitewood":"Ak Ağaç",
  # renk/madde ek
  "Amber":"Kehribar","Jade":"Yeşim","Ruby":"Yakut","Sapphire":"Safir","Emerald":"Zümrüt",
  "Diamond":"Elmas","Opal":"Opal","Topaz":"Topaz","Pearl":"İnci","Ivory":"Fildişi",
  "Blood":"Kan","Bloody":"Kanlı","Rust":"Pas","Rusty":"Paslı","Slime":"Balçık","Sludge":"Çamur",
  "Tar":"Katran","Pitch":"Zift","Wax":"Balmumu","Resin":"Reçine","Amberwax":"Kehribar Balmumu",
  # yer/yapi ek
  "Cybercity":"Sibernetik Şehir","Marsh":"Bataklık","Swamp":"Bataklık","Bog":"Bataklık",
  "Desert":"Çöl","Tundra":"Tundra","Jungle":"Orman","Forest":"Orman","Meadow":"Çayır",
  "Plains":"Ova","Canyon":"Kanyon","Cliff":"Uçurum","Peak":"Zirve","Valley":"Vadi","Hill":"Tepe",
  "Shore":"Kıyı","Beach":"Plaj","Reef":"Resif","Abyss":"Uçurum","Depths":"Derinlikler",
  "Sandswept":"Kum Savrulmuş","Frostbitten":"Ayaz Isırığı","Sunbaked":"Güneşte Pişmiş",
  # muhtelif ek
  "Arcade":"Oyun","Machine":"Makine","Device":"Aygıt","Contraption":"Düzenek","Gadget":"Alet",
  "Mechanism":"Mekanizma","Gear":"Dişli","Cog":"Dişli","Lever":"Kol","Button":"Düğme",
  "Switch":"Anahtar","Plate":"Levha","Pressure":"Basınç","Piston":"Piston","Pump":"Pompa",
  "Filter":"Filtre","Valve":"Vana","Gutter":"Oluk","Drain":"Gider","Vent":"Havalandırma",
  "Spike":"Diken","Spikes":"Dikenler","Barb":"Diken","Wire":"Tel","Mesh":"Ağ","Grid":"Izgara",
  "Cage":"Kafes","Coffin":"Tabut","Skull":"Kafatası","Skeleton":"İskelet","Rib":"Kaburga",
  "Claw":"Pençe","Fang":"Diş","Horn":"Boynuz","Tusk":"Fildişi","Scale":"Pul","Feather":"Tüy",
  "Fur":"Kürk","Hide":"Post","Pelt":"Post","Sinew":"Kiriş","Gut":"Bağırsak",
  "Backpack":"Sırt Çantası","Upgrade":"Yükseltme","Component":"Bileşen","Part":"Parça",
  "Core":"Çekirdek","Shell":"Kabuk","Husk":"Kabuk","Pod":"Kapsül","Bulb":"Ampul",
  "Essence":"Öz","Extract":"Öz","Powder":"Toz","Dust":"Toz","Crystal":"Kristal","Nugget":"Külçe",
  "Ingot":"Külçe","Bar":"Külçe","Coin":"Sikke","Gold ":"Altın ","Token":"Jeton","Key":"Anahtar",
  "Map":"Harita","Compass":"Pusula","Spyglass":"Dürbün","Telescope":"Teleskop","Hourglass":"Kum Saati",
}

# --- Yaratik / NPC sozlugu (npcRoles icin) ---
YARATIK = {
  "Antelope":"Antilop","Armadillo":"Armadillo","Bat":"Yarasa","Bear":"Ayı","Grizzly":"Boz",
  "Polar":"Kutup","Bison":"Bizon","Calf":"Yavru","Bluebird":"Mavi Kuş","Boar":"Yaban Domuzu",
  "Piglet":"Domuz Yavrusu","Bunny":"Tavşan","Camel":"Deve","Catfish":"Yayın Balığı",
  "Chicken":"Tavuk","Chick":"Civciv","Desert":"Çöl","Undead":"Hortlak","Clownfish":"Palyaço Balığı",
  "Cow":"İnek","Crab":"Yengeç","Crawler":"Sürüngen","Crocodile":"Timsah","Crow":"Karga",
  "Doe":"Dişi Geyik","Stag":"Erkek Geyik","Deer":"Geyik","Dragon":"Ejderha","Ember":"Kor",
  "Frost":"Ayaz","Duck":"Ördek","Eel":"Yılan Balığı","Moray":"Mırına","Eye":"Göz","Void":"Boşluk",
  "Fox":"Tilki","Frog":"Kurbağa","Gecko":"Kertenkele","Ghoul":"Gulyabani","Goat":"Keçi","Kid":"Oğlak",
  "Goblin":"Goblin","Duke":"Dük","Hermit":"Münzevi","Lobber":"Fırlatıcı","Miner":"Madenci",
  "Ogre":"Dev","Scavenger":"Leşçi","Scrapper":"Hurdacı","Thief":"Hırsız","Golem":"Golem",
  "Earthen":"Topraksı","Guardian":"Muhafız","Hawk":"Şahin","Horse":"At","Foal":"Tay","Armored":"Zırhlı",
  "Skeleton":"İskelet","Hound":"Tazı","Bleached":"Solmuş","Hyena":"Sırtlan","Jellyfish":"Denizanası",
  "Elder":"İhtiyar","Prisoner":"Tutsak","Merchant":"Tüccar","Larva":"Larva","Silk":"İpek",
  "Leopard":"Leopar","Snow":"Kar","Lizard":"Kertenkele","Sand":"Kum","Lobster":"Istakoz",
  "Meerkat":"Mirket","Minnow":"Küçük Balık","Molerat":"Köstebek Sıçan","Moose":"Boz Geyik",
  "Bull":"Boğa","Mouse":"Fare","Owl":"Baykuş","Brown":"Kahverengi","Snowy":"Karlı","Parrot":"Papağan",
  "Penguin":"Penguen","Pig":"Domuz","Wild":"Yabani","Pigeon":"Güvercin","Pike":"Turnabalığı",
  "Piranha":"Pirana","Black":"Kara","Pterodactyl":"Pterodaktil","Pufferfish":"Balon Balığı",
  "Quest":"Görev","Master":"Ustası","Rabbit":"Tavşan","Ram":"Koç","Lamb":"Kuzu","Raptor":"Raptor",
  "Cave":"Mağara","Rat":"Sıçan","Raven":"Kuzgun","Rex":"Rex","Salmon":"Somon","Scorpion":"Akrep",
  "Shadow":"Gölge","Knight":"Şövalye","Shark":"Köpekbalığı","Hammerhead":"Çekiçbaş","Sheep":"Koyun",
  "Archer":"Okçu","Archmage":"Baş Büyücü","Burnt":"Yanmış","Alchemist":"Simyacı","Gunner":"Nişancı",
  "Lancer":"Mızrakçı","Praetorian":"Muhafız","Soldier":"Asker","Wizard":"Büyücü","Fighter":"Savaşçı",
  "Mage":"Büyücü","Ranger":"Korucu","Scout":"İzci","Incandescent":"Akkor","Footman":"Piyade",
  "Head":"Kafa","Pirate":"Korsan","Captain":"Kaptan","Striker":"Vurucu","Assassin":"Suikastçı",
  "Guard":"Muhafız","Warlock":"Kara Büyücü","Sandswept":"Kum Savrulmuş","Berserker":"Cılgın Savaşçı",
  "Brute":"Kabadayı","Cultist":"Tarikatçı","Initiate":"Acemi","Hunter":"Avcı","Marauder":"Yağmacı",
  "Peon":"Irgat","Unsworn":"Yeminsiz","Priest":"Rahip","Sorcerer":"Büyücü","Stalker":"Sinsi",
  "Broodmother":"Kuluçka Anası","Defender":"Savunucu","Royal":"Kraliyet","Imperial":"İmparatorluk",
  "Louse":"Bit","Seeker":"Arayıcı","Fledgling":"Acemi","Young":"Genç","Spider":"Örümcek",
  "Wolf":"Kurt","Toad":"Karakurbağası","Turtle":"Kaplumbağa","Snake":"Yılan","Beetle":"Böcek",
  "Moth":"Güve","Butterfly":"Kelebek","Bee":"Arı","Wasp":"Eşek Arısı","Ant":"Karınca",
  "Worm":"Solucan","Slug":"Sümüklüböcek","Snail":"Salyangoz","Fish":"Balık","Shrimp":"Karides",
  "Octopus":"Ahtapot","Squid":"Kalamar","Whale":"Balina","Dolphin":"Yunus","Seal":"Fok",
  "Eagle":"Kartal","Falcon":"Doğan","Vulture":"Akbaba","Crane":"Turna","Heron":"Balıkçıl",
  "Swan":"Kuğu","Goose":"Kaz","Rooster":"Horoz","Hen":"Tavuk","Turkey":"Hindi","Peacock":"Tavus",
  "Elephant":"Fil","Rhino":"Gergedan","Hippo":"Su Aygırı","Giraffe":"Zürafa","Zebra":"Zebra",
  "Lion":"Aslan","Tiger":"Kaplan","Panther":"Panter","Cheetah":"Çita","Lynx":"Vaşak",
  "Cub":"Yavru","Pup":"Yavru","Kitten":"Yavru Kedi","Foe":"Düşman","Zombie":"Zombi",
  "Warrior":"Savaşçı","Shaman":"Şaman","Chief":"Reis","King":"Kral","Queen":"Kraliçe",
  "Lord":"Lord","Prince":"Prens","Princess":"Prenses","Baron":"Baron","Emperor":"İmparator",
  "Civilian":"Sivil","Villager":"Köylü","Guardian ":"Muhafız ","Golem ":"Golem ",
  "Thunder":"Şimşek","Flame":"Alev","Firesteel":"Ateş Çeliği","Firebrand":"Ateş Közü",
  "Warthog":"Yaban Domuzu","Werewolf":"Kurt Adam","Woodpecker":"Ağaçkakan","Wraith":"Tayf",
  "Yeti":"Yeti","Aberrant":"Sapkın","Humpback":"Kambur","Hunting":"Avcı","Blank":"Boş",
  "Empty":"Boş","Grizzly":"Boz","Bluegill":"Mavi Solungaç","Frostgill":"Ayaz Solungaç",
  "Greenfinch":"Yeşil İspinoz","Finch":"İspinoz","Flamingo":"Flamingo","Ghost":"Hayalet",
  "Spirit":"Ruh","Phantom":"Hayalet","Wisp":"Ruh Işığı","Banshee":"Ölüm Perisi","Lich":"Lich",
  "Doe":"Dişi Geyik","Stag":"Erkek Geyik","Fawn":"Geyik Yavrusu","Buck":"Erkek Geyik",
  "Coelacanth":"Latimeria","Fen":"Bataklık","Longtooth":"Uzundiş","Sharptooth":"Keskindiş",
  "Windwalker":"Rüzgaryürüyen","Burrower":"Yuvakazan","Razorleaf":"Jiletyaprak","Rootling":"Köklü",
  "Seedling":"Fide","Sproutling":"Filizcik","Gentleman":"Beyefendi","Elder":"İhtiyar",
}

# Bir onceki kelime bunlardan biriyse SONRAKI Turkce isme 3. tekil iyelik eki gelir (kaba yaklasim).
IYELIK = {
  "Torba":"Torbası","Yosun":"Yosunu","Kök":"Kökü","Çatı":"Çatısı","Tohum":"Tohumu",
  "Kütük":"Kütüğü","Dal":"Dalı","Yaprak":"Yaprağı","Gövde":"Gövdesi","Blok":"Bloğu",
  "İksir":"İksiri","Tarif":"Tarifi","Parça":"Parçası","Set":"Seti","Kazan":"Kazanı",
}

BOL = re.compile(r"\{[^}]*\}|<[^>]+>")  # degiskenler / etiketler

def kelime_cevir(w):
    ham = w.strip(".,!?\"'()[]")
    if ham.endswith("'s"):          # "Builder's" -> "Builder"
        ham = ham[:-2]
    if not ham:
        return w
    tr = SOZLUK.get(ham) or SOZLUK.get(ham.capitalize())
    if tr is None:
        return w
    if tr == "":                    # "the" gibi -> at
        return ""
    return tr

def isim_cevir(s):
    # " - " ile ayrilan modifiye kismini koru
    parcalar = s.split(" - ")
    ceviri = []
    for p in parcalar:
        # degisken/etiket varsa dokunma
        if BOL.search(p):
            ceviri.append(p); continue
        kelimeler = p.split()
        cev = [kelime_cevir(w) for w in kelimeler]
        ceviri.append(" ".join(x for x in cev if x))
    return " - ".join(ceviri)

def oku(p):
    d, sec, devam = {}, None, False
    if not p.exists(): return d
    for raw in p.read_text(encoding="utf-8").splitlines():
        s = raw.strip(); onceki = devam; devam = raw.endswith("\\")
        if onceki: continue
        m = re.match(r"#\s*===\s*(.+?)\s*===", s)
        if m: sec = m.group(1); continue
        if not s or s.startswith("#") or "=" not in s: continue
        k, v = s.split("=", 1)
        if re.fullmatch(r"[A-Za-z0-9_.]+", k.strip()):
            d[k.strip()] = v.strip()
    return d

kaynak = oku(KAYNAK)
mevcut = set(oku(HEDEF))

if len(sys.argv) > 1 and sys.argv[1] == "eksik":
    n = 0
    for k, v in kaynak.items():
        if k.startswith("items.") and k.endswith(".name") and k not in mevcut:
            print(f"{k} = {v}"); n += 1
    print(f"\n# {n} cevrilmemis item.name", file=sys.stderr)
    sys.exit()

mod = sys.argv[1] if len(sys.argv) > 1 else "taslak"

if mod == "npcroles":
    S2 = dict(SOZLUK); S2.update(YARATIK)
    def yc(s):
        return " ".join(S2.get(w.strip(".,"), S2.get(w.strip(".,").capitalize(), w)) for w in s.split())
    cikti = ["", "# === npcRoles (OTOMATIK TASLAK) ==="]
    for k, v in kaynak.items():
        if k.startswith("npcRoles.") and k.endswith(".name") and k not in mevcut:
            cikti.append(f"{k} = {yc(v)}")
    print("\n".join(cikti)); sys.exit()

# taslak uret (items)
cikti = ["", "# === items (OTOMATIK TASLAK - elle kontrol et) ==="]
for k, v in kaynak.items():
    if not k.startswith("items."): continue
    if k in mevcut: continue
    if k.endswith(".name") or k.endswith(".nameFull"):
        cikti.append(f"{k} = {isim_cevir(v)}")
print("\n".join(cikti))
