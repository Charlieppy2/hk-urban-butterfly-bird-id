"""
批量更新鳥類信息的腳本
可以從多個來源獲取鳥類詳細資料並更新到模板文件
"""

import json
import os
import re

def load_bird_template():
    """加載鳥類模板文件"""
    template_path = os.path.join(os.path.dirname(__file__), 'bird_info_template.json')
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_bird_template(data):
    """保存鳥類模板文件"""
    template_path = os.path.join(os.path.dirname(__file__), 'bird_info_template.json')
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {template_path}")

def update_bird_info(bird_data, scientific_name, description, habitat, distribution, size, diet, behavior):
    """更新單個鳥類的信息"""
    bird_data['scientific_name'] = scientific_name
    bird_data['description'] = description
    bird_data['habitat'] = habitat
    bird_data['distribution'] = distribution
    bird_data['size'] = size
    bird_data['diet'] = diet
    bird_data['behavior'] = behavior
    return bird_data

# 常見鳥類的詳細信息（可以擴展）
COMMON_BIRDS_INFO = {
    "House_Sparrow": {
        "scientific_name": "Passer domesticus",
        "description": "Small, chunky bird. Males have gray crown, black bib, and chestnut nape. Females are streaked brown and gray.",
        "habitat": "Urban areas, farms, parks, and gardens. Closely associated with human settlements.",
        "distribution": "Worldwide, introduced to many regions. Native to Europe, Asia, and North Africa.",
        "size": "Length: 14-16 cm, Wingspan: 19-25 cm, Weight: 24-40 g",
        "diet": "Seeds, grains, insects, and human food scraps. Visits bird feeders.",
        "behavior": "Social, forms flocks. Nests in cavities, buildings, and nest boxes. Year-round resident."
    },
    "Purple_Finch": {
        "scientific_name": "Haemorhous purpureus",
        "description": "Medium-sized finch. Males are raspberry-red on head, breast, and back. Females are streaked brown with white eyebrow.",
        "habitat": "Coniferous and mixed forests, parks, and gardens",
        "distribution": "North America, from Canada to southern United States",
        "size": "Length: 12-16 cm, Wingspan: 22-26 cm, Weight: 18-32 g",
        "diet": "Seeds, buds, fruits, and insects. Eats sunflower seeds at feeders.",
        "behavior": "Migratory in northern range, resident in south. Visits bird feeders, especially in winter."
    },
    "Anna_Hummingbird": {
        "scientific_name": "Calypte anna",
        "description": "Medium-sized hummingbird. Males have iridescent rose-red crown and throat. Females are green above, gray below with red spots on throat.",
        "habitat": "Gardens, parks, open woodlands, and coastal scrub",
        "distribution": "Western North America, from British Columbia to Baja California",
        "size": "Length: 10-11 cm, Wingspan: 12-13 cm, Weight: 3-6 g",
        "diet": "Nectar from flowers, small insects, and tree sap",
        "behavior": "Year-round resident in many areas. Aggressive defender of feeding territories. Can hover and fly backwards."
    },
    "Gray_crowned_Rosy_Finch": {
        "scientific_name": "Leucosticte tephrocotis",
        "description": "Medium-sized finch with gray crown, brown body, and pink patches on wings and rump. Bill is yellow in summer, dark in winter.",
        "habitat": "Alpine and subalpine areas, rocky slopes, and tundra",
        "distribution": "Western North America, from Alaska to California and Rocky Mountains",
        "size": "Length: 14-16 cm, Wingspan: 33 cm, Weight: 22-60 g",
        "diet": "Seeds, insects, and berries. Forages on ground and in snow.",
        "behavior": "Forms large flocks in winter. Breeds at high elevations. Hardy, survives in harsh mountain conditions."
    },
    "Red_winged_Blackbird": {
        "scientific_name": "Agelaius phoeniceus",
        "description": "Medium-sized blackbird. Males are black with red and yellow shoulder patches. Females are streaked brown and black.",
        "habitat": "Marshes, wetlands, fields, and agricultural areas",
        "distribution": "Throughout North America, from Alaska to Central America",
        "size": "Length: 17-23 cm, Wingspan: 31-40 cm, Weight: 41-65 g",
        "diet": "Seeds, grains, insects, and small vertebrates",
        "behavior": "Forms large flocks, especially in winter. Males defend breeding territories aggressively. Migratory in northern range."
    },
    "Indigo_Bunting": {
        "scientific_name": "Passerina cyanea",
        "description": "Small songbird. Breeding males are brilliant blue all over. Females and winter males are brown with blue tinges.",
        "habitat": "Brushy areas, forest edges, and open woodlands",
        "distribution": "Eastern and central North America, winters in Central America and Caribbean",
        "size": "Length: 11-13 cm, Wingspan: 18-23 cm, Weight: 12-18 g",
        "diet": "Seeds, insects, and berries. Eats small seeds and insects during breeding season.",
        "behavior": "Migratory. Males sing from high perches. Nests in dense shrubs."
    },
    "Lazuli_Bunting": {
        "scientific_name": "Passerina amoena",
        "description": "Small songbird. Males have bright blue head and back, orange breast, white belly. Females are brown with blue tinges.",
        "habitat": "Brushy areas, open woodlands, and streamside thickets",
        "distribution": "Western North America, from Canada to Mexico",
        "size": "Length: 13-14 cm, Wingspan: 21-23 cm, Weight: 13-18 g",
        "diet": "Seeds, insects, and berries",
        "behavior": "Migratory. Males sing from exposed perches. Forms small flocks in winter."
    },
    "Painted_Bunting": {
        "scientific_name": "Passerina ciris",
        "description": "Small, colorful songbird. Males are brightly colored with blue head, green back, red underparts. Females are green above, yellow-green below.",
        "habitat": "Brushy areas, woodland edges, and gardens",
        "distribution": "Southeastern United States and Mexico, winters in Central America",
        "size": "Length: 12-13 cm, Wingspan: 21-23 cm, Weight: 13-19 g",
        "diet": "Seeds, insects, and berries",
        "behavior": "Migratory. Shy and secretive. Males are territorial during breeding season."
    },
    "Bobolink": {
        "scientific_name": "Dolichonyx oryzivorus",
        "description": "Medium-sized songbird. Breeding males are black with white back and yellow nape. Females and winter males are streaked brown.",
        "habitat": "Grasslands, meadows, and agricultural fields",
        "distribution": "North America, breeds in northern United States and Canada, winters in South America",
        "size": "Length: 16-18 cm, Wingspan: 25-28 cm, Weight: 30-50 g",
        "diet": "Seeds, grains, and insects",
        "behavior": "Long-distance migrant. Forms large flocks. Males perform flight displays during breeding."
    },
    "Gray_Catbird": {
        "scientific_name": "Dumetella carolinensis",
        "description": "Medium-sized songbird. Slate gray overall with black cap and chestnut undertail coverts.",
        "habitat": "Dense thickets, shrublands, gardens, and parks",
        "distribution": "Eastern and central North America, winters in southeastern United States, Mexico, and Central America",
        "size": "Length: 20-24 cm, Wingspan: 22-30 cm, Weight: 23-56 g",
        "diet": "Fruits, berries, and insects",
        "behavior": "Mimics other birds. Skulks in dense vegetation. Migratory in northern range."
    },
    "Spotted_Catbird": {
        "scientific_name": "Ailuroedus maculosus",
        "description": "Medium-sized bird with olive-green plumage and white spots. Has distinctive cat-like call.",
        "habitat": "Tropical and subtropical rainforests",
        "distribution": "Northeastern Australia and New Guinea",
        "size": "Length: 26-30 cm, Weight: 100-150 g",
        "diet": "Fruits, berries, and insects",
        "behavior": "Territorial, builds large stick nests. Known for cat-like mewing calls."
    },
    "Yellow_breasted_Chat": {
        "scientific_name": "Icteria virens",
        "description": "Large warbler with bright yellow breast, olive-green back, white spectacles, and long tail.",
        "habitat": "Dense thickets, brushy areas, and woodland edges",
        "distribution": "North America, breeds in United States and southern Canada, winters in Central America",
        "size": "Length: 17-19 cm, Wingspan: 23-27 cm, Weight: 20-34 g",
        "diet": "Insects, fruits, and berries",
        "behavior": "Largest North American warbler. Skulks in dense vegetation. Mimics other birds."
    },
    "Eastern_Towhee": {
        "scientific_name": "Pipilo erythrophthalmus",
        "description": "Large sparrow. Males are black above with white spots, rufous sides, and white belly. Females are brown where males are black.",
        "habitat": "Brushy areas, forest edges, and thickets",
        "distribution": "Eastern North America, from Canada to Gulf Coast",
        "size": "Length: 17-21 cm, Wingspan: 20-30 cm, Weight: 32-53 g",
        "diet": "Seeds, fruits, and insects",
        "behavior": "Forages on ground by scratching. Sings 'drink-your-tea' song. Year-round resident in south."
    },
    "Northern_Flicker": {
        "scientific_name": "Colaptes auratus",
        "description": "Large woodpecker. Brown with black bars, white rump, and yellow or red under wings. Has black crescent on chest.",
        "habitat": "Open woodlands, parks, and suburban areas",
        "distribution": "Throughout North America",
        "size": "Length: 28-31 cm, Wingspan: 42-51 cm, Weight: 110-160 g",
        "diet": "Ants, beetles, fruits, and seeds. Often forages on ground.",
        "behavior": "Drums on trees and metal objects. Migratory in northern range. Nests in tree cavities."
    },
    "Acadian_Flycatcher": {
        "scientific_name": "Empidonax virescens",
        "description": "Small flycatcher with olive-green upperparts, white underparts, and two white wing bars.",
        "habitat": "Mature deciduous forests, especially near streams",
        "distribution": "Eastern North America, winters in Central and South America",
        "size": "Length: 13-15 cm, Wingspan: 21-24 cm, Weight: 12-14 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Sits on perch and sallies out to catch insects. Builds hanging nest."
    },
    "Great_Crested_Flycatcher": {
        "scientific_name": "Myiarchus crinitus",
        "description": "Large flycatcher with gray head, olive-brown back, yellow belly, and rufous tail.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "Eastern North America, winters in Central and South America",
        "size": "Length: 17-21 cm, Wingspan: 34 cm, Weight: 27-40 g",
        "diet": "Insects, fruits, and berries",
        "behavior": "Migratory. Nests in tree cavities, often uses snake skins in nest. Loud 'wheep' call."
    },
    "American_Goldfinch": {
        "scientific_name": "Spinus tristis",
        "description": "Small finch. Breeding males are bright yellow with black cap, wings, and tail. Females and winter males are duller, olive-brown with yellow highlights.",
        "habitat": "Weedy fields, open woodlands, gardens, parks, and roadsides",
        "distribution": "Throughout North America, from southern Canada to northern Mexico",
        "size": "Length: 11-13 cm, Wingspan: 19-22 cm, Weight: 11-20 g",
        "diet": "Primarily seeds, especially from thistles, sunflowers, and dandelions. Also eats some insects during breeding season.",
        "behavior": "Late breeder, nests in mid-summer when seeds are abundant. Flocks in winter. Bouncy, undulating flight pattern. Visits bird feeders for nyjer and sunflower seeds."
    },
    "European_Goldfinch": {
        "scientific_name": "Carduelis carduelis",
        "description": "Small finch with red face, black and white head, brown back, and yellow wing patches.",
        "habitat": "Open woodlands, gardens, parks, and agricultural areas",
        "distribution": "Europe, North Africa, and western Asia. Introduced to Australia and New Zealand",
        "size": "Length: 12-13 cm, Wingspan: 21-25 cm, Weight: 14-19 g",
        "diet": "Seeds, especially thistle and teasel seeds",
        "behavior": "Social, forms flocks. Visits bird feeders. Beautiful song."
    },
    "House_Wren": {
        "scientific_name": "Troglodytes aedon",
        "description": "Small, brown wren with barred wings and tail. Short, slightly curved bill.",
        "habitat": "Open woodlands, gardens, parks, and suburban areas",
        "distribution": "Throughout North and South America",
        "size": "Length: 11-13 cm, Wingspan: 15 cm, Weight: 10-12 g",
        "diet": "Insects and spiders",
        "behavior": "Very vocal, sings complex songs. Nests in cavities, including nest boxes. Aggressive towards other cavity nesters."
    },
    "Carolina_Wren": {
        "scientific_name": "Thryothorus ludovicianus",
        "description": "Large wren with reddish-brown upperparts, buff underparts, and white eyebrow stripe.",
        "habitat": "Dense vegetation, woodlands, gardens, and parks",
        "distribution": "Eastern and southeastern United States, year-round resident",
        "size": "Length: 12-14 cm, Wingspan: 29 cm, Weight: 18-22 g",
        "diet": "Insects, spiders, and small fruits",
        "behavior": "Year-round resident. Loud 'tea-kettle' song. Pairs stay together year-round. Nests in various cavities."
    },
    # 第二批：20種鳥類
    "Laysan_Albatross": {
        "scientific_name": "Phoebastria immutabilis",
        "description": "Large seabird with white head and body, dark back and wings. Has distinctive dark eye patch.",
        "habitat": "Pelagic (open ocean), breeds on remote islands",
        "distribution": "North Pacific Ocean, breeds on Hawaiian Islands and other Pacific islands",
        "size": "Length: 71-79 cm, Wingspan: 195-203 cm, Weight: 2.4-4.1 kg",
        "diet": "Squid, fish, crustaceans, and other marine life",
        "behavior": "Spends most of life at sea. Returns to land only to breed. Forms large colonies. Long-lived, can live 40+ years."
    },
    "Sooty_Albatross": {
        "scientific_name": "Phoebetria fusca",
        "description": "Large seabird with dark sooty-brown to blackish plumage. Has white crescent behind eye.",
        "habitat": "Pelagic (open ocean), breeds on remote islands",
        "distribution": "Southern Ocean, breeds on subantarctic islands",
        "size": "Length: 84-89 cm, Wingspan: 200-213 cm, Weight: 2.5-3.5 kg",
        "diet": "Squid, fish, and other marine life",
        "behavior": "Spends most of life at sea. Excellent glider. Forms breeding colonies on remote islands."
    },
    "Groove_billed_Ani": {
        "scientific_name": "Crotophaga sulcirostris",
        "description": "Large black bird with long tail, grooved bill, and iridescent black plumage.",
        "habitat": "Open grasslands, agricultural areas, and scrublands",
        "distribution": "Southern United States, Mexico, Central America, and northern South America",
        "size": "Length: 30-36 cm, Weight: 70-90 g",
        "diet": "Insects, small vertebrates, and fruits",
        "behavior": "Social, forms groups. Cooperative breeding. Communal nesting."
    },
    "Crested_Auklet": {
        "scientific_name": "Aethia cristatella",
        "description": "Small seabird with black body, white belly, and distinctive forward-curving crest on forehead.",
        "habitat": "Coastal waters and rocky islands",
        "distribution": "North Pacific, from Alaska to Japan",
        "size": "Length: 18-27 cm, Wingspan: 40-50 cm, Weight: 195-330 g",
        "diet": "Small fish, krill, and other marine invertebrates",
        "behavior": "Forms large breeding colonies. Dives for food. Nocturnal at breeding sites."
    },
    "Least_Auklet": {
        "scientific_name": "Aethia pusilla",
        "description": "Very small seabird, smallest auklet. Black above, white below, with white facial plumes in breeding season.",
        "habitat": "Coastal waters and rocky islands",
        "distribution": "North Pacific, from Alaska to Japan",
        "size": "Length: 14-18 cm, Wingspan: 35-40 cm, Weight: 75-100 g",
        "diet": "Small zooplankton, krill, and small fish",
        "behavior": "Forms huge breeding colonies. Very social. Dives for food."
    },
    "Parakeet_Auklet": {
        "scientific_name": "Aethia psittacula",
        "description": "Small seabird with dark gray body, white belly, and distinctive upturned red bill.",
        "habitat": "Coastal waters and rocky islands",
        "distribution": "North Pacific, from Alaska to Japan",
        "size": "Length: 23-25 cm, Wingspan: 40-45 cm, Weight: 200-300 g",
        "diet": "Small fish, krill, and jellyfish",
        "behavior": "Forms breeding colonies. Dives for food. Nocturnal at breeding sites."
    },
    "Rhinoceros_Auklet": {
        "scientific_name": "Cerorhinca monocerata",
        "description": "Medium-sized seabird with dark gray-brown body, white belly, and distinctive horn-like projection on bill during breeding.",
        "habitat": "Coastal waters and rocky islands",
        "distribution": "North Pacific, from Alaska to California and Japan",
        "size": "Length: 30-35 cm, Wingspan: 60-70 cm, Weight: 350-500 g",
        "diet": "Small fish, especially sand lance and herring",
        "behavior": "Forms breeding colonies. Nocturnal at breeding sites. Dives for food."
    },
    "Brewer_Blackbird": {
        "scientific_name": "Euphagus cyanocephalus",
        "description": "Medium-sized blackbird. Males are black with purple-blue iridescence. Females are brown with dark eyes.",
        "habitat": "Open areas, fields, parks, and urban areas",
        "distribution": "Western North America, from Canada to Mexico",
        "size": "Length: 20-25 cm, Wingspan: 36-40 cm, Weight: 60-90 g",
        "diet": "Seeds, grains, insects, and fruits",
        "behavior": "Forms flocks. Nests in colonies. Year-round resident in many areas."
    },
    "Rusty_Blackbird": {
        "scientific_name": "Euphagus carolinus",
        "description": "Medium-sized blackbird. Breeding males are black with greenish iridescence. Females are brown with rusty edges.",
        "habitat": "Wetlands, bogs, and forested swamps",
        "distribution": "North America, breeds in Canada and Alaska, winters in southeastern United States",
        "size": "Length: 22-25 cm, Wingspan: 36-40 cm, Weight: 60-70 g",
        "diet": "Insects, seeds, and small aquatic animals",
        "behavior": "Migratory. Declining population. Nests in coniferous forests near water."
    },
    "Yellow_headed_Blackbird": {
        "scientific_name": "Xanthocephalus xanthocephalus",
        "description": "Medium-sized blackbird. Males are black with bright yellow head and chest. Females are brown with yellow throat.",
        "habitat": "Marshes, wetlands, and reed beds",
        "distribution": "Western and central North America, winters in southwestern United States and Mexico",
        "size": "Length: 20-26 cm, Wingspan: 36-42 cm, Weight: 60-100 g",
        "diet": "Insects, seeds, and grains",
        "behavior": "Migratory. Forms large flocks. Males are polygamous. Nests in colonies in marshes."
    },
    "Brewer_Sparrow": {
        "scientific_name": "Spizella breweri",
        "description": "Small sparrow with gray head, brown back with streaks, and white underparts.",
        "habitat": "Sagebrush, arid grasslands, and shrublands",
        "distribution": "Western North America, from Canada to Mexico",
        "size": "Length: 12-14 cm, Wingspan: 18-20 cm, Weight: 10-14 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory in northern range. Nests on ground or low in shrubs."
    },
    "Chipping_Sparrow": {
        "scientific_name": "Spizella passerina",
        "description": "Small sparrow with rufous cap, gray face, and brown streaked back.",
        "habitat": "Open woodlands, parks, gardens, and suburban areas",
        "distribution": "North America, from Canada to Mexico",
        "size": "Length: 12-15 cm, Wingspan: 20-23 cm, Weight: 11-16 g",
        "diet": "Seeds, grains, and insects",
        "behavior": "Migratory in northern range. Visits bird feeders. Nests in trees or shrubs."
    },
    "Clay_colored_Sparrow": {
        "scientific_name": "Spizella pallida",
        "description": "Small sparrow with gray head with brown crown stripe, pale brown back, and buff underparts.",
        "habitat": "Grasslands, prairies, and shrublands",
        "distribution": "Central North America, breeds in Canada and northern United States, winters in Mexico",
        "size": "Length: 12-14 cm, Wingspan: 20-22 cm, Weight: 10-13 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Nests on ground or low in shrubs. Shy and secretive."
    },
    "Field_Sparrow": {
        "scientific_name": "Spizella pusilla",
        "description": "Small sparrow with pink bill, gray head with rufous crown, and brown streaked back.",
        "habitat": "Old fields, grasslands, and open woodlands",
        "distribution": "Eastern and central North America",
        "size": "Length: 12-15 cm, Wingspan: 20-22 cm, Weight: 11-15 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory in northern range. Sings beautiful trilling song. Nests on ground."
    },
    "Fox_Sparrow": {
        "scientific_name": "Passerella iliaca",
        "description": "Large sparrow with heavily streaked brown and gray plumage, rufous tail, and spotted breast.",
        "habitat": "Dense thickets, forest undergrowth, and brushy areas",
        "distribution": "North America, breeds in Canada and Alaska, winters in United States",
        "size": "Length: 15-19 cm, Wingspan: 26-29 cm, Weight: 26-44 g",
        "diet": "Seeds, fruits, and insects",
        "behavior": "Migratory. Forages on ground by scratching. Shy and secretive."
    },
    "Grasshopper_Sparrow": {
        "scientific_name": "Ammodramus savannarum",
        "description": "Small sparrow with flat head, short tail, and buffy underparts with fine streaks.",
        "habitat": "Grasslands, prairies, and hayfields",
        "distribution": "North America, breeds in United States and Canada, winters in southern United States and Mexico",
        "size": "Length: 11-13 cm, Wingspan: 18-20 cm, Weight: 13-20 g",
        "diet": "Insects and seeds",
        "behavior": "Migratory. Sings insect-like buzz. Nests on ground in grass."
    },
    "Harris_Sparrow": {
        "scientific_name": "Zonotrichia querula",
        "description": "Large sparrow with black face and bib, pink bill, and brown streaked back.",
        "habitat": "Brushy areas, woodlands, and gardens",
        "distribution": "Central North America, breeds in Canada, winters in central United States",
        "size": "Length: 17-20 cm, Wingspan: 27-30 cm, Weight: 26-49 g",
        "diet": "Seeds, grains, and insects",
        "behavior": "Migratory. Visits bird feeders. Nests on ground in tundra."
    },
    "Henslow_Sparrow": {
        "scientific_name": "Centronyx henslowii",
        "description": "Small sparrow with olive head, brown streaked back, and buffy underparts with streaks.",
        "habitat": "Tall grasslands and meadows",
        "distribution": "Eastern and central North America",
        "size": "Length: 11-13 cm, Wingspan: 18-20 cm, Weight: 11-14 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Very secretive. Sings short, insect-like song. Declining population."
    },
    "Le_Conte_Sparrow": {
        "scientific_name": "Ammospiza leconteii",
        "description": "Small sparrow with orange face, gray crown with central stripe, and buffy underparts with fine streaks.",
        "habitat": "Wet grasslands and marshes",
        "distribution": "Central North America, breeds in Canada and northern United States, winters in southeastern United States",
        "size": "Length: 11-13 cm, Wingspan: 18-20 cm, Weight: 11-15 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Very secretive. Nests on ground in wet grass."
    },
    "Lincoln_Sparrow": {
        "scientific_name": "Melospiza lincolnii",
        "description": "Small sparrow with gray face with brown crown, buffy breast with fine streaks, and brown streaked back.",
        "habitat": "Dense thickets, brushy areas, and wet meadows",
        "distribution": "North America, breeds in Canada and Alaska, winters in southern United States and Mexico",
        "size": "Length: 13-15 cm, Wingspan: 20-22 cm, Weight: 15-20 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Shy and secretive. Beautiful warbling song."
    },
    "Nelson_Sharp_tailed_Sparrow": {
        "scientific_name": "Ammospiza nelsoni",
        "description": "Small sparrow with orange face, gray crown, and buffy underparts with fine streaks.",
        "habitat": "Salt marshes and brackish wetlands",
        "distribution": "Eastern North America, breeds in Canada, winters in southeastern United States",
        "size": "Length: 12-14 cm, Wingspan: 18-20 cm, Weight: 15-20 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Very secretive. Nests on ground in marsh vegetation."
    },
    "Savannah_Sparrow": {
        "scientific_name": "Passerculus sandwichensis",
        "description": "Small sparrow with yellow eyebrow, streaked brown back, and white underparts with streaks.",
        "habitat": "Grasslands, fields, and open areas",
        "distribution": "North America, breeds in Canada and northern United States, winters in southern United States and Mexico",
        "size": "Length: 11-17 cm, Wingspan: 18-20 cm, Weight: 15-28 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Nests on ground. Common in open habitats."
    },
    # 第三批：20種鳥類
    "Seaside_Sparrow": {
        "scientific_name": "Ammospiza maritima",
        "description": "Medium-sized sparrow with gray head, olive back, and white underparts with dark streaks.",
        "habitat": "Salt marshes and coastal wetlands",
        "distribution": "Eastern and Gulf coasts of United States",
        "size": "Length: 13-15 cm, Wingspan: 20-22 cm, Weight: 18-25 g",
        "diet": "Insects, small crustaceans, and seeds",
        "behavior": "Year-round resident in many areas. Nests in marsh vegetation. Very secretive."
    },
    "Song_Sparrow": {
        "scientific_name": "Melospiza melodia",
        "description": "Medium-sized sparrow with streaked brown back, white underparts with dark central spot, and brown streaks.",
        "habitat": "Thickets, brushy areas, gardens, and parks",
        "distribution": "North America, from Alaska to Mexico",
        "size": "Length: 12-17 cm, Wingspan: 20-24 cm, Weight: 18-25 g",
        "diet": "Seeds, grains, and insects",
        "behavior": "Year-round resident in many areas. Beautiful, complex song. Visits bird feeders."
    },
    "Tree_Sparrow": {
        "scientific_name": "Spizelloides arborea",
        "description": "Small sparrow with rufous crown, gray face with dark spot, and brown streaked back.",
        "habitat": "Open woodlands, fields, and gardens",
        "distribution": "North America, breeds in Canada and Alaska, winters in central United States",
        "size": "Length: 14-16 cm, Wingspan: 22-24 cm, Weight: 18-26 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Visits bird feeders. Forms flocks in winter."
    },
    "Vesper_Sparrow": {
        "scientific_name": "Pooecetes gramineus",
        "description": "Medium-sized sparrow with streaked brown back, white outer tail feathers, and white eye ring.",
        "habitat": "Grasslands, fields, and open areas",
        "distribution": "North America, breeds in Canada and United States, winters in southern United States and Mexico",
        "size": "Length: 14-17 cm, Wingspan: 23-25 cm, Weight: 20-28 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Sings beautiful song, especially at dusk. Nests on ground."
    },
    "White_crowned_Sparrow": {
        "scientific_name": "Zonotrichia leucophrys",
        "description": "Large sparrow with black and white striped crown, gray face, and brown streaked back.",
        "habitat": "Brushy areas, woodlands, and gardens",
        "distribution": "North America, breeds in Canada and Alaska, winters in United States and Mexico",
        "size": "Length: 15-19 cm, Wingspan: 24-26 cm, Weight: 25-28 g",
        "diet": "Seeds, grains, and insects",
        "behavior": "Migratory. Visits bird feeders. Beautiful whistled song."
    },
    "White_throated_Sparrow": {
        "scientific_name": "Zonotrichia albicollis",
        "description": "Large sparrow with black and white striped crown, white throat, and yellow spot between eye and bill.",
        "habitat": "Woodlands, brushy areas, and gardens",
        "distribution": "North America, breeds in Canada, winters in United States",
        "size": "Length: 16-18 cm, Wingspan: 23-25 cm, Weight: 22-32 g",
        "diet": "Seeds, fruits, and insects",
        "behavior": "Migratory. Visits bird feeders. Sings 'Old Sam Peabody' song."
    },
    "Baird_Sparrow": {
        "scientific_name": "Centronyx bairdii",
        "description": "Small sparrow with streaked brown back, buffy underparts with fine streaks, and central crown stripe.",
        "habitat": "Native grasslands and prairies",
        "distribution": "Central North America, breeds in Canada and northern United States, winters in southwestern United States and Mexico",
        "size": "Length: 12-14 cm, Wingspan: 20-22 cm, Weight: 15-20 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Very secretive. Nests on ground in grass."
    },
    "Black_throated_Sparrow": {
        "scientific_name": "Amphispiza bilineata",
        "description": "Small sparrow with black throat, white eyebrow, and gray body.",
        "habitat": "Desert scrub, arid grasslands, and rocky areas",
        "distribution": "Southwestern United States and Mexico",
        "size": "Length: 12-14 cm, Wingspan: 20-22 cm, Weight: 11-15 g",
        "diet": "Seeds and insects",
        "behavior": "Year-round resident in many areas. Nests in shrubs or on ground."
    },
    "Mallard": {
        "scientific_name": "Anas platyrhynchos",
        "description": "Large dabbling duck. Males have green head, yellow bill, brown breast, and gray body. Females are mottled brown.",
        "habitat": "Wetlands, ponds, lakes, and rivers",
        "distribution": "Worldwide, native to Northern Hemisphere",
        "size": "Length: 50-65 cm, Wingspan: 81-98 cm, Weight: 0.7-1.6 kg",
        "diet": "Aquatic plants, seeds, insects, and small aquatic animals",
        "behavior": "Dabbling duck, tips up to feed. Migratory in northern range. Common in urban parks."
    },
    "Gadwall": {
        "scientific_name": "Mareca strepera",
        "description": "Medium-sized dabbling duck. Males are gray with black rear, white speculum. Females are mottled brown.",
        "habitat": "Wetlands, marshes, and shallow lakes",
        "distribution": "North America, Europe, and Asia",
        "size": "Length: 46-56 cm, Wingspan: 78-90 cm, Weight: 0.5-1.1 kg",
        "diet": "Aquatic plants, seeds, and small invertebrates",
        "behavior": "Dabbling duck. Migratory. Forms flocks in winter."
    },
    "Ruby_throated_Hummingbird": {
        "scientific_name": "Archilochus colubris",
        "description": "Small hummingbird. Males have iridescent red throat, green back, and white underparts. Females lack red throat.",
        "habitat": "Forests, gardens, parks, and meadows with flowers",
        "distribution": "Eastern North America, breeds in United States and Canada, winters in Central America",
        "size": "Length: 7-9 cm, Wingspan: 8-11 cm, Weight: 2-6 g",
        "diet": "Nectar from flowers, small insects, and tree sap",
        "behavior": "Migratory. Only hummingbird in eastern North America. Can hover and fly backwards. Aggressive at feeders."
    },
    "Rufous_Hummingbird": {
        "scientific_name": "Selasphorus rufus",
        "description": "Small hummingbird. Males are rufous (reddish-brown) overall with iridescent red throat. Females are green above, rufous below.",
        "habitat": "Forests, meadows, and gardens with flowers",
        "distribution": "Western North America, breeds in Alaska and Canada, winters in Mexico",
        "size": "Length: 7-9 cm, Wingspan: 11 cm, Weight: 2-5 g",
        "diet": "Nectar from flowers and small insects",
        "behavior": "Long-distance migrant. Very aggressive. Defends feeding territories."
    },
    "Dark_eyed_Junco": {
        "scientific_name": "Junco hyemalis",
        "description": "Medium-sized sparrow. Slate-gray or brown above, white below, with pink bill. Several color variations.",
        "habitat": "Woodlands, forests, parks, and gardens",
        "distribution": "North America, breeds in Canada and Alaska, winters throughout United States",
        "size": "Length: 13-17 cm, Wingspan: 18-25 cm, Weight: 18-30 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Visits bird feeders. Forms flocks in winter. Nests on ground."
    },
    "Mockingbird": {
        "scientific_name": "Mimus polyglottos",
        "description": "Medium-sized songbird. Gray above, white below, with white wing patches and long tail.",
        "habitat": "Open woodlands, parks, gardens, and suburban areas",
        "distribution": "North America, from Canada to Mexico and Caribbean",
        "size": "Length: 20-28 cm, Wingspan: 31-38 cm, Weight: 40-58 g",
        "diet": "Fruits, berries, and insects",
        "behavior": "Excellent mimic, imitates other birds and sounds. Year-round resident in many areas. Defends territory aggressively."
    },
    "Brown_Thrasher": {
        "scientific_name": "Toxostoma rufum",
        "description": "Large songbird with reddish-brown upperparts, streaked white underparts, long tail, and curved bill.",
        "habitat": "Dense thickets, brushy areas, and woodland edges",
        "distribution": "Eastern and central North America",
        "size": "Length: 23-30 cm, Wingspan: 29-33 cm, Weight: 61-89 g",
        "diet": "Insects, fruits, and berries",
        "behavior": "Mimics other birds. Skulks in dense vegetation. Year-round resident in south."
    },
    "Sage_Thrasher": {
        "scientific_name": "Oreoscoptes montanus",
        "description": "Medium-sized songbird with gray-brown upperparts, white underparts with dark streaks, and long tail.",
        "habitat": "Sagebrush and arid shrublands",
        "distribution": "Western North America, breeds in western United States, winters in southwestern United States and Mexico",
        "size": "Length: 20-23 cm, Wingspan: 28-32 cm, Weight: 35-50 g",
        "diet": "Insects, fruits, and berries",
        "behavior": "Migratory. Sings beautiful song. Nests in sagebrush."
    },
    "Scarlet_Tanager": {
        "scientific_name": "Piranga olivacea",
        "description": "Medium-sized songbird. Breeding males are bright red with black wings and tail. Females are olive-yellow.",
        "habitat": "Mature deciduous forests",
        "distribution": "Eastern North America, breeds in United States and Canada, winters in South America",
        "size": "Length: 16-19 cm, Wingspan: 25-29 cm, Weight: 23-38 g",
        "diet": "Insects, fruits, and berries",
        "behavior": "Migratory. Sings robin-like song. Nests high in trees."
    },
    "Summer_Tanager": {
        "scientific_name": "Piranga rubra",
        "description": "Medium-sized songbird. Males are entirely red. Females are olive-yellow with orange tinges.",
        "habitat": "Open woodlands, parks, and gardens",
        "distribution": "Southern and eastern United States, winters in Central and South America",
        "size": "Length: 17-19 cm, Wingspan: 28-30 cm, Weight: 29-38 g",
        "diet": "Insects, especially bees and wasps, fruits, and berries",
        "behavior": "Migratory. Catches bees and wasps in flight. Nests in trees."
    },
    "Baltimore_Oriole": {
        "scientific_name": "Icterus galbula",
        "description": "Medium-sized songbird. Males are bright orange with black head, back, and wings. Females are orange-yellow with dark wings.",
        "habitat": "Open woodlands, parks, and gardens",
        "distribution": "Eastern and central North America, winters in Central America and northern South America",
        "size": "Length: 17-22 cm, Wingspan: 23-30 cm, Weight: 30-40 g",
        "diet": "Insects, fruits, and nectar",
        "behavior": "Migratory. Builds hanging pouch nests. Visits feeders for oranges and jelly."
    },
    "Orchard_Oriole": {
        "scientific_name": "Icterus spurius",
        "description": "Small oriole. Males are dark chestnut with black head and throat. Females are olive-yellow with dark wings.",
        "habitat": "Open woodlands, orchards, and parks",
        "distribution": "Eastern and central North America, winters in Central America and northern South America",
        "size": "Length: 15-18 cm, Wingspan: 25 cm, Weight: 16-28 g",
        "diet": "Insects, fruits, and nectar",
        "behavior": "Migratory. Builds hanging nests. Arrives later than Baltimore Oriole."
    },
    "Hooded_Oriole": {
        "scientific_name": "Icterus cucullatus",
        "description": "Medium-sized oriole. Males are orange-yellow with black face, throat, and back. Females are yellow-olive.",
        "habitat": "Open woodlands, parks, and gardens, especially with palms",
        "distribution": "Southwestern United States and Mexico",
        "size": "Length: 18-20 cm, Wingspan: 25-28 cm, Weight: 24-36 g",
        "diet": "Insects, fruits, and nectar",
        "behavior": "Migratory in northern range. Builds hanging nests, often in palm trees."
    },
    "Scott_Oriole": {
        "scientific_name": "Icterus parisorum",
        "description": "Medium-sized oriole. Males are black with yellow head, breast, and rump. Females are olive-yellow.",
        "habitat": "Desert scrub, open woodlands, and yucca stands",
        "distribution": "Southwestern United States and Mexico",
        "size": "Length: 20-23 cm, Wingspan: 30-32 cm, Weight: 30-40 g",
        "diet": "Insects, fruits, and nectar",
        "behavior": "Migratory. Builds hanging nests in yucca or trees."
    },
    # 第四批：20種鳥類
    "Ovenbird": {
        "scientific_name": "Seiurus aurocapilla",
        "description": "Large warbler with olive-brown upperparts, white underparts with dark streaks, and orange crown stripe.",
        "habitat": "Mature deciduous and mixed forests",
        "distribution": "Eastern North America, breeds in United States and Canada, winters in Central America and Caribbean",
        "size": "Length: 11-16 cm, Wingspan: 19-26 cm, Weight: 16-28 g",
        "diet": "Insects, spiders, and small invertebrates",
        "behavior": "Migratory. Walks on forest floor. Builds domed nest on ground."
    },
    "Common_Yellowthroat": {
        "scientific_name": "Geothlypis trichas",
        "description": "Small warbler. Males have black mask, yellow throat, and olive back. Females lack mask.",
        "habitat": "Marshes, wetlands, and dense vegetation",
        "distribution": "North America, breeds throughout United States and Canada, winters in southern United States, Mexico, and Central America",
        "size": "Length: 11-14 cm, Wingspan: 15-19 cm, Weight: 8-11 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Skulks in dense vegetation. Sings 'wichity-wichity' song."
    },
    "Yellow_Warbler": {
        "scientific_name": "Setophaga petechia",
        "description": "Small warbler. Males are bright yellow with reddish streaks on breast. Females are duller yellow.",
        "habitat": "Wetlands, shrublands, and open woodlands",
        "distribution": "North America, breeds in United States and Canada, winters in Central and South America",
        "size": "Length: 12-13 cm, Wingspan: 16-20 cm, Weight: 7-16 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Sings sweet 'sweet-sweet-sweet' song. Nests in shrubs or trees."
    },
    "Chestnut_sided_Warbler": {
        "scientific_name": "Setophaga pensylvanica",
        "description": "Small warbler. Breeding males have yellow crown, black face, white underparts, and chestnut sides. Females are duller.",
        "habitat": "Second-growth forests, shrublands, and woodland edges",
        "distribution": "Eastern North America, breeds in United States and Canada, winters in Central America",
        "size": "Length: 11-13 cm, Wingspan: 19-21 cm, Weight: 8-13 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Active forager. Nests low in shrubs."
    },
    "Magnolia_Warbler": {
        "scientific_name": "Setophaga magnolia",
        "description": "Small warbler. Breeding males have black back with white wing bars, yellow underparts with black streaks, and white tail patches.",
        "habitat": "Coniferous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in Central America and Caribbean",
        "size": "Length: 11-13 cm, Wingspan: 16-20 cm, Weight: 6-12 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Active forager. Nests in coniferous trees."
    },
    "Cape_May_Warbler": {
        "scientific_name": "Setophaga tigrina",
        "description": "Small warbler. Breeding males have yellow head with chestnut cheek patch, streaked yellow underparts, and white wing patches.",
        "habitat": "Coniferous forests, especially spruce",
        "distribution": "North America, breeds in Canada and northern United States, winters in Caribbean",
        "size": "Length: 12-13 cm, Wingspan: 20-22 cm, Weight: 9-17 g",
        "diet": "Insects, especially spruce budworms, and nectar",
        "behavior": "Migratory. Sips nectar from flowers. Nests high in spruce trees."
    },
    "Black_throated_Blue_Warbler": {
        "scientific_name": "Setophaga caerulescens",
        "description": "Small warbler. Males are blue above with black face and throat, white underparts. Females are olive with white wing spot.",
        "habitat": "Mature deciduous and mixed forests",
        "distribution": "Eastern North America, breeds in United States and Canada, winters in Caribbean",
        "size": "Length: 12-13 cm, Wingspan: 18-20 cm, Weight: 8-12 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Forages in lower to mid-levels of trees. Nests low in shrubs."
    },
    "Myrtle_Warbler": {
        "scientific_name": "Setophaga coronata",
        "description": "Small warbler. Breeding males have yellow rump, yellow crown patch, white throat, and streaked sides.",
        "habitat": "Coniferous and mixed forests",
        "distribution": "North America, breeds in Canada and Alaska, winters in United States, Mexico, and Central America",
        "size": "Length: 12-15 cm, Wingspan: 19-24 cm, Weight: 12-15 g",
        "diet": "Insects, fruits, and berries",
        "behavior": "Migratory. Visits feeders for suet. Forms large flocks in winter."
    },
    "Black_and_white_Warbler": {
        "scientific_name": "Mniotilta varia",
        "description": "Small warbler with black and white striped plumage, resembling a zebra. Creeps along tree trunks.",
        "habitat": "Mature deciduous and mixed forests",
        "distribution": "Eastern and central North America, breeds in United States and Canada, winters in Central America and Caribbean",
        "size": "Length: 11-13 cm, Wingspan: 18-22 cm, Weight: 8-15 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Creeps along tree trunks like a nuthatch. Nests on ground."
    },
    "American_Redstart": {
        "scientific_name": "Setophaga ruticilla",
        "description": "Small warbler. Males are black with orange patches on wings, tail, and sides. Females are gray with yellow patches.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "North America, breeds in United States and Canada, winters in Central America, Caribbean, and northern South America",
        "size": "Length: 11-14 cm, Wingspan: 16-23 cm, Weight: 6-9 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Active, flits wings and tail. Nests in trees."
    },
    "Pine_Warbler": {
        "scientific_name": "Setophaga pinus",
        "description": "Small warbler with olive-yellow upperparts, yellow underparts with faint streaks, and white wing bars.",
        "habitat": "Pine forests and mixed woodlands",
        "distribution": "Eastern and southeastern United States, year-round resident in many areas",
        "size": "Length: 12-14 cm, Wingspan: 20-23 cm, Weight: 9-15 g",
        "diet": "Insects, seeds, and berries",
        "behavior": "Year-round resident in many areas. Visits feeders for suet. Nests in pine trees."
    },
    "Palm_Warbler": {
        "scientific_name": "Setophaga palmarum",
        "description": "Small warbler with brown cap, yellow underparts with streaks, and constantly bobs tail.",
        "habitat": "Bogs, open woodlands, and scrublands",
        "distribution": "North America, breeds in Canada, winters in southeastern United States, Caribbean, and Central America",
        "size": "Length: 12-14 cm, Wingspan: 20-22 cm, Weight: 9-14 g",
        "diet": "Insects and berries",
        "behavior": "Migratory. Constantly bobs tail. Forages on ground."
    },
    "Bay_breasted_Warbler": {
        "scientific_name": "Setophaga castanea",
        "description": "Small warbler. Breeding males have chestnut crown and sides, black face, and yellow nape.",
        "habitat": "Coniferous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in Central and South America",
        "size": "Length: 12-14 cm, Wingspan: 20-22 cm, Weight: 10-15 g",
        "diet": "Insects, especially spruce budworms",
        "behavior": "Migratory. Forages in tree canopy. Nests in coniferous trees."
    },
    "Black_capped_Vireo": {
        "scientific_name": "Vireo atricapilla",
        "description": "Small vireo with black cap, white eye ring, and olive-yellow body.",
        "habitat": "Oak scrub and brushy areas",
        "distribution": "South-central United States and northern Mexico",
        "size": "Length: 11-12 cm, Wingspan: 18-19 cm, Weight: 8-11 g",
        "diet": "Insects and small fruits",
        "behavior": "Migratory. Endangered species. Nests in shrubs."
    },
    "Red_eyed_Vireo": {
        "scientific_name": "Vireo olivaceus",
        "description": "Medium-sized vireo with olive-green upperparts, white underparts, gray crown, and red eyes.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "North America, breeds in United States and Canada, winters in South America",
        "size": "Length: 12-14 cm, Wingspan: 23-25 cm, Weight: 12-26 g",
        "diet": "Insects and small fruits",
        "behavior": "Migratory. Sings continuously. Nests in trees."
    },
    "Warbling_Vireo": {
        "scientific_name": "Vireo gilvus",
        "description": "Small vireo with gray head, olive back, white underparts, and faint eye stripe.",
        "habitat": "Deciduous woodlands, parks, and gardens",
        "distribution": "North America, breeds in United States and Canada, winters in Mexico and Central America",
        "size": "Length: 12-14 cm, Wingspan: 20-22 cm, Weight: 10-16 g",
        "diet": "Insects and small fruits",
        "behavior": "Migratory. Sings warbling song. Nests in trees."
    },
    "White_eyed_Vireo": {
        "scientific_name": "Vireo griseus",
        "description": "Small vireo with gray head, yellow spectacles, white eyes, and olive-yellow body.",
        "habitat": "Dense thickets and brushy areas",
        "distribution": "Eastern and central United States, winters in southeastern United States, Mexico, and Central America",
        "size": "Length: 11-13 cm, Wingspan: 18-20 cm, Weight: 10-14 g",
        "diet": "Insects and small fruits",
        "behavior": "Migratory in northern range. Skulks in dense vegetation. Nests in shrubs."
    },
    "Blue_headed_Vireo": {
        "scientific_name": "Vireo solitarius",
        "description": "Small vireo with blue-gray head, white spectacles, olive back, and yellow sides.",
        "habitat": "Coniferous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in southeastern United States, Mexico, and Central America",
        "size": "Length: 12-14 cm, Wingspan: 20-22 cm, Weight: 12-18 g",
        "diet": "Insects and small fruits",
        "behavior": "Migratory. Forages methodically. Nests in trees."
    },
    "Yellow_throated_Vireo": {
        "scientific_name": "Vireo flavifrons",
        "description": "Medium-sized vireo with yellow throat and breast, gray head, and olive back.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "Eastern and central North America, breeds in United States, winters in Central America and Caribbean",
        "size": "Length: 13-14 cm, Wingspan: 23-25 cm, Weight: 16-21 g",
        "diet": "Insects and small fruits",
        "behavior": "Migratory. Sings slow, deliberate song. Nests high in trees."
    },
    "Cedar_Waxwing": {
        "scientific_name": "Bombycilla cedrorum",
        "description": "Medium-sized songbird with sleek brown body, yellow-tipped tail, red waxy wing tips, and black mask.",
        "habitat": "Open woodlands, parks, and gardens with fruit trees",
        "distribution": "North America, breeds in Canada and northern United States, winters throughout United States and Mexico",
        "size": "Length: 14-17 cm, Wingspan: 22-30 cm, Weight: 30-40 g",
        "diet": "Fruits, berries, and insects",
        "behavior": "Social, forms large flocks. Visits berry trees. Passes berries to each other."
    },
    "Bohemian_Waxwing": {
        "scientific_name": "Bombycilla garrulus",
        "description": "Medium-sized songbird similar to Cedar Waxwing but larger, with gray belly and white wing patches.",
        "habitat": "Coniferous forests and open areas with fruit trees",
        "distribution": "Northern North America, breeds in Alaska and Canada, winters in northern United States",
        "size": "Length: 19-21 cm, Wingspan: 32-35 cm, Weight: 50-60 g",
        "diet": "Fruits, berries, and insects",
        "behavior": "Irruptive migrant. Forms large flocks. Visits berry trees."
    },
    # 第五批：20種鳥類
    "Downy_Woodpecker": {
        "scientific_name": "Picoides pubescens",
        "description": "Small woodpecker with black and white plumage, white back, and small bill. Males have red nape patch.",
        "habitat": "Woodlands, parks, and gardens",
        "distribution": "North America, from Alaska to Mexico",
        "size": "Length: 14-18 cm, Wingspan: 25-30 cm, Weight: 20-33 g",
        "diet": "Insects, seeds, and suet",
        "behavior": "Year-round resident. Visits bird feeders. Drums on trees. Nests in tree cavities."
    },
    "Red_bellied_Woodpecker": {
        "scientific_name": "Melanerpes carolinus",
        "description": "Medium-sized woodpecker with black and white barred back, red cap and nape, and pale belly.",
        "habitat": "Deciduous and mixed forests, parks, and gardens",
        "distribution": "Eastern and central United States, year-round resident",
        "size": "Length: 22-26 cm, Wingspan: 38-46 cm, Weight: 56-91 g",
        "diet": "Insects, fruits, nuts, and seeds",
        "behavior": "Year-round resident. Visits bird feeders. Stores food in bark crevices."
    },
    "Red_headed_Woodpecker": {
        "scientific_name": "Melanerpes erythrocephalus",
        "description": "Medium-sized woodpecker with entirely red head, black and white body, and white wing patches.",
        "habitat": "Open woodlands, parks, and areas with dead trees",
        "distribution": "Eastern and central North America",
        "size": "Length: 19-23 cm, Wingspan: 42 cm, Weight: 56-97 g",
        "diet": "Insects, fruits, nuts, and seeds",
        "behavior": "Stores food in tree cavities. Declining population. Nests in dead trees."
    },
    "Pileated_Woodpecker": {
        "scientific_name": "Dryocopus pileatus",
        "description": "Very large woodpecker with black body, white stripes on face, and red crest. Males have red mustache.",
        "habitat": "Mature forests with large trees",
        "distribution": "North America, from Canada to southeastern United States",
        "size": "Length: 40-49 cm, Wingspan: 66-75 cm, Weight: 250-350 g",
        "diet": "Carpenter ants, wood-boring beetles, fruits, and nuts",
        "behavior": "Year-round resident. Creates large rectangular holes in trees. Loud call."
    },
    "American_Three_toed_Woodpecker": {
        "scientific_name": "Picoides dorsalis",
        "description": "Medium-sized woodpecker with black and white barred back, yellow crown patch (males), and three toes.",
        "habitat": "Coniferous forests, especially burned areas",
        "distribution": "North America, breeds in Canada and Alaska, winters in northern United States",
        "size": "Length: 20-23 cm, Wingspan: 35-38 cm, Weight: 50-70 g",
        "diet": "Bark beetles and other wood-boring insects",
        "behavior": "Year-round resident in many areas. Forages on dead and dying trees."
    },
    "Red_cockaded_Woodpecker": {
        "scientific_name": "Leuconotopicus borealis",
        "description": "Medium-sized woodpecker with black and white barred back, white cheek patches, and small red spot on head (males).",
        "habitat": "Mature pine forests",
        "distribution": "Southeastern United States",
        "size": "Length: 18-23 cm, Wingspan: 35-41 cm, Weight: 40-50 g",
        "diet": "Insects, especially ants and beetles",
        "behavior": "Endangered species. Cooperative breeder. Nests in living pine trees."
    },
    "Belted_Kingfisher": {
        "scientific_name": "Megaceryle alcyon",
        "description": "Large kingfisher with blue-gray upperparts, white underparts, and shaggy crest. Females have rufous belly band.",
        "habitat": "Rivers, lakes, ponds, and coastal areas",
        "distribution": "North America, breeds throughout United States and Canada, winters in southern United States, Mexico, and Central America",
        "size": "Length: 28-35 cm, Wingspan: 48-58 cm, Weight: 140-170 g",
        "diet": "Fish, crayfish, and other aquatic animals",
        "behavior": "Dives for fish. Hovers over water. Nests in burrows in banks. Loud rattling call."
    },
    "Common_Raven": {
        "scientific_name": "Corvus corax",
        "description": "Very large, all-black bird with thick bill, shaggy throat feathers, and wedge-shaped tail.",
        "habitat": "Various habitats including forests, mountains, deserts, and urban areas",
        "distribution": "Throughout Northern Hemisphere",
        "size": "Length: 56-69 cm, Wingspan: 115-130 cm, Weight: 0.7-2.0 kg",
        "diet": "Omnivorous. Eats carrion, small animals, eggs, fruits, and human food waste.",
        "behavior": "Highly intelligent. Uses tools. Forms pairs. Acrobatic flight displays."
    },
    "White_breasted_Nuthatch": {
        "scientific_name": "Sitta carolinensis",
        "description": "Medium-sized nuthatch with blue-gray upperparts, white face and underparts, and black cap.",
        "habitat": "Deciduous and mixed forests, parks, and gardens",
        "distribution": "North America, from Canada to Mexico",
        "size": "Length: 13-14 cm, Wingspan: 20-27 cm, Weight: 18-30 g",
        "diet": "Insects, seeds, and nuts",
        "behavior": "Year-round resident. Climbs down tree trunks headfirst. Visits bird feeders. Stores food."
    },
    "Brown_Pelican": {
        "scientific_name": "Pelecanus occidentalis",
        "description": "Large seabird with brown body, white head and neck, and huge bill with expandable pouch.",
        "habitat": "Coastal waters, bays, and estuaries",
        "distribution": "Coasts of North and South America, from Canada to Chile",
        "size": "Length: 106-137 cm, Wingspan: 200-228 cm, Weight: 2.7-5.0 kg",
        "diet": "Fish, caught by diving from air",
        "behavior": "Dives from air to catch fish. Forms colonies. Nests on ground or in trees."
    },
    "White_Pelican": {
        "scientific_name": "Pelecanus erythrorhynchos",
        "description": "Very large white bird with black wing tips, huge bill, and expandable pouch.",
        "habitat": "Lakes, rivers, and wetlands",
        "distribution": "North America, breeds in Canada and northern United States, winters in southern United States and Mexico",
        "size": "Length: 127-165 cm, Wingspan: 244-290 cm, Weight: 5-9 kg",
        "diet": "Fish, caught by cooperative fishing",
        "behavior": "Migratory. Forms large flocks. Cooperative fishing. Nests in colonies on islands."
    },
    "Eared_Grebe": {
        "scientific_name": "Podiceps nigricollis",
        "description": "Small grebe with black head and neck, golden ear tufts in breeding season, and red eyes.",
        "habitat": "Lakes, ponds, and marshes",
        "distribution": "North America, breeds in western United States and Canada, winters in southwestern United States and Mexico",
        "size": "Length: 28-34 cm, Wingspan: 55-60 cm, Weight: 250-400 g",
        "diet": "Aquatic insects, small fish, and crustaceans",
        "behavior": "Migratory. Excellent diver. Forms large flocks in winter."
    },
    "Horned_Grebe": {
        "scientific_name": "Podiceps auritus",
        "description": "Small grebe with black head, golden ear tufts, red eyes, and chestnut neck in breeding season.",
        "habitat": "Lakes, ponds, and coastal waters",
        "distribution": "North America, breeds in Canada and Alaska, winters in coastal United States",
        "size": "Length: 31-38 cm, Wingspan: 55-60 cm, Weight: 300-570 g",
        "diet": "Aquatic insects, small fish, and crustaceans",
        "behavior": "Migratory. Excellent diver. Nests on floating vegetation."
    },
    "Pied_billed_Grebe": {
        "scientific_name": "Podilymbus podiceps",
        "description": "Small grebe with brown body, black ring around bill in breeding season, and short tail.",
        "habitat": "Freshwater lakes, ponds, and marshes",
        "distribution": "North and South America",
        "size": "Length: 30-38 cm, Wingspan: 45-55 cm, Weight: 250-600 g",
        "diet": "Aquatic insects, small fish, and crustaceans",
        "behavior": "Year-round resident in many areas. Excellent diver. Builds floating nest."
    },
    "Western_Grebe": {
        "scientific_name": "Aechmophorus occidentalis",
        "description": "Large grebe with long neck, black cap, white face and neck, and red eyes.",
        "habitat": "Large lakes and coastal waters",
        "distribution": "Western North America, breeds in western United States and Canada, winters along Pacific Coast",
        "size": "Length: 55-75 cm, Wingspan: 79-102 cm, Weight: 800-1800 g",
        "diet": "Fish and aquatic invertebrates",
        "behavior": "Migratory. Performs elaborate courtship displays. Nests in colonies."
    },
    "Boat_tailed_Grackle": {
        "scientific_name": "Quiscalus major",
        "description": "Large blackbird with long tail, iridescent black plumage, and yellow eyes.",
        "habitat": "Coastal marshes, wetlands, and urban areas",
        "distribution": "Southeastern United States, year-round resident",
        "size": "Length: 37-43 cm, Wingspan: 39-50 cm, Weight: 165-250 g",
        "diet": "Insects, seeds, grains, and human food scraps",
        "behavior": "Year-round resident. Forms large flocks. Nests in colonies."
    },
    "California_Gull": {
        "scientific_name": "Larus californicus",
        "description": "Medium-sized gull with white head and body, gray back, yellow bill with black and red spots, and yellow legs.",
        "habitat": "Lakes, rivers, coastal areas, and landfills",
        "distribution": "Western North America, breeds in interior, winters along Pacific Coast",
        "size": "Length: 46-55 cm, Wingspan: 122-140 cm, Weight: 430-1045 g",
        "diet": "Fish, insects, eggs, and human food waste",
        "behavior": "Migratory. Forms large flocks. Nests in colonies."
    },
    "Herring_Gull": {
        "scientific_name": "Larus argentatus",
        "description": "Large gull with white head and body, gray back, yellow bill with red spot, and pink legs.",
        "habitat": "Coastal areas, lakes, and urban areas",
        "distribution": "North America, Europe, and Asia",
        "size": "Length: 55-66 cm, Wingspan: 125-155 cm, Weight: 0.7-1.5 kg",
        "diet": "Fish, invertebrates, eggs, and human food waste",
        "behavior": "Opportunistic feeder. Forms large flocks. Nests in colonies."
    },
    "Ring_billed_Gull": {
        "scientific_name": "Larus delawarensis",
        "description": "Medium-sized gull with white head and body, gray back, yellow bill with black ring, and yellow legs.",
        "habitat": "Lakes, rivers, coastal areas, and parking lots",
        "distribution": "North America, breeds in Canada and northern United States, winters throughout United States and Mexico",
        "size": "Length: 43-54 cm, Wingspan: 105-117 cm, Weight: 300-700 g",
        "diet": "Fish, insects, worms, and human food waste",
        "behavior": "Migratory. Common in urban areas. Visits parking lots and landfills."
    },
    "Hooded_Merganser": {
        "scientific_name": "Lophodytes cucullatus",
        "description": "Small diving duck. Males have black and white crested head, brown sides, and white breast. Females have brown crested head.",
        "habitat": "Forest lakes, ponds, and rivers",
        "distribution": "North America, breeds in Canada and northern United States, winters in southern United States and Mexico",
        "size": "Length: 40-49 cm, Wingspan: 60-66 cm, Weight: 450-880 g",
        "diet": "Small fish, aquatic insects, and crustaceans",
        "behavior": "Migratory. Dives for food. Nests in tree cavities."
    },
    "Red_breasted_Merganser": {
        "scientific_name": "Mergus serrator",
        "description": "Medium-sized diving duck. Males have dark green head, white collar, and rusty breast. Females have brown crested head.",
        "habitat": "Coastal waters, lakes, and rivers",
        "distribution": "North America, breeds in Canada and Alaska, winters along coasts of United States and Mexico",
        "size": "Length: 51-64 cm, Wingspan: 70-86 cm, Weight: 0.7-1.3 kg",
        "diet": "Fish, aquatic insects, and crustaceans",
        "behavior": "Migratory. Dives for food. Nests on ground near water."
    },
    # 第六批：20種鳥類
    "Blue_Jay": {
        "scientific_name": "Cyanocitta cristata",
        "description": "Large songbird with blue upperparts, white face and underparts, black collar, and crested head.",
        "habitat": "Deciduous and mixed forests, parks, and gardens",
        "distribution": "Eastern and central North America, year-round resident",
        "size": "Length: 28-30 cm, Wingspan: 34-43 cm, Weight: 70-100 g",
        "diet": "Nuts, seeds, fruits, insects, and eggs",
        "behavior": "Year-round resident. Intelligent, mimics other birds. Visits bird feeders. Stores food."
    },
    "Stellers_Jay": {
        "scientific_name": "Cyanocitta stelleri",
        "description": "Large songbird with dark blue and black body, crested head, and no white markings.",
        "habitat": "Coniferous and mixed forests, especially in mountains",
        "distribution": "Western North America, from Alaska to Central America",
        "size": "Length: 30-34 cm, Wingspan: 44-48 cm, Weight: 100-140 g",
        "diet": "Nuts, seeds, fruits, insects, and eggs",
        "behavior": "Year-round resident. Intelligent, mimics other birds. Stores food."
    },
    "Scrub_Jay": {
        "scientific_name": "Aphelocoma californica",
        "description": "Medium-sized jay with blue head, wings, and tail, gray back, and white throat.",
        "habitat": "Oak woodlands, scrublands, and parks",
        "distribution": "Western United States and Mexico",
        "size": "Length: 27-31 cm, Wingspan: 39 cm, Weight: 70-100 g",
        "diet": "Nuts, seeds, fruits, insects, and eggs",
        "behavior": "Year-round resident. Stores acorns. Intelligent."
    },
    "Green_Jay": {
        "scientific_name": "Cyanocorax yncas",
        "description": "Medium-sized jay with green upperparts, yellow underparts, blue head, and black throat.",
        "habitat": "Tropical and subtropical woodlands",
        "distribution": "Southern Texas, Mexico, and Central America",
        "size": "Length: 25-27 cm, Wingspan: 35-38 cm, Weight: 66-110 g",
        "diet": "Fruits, insects, and small vertebrates",
        "behavior": "Year-round resident. Social, forms groups. Intelligent."
    },
    "Blue_Grosbeak": {
        "scientific_name": "Passerina caerulea",
        "description": "Medium-sized songbird. Males are deep blue with chestnut wing bars. Females are brown with blue tinges.",
        "habitat": "Brushy areas, open woodlands, and fields",
        "distribution": "Southern and central United States, winters in Mexico and Central America",
        "size": "Length: 14-19 cm, Wingspan: 26-29 cm, Weight: 26-31 g",
        "diet": "Seeds, insects, and fruits",
        "behavior": "Migratory. Sings beautiful song. Nests in shrubs."
    },
    "Evening_Grosbeak": {
        "scientific_name": "Coccothraustes vespertinus",
        "description": "Large finch. Males are yellow with black head, wings, and tail. Females are gray with yellow highlights.",
        "habitat": "Coniferous and mixed forests",
        "distribution": "North America, breeds in Canada and western United States, winters throughout United States",
        "size": "Length: 16-22 cm, Wingspan: 30-36 cm, Weight: 38-86 g",
        "diet": "Seeds, especially from trees, and fruits",
        "behavior": "Irruptive migrant. Visits bird feeders. Forms large flocks."
    },
    "Pine_Grosbeak": {
        "scientific_name": "Pinicola enucleator",
        "description": "Large finch. Males are rose-red with gray wings and tail. Females are gray with yellow-orange highlights.",
        "habitat": "Coniferous forests, especially in mountains",
        "distribution": "North America, breeds in Canada and Alaska, winters in northern United States",
        "size": "Length: 20-25 cm, Wingspan: 33-35 cm, Weight: 47-64 g",
        "diet": "Seeds, buds, and fruits",
        "behavior": "Irruptive migrant. Visits bird feeders. Forms flocks."
    },
    "Rose_breasted_Grosbeak": {
        "scientific_name": "Pheucticus ludovicianus",
        "description": "Medium-sized songbird. Males are black and white with rose-red breast. Females are streaked brown.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "Eastern and central North America, breeds in United States and Canada, winters in Central and South America",
        "size": "Length: 18-22 cm, Wingspan: 29-33 cm, Weight: 35-65 g",
        "diet": "Seeds, fruits, and insects",
        "behavior": "Migratory. Sings beautiful song. Visits bird feeders."
    },
    "Horned_Lark": {
        "scientific_name": "Eremophila alpestris",
        "description": "Small lark with brown upperparts, pale underparts, black face mask, and small black 'horns' on head.",
        "habitat": "Open areas, fields, grasslands, and tundra",
        "distribution": "North America, breeds in Canada and Alaska, winters throughout United States",
        "size": "Length: 15-17 cm, Wingspan: 30-35 cm, Weight: 28-48 g",
        "diet": "Seeds and insects",
        "behavior": "Migratory. Nests on ground. Sings in flight."
    },
    "Pacific_Loon": {
        "scientific_name": "Gavia pacifica",
        "description": "Large loon with black head and neck, white underparts, and gray back with white spots.",
        "habitat": "Large lakes and coastal waters",
        "distribution": "North America, breeds in Alaska and Canada, winters along Pacific Coast",
        "size": "Length: 58-73 cm, Wingspan: 110-128 cm, Weight: 1.0-2.5 kg",
        "diet": "Fish and aquatic invertebrates",
        "behavior": "Migratory. Excellent diver. Nests on lakes."
    },
    "Common_Loon": {
        "scientific_name": "Gavia immer",
        "description": "Very large loon with black head and neck, white underparts, and black and white checkered back.",
        "habitat": "Large lakes and coastal waters",
        "distribution": "North America, breeds in Canada and northern United States, winters along coasts",
        "size": "Length: 66-91 cm, Wingspan: 127-147 cm, Weight: 2.2-6.4 kg",
        "diet": "Fish and aquatic invertebrates",
        "behavior": "Migratory. Excellent diver. Famous yodeling call. Nests on lakes."
    },
    "Artic_Tern": {
        "scientific_name": "Sterna paradisaea",
        "description": "Medium-sized tern with white body, gray wings, black cap, and red bill and legs.",
        "habitat": "Coastal waters and tundra",
        "distribution": "Arctic and subarctic, breeds in northern regions, winters in Antarctic",
        "size": "Length: 33-39 cm, Wingspan: 76-85 cm, Weight: 86-127 g",
        "diet": "Small fish and marine invertebrates",
        "behavior": "Longest migration of any bird. Dives for fish. Nests in colonies on ground."
    },
    "Black_Tern": {
        "scientific_name": "Chlidonias niger",
        "description": "Small tern. Breeding adults are black with gray wings. Non-breeding adults are white with black cap.",
        "habitat": "Freshwater marshes and wetlands",
        "distribution": "North America, breeds in Canada and northern United States, winters in Central and South America",
        "size": "Length: 22-28 cm, Wingspan: 64-68 cm, Weight: 50-62 g",
        "diet": "Insects, small fish, and aquatic invertebrates",
        "behavior": "Migratory. Hovers and dives for food. Nests in marshes."
    },
    "Caspian_Tern": {
        "scientific_name": "Hydroprogne caspia",
        "description": "Very large tern with white body, gray wings, black cap, and large red bill.",
        "habitat": "Coastal waters, lakes, and rivers",
        "distribution": "Worldwide, breeds in North America, Europe, Asia, and Africa",
        "size": "Length: 48-56 cm, Wingspan: 127-140 cm, Weight: 530-782 g",
        "diet": "Fish, caught by diving",
        "behavior": "Migratory. Dives for fish. Nests in colonies."
    },
    "Common_Tern": {
        "scientific_name": "Sterna hirundo",
        "description": "Medium-sized tern with white body, gray wings, black cap, and red bill with black tip.",
        "habitat": "Coastal waters, lakes, and rivers",
        "distribution": "North America, Europe, and Asia",
        "size": "Length: 31-35 cm, Wingspan: 77-98 cm, Weight: 110-141 g",
        "diet": "Small fish and marine invertebrates",
        "behavior": "Migratory. Dives for fish. Nests in colonies on ground."
    },
    "Elegant_Tern": {
        "scientific_name": "Thalasseus elegans",
        "description": "Medium-sized tern with white body, gray wings, black cap, and long orange bill.",
        "habitat": "Coastal waters and estuaries",
        "distribution": "Pacific Coast of North America, breeds in California and Mexico, winters along Pacific Coast",
        "size": "Length: 37-41 cm, Wingspan: 89-102 cm, Weight: 200-300 g",
        "diet": "Small fish, caught by diving",
        "behavior": "Migratory. Dives for fish. Nests in large colonies."
    },
    "Forsters_Tern": {
        "scientific_name": "Sterna forsteri",
        "description": "Medium-sized tern with white body, gray wings, black cap, and orange bill with black tip.",
        "habitat": "Freshwater marshes, lakes, and coastal waters",
        "distribution": "North America, breeds in central and western United States and Canada, winters along coasts",
        "size": "Length: 33-36 cm, Wingspan: 64-70 cm, Weight: 130-190 g",
        "diet": "Small fish and aquatic invertebrates",
        "behavior": "Migratory. Dives for food. Nests in marshes."
    },
    "Least_Tern": {
        "scientific_name": "Sternula antillarum",
        "description": "Very small tern with white body, gray wings, black cap, and yellow bill with black tip.",
        "habitat": "Coastal beaches, sandbars, and riverbanks",
        "distribution": "North America, breeds along coasts and rivers, winters in Central and South America",
        "size": "Length: 22-24 cm, Wingspan: 48-53 cm, Weight: 39-52 g",
        "diet": "Small fish and aquatic invertebrates",
        "behavior": "Migratory. Endangered in some areas. Nests on ground in colonies."
    },
    "Green_tailed_Towhee": {
        "scientific_name": "Pipilo chlorurus",
        "description": "Large sparrow with green tail, rufous cap, white throat, and gray body.",
        "habitat": "Brushy areas, shrublands, and mountain slopes",
        "distribution": "Western North America, breeds in western United States, winters in southwestern United States and Mexico",
        "size": "Length: 18-21 cm, Wingspan: 25-28 cm, Weight: 29-52 g",
        "diet": "Seeds, fruits, and insects",
        "behavior": "Migratory. Forages on ground by scratching. Skulks in dense vegetation."
    },
    "Louisiana_Waterthrush": {
        "scientific_name": "Parkesia motacilla",
        "description": "Large warbler with brown upperparts, white underparts with dark streaks, and white eyebrow stripe.",
        "habitat": "Forested streams and swamps",
        "distribution": "Eastern North America, breeds in United States, winters in Central America and Caribbean",
        "size": "Length: 14-16 cm, Wingspan: 21-25 cm, Weight: 14-28 g",
        "diet": "Aquatic insects and small invertebrates",
        "behavior": "Migratory. Walks along stream banks. Nests on ground near water."
    },
    "Northern_Waterthrush": {
        "scientific_name": "Parkesia noveboracensis",
        "description": "Large warbler with brown upperparts, white underparts with dark streaks, and white eyebrow stripe.",
        "habitat": "Forested wetlands, bogs, and swamps",
        "distribution": "North America, breeds in Canada and Alaska, winters in Central America, Caribbean, and northern South America",
        "size": "Length: 12-15 cm, Wingspan: 21-24 cm, Weight: 13-25 g",
        "diet": "Aquatic insects and small invertebrates",
        "behavior": "Migratory. Walks along water edges. Constantly bobs tail. Nests on ground."
    },
    # 第七批：20種鳥類
    "Cardinal": {
        "scientific_name": "Cardinalis cardinalis",
        "description": "Medium-sized songbird. Males are bright red with black face mask and crested head. Females are brown with red tinges.",
        "habitat": "Woodlands, gardens, parks, and shrublands",
        "distribution": "Eastern and central North America, from Canada to Mexico",
        "size": "Length: 21-24 cm, Wingspan: 25-31 cm, Weight: 33-65 g",
        "diet": "Seeds, fruits, and insects",
        "behavior": "Year-round resident. Visits bird feeders. Sings beautiful song. Pairs stay together year-round."
    },
    "American_Crow": {
        "scientific_name": "Corvus brachyrhynchos",
        "description": "Large, all-black bird with thick bill and fan-shaped tail.",
        "habitat": "Various habitats including forests, fields, and urban areas",
        "distribution": "North America, from Canada to Mexico",
        "size": "Length: 40-50 cm, Wingspan: 85-100 cm, Weight: 300-600 g",
        "diet": "Omnivorous. Eats carrion, insects, fruits, seeds, and human food waste",
        "behavior": "Highly intelligent. Forms large flocks. Uses tools. Year-round resident."
    },
    "Fish_Crow": {
        "scientific_name": "Corvus ossifragus",
        "description": "Medium-sized, all-black bird similar to American Crow but smaller with higher-pitched call.",
        "habitat": "Coastal areas, rivers, and wetlands",
        "distribution": "Eastern and southeastern United States, year-round resident",
        "size": "Length: 36-40 cm, Wingspan: 75-90 cm, Weight: 200-300 g",
        "diet": "Fish, carrion, eggs, and human food waste",
        "behavior": "Year-round resident. Forms flocks. Often near water."
    },
    "Brown_Creeper": {
        "scientific_name": "Certhia americana",
        "description": "Small bird with brown mottled upperparts, white underparts, and curved bill. Climbs up tree trunks.",
        "habitat": "Mature forests, especially coniferous",
        "distribution": "North America, breeds in Canada and United States, winters throughout United States",
        "size": "Length: 12-14 cm, Wingspan: 17-20 cm, Weight: 5-10 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory in northern range. Climbs up tree trunks in spiral pattern. Nests behind loose bark."
    },
    "Black_billed_Cuckoo": {
        "scientific_name": "Coccyzus erythropthalmus",
        "description": "Medium-sized bird with brown upperparts, white underparts, and long tail with white spots.",
        "habitat": "Deciduous woodlands and thickets",
        "distribution": "Eastern and central North America, breeds in United States and Canada, winters in South America",
        "size": "Length: 28-31 cm, Wingspan: 38-42 cm, Weight: 40-65 g",
        "diet": "Caterpillars, insects, and fruits",
        "behavior": "Migratory. Secretive. Eats hairy caterpillars that other birds avoid."
    },
    "Yellow_billed_Cuckoo": {
        "scientific_name": "Coccyzus americanus",
        "description": "Medium-sized bird with brown upperparts, white underparts, and long tail with large white spots.",
        "habitat": "Deciduous woodlands, thickets, and riparian areas",
        "distribution": "North America, breeds in United States and Canada, winters in South America",
        "size": "Length: 26-30 cm, Wingspan: 38-44 cm, Weight: 55-65 g",
        "diet": "Caterpillars, insects, and fruits",
        "behavior": "Migratory. Secretive. Eats large numbers of caterpillars."
    },
    "Mangrove_Cuckoo": {
        "scientific_name": "Coccyzus minor",
        "description": "Medium-sized bird with brown upperparts, buff underparts, and long tail with white spots.",
        "habitat": "Mangrove forests and coastal thickets",
        "distribution": "Southern Florida, Caribbean, and Central America",
        "size": "Length: 28-33 cm, Wingspan: 38-42 cm, Weight: 60-80 g",
        "diet": "Insects, lizards, and fruits",
        "behavior": "Year-round resident in many areas. Secretive. Nests in trees."
    },
    "Least_Flycatcher": {
        "scientific_name": "Empidonax minimus",
        "description": "Small flycatcher with olive-gray upperparts, white underparts, and two white wing bars.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in Mexico and Central America",
        "size": "Length: 12-14 cm, Wingspan: 19-22 cm, Weight: 8-12 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Sits on perch and sallies out to catch insects. Sings 'che-bek' song."
    },
    "Olive_sided_Flycatcher": {
        "scientific_name": "Contopus cooperi",
        "description": "Large flycatcher with dark olive-gray upperparts, white underparts with dark sides, and white tufts on back.",
        "habitat": "Coniferous forests, especially burned areas",
        "distribution": "North America, breeds in Canada and western United States, winters in South America",
        "size": "Length: 18-20 cm, Wingspan: 30-33 cm, Weight: 28-40 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Sits on high perch. Sings 'quick-three-beers' song."
    },
    "Scissor_tailed_Flycatcher": {
        "scientific_name": "Tyrannus forficatus",
        "description": "Medium-sized flycatcher with gray head, white underparts, salmon-pink sides, and very long forked tail.",
        "habitat": "Open areas, grasslands, and agricultural fields",
        "distribution": "Central and southern United States, winters in Central America",
        "size": "Length: 28-38 cm (including tail), Wingspan: 38-41 cm, Weight: 30-43 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Performs aerial displays. Nests in trees or shrubs."
    },
    "Vermilion_Flycatcher": {
        "scientific_name": "Pyrocephalus rubinus",
        "description": "Small flycatcher. Males are bright red with dark brown back and wings. Females are brown with red underparts.",
        "habitat": "Open areas, grasslands, and desert scrub",
        "distribution": "Southwestern United States, Mexico, and Central and South America",
        "size": "Length: 13-14 cm, Wingspan: 25-27 cm, Weight: 11-14 g",
        "diet": "Flying insects caught in air",
        "behavior": "Year-round resident in many areas. Performs aerial displays. Nests in trees."
    },
    "Yellow_bellied_Flycatcher": {
        "scientific_name": "Empidonax flaviventris",
        "description": "Small flycatcher with olive-green upperparts, yellow underparts, and two white wing bars.",
        "habitat": "Coniferous and mixed forests, especially bogs",
        "distribution": "North America, breeds in Canada and northern United States, winters in Central America",
        "size": "Length: 13-15 cm, Wingspan: 20-23 cm, Weight: 11-14 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Secretive. Sits on low perch. Nests on ground in moss."
    },
    "Sayornis": {
        "scientific_name": "Sayornis phoebe",
        "description": "Medium-sized flycatcher with brown-gray upperparts, white underparts, and dark head.",
        "habitat": "Open areas, farms, and bridges",
        "distribution": "North America, breeds in United States and Canada, winters in southern United States and Mexico",
        "size": "Length: 16-18 cm, Wingspan: 26-28 cm, Weight: 16-21 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Nests on ledges, bridges, and buildings. Sings 'phoebe' song."
    },
    "Western_Wood_Pewee": {
        "scientific_name": "Contopus sordidulus",
        "description": "Medium-sized flycatcher with olive-gray upperparts, white underparts, and two white wing bars.",
        "habitat": "Open woodlands and forest edges",
        "distribution": "Western North America, breeds in United States and Canada, winters in South America",
        "size": "Length: 15-16 cm, Wingspan: 26-28 cm, Weight: 12-15 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Sits on perch and sallies out. Sings 'pee-wee' song."
    },
    "American_Pipit": {
        "scientific_name": "Anthus rubescens",
        "description": "Small bird with streaked brown upperparts, white underparts with streaks, and white outer tail feathers.",
        "habitat": "Open areas, tundra, fields, and shorelines",
        "distribution": "North America, breeds in Arctic, winters in United States and Mexico",
        "size": "Length: 14-17 cm, Wingspan: 22-25 cm, Weight: 18-25 g",
        "diet": "Insects and seeds",
        "behavior": "Migratory. Walks on ground. Constantly bobs tail. Nests on ground."
    },
    "Whip_poor_Will": {
        "scientific_name": "Antrostomus vociferus",
        "description": "Medium-sized nightjar with mottled brown and gray plumage, large eyes, and wide mouth.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "Eastern and central North America, breeds in United States and Canada, winters in Central America",
        "size": "Length: 22-26 cm, Wingspan: 45-48 cm, Weight: 43-64 g",
        "diet": "Flying insects caught at night",
        "behavior": "Migratory. Nocturnal. Sings 'whip-poor-will' song at night. Nests on ground."
    },
    "Nighthawk": {
        "scientific_name": "Chordeiles minor",
        "description": "Medium-sized nightjar with mottled gray and brown plumage, white wing patches, and large eyes.",
        "habitat": "Open areas, cities, and grasslands",
        "distribution": "North America, breeds throughout United States and Canada, winters in South America",
        "size": "Length: 22-25 cm, Wingspan: 55-65 cm, Weight: 55-98 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Active at dusk and dawn. Performs aerial displays. Nests on ground."
    },
    "Chuck_will_Widow": {
        "scientific_name": "Antrostomus carolinensis",
        "description": "Large nightjar with mottled brown and gray plumage, large eyes, and wide mouth.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "Southeastern United States, winters in Central America and Caribbean",
        "size": "Length: 28-33 cm, Wingspan: 58-66 cm, Weight: 65-100 g",
        "diet": "Flying insects and small birds caught at night",
        "behavior": "Migratory. Nocturnal. Sings 'chuck-will's-widow' song at night. Nests on ground."
    },
    "Horned_Puffin": {
        "scientific_name": "Fratercula corniculata",
        "description": "Medium-sized seabird with black body, white face, large colorful bill, and yellow horn-like projections above eyes.",
        "habitat": "Coastal waters and rocky islands",
        "distribution": "North Pacific, from Alaska to Japan",
        "size": "Length: 32-38 cm, Wingspan: 50-60 cm, Weight: 450-550 g",
        "diet": "Small fish and marine invertebrates",
        "behavior": "Nests in burrows on cliffs. Dives for food. Forms colonies."
    },
    "Pigeon_Guillemot": {
        "scientific_name": "Cepphus columba",
        "description": "Medium-sized seabird with black body, white wing patches, and red feet.",
        "habitat": "Coastal waters and rocky shores",
        "distribution": "North Pacific, from Alaska to California",
        "size": "Length: 30-35 cm, Wingspan: 58-63 cm, Weight: 380-620 g",
        "diet": "Small fish and marine invertebrates",
        "behavior": "Year-round resident in many areas. Dives for food. Nests in rock crevices."
    },
    "Clark_Nutcracker": {
        "scientific_name": "Nucifraga columbiana",
        "description": "Large songbird with gray body, black wings with white patches, and long pointed bill.",
        "habitat": "Coniferous forests, especially in mountains",
        "distribution": "Western North America, from Canada to Mexico",
        "size": "Length: 28-30 cm, Wingspan: 58-61 cm, Weight: 106-161 g",
        "diet": "Seeds, especially pine nuts, insects, and carrion",
        "behavior": "Year-round resident. Stores seeds. Intelligent. Nests in coniferous trees."
    },
    # 第八批：20種鳥類
    "Bewick_Wren": {
        "scientific_name": "Thryomanes bewickii",
        "description": "Small wren with brown upperparts, white underparts, and long tail with white corners.",
        "habitat": "Brushy areas, woodlands, and gardens",
        "distribution": "Western and central North America, year-round resident in many areas",
        "size": "Length: 13 cm, Wingspan: 18 cm, Weight: 8-12 g",
        "diet": "Insects and spiders",
        "behavior": "Year-round resident in many areas. Very vocal. Nests in cavities."
    },
    "Cactus_Wren": {
        "scientific_name": "Campylorhynchus brunneicapillus",
        "description": "Large wren with brown upperparts with white spots, white underparts with dark spots, and long tail.",
        "habitat": "Desert scrub and arid areas with cacti",
        "distribution": "Southwestern United States and Mexico",
        "size": "Length: 18-22 cm, Wingspan: 28-30 cm, Weight: 33-47 g",
        "diet": "Insects, fruits, and seeds",
        "behavior": "Year-round resident. Builds large domed nests in cacti. Very vocal."
    },
    "Marsh_Wren": {
        "scientific_name": "Cistothorus palustris",
        "description": "Small wren with brown upperparts with white streaks, white underparts, and short tail.",
        "habitat": "Marshes and wetlands with dense vegetation",
        "distribution": "North America, breeds in Canada and United States, winters in southern United States and Mexico",
        "size": "Length: 10-14 cm, Wingspan: 15 cm, Weight: 9-14 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory in northern range. Very vocal. Builds domed nests in marsh vegetation."
    },
    "Rock_Wren": {
        "scientific_name": "Salpinctes obsoletus",
        "description": "Medium-sized wren with gray-brown upperparts, buff underparts, and long tail.",
        "habitat": "Rocky areas, cliffs, and canyons",
        "distribution": "Western North America, from Canada to Mexico",
        "size": "Length: 14-16 cm, Wingspan: 20-22 cm, Weight: 14-18 g",
        "diet": "Insects and spiders",
        "behavior": "Year-round resident in many areas. Nests in rock crevices. Constantly bobs."
    },
    "Winter_Wren": {
        "scientific_name": "Troglodytes hiemalis",
        "description": "Very small wren with brown mottled upperparts, buff underparts, and short tail.",
        "habitat": "Dense forests, especially coniferous",
        "distribution": "North America, breeds in Canada and northern United States, winters in southern United States",
        "size": "Length: 9-10 cm, Wingspan: 13-15 cm, Weight: 8-12 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Very secretive. Sings loud, complex song. Nests in cavities."
    },
    "Canada_Warbler": {
        "scientific_name": "Cardellina canadensis",
        "description": "Small warbler with yellow underparts, gray upperparts, and black necklace on yellow breast.",
        "habitat": "Dense undergrowth in deciduous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in South America",
        "size": "Length: 12-13 cm, Wingspan: 17-20 cm, Weight: 9-13 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Active forager. Nests on ground in dense vegetation."
    },
    "Cerulean_Warbler": {
        "scientific_name": "Setophaga cerulea",
        "description": "Small warbler. Males are blue above with white underparts and black streaks. Females are blue-gray.",
        "habitat": "Mature deciduous forests",
        "distribution": "Eastern North America, breeds in United States, winters in South America",
        "size": "Length: 11-12 cm, Wingspan: 19-20 cm, Weight: 8-10 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Forages high in tree canopy. Declining population."
    },
    "Golden_winged_Warbler": {
        "scientific_name": "Vermivora chrysoptera",
        "description": "Small warbler. Males have yellow crown, black face, white wing patches, and gray body.",
        "habitat": "Shrubby areas and young forests",
        "distribution": "Eastern and central North America, breeds in United States and Canada, winters in Central and South America",
        "size": "Length: 12-13 cm, Wingspan: 19-20 cm, Weight: 8-11 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Declining population. Hybridizes with Blue-winged Warbler."
    },
    "Blue_winged_Warbler": {
        "scientific_name": "Vermivora cyanoptera",
        "description": "Small warbler. Males have yellow head and underparts, blue-gray wings with white bars, and olive back.",
        "habitat": "Shrubby areas and young forests",
        "distribution": "Eastern and central North America, breeds in United States, winters in Central America",
        "size": "Length: 11-12 cm, Wingspan: 18-19 cm, Weight: 8-11 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Hybridizes with Golden-winged Warbler. Nests on ground."
    },
    "Hooded_Warbler": {
        "scientific_name": "Setophaga citrina",
        "description": "Small warbler. Males have black hood, yellow face, and yellow underparts. Females lack hood.",
        "habitat": "Dense undergrowth in deciduous and mixed forests",
        "distribution": "Eastern North America, breeds in United States, winters in Central America and Caribbean",
        "size": "Length: 13 cm, Wingspan: 19-20 cm, Weight: 9-12 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Skulks in dense vegetation. Nests low in shrubs."
    },
    "Kentucky_Warbler": {
        "scientific_name": "Geothlypis formosa",
        "description": "Medium-sized warbler with olive upperparts, yellow underparts, black mask, and yellow spectacles.",
        "habitat": "Dense undergrowth in deciduous forests",
        "distribution": "Eastern and central United States, winters in Central America",
        "size": "Length: 13 cm, Wingspan: 20-22 cm, Weight: 11-13 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Skulks on ground. Nests on ground in dense vegetation."
    },
    "Mourning_Warbler": {
        "scientific_name": "Geothlypis philadelphia",
        "description": "Medium-sized warbler with olive upperparts, yellow underparts, and gray hood with black bib.",
        "habitat": "Dense undergrowth in deciduous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in Central and South America",
        "size": "Length: 12-14 cm, Wingspan: 19-21 cm, Weight: 11-15 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Skulks on ground. Nests on ground."
    },
    "Nashville_Warbler": {
        "scientific_name": "Leiothlypis ruficapilla",
        "description": "Small warbler with olive upperparts, yellow underparts, gray head, and white eye ring.",
        "habitat": "Coniferous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in Mexico and Central America",
        "size": "Length: 11-13 cm, Wingspan: 18-20 cm, Weight: 7-11 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Forages in trees. Nests on ground."
    },
    "Orange_crowned_Warbler": {
        "scientific_name": "Leiothlypis celata",
        "description": "Small warbler with olive-yellow upperparts, yellow underparts, and faint orange crown patch.",
        "habitat": "Shrubby areas, woodlands, and gardens",
        "distribution": "North America, breeds in Canada and western United States, winters in southern United States, Mexico, and Central America",
        "size": "Length: 12-13 cm, Wingspan: 19-21 cm, Weight: 7-11 g",
        "diet": "Insects, fruits, and nectar",
        "behavior": "Migratory. Visits feeders for suet. Nests on ground or low in shrubs."
    },
    "Prairie_Warbler": {
        "scientific_name": "Setophaga discolor",
        "description": "Small warbler with olive upperparts, yellow underparts with black streaks, and chestnut streaks on back.",
        "habitat": "Shrubby areas, pine barrens, and young forests",
        "distribution": "Eastern United States, winters in Caribbean and Central America",
        "size": "Length: 11-12 cm, Wingspan: 18-19 cm, Weight: 6-9 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Constantly bobs tail. Nests in shrubs."
    },
    "Prothonotary_Warbler": {
        "scientific_name": "Protonotaria citrea",
        "description": "Medium-sized warbler with bright yellow head and underparts, blue-gray wings, and olive back.",
        "habitat": "Forested swamps and bottomland forests",
        "distribution": "Eastern and central United States, winters in Central America and Caribbean",
        "size": "Length: 13-14 cm, Wingspan: 20-22 cm, Weight: 12-15 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Nests in tree cavities. Only eastern warbler that nests in cavities."
    },
    "Swainson_Warbler": {
        "scientific_name": "Limnothlypis swainsonii",
        "description": "Medium-sized warbler with brown upperparts, white underparts, and brown crown stripe.",
        "habitat": "Dense undergrowth in bottomland forests and swamps",
        "distribution": "Southeastern United States, winters in Caribbean and Central America",
        "size": "Length: 13-14 cm, Wingspan: 20-22 cm, Weight: 15-19 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Very secretive. Skulks on ground. Nests on ground."
    },
    "Tennessee_Warbler": {
        "scientific_name": "Leiothlypis peregrina",
        "description": "Small warbler with olive upperparts, white underparts, gray head, and white eyebrow stripe.",
        "habitat": "Coniferous and mixed forests",
        "distribution": "North America, breeds in Canada and Alaska, winters in Central and South America",
        "size": "Length: 11-13 cm, Wingspan: 19-20 cm, Weight: 8-11 g",
        "diet": "Insects, especially spruce budworms, and fruits",
        "behavior": "Migratory. Forages in trees. Nests on ground."
    },
    "Wilson_Warbler": {
        "scientific_name": "Cardellina pusilla",
        "description": "Small warbler with olive upperparts, yellow underparts, and black cap (males) or olive cap (females).",
        "habitat": "Dense undergrowth in forests and shrublands",
        "distribution": "North America, breeds in Canada and Alaska, winters in Mexico and Central America",
        "size": "Length: 10-12 cm, Wingspan: 16-18 cm, Weight: 5-10 g",
        "diet": "Insects and spiders",
        "behavior": "Migratory. Constantly flicks tail. Nests on ground."
    },
    "Worm_eating_Warbler": {
        "scientific_name": "Helmitheros vermivorum",
        "description": "Medium-sized warbler with olive upperparts, buff underparts, and black and buff striped head.",
        "habitat": "Dense undergrowth in deciduous forests",
        "distribution": "Eastern United States, winters in Caribbean and Central America",
        "size": "Length: 13 cm, Wingspan: 20-22 cm, Weight: 11-15 g",
        "diet": "Insects, especially caterpillars, and spiders",
        "behavior": "Migratory. Skulks on ground. Nests on ground in dense vegetation."
    },
    "Philadelphia_Vireo": {
        "scientific_name": "Vireo philadelphicus",
        "description": "Small vireo with olive upperparts, yellow underparts, gray head, and white eyebrow stripe.",
        "habitat": "Deciduous and mixed forests",
        "distribution": "North America, breeds in Canada and northern United States, winters in Central America",
        "size": "Length: 12-13 cm, Wingspan: 20-22 cm, Weight: 11-14 g",
        "diet": "Insects and small fruits",
        "behavior": "Migratory. Forages methodically. Nests in trees."
    },
    # 最後一批：剩餘34種鳥類
    "Brandt_Cormorant": {
        "scientific_name": "Urile penicillatus",
        "description": "Large seabird with black body, blue throat patch in breeding season, and long tail.",
        "habitat": "Coastal waters and rocky shores",
        "distribution": "Pacific Coast of North America, from Alaska to Baja California",
        "size": "Length: 81-91 cm, Wingspan: 122-137 cm, Weight: 1.4-2.5 kg",
        "diet": "Fish, caught by diving",
        "behavior": "Year-round resident. Dives for fish. Nests in colonies on cliffs."
    },
    "Red_faced_Cormorant": {
        "scientific_name": "Urile urile",
        "description": "Large seabird with black body, red face in breeding season, and white flank patches.",
        "habitat": "Coastal waters and rocky islands",
        "distribution": "North Pacific, from Alaska to Japan",
        "size": "Length: 71-79 cm, Wingspan: 110-122 cm, Weight: 1.2-2.0 kg",
        "diet": "Fish, caught by diving",
        "behavior": "Year-round resident. Dives for fish. Nests in colonies on cliffs."
    },
    "Pelagic_Cormorant": {
        "scientific_name": "Urile pelagicus",
        "description": "Medium-sized seabird with black body, white flank patches, and red face in breeding season.",
        "habitat": "Coastal waters and rocky shores",
        "distribution": "North Pacific, from Alaska to California",
        "size": "Length: 64-89 cm, Wingspan: 100-120 cm, Weight: 1.2-2.3 kg",
        "diet": "Fish, caught by diving",
        "behavior": "Year-round resident. Dives for fish. Nests in colonies on cliffs."
    },
    "Bronzed_Cowbird": {
        "scientific_name": "Molothrus aeneus",
        "description": "Medium-sized blackbird. Males are black with bronzy iridescence and red eyes. Females are brown.",
        "habitat": "Open areas, grasslands, and agricultural fields",
        "distribution": "Southwestern United States, Mexico, and Central America",
        "size": "Length: 20-23 cm, Wingspan: 32-36 cm, Weight: 50-70 g",
        "diet": "Seeds, grains, and insects",
        "behavior": "Brood parasite. Lays eggs in other birds' nests. Year-round resident in many areas."
    },
    "Shiny_Cowbird": {
        "scientific_name": "Molothrus bonariensis",
        "description": "Small blackbird. Males are black with purple-blue iridescence. Females are brown.",
        "habitat": "Open areas, grasslands, and agricultural fields",
        "distribution": "South America, introduced to Caribbean and Florida",
        "size": "Length: 18-22 cm, Wingspan: 30-35 cm, Weight: 30-50 g",
        "diet": "Seeds, grains, and insects",
        "behavior": "Brood parasite. Lays eggs in other birds' nests. Forms flocks."
    },
    "Frigatebird": {
        "scientific_name": "Fregata magnificens",
        "description": "Very large seabird with black body, long pointed wings, deeply forked tail, and red throat pouch (males).",
        "habitat": "Tropical and subtropical coastal waters",
        "distribution": "Tropical oceans worldwide, breeds on islands",
        "size": "Length: 89-114 cm, Wingspan: 217-244 cm, Weight: 1.0-1.6 kg",
        "diet": "Fish, caught from surface or stolen from other birds",
        "behavior": "Pirates food from other seabirds. Excellent flier. Nests in colonies on islands."
    },
    "Northern_Fulmar": {
        "scientific_name": "Fulmarus glacialis",
        "description": "Medium-sized seabird with gray and white plumage, thick bill, and tube-like nostrils.",
        "habitat": "Pelagic (open ocean) and coastal cliffs",
        "distribution": "North Atlantic and North Pacific, breeds on cliffs",
        "size": "Length: 43-52 cm, Wingspan: 102-112 cm, Weight: 450-1000 g",
        "diet": "Fish, squid, and marine invertebrates",
        "behavior": "Spends most of life at sea. Returns to land only to breed. Defends nest by spitting oil."
    },
    "Glaucous_winged_Gull": {
        "scientific_name": "Larus glaucescens",
        "description": "Large gull with white head and body, gray back, and pale gray wings (no black tips).",
        "habitat": "Coastal waters and beaches",
        "distribution": "North Pacific, from Alaska to California",
        "size": "Length: 50-68 cm, Wingspan: 120-150 cm, Weight: 0.8-1.6 kg",
        "diet": "Fish, invertebrates, eggs, and human food waste",
        "behavior": "Year-round resident in many areas. Forms large flocks. Nests in colonies."
    },
    "Heermann_Gull": {
        "scientific_name": "Larus heermanni",
        "description": "Medium-sized gull with dark gray body, white head, and red bill with black tip.",
        "habitat": "Coastal waters and beaches",
        "distribution": "Pacific Coast of North America, breeds in Mexico, winters along California coast",
        "size": "Length: 46-51 cm, Wingspan: 122-130 cm, Weight: 500-700 g",
        "diet": "Fish, invertebrates, and human food waste",
        "behavior": "Migratory. Forms large flocks. Nests in colonies."
    },
    "Ivory_Gull": {
        "scientific_name": "Pagophila eburnea",
        "description": "Medium-sized gull with entirely white plumage, black legs, and yellow-tipped bill.",
        "habitat": "Arctic pack ice and coastal areas",
        "distribution": "High Arctic, breeds in Greenland and Arctic islands",
        "size": "Length: 40-47 cm, Wingspan: 106-118 cm, Weight: 450-700 g",
        "diet": "Fish, carrion, and marine invertebrates",
        "behavior": "Year-round resident in Arctic. Follows polar bears for carrion. Nests on cliffs."
    },
    "Slaty_backed_Gull": {
        "scientific_name": "Larus schistisagus",
        "description": "Very large gull with white head and body, dark slate-gray back, and pink legs.",
        "habitat": "Coastal waters and beaches",
        "distribution": "North Pacific, from Alaska to Japan",
        "size": "Length: 55-68 cm, Wingspan: 132-160 cm, Weight: 1.0-2.0 kg",
        "diet": "Fish, invertebrates, and human food waste",
        "behavior": "Year-round resident in many areas. Forms large flocks. Nests in colonies."
    },
    "Western_Gull": {
        "scientific_name": "Larus occidentalis",
        "description": "Large gull with white head and body, dark gray back, yellow bill with red spot, and pink legs.",
        "habitat": "Coastal waters and beaches",
        "distribution": "Pacific Coast of North America, from Washington to Baja California",
        "size": "Length: 55-66 cm, Wingspan: 130-144 cm, Weight: 0.8-1.4 kg",
        "diet": "Fish, invertebrates, eggs, and human food waste",
        "behavior": "Year-round resident. Forms large flocks. Nests in colonies."
    },
    "Green_Violetear": {
        "scientific_name": "Colibri thalassinus",
        "description": "Medium-sized hummingbird with green body, violet ear patches, and blue tail.",
        "habitat": "Mountain forests and gardens",
        "distribution": "Mexico and Central America, occasionally in southwestern United States",
        "size": "Length: 9-10 cm, Wingspan: 12-13 cm, Weight: 4-6 g",
        "diet": "Nectar from flowers and small insects",
        "behavior": "Year-round resident in many areas. Aggressive at feeders. Can hover and fly backwards."
    },
    "Long_tailed_Jaeger": {
        "scientific_name": "Stercorarius longicaudus",
        "description": "Medium-sized seabird with gray-brown body, long pointed tail, and white underparts.",
        "habitat": "Tundra and open ocean",
        "distribution": "Arctic, breeds in tundra, winters at sea",
        "size": "Length: 38-58 cm (including tail), Wingspan: 105-125 cm, Weight: 230-440 g",
        "diet": "Small birds, eggs, lemmings, and fish",
        "behavior": "Migratory. Pirates food from other birds. Nests on ground in tundra."
    },
    "Pomarine_Jaeger": {
        "scientific_name": "Stercorarius pomarinus",
        "description": "Large seabird with dark brown body, white wing flashes, and twisted tail streamers.",
        "habitat": "Open ocean and tundra",
        "distribution": "Arctic, breeds in tundra, winters at sea",
        "size": "Length: 46-67 cm, Wingspan: 125-138 cm, Weight: 540-920 g",
        "diet": "Small birds, eggs, lemmings, and fish",
        "behavior": "Migratory. Pirates food from other birds. Nests on ground in tundra."
    },
    "Florida_Jay": {
        "scientific_name": "Aphelocoma coerulescens",
        "description": "Medium-sized jay with blue head, wings, and tail, gray back, and white underparts.",
        "habitat": "Scrublands and oak woodlands",
        "distribution": "Florida, year-round resident",
        "size": "Length: 28-30 cm, Wingspan: 33-36 cm, Weight: 66-92 g",
        "diet": "Acorns, insects, and small vertebrates",
        "behavior": "Year-round resident. Stores acorns. Cooperative breeder. Endangered species."
    },
    "Tropical_Kingbird": {
        "scientific_name": "Tyrannus melancholicus",
        "description": "Large flycatcher with gray head, olive back, yellow underparts, and notched tail.",
        "habitat": "Open areas, parks, and gardens",
        "distribution": "Southern United States, Mexico, Central and South America",
        "size": "Length: 20-23 cm, Wingspan: 38-41 cm, Weight: 33-47 g",
        "diet": "Flying insects caught in air",
        "behavior": "Year-round resident in many areas. Sits on exposed perch. Aggressive defender of territory."
    },
    "Gray_Kingbird": {
        "scientific_name": "Tyrannus dominicensis",
        "description": "Large flycatcher with gray head and back, white underparts, and notched tail.",
        "habitat": "Open areas, parks, and coastal areas",
        "distribution": "Southeastern United States, Caribbean, and Central America",
        "size": "Length: 20-24 cm, Wingspan: 38-41 cm, Weight: 37-52 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory in northern range. Sits on exposed perch. Aggressive."
    },
    "Green_Kingfisher": {
        "scientific_name": "Chloroceryle americana",
        "description": "Small kingfisher with green upperparts, white underparts with green spots, and long bill.",
        "habitat": "Rivers, streams, and ponds",
        "distribution": "Southwestern United States, Mexico, Central and South America",
        "size": "Length: 19-20 cm, Wingspan: 33-35 cm, Weight: 35-40 g",
        "diet": "Small fish and aquatic insects",
        "behavior": "Year-round resident in many areas. Dives for fish. Nests in burrows in banks."
    },
    "Pied_Kingfisher": {
        "scientific_name": "Ceryle rudis",
        "description": "Medium-sized kingfisher with black and white plumage, crested head, and long bill.",
        "habitat": "Rivers, lakes, and coastal waters",
        "distribution": "Africa, Asia, and Middle East",
        "size": "Length: 25-30 cm, Wingspan: 45-50 cm, Weight: 70-110 g",
        "diet": "Fish, caught by diving",
        "behavior": "Year-round resident. Hovers over water before diving. Nests in burrows."
    },
    "Ringed_Kingfisher": {
        "scientific_name": "Megaceryle torquata",
        "description": "Very large kingfisher with blue-gray upperparts, white collar, rufous underparts, and shaggy crest.",
        "habitat": "Rivers, lakes, and coastal waters",
        "distribution": "Southwestern United States, Mexico, Central and South America",
        "size": "Length: 38-42 cm, Wingspan: 63-71 cm, Weight: 300-400 g",
        "diet": "Fish, caught by diving",
        "behavior": "Year-round resident in many areas. Dives for fish. Nests in burrows in banks."
    },
    "White_breasted_Kingfisher": {
        "scientific_name": "Halcyon smyrnensis",
        "description": "Large kingfisher with bright blue back, white breast, rufous head, and long red bill.",
        "habitat": "Rivers, lakes, and open areas",
        "distribution": "Asia, from Middle East to Southeast Asia",
        "size": "Length: 27-28 cm, Wingspan: 40-45 cm, Weight: 65-90 g",
        "diet": "Fish, insects, and small vertebrates",
        "behavior": "Year-round resident. Perches on branches. Nests in burrows."
    },
    "Red_legged_Kittiwake": {
        "scientific_name": "Rissa brevirostris",
        "description": "Small gull with white head and body, gray back, black wing tips, and red legs.",
        "habitat": "Coastal waters and rocky islands",
        "distribution": "North Pacific, breeds on Bering Sea islands, winters at sea",
        "size": "Length: 35-39 cm, Wingspan: 84-92 cm, Weight: 325-400 g",
        "diet": "Fish and marine invertebrates",
        "behavior": "Migratory. Nests in colonies on cliffs. Dives for food."
    },
    "Western_Meadowlark": {
        "scientific_name": "Sturnella neglecta",
        "description": "Medium-sized songbird with yellow underparts, black V on breast, and brown streaked back.",
        "habitat": "Grasslands, prairies, and agricultural fields",
        "distribution": "Western and central North America, year-round resident in many areas",
        "size": "Length: 20-28 cm, Wingspan: 36-40 cm, Weight: 90-115 g",
        "diet": "Insects, seeds, and grains",
        "behavior": "Year-round resident in many areas. Sings beautiful song. Nests on ground."
    },
    "White_necked_Raven": {
        "scientific_name": "Corvus albicollis",
        "description": "Large, all-black bird with white patch on back of neck, thick bill, and wedge-shaped tail.",
        "habitat": "Mountains, cliffs, and arid areas",
        "distribution": "Eastern and southern Africa",
        "size": "Length: 50-54 cm, Wingspan: 100-120 cm, Weight: 0.7-1.2 kg",
        "diet": "Omnivorous. Eats carrion, insects, fruits, and human food waste",
        "behavior": "Highly intelligent. Forms pairs. Acrobatic flight displays."
    },
    "Geococcyx": {
        "scientific_name": "Geococcyx californianus",
        "description": "Large ground-dwelling bird with brown and white streaked plumage, long tail, and strong legs.",
        "habitat": "Desert scrub and arid grasslands",
        "distribution": "Southwestern United States and Mexico",
        "size": "Length: 51-61 cm, Wingspan: 43-61 cm, Weight: 200-300 g",
        "diet": "Insects, lizards, snakes, and small mammals",
        "behavior": "Year-round resident. Fast runner. Rarely flies. Nests in shrubs or on ground."
    },
    "Loggerhead_Shrike": {
        "scientific_name": "Lanius ludovicianus",
        "description": "Medium-sized songbird with gray head and back, white underparts, black mask, and hooked bill.",
        "habitat": "Open areas, grasslands, and shrublands",
        "distribution": "North America, breeds in United States and Canada, winters in southern United States and Mexico",
        "size": "Length: 20-23 cm, Wingspan: 28-32 cm, Weight: 45-60 g",
        "diet": "Insects, small birds, and mammals",
        "behavior": "Migratory in northern range. Impales prey on thorns. Nests in shrubs."
    },
    "Great_Grey_Shrike": {
        "scientific_name": "Lanius excubitor",
        "description": "Large shrike with gray head and back, white underparts, black mask, and hooked bill.",
        "habitat": "Open areas, tundra, and boreal forests",
        "distribution": "Northern North America, Europe, and Asia",
        "size": "Length: 22-26 cm, Wingspan: 30-34 cm, Weight: 50-80 g",
        "diet": "Insects, small birds, and mammals",
        "behavior": "Migratory in northern range. Impales prey on thorns. Nests in trees."
    },
    "Cape_Glossy_Starling": {
        "scientific_name": "Lamprotornis nitens",
        "description": "Medium-sized starling with iridescent blue-green plumage, yellow eyes, and long tail.",
        "habitat": "Open woodlands, savannas, and urban areas",
        "distribution": "Southern Africa",
        "size": "Length: 24-27 cm, Wingspan: 40-45 cm, Weight: 70-100 g",
        "diet": "Fruits, insects, and human food waste",
        "behavior": "Year-round resident. Forms large flocks. Nests in tree cavities."
    },
    "Bank_Swallow": {
        "scientific_name": "Riparia riparia",
        "description": "Small swallow with brown upperparts, white underparts, and brown breast band.",
        "habitat": "Rivers, lakes, and areas with vertical banks",
        "distribution": "North America, breeds in United States and Canada, winters in South America",
        "size": "Length: 12-14 cm, Wingspan: 26-29 cm, Weight: 11-20 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Nests in burrows in banks. Forms large colonies."
    },
    "Barn_Swallow": {
        "scientific_name": "Hirundo rustica",
        "description": "Medium-sized swallow with blue upperparts, rufous underparts, and deeply forked tail.",
        "habitat": "Open areas, farms, and near buildings",
        "distribution": "Worldwide, breeds in Northern Hemisphere, winters in Southern Hemisphere",
        "size": "Length: 15-19 cm, Wingspan: 29-32 cm, Weight: 16-22 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Nests in buildings and barns. Forms colonies."
    },
    "Cliff_Swallow": {
        "scientific_name": "Petrochelidon pyrrhonota",
        "description": "Medium-sized swallow with blue upperparts, buff rump, white underparts, and square tail.",
        "habitat": "Open areas, cliffs, and bridges",
        "distribution": "North America, breeds in United States and Canada, winters in South America",
        "size": "Length: 13-15 cm, Wingspan: 27-29 cm, Weight: 19-28 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Nests in mud nests on cliffs and bridges. Forms large colonies."
    },
    "Tree_Swallow": {
        "scientific_name": "Tachycineta bicolor",
        "description": "Medium-sized swallow with blue-green upperparts, white underparts, and slightly forked tail.",
        "habitat": "Open areas, fields, and near water",
        "distribution": "North America, breeds in United States and Canada, winters in southern United States, Mexico, and Central America",
        "size": "Length: 12-14 cm, Wingspan: 30-35 cm, Weight: 16-25 g",
        "diet": "Flying insects caught in air",
        "behavior": "Migratory. Nests in tree cavities and nest boxes. Forms flocks."
    }
}

def batch_update_common_birds():
    """批量更新常見鳥類的信息"""
    data = load_bird_template()
    updated_count = 0
    
    for bird_key, bird_data in data.items():
        # 提取鳥類名稱（去掉編號前綴）
        bird_name = bird_key.split('.', 1)[1] if '.' in bird_key else bird_key
        
        # 檢查是否有預定義的信息
        if bird_name in COMMON_BIRDS_INFO:
            info = COMMON_BIRDS_INFO[bird_name]
            bird_data['scientific_name'] = info['scientific_name']
            bird_data['description'] = info['description']
            bird_data['habitat'] = info['habitat']
            bird_data['distribution'] = info['distribution']
            bird_data['size'] = info['size']
            bird_data['diet'] = info['diet']
            bird_data['behavior'] = info['behavior']
            updated_count += 1
            print(f"Updated: {bird_name}")
    
    save_bird_template(data)
    print(f"\nTotal updated: {updated_count} bird species")
    return updated_count

if __name__ == '__main__':
    print("Batch updating bird information...")
    print("="*60)
    batch_update_common_birds()
    print("="*60)
    print("Done!")

