import json
data = [
    {
        "id": 1,
        "user_id": "3",
        "name": "할메가커피",
        "category": "커피",
        "price_ice": "0",
        "price_hot": "1900",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "우리 할머니께서 즐겨드시던 달달한 믹스 커피 스타일로 만든  메가MGC커피만의 시원한 커피 음료",
        "image": "할메가커피.jpg"
    },
    {
        "id": 2,
        "user_id": "3",
        "name": "왕할메가커피",
        "category": "커피",
        "price_ice": "0",
        "price_hot": "2900",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "우리 할머니께서 즐겨드시던 달달한 믹스 커피 스타일로 만든  메가MGC커피만의 메가사이즈 커피 음료",
        "image": "왕할메가커피.jpg"
    },
    {
        "id": 3,
        "user_id": "3",
        "name": "아메리카노",
        "category": "커피",
        "price_ice": "1500",
        "price_hot": "2000",
        "price_constant": "0",
        "menu_type": "both",
        "description": "[기본2샷]메가MGC커피 블렌드 원두로 추출한 에스프레소에 물을 더해, 풍부한 바디감을 느낄 수 있는 스탠다드 커피.",
        "image": "아메리카노.jpg"
    },
    {
        "id": 4,
        "user_id": "3",
        "name": "메가리카노",
        "category": "커피",
        "price_ice": "0",
        "price_hot": "3000",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "깊고 진한 메가MGC커피 아메리카노를 '960ml' 더 큼직하게 즐길 수 있는 대용량 커피.",
        "image": "메가리카노.jpg"
    },
    {
        "id": 5,
        "user_id": "3",
        "name": "꿀아메리카노",
        "category": "커피",
        "price_ice": "2700",
        "price_hot": "2700",
        "price_constant": "0",
        "menu_type": "both",
        "description": "아메리카노의 묵직한 바디감에 달콤한 사양벌꿀이 소프트하게 어우러진 커피.",
        "image": "꿀아메리카노.jpg"
    },
    {
        "id": 6,
        "user_id": "3",
        "name": "바닐라아메리카노",
        "category": "커피",
        "price_ice": "2700",
        "price_hot": "2700",
        "price_constant": "0",
        "menu_type": "both",
        "description": "아메리카노에 바닐라의 부드러운 향과 달콤함을 조화롭게 담아낸 커피.",
        "image": "바닐라아메리카노.jpg"
    },
    {
        "id": 7,
        "user_id": "3",
        "name": "헤이즐넛아메리카노",
        "category": "커피",
        "price_ice": "2700",
        "price_hot": "2700",
        "price_constant": "0",
        "menu_type": "both",
        "description": "아메리카노에 헤이즐넛의 풍성한 향과 달콤함을 담아 향긋하고 부드럽게 즐기는 커피.",
        "image": "헤이즐넛아메리카노.jpg"
    },
    {
        "id": 8,
        "user_id": "3",
        "name": "카페라떼",
        "category": "커피",
        "price_ice": "2900",
        "price_hot": "2900",
        "price_constant": "0",
        "menu_type": "both",
        "description": "진한 에스프레소와 부드러운 우유가 어우러져 고소한 풍미를 완성한 라떼.",
        "image": "카페라떼.jpg"
    },
    {
        "id": 9,
        "user_id": "3",
        "name": "카푸치노",
        "category": "커피",
        "price_ice": "2900",
        "price_hot": "2900",
        "price_constant": "0",
        "menu_type": "both",
        "description": "에스프레소 위에 올려진 우유 거품, 그리고 시나몬 파우더로 완성한 조화로운 맛의 커피.",
        "image": "카푸치노.jpg"
    },
    {
        "id": 10,
        "user_id": "3",
        "name": "바닐라라떼",
        "category": "커피",
        "price_ice": "3400",
        "price_hot": "3400",
        "price_constant": "0",
        "menu_type": "both",
        "description": "바닐라의 짙은 향과 풍부한 폼 밀크의 조화가 인상적인 달콤한 라떼.",
        "image": "바닐라라떼.jpg"
    },
    {
        "id": 11,
        "user_id": "3",
        "name": "헤이즐넛라떼",
        "category": "커피",
        "price_ice": "3400",
        "price_hot": "3400",
        "price_constant": "0",
        "menu_type": "both",
        "description": "부드러운 카페라떼에 헤이즐넛의 풍부한 향과 달콤함을 담아 향긋하게 즐길 수 있는 라떼.",
        "image": "헤이즐넛라떼.jpg"
    },
    {
        "id": 12,
        "user_id": "3",
        "name": "연유라떼",
        "category": "커피",
        "price_ice": "3900",
        "price_hot": "0",
        "price_constant": "0",
        "menu_type": "onlyhot",
        "description": "향기로운 에스프레소 샷, 부드러운 우유 그리고 달콤한 연유가 조화롭게 어우러진 라떼.",
        "image": "연유라떼.jpg"
    },
    {
        "id": 13,
        "user_id": "3",
        "name": "카라멜마끼아또",
        "category": "커피",
        "price_ice": "3700",
        "price_hot": "3700",
        "price_constant": "0",
        "menu_type": "both",
        "description": "폼 밀크 속에 진한 에스프레소와 달콤한 카라멜을 가미해 부드럽게 즐기는 커피.",
        "image": "카라멜마끼아또.jpg"
    },
    {
        "id": 14,
        "user_id": "3",
        "name": "카페모카",
        "category": "커피",
        "price_ice": "3900",
        "price_hot": "3900",
        "price_constant": "0",
        "menu_type": "both",
        "description": "초코를 만나 풍부해진 에스프레소와 고소한 우유, 부드러운 휘핑크림까지 더해 달콤하게 즐기는 커피.",
        "image": "카페모카.jpg"
    },
    {
        "id": 15,
        "user_id": "3",
        "name": "콜드브루오리지널",
        "category": "커피",
        "price_ice": "3500",
        "price_hot": "3500",
        "price_constant": "0",
        "menu_type": "both",
        "description": "차가운 물에 장시간 우려내 깔끔한 목넘김을 느낄 수 있는 콜드브루.",
        "image": "콜드브루오리지널.jpg"
    },
    {
        "id": 16,
        "user_id": "3",
        "name": "콜드브루라떼",
        "category": "커피",
        "price_ice": "4000",
        "price_hot": "4000",
        "price_constant": "0",
        "menu_type": "both",
        "description": "콜드브루에 고소한 우유를 섞어, 깔끔함과 부드러움을 잡은 라떼.",
        "image": "콜드브루라떼.jpg"
    },
    {
        "id": 17,
        "user_id": "3",
        "name": "티라미수라떼",
        "category": "커피",
        "price_ice": "3900",
        "price_hot": "3900",
        "price_constant": "0",
        "menu_type": "both",
        "description": "에스프레소와 티라미수 소스 & 우유 그리고 풍미를 더해주는 달달한 크림까지 곁들여 완성한 티라미수 라떼.",
        "image": "티라미수라떼.jpg"
    },
    {
        "id": 18,
        "user_id": "3",
        "name": "큐브라떼",
        "category": "커피",
        "price_ice": "0",
        "price_hot": "4200",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "연유를 섞은 라떼에 에스프레소를 얼린 커피큐브를 올려, 녹을수록 더 진한 커피가 느껴지는 라떼.",
        "image": "큐브라떼.jpg"
    },
    {
        "id": 19,
        "user_id": "3",
        "name": "콜드브루디카페인",
        "category": "커피",
        "price_ice": "3500",
        "price_hot": "3500",
        "price_constant": "0",
        "menu_type": "both",
        "description": "카페인을 줄였지만, 원두 본연의 향미를 풍부하게 살려 맛을 잡은 디카페인 콜드브루.",
        "image": "콜드브루디카페인.jpg"
    },
    {
        "id": 20,
        "user_id": "3",
        "name": "콜드브루디카페인라떼",
        "category": "커피",
        "price_ice": "4000",
        "price_hot": "4000",
        "price_constant": "0",
        "menu_type": "both",
        "description": "우유와 만나 부드럽고 고소한 풍미가 더해진 콜드브루 디카페인 라떼.",
        "image": "콜드브루디카페인라떼.jpg"
    },
    {
        "id": 21,
        "user_id": "3",
        "name": "딸기라떼",
        "category": "음료 메뉴",
        "price_ice": "0",
        "price_hot": "3700",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "산뜻하고 달콤한 딸기가 부드러운 우유와 어우러져 더욱 기분 좋게 즐기는 아이스 라떼.",
        "image": "딸기라떼.jpg"
    },
    {
        "id": 22,
        "user_id": "3",
        "name": "고구마라떼",
        "category": "음료 메뉴",
        "price_ice": "3500",
        "price_hot": "3500",
        "price_constant": "0",
        "menu_type": "both",
        "description": "달콤하고 고소한 고구마와 부드러운 우유가 만나 누구나 즐기기 좋은 든든한 라떼.",
        "image": "고구마라떼.jpg"
    },
    {
        "id": 23,
        "user_id": "3",
        "name": "곡물라떼",
        "category": "음료 메뉴",
        "price_ice": "3300",
        "price_hot": "3300",
        "price_constant": "0",
        "menu_type": "both",
        "description": "우유에 곡물을 더해 고소하고 든든하게 즐기는 라떼.",
        "image": "곡물라떼.jpg"
    },
    {
        "id": 24,
        "user_id": "3",
        "name": "메가초코",
        "category": "음료 메뉴",
        "price_ice": "3800",
        "price_hot": "3800",
        "price_constant": "0",
        "menu_type": "both",
        "description": "부드러운 우유에 진한 초코소스, 달콤한 휘핑크림의 삼박자 조화로 완성한 달콤 초코 음료.",
        "image": "메가초코.jpg"
    },
    {
        "id": 25,
        "user_id": "3",
        "name": "토피넛라떼",
        "category": "음료 메뉴",
        "price_ice": "3800",
        "price_hot": "3800",
        "price_constant": "0",
        "menu_type": "both",
        "description": "은은하게 퍼지는 카라멜의 달달한 향기와 견과의 고소함을 한입에 즐길 수 있는 라떼.",
        "image": "토피넛라떼.jpg"
    },
    {
        "id": 26,
        "user_id": "3",
        "name": "오레오초코라떼",
        "category": "음료 메뉴",
        "price_ice": "0",
        "price_hot": "3900",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "진한 초코와 리얼 오레오를 블렌딩해 씹는 맛을 더한 달콤한 아이스 라떼.",
        "image": "오레오초코라떼.jpg"
    },
    {
        "id": 27,
        "user_id": "3",
        "name": "흑당버블밀크티라떼",
        "category": "음료 메뉴",
        "price_ice": "0",
        "price_hot": "3800",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "타바론 얼그레이 홍차의 깊은 맛을 살린 일크티 라떼에 진한 흑당과 흑당 버블의 달콤함을 채운 음료.",
        "image": "흑당버블밀크티라떼.jpg"
    },
    {
        "id": 28,
        "user_id": "3",
        "name": "흑당버블라떼",
        "category": "음료 메뉴",
        "price_ice": "0",
        "price_hot": "3700",
        "price_constant": "0",
        "menu_type": "onlyice",
        "description": "모리셔스의 진한 흑당과 부드러운 우유가 달콤한 조화에 흑당 버블을 함께 즐기는 라떼.",
        "image": "흑당버블라떼.jpg"
    },
    {
        "id": 29,
        "user_id": "3",
        "name": "메가초코",
        "category": "음료 메뉴",
        "price_ice": "3800",
        "price_hot": "3800",
        "price_constant": "0",
        "menu_type": "both",
        "description": "부드러운 우유에 진한 초코소스, 달콤한 휘핑크림의 삼박자 조화로 완성한 달콤 초코 음료.",
        "image": "메가초코.jpg"
    },
    {
        "id": 30,
        "user_id": "3",
        "name": "녹차라떼",
        "category": "음료 메뉴",
        "price_ice": "3500",
        "price_hot": "3500",
        "price_constant": "0",
        "menu_type": "both",
        "description": "향긋한 녹차에 우유를 더해 입 안에 부드러운 푸릇함을 선물하는 라떼.",
        "image": "녹차라떼.jpg"
    },
]
# Re-processing the data after importing the json library
cleaned_data = []
for entry in data:
    cleaned_entry = {key: value for key, value in entry.items() if key not in ['id', 'user_id', 'image']}
    cleaned_data.append(cleaned_entry)

# Converting the cleaned data back to JSON format
cleaned_data_json = json.dumps(cleaned_data, indent=4, ensure_ascii=False)
file_path = "clean.json"
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, indent=4, ensure_ascii=False)