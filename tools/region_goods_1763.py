# [#278] Region -> weighted trade-good rotation for 1763 economic geography.
# Applied ONLY to placeholder-cloth provinces; hand-assigned goods are preserved.
# Goods restricted to those DEFINED in common/trade_goods/. Deterministic rotation
# by province-index-within-region gives realistic intra-region variety w/o randomness.
REGION_GOODS = {
 # ---- Russia / Siberia / Central Asia ----
 "Moscow":["grain","hemp","wood","iron"], "Kazan":["grain","livestock","fur"],
 "Siberia":["fur","wood"], "Far_East":["fur","fish"], "Voiska_Donskova":["grain","horses","livestock"],
 "Kiev":["grain","hemp"], "Minsk":["grain","wood","hemp"], "Mongolia":["livestock","horses"],
 "Tannu_Tuva":["fur","livestock"], "Turkestan":["cotton","livestock"], "Bukhara":["cotton","silk","livestock"],
 "Khwarezm":["cotton","silk"], "Fergana":["cotton","silk"], "Tokharistan":["horses","cotton"],
 "Balochistan":["livestock","wool","generic_fruit"], "Pashtunistan":["wool","livestock","gems"],
 # ---- Europe: North / Baltic ----
 "Sweden":["iron","copper","wood"], "Finland":["wood","fur","fish"], "Norway":["fish","wood"],
 "Denmark":["livestock","grain","fish"], "Jutland":["livestock","grain"], "Iceland":["fish","wool"],
 "Greenland":["fish","whales"], "Saapmi":["fur","fish"], "Baltic_states":["grain","hemp","linen"],
 "Poland":["grain","wood"], "Galicia":["grain","salt","wood"], "Prussia":["grain","amber","wood"],
 "Pomerania":["grain","fish"], "Brandenburg":["grain","wood"], "Silesia":["coal","iron","linen"],
 # ---- Europe: British Isles ----
 "Southern_England":["wool","cloth","coal","tin"], "Northern_England":["coal","wool","iron"],
 "Wales_Mercia":["coal","wool","iron"], "Scotland":["wool","fish","coal"], "Ireland":["livestock","linen","wool"],
 # ---- Europe: France / Low Countries ----
 "Atlantic_France":["generic_fruit","grain","salt"], "Northern_France":["grain","wool","linen"],
 "Grand_Est":["grain","iron","generic_fruit"], "Occitanie":["generic_fruit","wool","mediterranean_fruit"],
 "Provence_Liguria":["mediterranean_fruit","silk","generic_fruit"], "Low_Countries":["cloth","linen","grain"],
 # ---- Europe: Germany / Alps / Bohemia ----
 "Low_Saxony":["grain","livestock"], "Westfalen":["coal","iron","grain"], "Hessen":["grain","wood","iron"],
 "Saxony":["silver","cloth","coal"], "Bavaria":["grain","livestock","wood"], "Bohemia":["grain","iron","silver"],
 "Helvetia":["livestock","cloth"], "Austria":["iron","wood","livestock"], "Pannonia":["grain","livestock","wool"],
 "Subcarpathia":["livestock","wood","salt"], "Bulgaria":["grain","wool","tobacco"], "Rumelia":["grain","tobacco","wool"],
 "Illyria":["livestock","wood","mediterranean_fruit"], "Caucasus":["livestock","wool","silk"],
 "Black_Sea":["grain","fish"], "Odessa":["grain"], "Armenia":["silk","wool","copper"], "Azerbaijan":["silk","oil","cotton"],
 # ---- Europe: Iberia / Italy / Mediterranean ----
 "La_Mancha":["wool","mediterranean_fruit","grain"], "Andalusia":["mediterranean_fruit","wool","salt"],
 "Valencia":["mediterranean_fruit","silk"], "Navarre":["wool","mediterranean_fruit"],
 "Portugal":["mediterranean_fruit","fish","salt"], "Macaronesia":["generic_fruit","sugar","mediterranean_fruit"],
 "Cisalpine_Italy":["silk","grain","livestock"], "Venetia":["silk","cloth","inorganic_compounds"],
 "Central_Italy":["mediterranean_fruit","generic_fruit","wool"], "Southern_Italy":["grain","mediterranean_fruit"],
 "Sicily":["sulphur","grain","mediterranean_fruit"], "Corsica_and_Sardinia":["mediterranean_fruit","salt","fish"],
 "Aegean":["mediterranean_fruit","generic_fruit","silk"], "Crete":["mediterranean_fruit","generic_fruit","wool"],
 "Marmara":["silk","mediterranean_fruit","grain"], "Cyprus":["mediterranean_fruit","copper","silk"],
 # ---- Ottoman / MENA / Persia ----
 "Anatolia":["wool","cotton","tobacco"], "Cilicia":["cotton","wood"], "Levant":["cotton","mediterranean_fruit","silk"],
 "Syria":["cotton","silk","wool"], "Arab_Iraq":["grain","generic_fruit","horses"], "Arabia":["incense","coffee","camel"],
 "Eastern_Arabia":["gems","generic_fruit","camel"], "Egypt":["grain","cotton","generic_fruit"],
 "Libya":["livestock","salt","camel"], "Tunisia":["mediterranean_fruit","wool","salt"],
 "Algeria":["mediterranean_fruit","wool","grain"], "Morocco":["mediterranean_fruit","wool","livestock"],
 "Western_Sahara":["salt","camel"], "Persian_Iraq":["grain","wool","opium"], "Caspian_Iran":["silk","grain"],
 "Southern_Iran":["generic_fruit","gems","wool"], "Kerman":["wool","copper"], "Khurasan":["wool","cotton","gems"],
 # ---- South Asia ----
 "Punjab":["grain","cotton","wool"], "Rajputana":["opium","cotton","wool"], "Central_India":["cotton","opium","iron"],
 "Bengal_region":["cotton","grain","silk"], "Bahar":["opium","grain","inorganic_compounds"],
 "West_India":["cotton","salt","textile_fibres"], "East_India":["grain","salt"],
 "South_India":["cotton","spices","textile_fibres"], "Kashmir":["wool","silk"], "Nepal":["grain","livestock","hardwood"],
 "Eastern_Himalayas":["hardwood","livestock"], "Ceylon":["spices","gems","palm"], "Maldives":["fish","spices"],
 "Andaman_and_Nicobar":["hardwood","spices"], "Bay_of_Bengal":["grain","fish"], "Arabian_Sea":["fish","cotton","salt"],
 # ---- China ----
 "Zhili":["grain","cotton"], "Shandong":["cotton","grain","silk"], "Shanxi":["coal","iron","grain"],
 "Shaanxi":["grain","coal"], "Gansu":["livestock","wool"], "Qinghai":["livestock","wool"], "Henan":["grain","cotton"],
 "Anhui":["tea","grain"], "Jiangsu":["silk","cotton","grain"], "Zhejiang":["silk","tea"],
 "Jiangxi":["porcelain","tea","grain"], "Fujian":["tea","sugar"], "Guangdong":["silk","tea","sugar"],
 "Guangxi":["grain","sugar","livestock"], "Hunan":["grain","tea","coal"], "Hubei":["grain","cotton","tea"],
 "Sichuan_Kham":["silk","salt","tea"], "Yunnan":["copper","tea","tin"], "Guizhou":["livestock","grain","opium"],
 "Liaoning":["grain","iron"], "Tibet":["wool","livestock","gold"],
 # ---- Korea / Japan ----
 "Korea":["grain","silk"], "Honshu":["silk","tea","grain"], "Kyushu":["porcelain","silk","coal"],
 "Shikoku":["salt","grain"], "Ezo":["fish","fur"], "Okinawa":["sugar","fish"], "Taiwan":["sugar","grain"],
 # ---- Southeast Asia ----
 "Vietnam":["grain","silk","sugar"], "Cambodia":["grain","fish","hardwood"], "Laos":["hardwood","elephants","livestock"],
 "Lan_Na":["hardwood","elephants","grain"], "Siam":["grain","hardwood","tin"], "South_Siam":["tin","hardwood","spices"],
 "Isan":["grain","livestock"], "Tenasserim":["tin","hardwood"], "Burma":["hardwood","gems","grain"],
 "Johore":["spices","tin","hardwood"], "Sumatra":["spices","gold","coffee"], "Java":["coffee","spices","sugar"],
 "Borneo":["hardwood","gold","spices"], "Sulawesi":["spices","hardwood"], "Maluku":["spices"],
 "Nusa_Tenggara":["hardwood","livestock","spices"], "Luzon":["sugar","spices","tobacco"],
 "Visayas":["sugar","hardwood","spices"], "Mindanao":["spices","hardwood"],
 # ---- Africa ----
 "Coastal_West_Africa":["palm","gold","elephants"], "Gulf_of_Guinea":["palm","gold","elephants"],
 "Sahel":["salt","livestock","gold"], "Sudan":["livestock","incense","camel"], "Horn_of_Africa":["incense","coffee","livestock"],
 "Lake_Victoria":["livestock","elephants","grain"], "Congo_Basin":["elephants","palm","hardwood"],
 "Angola":["elephants","palm","copper"], "Mozambique":["gold","elephants","hardwood"], "Zimbabwe":["gold","elephants","livestock"],
 "South_Africa":["livestock","generic_fruit","grain"], "Kalahari":["livestock","elephants"],
 "Madagascar":["spices","grain","livestock"], "Reunion":["coffee","sugar"],
 # ---- North America ----
 "Mountain_West":["fur","livestock"], "Great_Plains":["fur","livestock","horses"], "Great_Forests":["fur","wood"],
 "Great_Lakes":["fur","wood","fish"], "Cascadia":["fur","wood","fish"], "British_Columbia":["fur","wood","fish"],
 "Alaska":["fur","fish","whales"], "Vancouver_Island":["fur","fish"], "California":["fur","livestock","grain"],
 "American_Southwest":["livestock","copper","silver"], "Appalachia":["fur","wood","tobacco"],
 "Deep_South":["tobacco","livestock","wood"], "New_England":["fish","wood","whales"], "Ontario":["fur","wood","grain"],
 "Quebec":["fur","wood","grain"], "Nova_Scotia":["fish","wood"], "New_Brunswick":["fish","wood"],
 "Praire_Provinces":["fur","wood"], "Northern_Territories":["fur","fish"], "Atlantic_Region":["fish","wood"],
 "Northern_Mexico":["silver","livestock"], "Pacific_Mexico":["silver","sugar","livestock"],
 "Eastern_Mexico":["silver","sugar","coffee"], "Central_America":["chocolate","sugar","hardwood"],
 # ---- Caribbean ----
 "Cuba":["sugar","tobacco","coffee"], "Haiti":["sugar","coffee","chocolate"], "Antilles":["sugar","coffee","tobacco"],
 "Lucayan_Archipelago":["salt","fish","wood"],
 # ---- South America ----
 "Colombia":["coffee","gold","chocolate"], "Venezuela":["coffee","chocolate","sugar"], "Ecuador":["chocolate","coffee"],
 "Guyana":["sugar","hardwood","coffee"], "Peru":["silver","sugar","cotton"], "Upper_Peru":["silver","tin"],
 "Chile":["copper","grain","generic_fruit"], "Argentina":["livestock","grain"], "Paraguay":["tobacco","livestock"],
 "Uruguay":["livestock","grain"], "Patagonia":["livestock","wool","fish"], "North_Brazil":["chocolate","hardwood","sugar"],
 "Northeast_Brazil":["sugar","cotton","tobacco"], "Southeast_Brazil":["gold","sugar"], "South_Brazil":["livestock","grain","hardwood"],
 # ---- Oceania / Pacific ----
 "North_Island":["fish","wood","hardwood"], "South_Island":["fish","wood","hardwood"],
 "Queensland":["fish","livestock","hardwood"], "South_Australia":["fish","livestock","hardwood"],
 "Western_Australia":["fish","livestock","hardwood"], "Northern_Territory":["fish","livestock","hardwood"],
 "Tasmania":["fish","wood","hardwood"], "New_Guinea":["spices","hardwood"], "New_Britain":["fish","tropical_fruit","palm"],
 "Fiji":["fish","tropical_fruit","palm"], "Samoa":["fish","tropical_fruit","palm"], "Tahiti":["fish","tropical_fruit","palm"],
 "Hawaii":["fish","tropical_fruit","palm"], "Vanuatu":["fish","tropical_fruit","palm"],
 "Salomon_Islands":["fish","tropical_fruit","palm"], "Bougainville_Island":["fish","tropical_fruit","palm"],
 "Caroline_Islands":["fish","tropical_fruit","palm"], "Marshall_Islands":["fish","tropical_fruit","palm"],
 "Gilbert_Islands":["fish","tropical_fruit","palm"], "Line_Islands":["fish","tropical_fruit","palm"],
 "Tuvalu":["fish","tropical_fruit","palm"], "Wake":["fish","palm"], "Palau":["fish","tropical_fruit","palm"],
 "Guam":["fish","tropical_fruit","palm"], "Mariana_Islands":["fish","tropical_fruit","palm"],
 "South_Atlantic_Islands":["fish","whales"],

 # ---- regions with hyphenated names (added #278 join-fix) ----
 "Sankt-Petersburg":["grain","hemp","wood","fish"], "Mid-Atlantic":["tobacco","wood","grain","fish"],
 "Mid-Atlantic_South":["tobacco","cotton","wood"], "Leon-Castille":["wool","grain","mediterranean_fruit"],
 "Catalonia-Aragon":["mediterranean_fruit","wool","salt"], "Indo-Gangetic_Plain":["grain","cotton","opium","silk"],
 "Auvergne-Rhone-Alpes":["grain","livestock","wood","iron"], "Baden-Wurttemberg":["grain","wood","iron"],
 "Nouvelle-Caledonie":["fish","tropical_fruit","hardwood"],
}
