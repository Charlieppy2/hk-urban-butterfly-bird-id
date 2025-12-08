"""
批量更新蝴蝶信息的腳本
可以從多個來源獲取蝴蝶詳細資料並更新到模板文件
"""

import json
import os
import sys

# 設置 UTF-8 編碼
sys.stdout.reconfigure(encoding='utf-8')

def load_butterfly_template():
    """加載蝴蝶模板文件"""
    template_path = os.path.join(os.path.dirname(__file__), 'butterfly_info_template.json')
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_butterfly_template(data):
    """保存蝴蝶模板文件"""
    template_path = os.path.join(os.path.dirname(__file__), 'butterfly_info_template.json')
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {template_path}")

# 常見蝴蝶的詳細信息（可以擴展）
COMMON_BUTTERFLIES_INFO = {
    # 第一批：20種蝴蝶
    "ADONIS": {
        "scientific_name": "Lysandra bellargus",
        "description": "Small butterfly with bright blue upperwings (males) or brown upperwings (females), and orange spots on hindwings.",
        "habitat": "Grasslands, meadows, and open areas with chalk or limestone soils",
        "distribution": "Europe, from southern England to the Mediterranean",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially thistles and knapweeds",
        "behavior": "Flies from May to September. Males are territorial. Forms colonies.",
        "lifecycle": "Eggs laid on horseshoe vetch. Caterpillars feed on host plant. Overwinters as pupa."
    },
    "AFRICAN GIANT SWALLOWTAIL": {
        "scientific_name": "Papilio antimachus",
        "description": "Very large butterfly with black and yellow wings, long tail-like extensions on hindwings, and distinctive wing pattern.",
        "habitat": "Tropical rainforests and forest edges",
        "distribution": "West and Central Africa",
        "wingspan": "15-25 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Strong flier. Males are territorial. Rarely seen at ground level.",
        "lifecycle": "Eggs laid on Rutaceae family plants. Large caterpillars with defensive spines."
    },
    "AMERICAN SNOOT": {
        "scientific_name": "Libytheana carinenta",
        "description": "Small butterfly with long snout-like projection on head, brown wings with orange patches, and white spots.",
        "habitat": "Open areas, fields, and woodland edges",
        "distribution": "North and South America, from United States to Argentina",
        "wingspan": "3.5-5 cm",
        "diet": "Nectar from flowers, especially composites",
        "behavior": "Migratory. Fast flier. Often perches with wings closed.",
        "lifecycle": "Eggs laid on hackberry trees. Caterpillars feed on leaves. Multiple generations per year."
    },
    "AN 88": {
        "scientific_name": "Diaethria anna",
        "description": "Small butterfly with black and white wings, distinctive '88' or '89' pattern on hindwings, and red markings.",
        "habitat": "Tropical and subtropical forests",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, rotting fruit, and tree sap",
        "behavior": "Fast flier. Males are territorial. Often seen on forest trails.",
        "lifecycle": "Eggs laid on plants in the Urticaceae family. Caterpillars are green with spines."
    },
    "APPOLLO": {
        "scientific_name": "Parnassius apollo",
        "description": "Large butterfly with white wings, black spots, red eye-spots on hindwings, and transparent wing tips.",
        "habitat": "Mountain meadows and alpine grasslands",
        "distribution": "Europe and Asia, in mountainous regions",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers, especially thistles and knapweeds",
        "behavior": "Slow flier. Flies from June to August. Endangered in many areas.",
        "lifecycle": "Eggs laid on stonecrop plants. Caterpillars feed on host plant. Overwinters as egg or young caterpillar."
    },
    "ARCIGERA FLOWER MOTH": {
        "scientific_name": "Schinia arcigera",
        "description": "Medium-sized moth with brown and white patterned wings, and distinctive flower-like markings.",
        "habitat": "Grasslands, prairies, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers, especially evening primroses",
        "behavior": "Nocturnal. Attracted to lights. Flies from May to September.",
        "lifecycle": "Eggs laid on host plants. Caterpillars feed on flowers and seeds."
    },
    "ATALA": {
        "scientific_name": "Eumaeus atala",
        "description": "Small butterfly with black wings, blue-green iridescent spots, and red abdomen.",
        "habitat": "Tropical and subtropical areas with cycad plants",
        "distribution": "Florida, Caribbean, and Central America",
        "wingspan": "3.5-4.5 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Slow flier. Forms colonies. Warning colors indicate toxicity.",
        "lifecycle": "Eggs laid on cycad plants. Caterpillars are toxic due to cycad consumption."
    },
    "ATLAS MOTH": {
        "scientific_name": "Attacus atlas",
        "description": "Very large moth with brown, red, and white patterned wings, and distinctive snake-like wing tips.",
        "habitat": "Tropical and subtropical forests",
        "distribution": "Southeast Asia, from India to Indonesia",
        "wingspan": "25-30 cm",
        "diet": "Adults do not feed. Caterpillars feed on various trees.",
        "behavior": "Nocturnal. Attracted to lights. Short-lived as adults.",
        "lifecycle": "Large caterpillars feed on various host plants. Cocoons are made of silk."
    },
    "BANDED ORANGE HELICONIAN": {
        "scientific_name": "Dryadula phaetusa",
        "description": "Medium-sized butterfly with orange and black banded wings, and long narrow shape.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "7-9 cm",
        "diet": "Nectar from flowers, especially Lantana and Pentas",
        "behavior": "Strong flier. Migratory. Forms aggregations at roosting sites.",
        "lifecycle": "Eggs laid on passionflower vines. Caterpillars feed on host plant."
    },
    "BANDED PEACOCK": {
        "scientific_name": "Anartia fatima",
        "description": "Medium-sized butterfly with brown wings, white bands, and distinctive eye-spots on hindwings.",
        "habitat": "Open areas, gardens, and forest edges",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Fast flier. Common in gardens. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on plants in the Acanthaceae family. Multiple generations per year."
    },
    "BANDED TIGER MOTH": {
        "scientific_name": "Apantesis vittata",
        "description": "Medium-sized moth with black and white banded wings, and orange or yellow markings.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers",
        "behavior": "Nocturnal. Attracted to lights. Flies from May to August.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars are woolly bears."
    },
    "BECKERS WHITE": {
        "scientific_name": "Pontia beckerii",
        "description": "Small butterfly with white wings, black spots on forewings, and gray-green undersides.",
        "habitat": "Deserts, grasslands, and open areas",
        "distribution": "Western North America, from Canada to Mexico",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially mustards",
        "behavior": "Fast flier. Flies from March to October. Multiple generations per year.",
        "lifecycle": "Eggs laid on plants in the Brassicaceae family. Caterpillars feed on host plant."
    },
    "BIRD CHERRY ERMINE MOTH": {
        "scientific_name": "Yponomeuta evonymella",
        "description": "Small white moth with black spots, and distinctive ermine-like pattern.",
        "habitat": "Woodlands and areas with cherry trees",
        "distribution": "Europe and Asia",
        "wingspan": "1.5-2.5 cm",
        "diet": "Adults do not feed. Caterpillars feed on cherry and related trees.",
        "behavior": "Nocturnal. Can form large colonies that defoliate trees.",
        "lifecycle": "Eggs laid on cherry trees. Caterpillars form communal webs. Overwinters as young caterpillar."
    },
    "BLACK HAIRSTREAK": {
        "scientific_name": "Satyrium pruni",
        "description": "Small butterfly with brown wings, orange band on hindwings, and white-tipped tail.",
        "habitat": "Woodlands and hedgerows with blackthorn",
        "distribution": "Europe, from England to Russia",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, honeydew from aphids",
        "behavior": "Flies from June to July. Rare and localized. Perches high in trees.",
        "lifecycle": "Eggs laid on blackthorn. Caterpillars feed on leaves. Overwinters as egg."
    },
    "BLUE MORPHO": {
        "scientific_name": "Morpho menelaus",
        "description": "Very large butterfly with brilliant blue iridescent upperwings and brown undersides with eye-spots.",
        "habitat": "Tropical rainforests",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "12-20 cm",
        "diet": "Nectar from flowers, rotting fruit, and tree sap",
        "behavior": "Strong flier. Males are territorial. Flies in forest canopy.",
        "lifecycle": "Eggs laid on various host plants. Large caterpillars with defensive spines."
    },
    "BLUE SPOTTED CROW": {
        "scientific_name": "Euploea midamus",
        "description": "Medium-sized butterfly with dark brown or black wings, blue spots, and white markings.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Southeast Asia, from India to Indonesia",
        "wingspan": "7-9 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Slow flier. Forms aggregations. Warning colors indicate toxicity.",
        "lifecycle": "Eggs laid on plants in the Apocynaceae family. Caterpillars are toxic."
    },
    "BROOKES BIRDWING": {
        "scientific_name": "Ornithoptera brookiana",
        "description": "Very large butterfly with black and green wings (males) or brown wings (females), and long tail-like extensions.",
        "habitat": "Tropical rainforests",
        "distribution": "Southeast Asia, especially Borneo and Sumatra",
        "wingspan": "15-20 cm",
        "diet": "Nectar from flowers, tree sap",
        "behavior": "Strong flier. Males are territorial. Rare and protected.",
        "lifecycle": "Eggs laid on Aristolochia plants. Large caterpillars. Protected species."
    },
    "BROWN ARGUS": {
        "scientific_name": "Aricia agestis",
        "description": "Small butterfly with brown wings, orange spots on hindwings, and white fringes.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Europe, from England to the Mediterranean",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers, especially knapweeds",
        "behavior": "Flies from May to September. Forms colonies. Low flier.",
        "lifecycle": "Eggs laid on rockrose and related plants. Caterpillars feed on host plant."
    },
    "BROWN SIPROETA": {
        "scientific_name": "Siproeta epaphus",
        "description": "Medium-sized butterfly with brown wings, orange bands, and distinctive eye-spots.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers, rotting fruit",
        "behavior": "Fast flier. Common in gardens. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on plants in the Acanthaceae family. Multiple generations per year."
    },
    "CABBAGE WHITE": {
        "scientific_name": "Pieris rapae",
        "description": "Small butterfly with white wings, black spots on forewings (males) or two spots (females), and yellow-green undersides.",
        "habitat": "Gardens, fields, and open areas",
        "distribution": "Worldwide, introduced to many regions",
        "wingspan": "4-6 cm",
        "diet": "Nectar from flowers, especially mustards",
        "behavior": "Common garden pest. Fast flier. Multiple generations per year.",
        "lifecycle": "Eggs laid on plants in the Brassicaceae family. Green caterpillars feed on leaves."
    },
    # 第二批：20種蝴蝶
    "CAIRNS BIRDWING": {
        "scientific_name": "Ornithoptera euphorion",
        "description": "Very large butterfly with black and green wings (males) or brown wings (females), and long tail-like extensions.",
        "habitat": "Tropical rainforests",
        "distribution": "Northeastern Australia and Papua New Guinea",
        "wingspan": "12-15 cm",
        "diet": "Nectar from flowers, tree sap",
        "behavior": "Strong flier. Males are territorial. Protected species.",
        "lifecycle": "Eggs laid on Aristolochia plants. Large caterpillars. Protected in Australia."
    },
    "CHALK HILL BLUE": {
        "scientific_name": "Lysandra coridon",
        "description": "Small butterfly with blue upperwings (males) or brown upperwings (females), and distinctive white fringes.",
        "habitat": "Chalk grasslands and limestone areas",
        "distribution": "Europe, from England to the Mediterranean",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially knapweeds",
        "behavior": "Flies from July to September. Forms colonies. Low flier.",
        "lifecycle": "Eggs laid on horseshoe vetch. Caterpillars feed on host plant. Overwinters as egg."
    },
    "CHECQUERED SKIPPER": {
        "scientific_name": "Carterocephalus palaemon",
        "description": "Small butterfly with brown and orange checkered wings, and distinctive pattern.",
        "habitat": "Woodlands, grasslands, and open areas",
        "distribution": "Europe, Asia, and North America",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers, especially bugle and bluebells",
        "behavior": "Fast flier. Flies from May to July. Low flier.",
        "lifecycle": "Eggs laid on grasses. Caterpillars feed on host plant. Overwinters as caterpillar."
    },
    "CHESTNUT": {
        "scientific_name": "Coenonympha glycerion",
        "description": "Small butterfly with brown wings, orange patches, and eye-spots on hindwings.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Europe and Asia",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially grasses",
        "behavior": "Flies from June to August. Low flier. Forms colonies.",
        "lifecycle": "Eggs laid on grasses. Caterpillars feed on host plant. Overwinters as caterpillar."
    },
    "CINNABAR MOTH": {
        "scientific_name": "Tyria jacobaeae",
        "description": "Medium-sized moth with black and red wings, and distinctive warning colors.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Europe, Asia, and introduced to North America and Australia",
        "wingspan": "3-4 cm",
        "diet": "Adults do not feed. Caterpillars feed on ragwort.",
        "behavior": "Nocturnal. Flies from May to August. Warning colors indicate toxicity.",
        "lifecycle": "Eggs laid on ragwort. Yellow and black striped caterpillars are toxic."
    },
    "CLEARWING MOTH": {
        "scientific_name": "Sesia apiformis",
        "description": "Medium-sized moth with transparent wings, yellow and black body, and wasp-like appearance.",
        "habitat": "Woodlands and areas with poplar trees",
        "distribution": "Europe and Asia",
        "wingspan": "3-4 cm",
        "diet": "Adults do not feed. Caterpillars feed on poplar trees.",
        "behavior": "Diurnal. Mimics wasps. Flies from May to July.",
        "lifecycle": "Eggs laid on poplar trees. Caterpillars bore into tree trunks."
    },
    "CLEOPATRA": {
        "scientific_name": "Gonepteryx cleopatra",
        "description": "Medium-sized butterfly with yellow wings (males) or greenish-white wings (females), and distinctive shape.",
        "habitat": "Woodlands, scrublands, and gardens",
        "distribution": "Europe, from Mediterranean to southern England",
        "wingspan": "5-6 cm",
        "diet": "Nectar from flowers, especially thistles",
        "behavior": "Strong flier. Flies from March to October. Overwinters as adult.",
        "lifecycle": "Eggs laid on buckthorn. Green caterpillars feed on leaves."
    },
    "CLODIUS PARNASSIAN": {
        "scientific_name": "Parnassius clodius",
        "description": "Large butterfly with white wings, black spots, red eye-spots on hindwings, and transparent wing tips.",
        "habitat": "Mountain meadows and alpine areas",
        "distribution": "Western North America, from Alaska to California",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, especially thistles",
        "behavior": "Slow flier. Flies from May to August. High altitude species.",
        "lifecycle": "Eggs laid on stonecrop plants. Caterpillars feed on host plant."
    },
    "CLOUDED SULPHUR": {
        "scientific_name": "Colias philodice",
        "description": "Medium-sized butterfly with yellow wings (males) or white/yellow wings (females), and black borders.",
        "habitat": "Grasslands, fields, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "4-6 cm",
        "diet": "Nectar from flowers, especially clovers",
        "behavior": "Fast flier. Migratory. Multiple generations per year.",
        "lifecycle": "Eggs laid on plants in the Fabaceae family. Green caterpillars feed on leaves."
    },
    "COMET MOTH": {
        "scientific_name": "Argema mittrei",
        "description": "Very large moth with yellow and brown wings, long tail-like extensions, and distinctive eye-spots.",
        "habitat": "Tropical rainforests",
        "distribution": "Madagascar",
        "wingspan": "15-20 cm",
        "diet": "Adults do not feed. Caterpillars feed on various trees.",
        "behavior": "Nocturnal. Attracted to lights. Short-lived as adults.",
        "lifecycle": "Large caterpillars feed on host plants. Cocoons are made of silk."
    },
    "COMMON BANDED AWL": {
        "scientific_name": "Hasora chromus",
        "description": "Medium-sized butterfly with brown wings, white bands, and distinctive shape.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Southeast Asia, from India to Australia",
        "wingspan": "4-5 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on plants in the Fabaceae family. Caterpillars feed on leaves."
    },
    "COMMON WOOD-NYMPH": {
        "scientific_name": "Cercyonis pegala",
        "description": "Medium-sized butterfly with brown wings, eye-spots on forewings, and yellow patches.",
        "habitat": "Woodlands, grasslands, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Slow flier. Flies from June to September. Low flier.",
        "lifecycle": "Eggs laid on grasses. Caterpillars feed on host plant. Overwinters as caterpillar."
    },
    "COPPER TAIL": {
        "scientific_name": "Lycaena phlaeas",
        "description": "Small butterfly with orange and brown wings, black spots, and copper-colored hindwings.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Europe, Asia, and North America",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers, especially daisies",
        "behavior": "Fast flier. Flies from April to October. Multiple generations per year.",
        "lifecycle": "Eggs laid on dock and sorrel plants. Green caterpillars feed on leaves."
    },
    "CRECENT": {
        "scientific_name": "Phyciodes tharos",
        "description": "Small butterfly with orange and black wings, crescent-shaped markings, and distinctive pattern.",
        "habitat": "Grasslands, fields, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially asters",
        "behavior": "Fast flier. Multiple generations per year. Flies from April to October.",
        "lifecycle": "Eggs laid on plants in the Asteraceae family. Caterpillars feed on leaves."
    },
    "CRIMSON PATCH": {
        "scientific_name": "Chlosyne janais",
        "description": "Medium-sized butterfly with black wings, red patches, and white spots.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Fast flier. Common in gardens. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on plants in the Acanthaceae family. Caterpillars feed on leaves."
    },
    "DANAID EGGFLY": {
        "scientific_name": "Hypolimnas misippus",
        "description": "Medium-sized butterfly with brown wings, white spots, and distinctive eye-spots on hindwings.",
        "habitat": "Tropical and subtropical areas",
        "distribution": "Africa, Asia, and Australia",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Fast flier. Mimics toxic species. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "EASTERN COMA": {
        "scientific_name": "Polygonia comma",
        "description": "Medium-sized butterfly with orange and black wings, jagged edges, and distinctive pattern.",
        "habitat": "Woodlands, fields, and open areas",
        "distribution": "Eastern North America",
        "wingspan": "4-6 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Fast flier. Overwinters as adult. Flies from March to November.",
        "lifecycle": "Eggs laid on elm and nettle plants. Spiny caterpillars feed on leaves."
    },
    "EASTERN DAPPLE WHITE": {
        "scientific_name": "Euchloe ausonides",
        "description": "Small butterfly with white wings, green marbling on undersides, and black spots.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Western North America, from Canada to Mexico",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially mustards",
        "behavior": "Fast flier. Flies from March to June. Single generation per year.",
        "lifecycle": "Eggs laid on plants in the Brassicaceae family. Green caterpillars feed on leaves."
    },
    "EASTERN PINE ELFIN": {
        "scientific_name": "Callophrys niphon",
        "description": "Small butterfly with brown wings, green undersides, and white line on hindwings.",
        "habitat": "Pine forests and woodlands",
        "distribution": "Eastern North America",
        "wingspan": "2-3 cm",
        "diet": "Nectar from flowers, especially blueberries",
        "behavior": "Fast flier. Flies from March to May. Low flier.",
        "lifecycle": "Eggs laid on pine trees. Green caterpillars feed on needles."
    },
    # 第三批：20種蝴蝶
    "ELBOWED PIERROT": {
        "scientific_name": "Caleta elna",
        "description": "Small butterfly with black and white wings, orange spots, and distinctive pattern.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Southeast Asia, from India to Indonesia",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "EMPEROR GUM MOTH": {
        "scientific_name": "Opodiphthera eucalypti",
        "description": "Large moth with brown and white patterned wings, and distinctive eye-spots.",
        "habitat": "Eucalyptus forests and woodlands",
        "distribution": "Australia and New Zealand",
        "wingspan": "10-15 cm",
        "diet": "Adults do not feed. Caterpillars feed on eucalyptus leaves.",
        "behavior": "Nocturnal. Attracted to lights. Flies from autumn to spring.",
        "lifecycle": "Large green caterpillars feed on eucalyptus. Cocoons are made of silk."
    },
    "GARDEN TIGER MOTH": {
        "scientific_name": "Arctia caja",
        "description": "Large moth with brown and white patterned wings, orange hindwings, and distinctive tiger-like pattern.",
        "habitat": "Gardens, meadows, and open areas",
        "distribution": "Europe, Asia, and North America",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers",
        "behavior": "Nocturnal. Attracted to lights. Flies from June to August.",
        "lifecycle": "Eggs laid on various host plants. Woolly bear caterpillars are common."
    },
    "GIANT LEOPARD MOTH": {
        "scientific_name": "Hypercompe scribonia",
        "description": "Large moth with white wings, black spots, and leopard-like pattern.",
        "habitat": "Woodlands, gardens, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "5-7 cm",
        "diet": "Adults do not feed. Caterpillars feed on various plants.",
        "behavior": "Nocturnal. Attracted to lights. Flies from May to August.",
        "lifecycle": "Eggs laid on various host plants. Black and red caterpillars with spines."
    },
    "GLITTERING SAPPHIRE": {
        "scientific_name": "Iolaus iasis",
        "description": "Small butterfly with blue iridescent wings, and distinctive shimmering appearance.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Africa, from South Africa to East Africa",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "GOLD BANDED": {
        "scientific_name": "Charaxes jasius",
        "description": "Large butterfly with brown wings, gold bands, and distinctive eye-spots.",
        "habitat": "Mediterranean woodlands and scrublands",
        "distribution": "Mediterranean region, from Spain to Greece",
        "wingspan": "7-9 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Strong flier. Flies from May to October. Males are territorial.",
        "lifecycle": "Eggs laid on strawberry trees. Large caterpillars with spines."
    },
    "GREAT EGGFLY": {
        "scientific_name": "Hypolimnas bolina",
        "description": "Medium-sized butterfly with black wings, white spots, and distinctive eye-spots on hindwings.",
        "habitat": "Tropical and subtropical areas",
        "distribution": "Africa, Asia, and Australia",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Fast flier. Flies year-round in tropical areas. Common in gardens.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "GREAT JAY": {
        "scientific_name": "Graphium eurypylus",
        "description": "Large butterfly with black and green wings, white spots, and long tail-like extensions.",
        "habitat": "Tropical rainforests",
        "distribution": "Southeast Asia, from India to Indonesia",
        "wingspan": "8-10 cm",
        "diet": "Nectar from flowers, tree sap",
        "behavior": "Strong flier. Flies in forest canopy. Males are territorial.",
        "lifecycle": "Eggs laid on various host plants. Large caterpillars feed on leaves."
    },
    "GREEN CELLED CATTLEHEART": {
        "scientific_name": "Parides sesostris",
        "description": "Large butterfly with black wings, green spots, and distinctive pattern.",
        "habitat": "Tropical rainforests",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "8-10 cm",
        "diet": "Nectar from flowers",
        "behavior": "Strong flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on Aristolochia plants. Large caterpillars feed on host plant."
    },
    "GREEN HAIRSTREAK": {
        "scientific_name": "Callophrys rubi",
        "description": "Small butterfly with brown upperwings, green undersides, and white line on hindwings.",
        "habitat": "Heathlands, grasslands, and open areas",
        "distribution": "Europe and Asia",
        "wingspan": "2.5-3 cm",
        "diet": "Nectar from flowers, especially gorse and broom",
        "behavior": "Fast flier. Flies from April to July. Low flier.",
        "lifecycle": "Eggs laid on various host plants. Green caterpillars feed on leaves."
    },
    "GREY HAIRSTREAK": {
        "scientific_name": "Strymon melinus",
        "description": "Small butterfly with gray wings, orange spots, and white-tipped tail.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers, especially clovers",
        "behavior": "Fast flier. Multiple generations per year. Flies from March to November.",
        "lifecycle": "Eggs laid on various host plants. Green caterpillars feed on flowers and fruits."
    },
    "HERCULES MOTH": {
        "scientific_name": "Coscinocera hercules",
        "description": "Very large moth with brown and white patterned wings, and distinctive eye-spots.",
        "habitat": "Tropical rainforests",
        "distribution": "Northeastern Australia and New Guinea",
        "wingspan": "25-27 cm",
        "diet": "Adults do not feed. Caterpillars feed on various trees.",
        "behavior": "Nocturnal. Attracted to lights. Short-lived as adults.",
        "lifecycle": "Very large caterpillars feed on host plants. Cocoons are made of silk."
    },
    "HUMMING BIRD HAWK MOTH": {
        "scientific_name": "Macroglossum stellatarum",
        "description": "Medium-sized moth with brown wings, orange hindwings, and long proboscis. Hovers like a hummingbird.",
        "habitat": "Gardens, meadows, and open areas",
        "distribution": "Europe, Asia, and Africa",
        "wingspan": "4-5 cm",
        "diet": "Nectar from flowers, especially honeysuckle",
        "behavior": "Diurnal. Hovers while feeding. Migratory. Flies year-round in warm areas.",
        "lifecycle": "Eggs laid on bedstraw plants. Green caterpillars feed on leaves."
    },
    "INDRA SWALLOW": {
        "scientific_name": "Papilio indra",
        "description": "Large butterfly with black wings, yellow spots, and long tail-like extensions.",
        "habitat": "Mountain meadows and alpine areas",
        "distribution": "Western North America, from Canada to Mexico",
        "wingspan": "7-9 cm",
        "diet": "Nectar from flowers",
        "behavior": "Strong flier. Flies from May to August. High altitude species.",
        "lifecycle": "Eggs laid on plants in the Apiaceae family. Large caterpillars feed on leaves."
    },
    "IO MOTH": {
        "scientific_name": "Automeris io",
        "description": "Large moth with yellow and pink wings, distinctive eye-spots, and warning colors.",
        "habitat": "Woodlands, fields, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "6-8 cm",
        "diet": "Adults do not feed. Caterpillars feed on various trees.",
        "behavior": "Nocturnal. Attracted to lights. Flies from May to August.",
        "lifecycle": "Large spiny caterpillars feed on host plants. Cocoons are made of silk."
    },
    "Iphiclus sister": {
        "scientific_name": "Adelpha iphiclus",
        "description": "Medium-sized butterfly with brown wings, white bands, and distinctive pattern.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, rotting fruit",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "JULIA": {
        "scientific_name": "Dryas iulia",
        "description": "Medium-sized butterfly with orange wings, black borders, and long narrow shape.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Texas to Brazil",
        "wingspan": "8-10 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Strong flier. Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on passionflower vines. Caterpillars feed on host plant."
    },
    "LARGE MARBLE": {
        "scientific_name": "Euchloe ausonides",
        "description": "Small butterfly with white wings, green marbling on undersides, and black spots.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Western North America, from Canada to Mexico",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially mustards",
        "behavior": "Fast flier. Flies from March to June. Single generation per year.",
        "lifecycle": "Eggs laid on plants in the Brassicaceae family. Green caterpillars feed on leaves."
    },
    "LUNA MOTH": {
        "scientific_name": "Actias luna",
        "description": "Very large moth with green wings, long tail-like extensions, and distinctive eye-spots.",
        "habitat": "Deciduous forests and woodlands",
        "distribution": "Eastern North America, from Canada to Mexico",
        "wingspan": "10-12 cm",
        "diet": "Adults do not feed. Caterpillars feed on various trees.",
        "behavior": "Nocturnal. Attracted to lights. Flies from May to July.",
        "lifecycle": "Large green caterpillars feed on host plants. Cocoons are made of silk."
    },
    # 第四批：20種蝴蝶
    "MADAGASCAN SUNSET MOTH": {
        "scientific_name": "Chrysiridia rhipheus",
        "description": "Large moth with iridescent wings showing rainbow colors, and distinctive tail-like extensions.",
        "habitat": "Tropical forests",
        "distribution": "Madagascar",
        "wingspan": "7-11 cm",
        "diet": "Adults do not feed. Caterpillars feed on Omphalea plants.",
        "behavior": "Diurnal. Flies during day. Iridescent colors are structural, not from pigments.",
        "lifecycle": "Large caterpillars feed on Omphalea. Cocoons are made of silk."
    },
    "MALACHITE": {
        "scientific_name": "Siproeta stelenes",
        "description": "Medium-sized butterfly with green and black wings, and distinctive malachite-like pattern.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Texas to Brazil",
        "wingspan": "8-10 cm",
        "diet": "Nectar from flowers, rotting fruit",
        "behavior": "Fast flier. Flies year-round in tropical areas. Common in gardens.",
        "lifecycle": "Eggs laid on plants in the Acanthaceae family. Caterpillars feed on leaves."
    },
    "MANGROVE SKIPPER": {
        "scientific_name": "Phocides pigmalion",
        "description": "Medium-sized butterfly with dark brown wings, white spots, and distinctive pattern.",
        "habitat": "Mangrove forests and coastal areas",
        "distribution": "Central and South America, from Florida to Brazil",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on mangrove trees. Caterpillars feed on leaves."
    },
    "MESTRA": {
        "scientific_name": "Mestra amymone",
        "description": "Medium-sized butterfly with brown wings, orange patches, and white spots.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "METALMARK": {
        "scientific_name": "Calephelis virginiensis",
        "description": "Small butterfly with brown wings, metallic spots, and distinctive pattern.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Eastern North America",
        "wingspan": "2-3 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies from May to September. Low flier.",
        "lifecycle": "Eggs laid on various host plants. Small caterpillars feed on leaves."
    },
    "MILBERTS TORTOISESHELL": {
        "scientific_name": "Aglais milberti",
        "description": "Medium-sized butterfly with orange and black wings, white spots, and jagged edges.",
        "habitat": "Woodlands, fields, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "4-6 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Fast flier. Overwinters as adult. Flies from March to October.",
        "lifecycle": "Eggs laid on nettle plants. Spiny caterpillars feed on leaves."
    },
    "MONARCH": {
        "scientific_name": "Danaus plexippus",
        "description": "Large butterfly with orange and black wings, white spots, and distinctive pattern. Famous for migration.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "North and South America, introduced to other regions",
        "wingspan": "8-10 cm",
        "diet": "Nectar from flowers, especially milkweeds",
        "behavior": "Long-distance migrant. Forms large aggregations. Warning colors indicate toxicity.",
        "lifecycle": "Eggs laid on milkweed. Striped caterpillars are toxic. Famous migration to Mexico."
    },
    "MOURNING CLOAK": {
        "scientific_name": "Nymphalis antiopa",
        "description": "Large butterfly with dark brown wings, yellow borders, and blue spots.",
        "habitat": "Woodlands, fields, and open areas",
        "distribution": "North America, Europe, and Asia",
        "wingspan": "6-10 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Overwinters as adult. Flies from March to October. Long-lived.",
        "lifecycle": "Eggs laid on elm, willow, and poplar trees. Spiny caterpillars feed on leaves."
    },
    "OLEANDER HAWK MOTH": {
        "scientific_name": "Daphnis nerii",
        "description": "Large moth with green and brown wings, and distinctive eye-spots.",
        "habitat": "Tropical and subtropical areas",
        "distribution": "Africa, Asia, and Mediterranean region",
        "wingspan": "9-13 cm",
        "diet": "Nectar from flowers, especially oleander",
        "behavior": "Nocturnal. Strong flier. Migratory. Attracted to lights.",
        "lifecycle": "Large green caterpillars feed on oleander and related plants. Cocoons are made of silk."
    },
    "ORANGE OAKLEAF": {
        "scientific_name": "Kallima inachus",
        "description": "Large butterfly with orange and black upperwings, and brown leaf-like undersides for camouflage.",
        "habitat": "Tropical forests",
        "distribution": "Southeast Asia, from India to Indonesia",
        "wingspan": "8-12 cm",
        "diet": "Nectar from flowers, rotting fruit",
        "behavior": "Masters of camouflage. When wings closed, resembles dead leaf. Flies year-round.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "ORANGE TIP": {
        "scientific_name": "Anthocharis cardamines",
        "description": "Small butterfly with white wings, orange tips on forewings (males), and green marbling on undersides.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Europe and Asia",
        "wingspan": "4-5 cm",
        "diet": "Nectar from flowers, especially cuckooflowers",
        "behavior": "Fast flier. Flies from April to June. Single generation per year.",
        "lifecycle": "Eggs laid on plants in the Brassicaceae family. Green caterpillars feed on seed pods."
    },
    "ORCHARD SWALLOW": {
        "scientific_name": "Papilio aegeus",
        "description": "Large butterfly with black wings, white spots, and long tail-like extensions.",
        "habitat": "Gardens, orchards, and open areas",
        "distribution": "Australia and New Guinea",
        "wingspan": "10-14 cm",
        "diet": "Nectar from flowers, especially citrus",
        "behavior": "Strong flier. Common in gardens. Flies year-round in warm areas.",
        "lifecycle": "Eggs laid on citrus trees. Large green caterpillars feed on leaves."
    },
    "PAINTED LADY": {
        "scientific_name": "Vanessa cardui",
        "description": "Medium-sized butterfly with orange and black wings, white spots, and distinctive pattern.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "Worldwide, except Antarctica",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, especially thistles",
        "behavior": "Long-distance migrant. Fast flier. Multiple generations per year.",
        "lifecycle": "Eggs laid on plants in the Asteraceae family. Spiny caterpillars feed on leaves."
    },
    "PAPER KITE": {
        "scientific_name": "Idea leuconoe",
        "description": "Large butterfly with white wings, black spots, and distinctive pattern.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Southeast Asia, from Philippines to Indonesia",
        "wingspan": "10-12 cm",
        "diet": "Nectar from flowers",
        "behavior": "Slow flier. Flies year-round in tropical areas. Warning colors indicate toxicity.",
        "lifecycle": "Eggs laid on plants in the Apocynaceae family. Caterpillars are toxic."
    },
    "PEACOCK": {
        "scientific_name": "Aglais io",
        "description": "Medium-sized butterfly with red and black wings, distinctive eye-spots, and jagged edges.",
        "habitat": "Gardens, meadows, and open areas",
        "distribution": "Europe and Asia",
        "wingspan": "5-6 cm",
        "diet": "Nectar from flowers, especially buddleia",
        "behavior": "Overwinters as adult. Flies from March to October. Common in gardens.",
        "lifecycle": "Eggs laid on nettle plants. Spiny black caterpillars feed on leaves."
    },
    "PINE WHITE": {
        "scientific_name": "Neophasia menapia",
        "description": "Medium-sized butterfly with white wings, black spots, and distinctive pattern.",
        "habitat": "Pine forests and woodlands",
        "distribution": "Western North America, from Canada to Mexico",
        "wingspan": "5-6 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies from July to September. Single generation per year.",
        "lifecycle": "Eggs laid on pine trees. Green caterpillars feed on needles."
    },
    "PIPEVINE SWALLOW": {
        "scientific_name": "Battus philenor",
        "description": "Large butterfly with black wings, blue iridescence, and distinctive pattern.",
        "habitat": "Woodlands, fields, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "7-10 cm",
        "diet": "Nectar from flowers",
        "behavior": "Strong flier. Warning colors indicate toxicity. Flies from March to October.",
        "lifecycle": "Eggs laid on pipevine plants. Red and black caterpillars are toxic."
    },
    "POLYPHEMUS MOTH": {
        "scientific_name": "Antheraea polyphemus",
        "description": "Very large moth with brown and tan wings, distinctive eye-spots, and transparent patches.",
        "habitat": "Deciduous forests and woodlands",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "10-15 cm",
        "diet": "Adults do not feed. Caterpillars feed on various trees.",
        "behavior": "Nocturnal. Attracted to lights. Flies from May to July.",
        "lifecycle": "Large green caterpillars feed on host plants. Cocoons are made of silk."
    },
    "POPINJAY": {
        "scientific_name": "Stibochiona nicea",
        "description": "Medium-sized butterfly with black and white wings, and distinctive pattern.",
        "habitat": "Tropical forests",
        "distribution": "Southeast Asia, from India to Indonesia",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    # 第五批：最後20種蝴蝶
    "PURPLE HAIRSTREAK": {
        "scientific_name": "Favonius quercus",
        "description": "Small butterfly with purple upperwings (males) or brown upperwings (females), and orange spots on hindwings.",
        "habitat": "Oak woodlands and forests",
        "distribution": "Europe and Asia",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, honeydew from aphids",
        "behavior": "Flies from July to August. Perches high in trees. Rarely seen at ground level.",
        "lifecycle": "Eggs laid on oak trees. Caterpillars feed on leaves. Overwinters as egg."
    },
    "PURPLISH COPPER": {
        "scientific_name": "Lycaena helloides",
        "description": "Small butterfly with orange and brown wings, purple sheen, and black spots.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Western North America, from Canada to Mexico",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers, especially clovers",
        "behavior": "Fast flier. Multiple generations per year. Flies from May to October.",
        "lifecycle": "Eggs laid on dock and sorrel plants. Green caterpillars feed on leaves."
    },
    "QUESTION MARK": {
        "scientific_name": "Polygonia interrogationis",
        "description": "Medium-sized butterfly with orange and black wings, jagged edges, and silver question mark on hindwings.",
        "habitat": "Woodlands, fields, and open areas",
        "distribution": "Eastern North America",
        "wingspan": "5-6 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Overwinters as adult. Flies from March to November. Fast flier.",
        "lifecycle": "Eggs laid on elm and nettle plants. Spiny caterpillars feed on leaves."
    },
    "RED ADMIRAL": {
        "scientific_name": "Vanessa atalanta",
        "description": "Medium-sized butterfly with black and red wings, white spots, and distinctive pattern.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "North America, Europe, Asia, and North Africa",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Migratory. Fast flier. Overwinters as adult. Flies from March to November.",
        "lifecycle": "Eggs laid on nettle plants. Spiny caterpillars feed on leaves."
    },
    "RED CRACKER": {
        "scientific_name": "Hamadryas amphinome",
        "description": "Medium-sized butterfly with brown and red wings, white spots, and distinctive pattern.",
        "habitat": "Tropical forests",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers, rotting fruit",
        "behavior": "Fast flier. Males make cracking sounds with wings. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "RED POSTMAN": {
        "scientific_name": "Heliconius erato",
        "description": "Medium-sized butterfly with black and red wings, white spots, and distinctive pattern.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Slow flier. Warning colors indicate toxicity. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on passionflower vines. Caterpillars are toxic."
    },
    "RED SPOTTED PURPLE": {
        "scientific_name": "Limenitis arthemis",
        "description": "Large butterfly with black wings, blue iridescence, and red spots on hindwings.",
        "habitat": "Woodlands and forest edges",
        "distribution": "Eastern North America",
        "wingspan": "7-10 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Fast flier. Flies from May to September. Mimics toxic species.",
        "lifecycle": "Eggs laid on cherry and poplar trees. Spiny caterpillars feed on leaves."
    },
    "ROSY MAPLE MOTH": {
        "scientific_name": "Dryocampa rubicunda",
        "description": "Small moth with pink and yellow wings, and distinctive pattern.",
        "habitat": "Deciduous forests and woodlands",
        "distribution": "Eastern North America, from Canada to Florida",
        "wingspan": "3-5 cm",
        "diet": "Adults do not feed. Caterpillars feed on maple and oak trees.",
        "behavior": "Nocturnal. Attracted to lights. Flies from May to August.",
        "lifecycle": "Large green and yellow caterpillars feed on host plants. Cocoons are made of silk."
    },
    "SCARCE SWALLOW": {
        "scientific_name": "Iphiclides podalirius",
        "description": "Large butterfly with yellow and black wings, blue spots, and long tail-like extensions.",
        "habitat": "Woodlands, gardens, and open areas",
        "distribution": "Europe, Asia, and North Africa",
        "wingspan": "8-10 cm",
        "diet": "Nectar from flowers",
        "behavior": "Strong flier. Flies from April to September. Males are territorial.",
        "lifecycle": "Eggs laid on fruit trees. Large green caterpillars feed on leaves."
    },
    "SILVER SPOT SKIPPER": {
        "scientific_name": "Hesperia comma",
        "description": "Small butterfly with brown wings, silver spots, and distinctive pattern.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Europe, Asia, and North America",
        "wingspan": "2.5-3.5 cm",
        "diet": "Nectar from flowers, especially thistles",
        "behavior": "Fast flier. Flies from July to September. Low flier.",
        "lifecycle": "Eggs laid on grasses. Caterpillars feed on host plant. Overwinters as egg."
    },
    "SIXSPOT BURNET MOTH": {
        "scientific_name": "Zygaena filipendulae",
        "description": "Medium-sized moth with black wings, red spots, and distinctive warning colors.",
        "habitat": "Grasslands, meadows, and open areas",
        "distribution": "Europe and Asia",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers",
        "behavior": "Diurnal. Flies during day. Warning colors indicate toxicity. Flies from June to August.",
        "lifecycle": "Eggs laid on plants in the Fabaceae family. Yellow and black caterpillars are toxic."
    },
    "SLEEPY ORANGE": {
        "scientific_name": "Eurema nicippe",
        "description": "Small butterfly with orange wings, black borders, and distinctive pattern.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "3-4 cm",
        "diet": "Nectar from flowers, especially clovers",
        "behavior": "Fast flier. Multiple generations per year. Flies from March to November.",
        "lifecycle": "Eggs laid on plants in the Fabaceae family. Green caterpillars feed on leaves."
    },
    "SOOTYWING": {
        "scientific_name": "Pholisora catullus",
        "description": "Small butterfly with dark brown or black wings, white spots, and distinctive pattern.",
        "habitat": "Open areas, fields, and disturbed areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "2-3 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Multiple generations per year. Flies from April to October.",
        "lifecycle": "Eggs laid on plants in the Chenopodiaceae family. Small caterpillars feed on leaves."
    },
    "SOUTHERN DOGFACE": {
        "scientific_name": "Zerene cesonia",
        "description": "Medium-sized butterfly with yellow wings, black borders, and dog face-like pattern on forewings.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "Southern United States and Mexico",
        "wingspan": "5-7 cm",
        "diet": "Nectar from flowers, especially clovers",
        "behavior": "Fast flier. Multiple generations per year. Flies year-round in warm areas.",
        "lifecycle": "Eggs laid on plants in the Fabaceae family. Green caterpillars feed on leaves."
    },
    "STRAITED QUEEN": {
        "scientific_name": "Danaus gilippus",
        "description": "Medium-sized butterfly with orange and black wings, white spots, and distinctive pattern.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "North and South America, from United States to Brazil",
        "wingspan": "7-9 cm",
        "diet": "Nectar from flowers, especially milkweeds",
        "behavior": "Fast flier. Warning colors indicate toxicity. Flies year-round in warm areas.",
        "lifecycle": "Eggs laid on milkweed. Striped caterpillars are toxic."
    },
    "TROPICAL LEAFWING": {
        "scientific_name": "Historis odius",
        "description": "Large butterfly with brown wings, orange patches, and leaf-like pattern on undersides.",
        "habitat": "Tropical forests",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "10-12 cm",
        "diet": "Nectar from flowers, rotting fruit",
        "behavior": "Strong flier. Masters of camouflage. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Large caterpillars feed on leaves."
    },
    "TWO BARRED FLASHER": {
        "scientific_name": "Astraptes fulgerator",
        "description": "Medium-sized butterfly with brown wings, white bars, and distinctive pattern.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Mexico to Brazil",
        "wingspan": "4-5 cm",
        "diet": "Nectar from flowers",
        "behavior": "Fast flier. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on various host plants. Caterpillars feed on leaves."
    },
    "ULYSES": {
        "scientific_name": "Papilio ulysses",
        "description": "Large butterfly with brilliant blue upperwings and black borders, and brown undersides.",
        "habitat": "Tropical rainforests",
        "distribution": "Northeastern Australia, Papua New Guinea, and Indonesia",
        "wingspan": "10-12 cm",
        "diet": "Nectar from flowers, especially Lantana",
        "behavior": "Strong flier. Males are territorial. Protected species in Australia.",
        "lifecycle": "Eggs laid on various host plants. Large green caterpillars feed on leaves."
    },
    "VICEROY": {
        "scientific_name": "Limenitis archippus",
        "description": "Medium-sized butterfly with orange and black wings, white spots, and distinctive pattern. Mimics Monarch.",
        "habitat": "Wetlands, meadows, and open areas",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "6-8 cm",
        "diet": "Nectar from flowers, tree sap, and rotting fruit",
        "behavior": "Fast flier. Mimics toxic Monarch butterfly. Flies from May to October.",
        "lifecycle": "Eggs laid on willow and poplar trees. Spiny caterpillars feed on leaves."
    },
    "WHITE LINED SPHINX MOTH": {
        "scientific_name": "Hyles lineata",
        "description": "Large moth with brown and white wings, pink hindwings, and distinctive pattern.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "North America, from Canada to Mexico",
        "wingspan": "6-9 cm",
        "diet": "Nectar from flowers, especially petunias",
        "behavior": "Nocturnal and crepuscular. Hovers like hummingbird. Attracted to lights.",
        "lifecycle": "Large green caterpillars feed on various host plants. Cocoons are made of silk."
    },
    "WOOD SATYR": {
        "scientific_name": "Megisto cymela",
        "description": "Medium-sized butterfly with brown wings, eye-spots, and distinctive pattern.",
        "habitat": "Woodlands and forest edges",
        "distribution": "Eastern North America",
        "wingspan": "4-5 cm",
        "diet": "Nectar from flowers, tree sap",
        "behavior": "Slow flier. Flies from May to September. Low flier.",
        "lifecycle": "Eggs laid on grasses. Caterpillars feed on host plant. Overwinters as caterpillar."
    },
    "YELLOW SWALLOW TAIL": {
        "scientific_name": "Papilio machaon",
        "description": "Large butterfly with yellow and black wings, blue spots, and long tail-like extensions.",
        "habitat": "Open areas, fields, and gardens",
        "distribution": "Europe, Asia, and North America",
        "wingspan": "8-10 cm",
        "diet": "Nectar from flowers, especially thistles",
        "behavior": "Strong flier. Flies from April to September. Males are territorial.",
        "lifecycle": "Eggs laid on plants in the Apiaceae family. Large green caterpillars feed on leaves."
    },
    "ZEBRA LONG WING": {
        "scientific_name": "Heliconius charithonia",
        "description": "Medium-sized butterfly with black wings, yellow stripes, and long narrow shape.",
        "habitat": "Tropical forests and gardens",
        "distribution": "Central and South America, from Texas to Brazil, and Florida",
        "wingspan": "7-10 cm",
        "diet": "Nectar from flowers, especially Lantana, and pollen",
        "behavior": "Slow flier. Long-lived. Warning colors indicate toxicity. Flies year-round in tropical areas.",
        "lifecycle": "Eggs laid on passionflower vines. Striped caterpillars are toxic. Adults can live for months."
    }
}

def batch_update_common_butterflies():
    """批量更新常見蝴蝶的信息"""
    data = load_butterfly_template()
    updated_count = 0
    
    for butterfly_key, butterfly_data in data.items():
        # 檢查是否有預定義的信息
        if butterfly_key in COMMON_BUTTERFLIES_INFO:
            info = COMMON_BUTTERFLIES_INFO[butterfly_key]
            butterfly_data['scientific_name'] = info['scientific_name']
            butterfly_data['description'] = info['description']
            butterfly_data['habitat'] = info['habitat']
            butterfly_data['distribution'] = info['distribution']
            butterfly_data['wingspan'] = info['wingspan']
            butterfly_data['diet'] = info['diet']
            butterfly_data['behavior'] = info['behavior']
            butterfly_data['lifecycle'] = info['lifecycle']
            updated_count += 1
            print(f"Updated: {butterfly_key}")
    
    save_butterfly_template(data)
    print(f"\nTotal updated: {updated_count} butterfly/moth species")
    return updated_count

if __name__ == '__main__':
    print("Batch updating butterfly information...")
    print("="*60)
    batch_update_common_butterflies()
    print("="*60)
    print("Done!")

