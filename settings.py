app_settings = {
   'client_id': "",  # go to https://developers.eveonline.com/ create app and get Client ID
   'client_secret': "",  # go to https://developers.eveonline.com/ create app and get Secret Key
   'client_callback_url': "",  # default http://localhost:8635/ need to be same as in your app in https://developers.eveonline.com/
   'user_agent': "",
   'scopes': [],
   'port': 8635,  # default 8635
}

white_list = {} # список персонажей, письма которых не будут игнорироваться. Указывать в формате: Id: "Имя персонажа"

# TODO: Обернуть в запрос
npc_corp_list = {
    1000165: "Hedion University",
    1000166: "Imperial Academy",
    1000077: "Royal Amarr Institute",
    1000044: "School of Applied Knowledge",
    1000045: "Science and Trade Institute",
    1000167: "State War Academy",
    1000169: "Center for Advanced Studies",
    1000168: "Federal Navy Academy",
    1000115: "University of Caille",
    1000172: "Pator Tech School",
    1000170: "Republic Military School",
    1000171: "Republic University",
    1000066: "Viziam",
    1000080: "Ministry of War",
    1000072: "Imperial Shipment",
    1000014: "Perkone",
    1000009: "Caldari Provisions",
    1000006: "Deep Core Mining Inc.",
    1000107: "The Scope",
    1000111: "Aliastra",
    1000114: "Garoun Investment Bank",
    1000049: "Brutor Tribe",
    1000046: "Sebiestor Tribe",
    1000060: "Native Freshfood",
    1000180: "State Protectorate",
    1000181: "Federal Defense Union",
    1000182: "Tribal Liberation Force",
    1000179: "24th Imperial Crusade",
}
