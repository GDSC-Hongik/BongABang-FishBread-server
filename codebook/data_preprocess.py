import re 
pattern = "[0-9]*,*[0-9]+원"
# category = {"카테고리 이름": "처음으로 카테고리 시작 메뉴"}
category1 = {"스모어 블랙쿠키 프라페":"스무디, 프라페", "스노우 샹그리아 에이드":"에이드, 주스",
            "따끈따끈 간식꾸러미":"디저트", "모어모어 스모어세트":"세트메뉴" , "골드메달 애플스파클링":"병음료", "엠지씨 머그":"MD상품"}
category2 = {"할메가커피": "커피", "딸기라떼": "음료 메뉴", "디카페인 아메리카노":"디카페인",
             "화이트 뱅쇼":"TEA"}
menu_str_2 = """ 
할메가커피	0원	1,900원
왕할메가커피	0원	2,900원
아메리카노	1,500원	2,000원
메가리카노		0원 3,000원
꿀아메리카노	2,700원	2,700원
바닐라아메리카노	2,700원	2,700원
헤이즐넛아메리카노	2,700원	2,700원
카페라떼	2,900원	2,900원
카푸치노	2,900원	2,900원
바닐라라떼	3,400원	3,400원
헤이즐넛라떼	3,400원	3,400원
연유라떼	3,900원	0원
카라멜마끼아또	3,700원	3,700원
카페모카	3,900원	3,900원
콜드브루오리지널	3,500원	3,500원
콜드브루라떼	4,000원	4,000원
티라미수라떼	3,900원	3,900원
큐브라떼	0원	4,200원
콜드브루디카페인	3,500원	3,500원
콜드브루디카페인라떼	4,000원	4,000원
딸기라떼	0원	3,700원
고구마라떼	3,500원	3,500원
곡물라떼	3,300원	3,300원
메가초코	3,800원	3,800원
토피넛라떼	3,800원	3,800원
오레오초코라떼	0원	3,900원
흑당버블밀크티라떼	0원	3,800원
흑당버블라떼	0원	3,700원
메가초코	3,800원	3,800원
녹차라떼	3,500원	3,500원
핫초코	3,500원	0원
로얄밀크티라떼	3,700원	0원
디카페인 아메리카노	2,500원	3,000원
디카페인 꿀아메리카노	3,700원	3,700원
디카페인 헤이즐넛 아메리카노	3,700원	3,700원
디카페인 바닐라 아메리카노	3,700원	3,700원
디카페인 카페라떼	3,900원	3,900원
디카페인 바닐라라떼	4,400원	4,400원
디카페인 연유라떼	4,900원	0원
디카페인 카라멜마끼아또	4,700원	4,700원
디카페인 카페모카	4,900원	4,900원
디카페인 카푸치노	3,900원	3,900원
디카페인헤이즐넛라떼	4,400원	4,400원
디카페인티라미수라떼	4,900원	4,900원
디카페인 메가리카노	0원	4,500원
화이트 뱅쇼	 0원	3,900원
복숭아아이스티	0원 	3,000원
허니자몽블랙티	3,700원	3,700원
사과유자차	3,500원	3,500원
유자차	3,300원	3,300원
레몬차	3,300원	3,300원
자몽차	3,300원	3,300원
녹차	2,500원	2,500원
페퍼민트	2,500원	2,500원
캐모마일	2,500원	2,500원
얼그레이	2,500원	2,500원
"""

menu_beverage = {'왁자지껄 팝핑 스무디언즈': '[한정판매] 달달한 바나나 우유 스무디에  톡톡 터지는 팝핑캔디가 가득! 스무디가 된 미니언즈 음료', '우당탕탕 뚝딱 미니언라떼': '[한정판매] 달달 고소한 바나나 라떼에 다양한 취향을 가진 미니언즈를 위한 5가지 토핑 중 하나를 선택해 즐기는 이색 라떼 음료', '바나바나 초코 미니언라떼': '[한정판매] 추운 겨울을 따뜻하고 달콤하게 채워 줄 바나나 핫초코 미니언즈 음료', '스모어 블랙쿠키 프라페': '진한 초코스무디에 바삭한 쿠키를 넣어 쫀득 달콤한 마시멜로우 잼과 함께 달콤하게 즐기는 겨울 한정 프라페', '스모어 카라멜쿠키 프라페': '로투스 쿠키와 함께 진한 카라멜 맛의 스무디를\n쫀득 달콤한 마시멜로우 잼과 함께 즐기는 겨울 한정 프라페', '스노우 샹그리아 에이드': '레몬, 자몽, 석류, 백포도, 사과 등 다양한 과일로 맛을 낸 새하얀 스노우를 표현한 겨울한정 샹그리아 에이드', '화이트 뱅쇼': '레몬, 자몽, 석류, 백포도, 사과 등 다양한 과일로 맛을 낸 겨울한정 화이트 뱅쇼', '할메가커피': '우리 할머니께서 즐겨드시던 달달한 믹스 커피 스타일로 만든 \n메가MGC커피만의 시원한 커피 음료', '왕할메가커피': '우리 할머니께서 즐겨드시던 달달한 믹스 커피 스타일로 만든 \n메가MGC커피만의 메가사이즈 커피 음료', '코코넛 커피 스무디': '바삭하고 고소한 코코넛 칩을 올리고 \n쌉싸름한 커피와 달콤한 코코넛이 조화로운 스무디', '레드오렌지자몽주스': '엄선된 시칠리아 레드오렌지와 자몽이 만난 상큼한 주스에\n프로바이오틱스를 더해 건강한 블렌딩 주스', '샤인머스캣그린주스': '달콤한 샤인머스캣과 케일이 만난 싱그러운 주스에\n칼슘을 더해 건강한 블렌딩 주스', '딸기주스': '새콤달콤한 딸기주스에 피쉬 콜라겐을 더해 건강한 블렌딩 주스', '딸기바나나주스': '상큼한 딸기와 부드러운 바나나가 만나, 새콤달콤한 매력이 살아 있는 과일 음료.', '디카페인 에스프레소': '디카페인으로 만나는 메가MGC커피 에스프레소', '디카페인 젤라또 아포카토': '바닐라 젤라또에 진한 디카페인 에스프레소를 부어 만든 디저트', '에스프레소 피에노': '크림과 코코아 파우더를 올려 \n부드럽게 즐길 수 있는 에스프레소', '디카페인 아메리카노': '향과 풍미 그대로 카페인만을 낮춰 민감한 분들도 안심하고 \n매일매일 즐길 수 있는 디카페인 커피', '디카페인 꿀아메리카노': '디카페인 아메리카노의 묵직한 바디감에 달콤한 사양벌꿀이 소프트하게 어우러진 커피.', '디카페인 헤이즐넛 아메리카노': '디카페인 아메리카노에 헤이즐넛의 풍성한 향과 달콤함을 담아 \n향긋하고 부드럽게 즐기는 커피.', '디카페인 바닐라 아메리카노': '디카페인 아메리카노에 바닐라의 부드러운 향과 달콤함을 조화롭게 담아낸 커피.', '디카페인 카페라떼': '디카페인 에스프레소와 부드러운 우유가 어우러져 고소한 풍미를 완성한 라떼.', '디카페인 카푸치노': '디카페인 에스프레소 위에 올려진 우유 거품, 그리고 시나몬 파우더로 완성한 \n조화로운 맛의 커피.', '디카페인 바닐라라떼': '디카페인으로 즐기는 바닐라의 짙은 향과 풍부한 폼 밀크의 조화가 인상적인 달콤한 라떼.', '디카페인 헤이즐넛 라떼': '부드러운 카페라떼에 헤이즐넛의 풍부한 향과 달콤함을 담아 향긋하게 즐길 수 있는 \n디카페인 라떼.', '디카페인 카라멜마끼아또': '폼 밀크 속에 진한 디카페인 에스프레소와 달콤한 카라멜을 가미해 부드럽게 즐기는 커피', '디카페인 연유라떼': '디카페인 에스프레소 샷, 부드러운 우유 그리고 달콤한 연유가 조화롭게 어우러진 라떼.', '디카페인 카페모카': '초코를 만나 풍부해진 디카페인 에스프레소와 고소한 우유, \n부드러운 휘핑크림까지 더해 달콤하게 즐기는 커피.', '디카페인 티라미수라떼': '디카페인 에스프레소와 티라미수 소스 & 우유 그리고 풍미를 더해주는\n달달한 크림까지 곁들여 완성한 티라미수 라떼.', '디카페인 메가리카노': "메가MGC커피 디카페인 아메리카노를 '960ml' 더 크고 가볍게 즐길 수 있는 대용량 커피", '딸기라떼': '산뜻하고 달콤한 딸기가 부드러운 우유와 어우러져 더욱 기분 좋게 즐기는 아이스 라떼.', '딸기쿠키프라페': '부드러운 바닐라와 달달한 딸기, 바삭한 오레오 쿠키가 달콤한 하모니를 선물하는 프라페.', '콜드브루디카페인': '카페인을 줄였지만, 원두 본연의 향미를 풍부하게 살려 맛을 잡은 디카페인 콜드브루.', '콜드브루디카페인라떼': '우유와 만나 부드럽고 고소한 풍미가 더해진 콜드브루 디카페인 라떼.', '에스프레소': '메가MGC커피 원두의 향미를 온전히 즐길 수 있는 에스프레소', '에스프레소 도피오': '더블샷으로 더욱 진하게 즐길 수 있는 에스프레소', '젤라또 아포가토': '바닐라 젤라또에 진한 에스프레소를 부어 만든 디저트', '쿠키프라페': '바삭하고 달콤한 오레오와 고소한 우유, 부드러운 바닐라향의 조화를 느낄 수 있는 프라페.', '고구마라떼': '달콤하고 고소한 고구마와 부드러운 우유가 만나 누구나 즐기기 좋은 든든한 라떼.', '곡물라떼': '우유에 곡물을 더해 고소하고 든든하게 즐기는 라떼.', '메가초코': '부드러운 우유에 진한 초코소스, 달콤한 휘핑크림의 삼박자 조화로 완성한 달콤 초코 음료.', '토피넛라떼': '은은하게 퍼지는 카라멜의 달달한 향기와 견과의 고소함을 한입에 즐길 수 있는 라떼.', '오레오초코라떼': '진한 초코와 리얼 오레오를 블렌딩해 씹는 맛을 더한 달콤한 아이스 라떼.', '흑당버블밀크티라떼': '타바론 얼그레이 홍차의 깊은 맛을 살린 일크티 라떼에 진한 흑당과 흑당 버블의 달콤함을 채운 음료.', '핫초코': '부드러운 우유에 진한 초코소스가 어우러져 달콤하게 입맛을 깨우는 초콜릿 음료.', '녹차라떼': '향긋한 녹차에 우유를 더해 입 안에 부드러운 푸릇함을 선물하는 라떼.', '로얄밀크티라떼': '우유와 은은한 홍차가 어우러져 부드럽고 향긋한 한 모금을 완성한 라떼.', '흑당라떼': '모리셔스의 진한 흑당과 부드러운 우유가 달콤하게 조화를 이루는 라떼.', '흑당밀크티라떼': '타바론 얼그레이 홍차의 깊은 맛을 살린 일크티 라떼에 진한 흑당의 달콤함을 채운 음료.', '흑당버블라떼': '모리셔스의 진한 흑당과 부드러운 우유가 달콤한 조화에 흑당 버블을 함께 즐기는 라떼.', '아이스초코': '부드러운 우유에 진한 초코소스가 어우러져 달콤하게 입맛을 깨우는 초콜릿 음료.', '아메리카노': '[기본2샷]메가MGC커피 블렌드 원두로 추출한 에스프레소에 물을 더해, 풍부한 바디감을 느낄 수 있는 스탠다드 커피.', '티라미수라떼': '에스프레소와 티라미수 소스 & 우유 그리고 풍미를 더해주는 달달한 크림까지 곁들여 완성한 티라미수 라떼.', '메가리카노': "깊고 진한 메가MGC커피 아메리카노를 '960ml' 더 큼직하게 즐길 수 있는 대용량 커피.", '꿀아메리카노': '아메리카노의 묵직한 바디감에 달콤한 사양벌꿀이 소프트하게 어우러진 커피.', '바닐라라떼': '바닐라의 짙은 향과 풍부한 폼 밀크의 조화가 인상적인 달콤한 라떼.', '바닐라아메리카노': '아메리카노에 바닐라의 부드러운 향과 달콤함을 조화롭게 담아낸 커피.', '연유라떼': '향기로운 에스프레소 샷, 부드러운 우유 그리고 달콤한 연유가 조화롭게 어우러진 라떼.', '카라멜마끼아또': '폼 밀크 속에 진한 에스프레소와 달콤한 카라멜을 가미해 부드럽게 즐기는 커피.', '카페라떼': '진한 에스프레소와 부드러운 우유가 어우러져 고소한 풍미를 완성한 라떼.', '카페모카': '초코를 만나 풍부해진 에스프레소와 고소한 우유, 부드러운 휘핑크림까지 더해 달콤하게 즐기는 커피.', '카푸치노': '에스프레소 위에 올려진 우유 거품, 그리고 시나몬 파우더로 완성한 조화로운 맛의 커피.', '콜드브루라떼': '콜드브루에 고소한 우유를 섞어, 깔끔함과 부드러움을 잡은 라떼.', '콜드브루오리지널': '차가운 물에 장시간 우려내 깔끔한 목넘김을 느낄 수 있는 콜드브루.', '헤이즐넛라떼': '부드러운 카페라떼에 헤이즐넛의 풍부한 향과 달콤함을 담아 향긋하게 즐길 수 있는 라떼.', '헤이즐넛아메리카노': '아메리카노에 헤이즐넛의 풍성한 향과 달콤함을 담아 향긋하고 부드럽게 즐기는 커피.', '큐브라떼': '연유를 섞은 라떼에 에스프레소를 얼린 커피큐브를 올려, 녹을수록 더 진한 커피가 느껴지는 라떼.', '녹차프라페': '향긋한 녹차 위에 우유와 휘핑크림을 더해 더 부드럽게 즐길 수 있는 프라페.', '딸기요거트스무디': '요거트의 상큼함과 딸기의 상큼함을 상냥하게 어우른 상큼 스무디.', '딸기퐁크러쉬': '바삭하고 달달한 퐁에 상큼한 딸기와 부드러운 우유, 얼음을 함께 블렌딩해 시원하게 즐기는 프라페.', '리얼초코프라페': '진한 초코소스와 부드러운 바닐라향의 만남으로 질리지 않는 달콤함을 완성한 프라페.', '망고요거트스무디': '열대과일 망고의 진한 단 맛과 산뜻한 요거트의 하모니가 인상적인 스무디.', '민트프라페': '상쾌한 민트에 달콤하게 씹는 재미를 더한 초콜릿칩의 즐거운 하모니가 매력적인 프라페.', '바나나퐁크러쉬': '바삭하고 달달한 퐁에 부드러운 바나나와 우유, 얼음을 함께 블렌딩해 부드럽고 시원하게 즐기는 프라페.', '스트로베리치즈홀릭': '상큼한 딸기 요거트 스무디 위에 고급스런 맛의 치즈케이크가 듬뿍 올라가 먹는 재미를 배가한 스무디.', '초코허니퐁크러쉬': '리얼 벌꿀이 들어가 더 달콤한 퍼프허니 시리얼과 부드럽게 달달한 초코가 함께 만드는 즐거운 맛의 프라페.', '커피프라페': '바삭한 쿠키와 부드러운 바닐라에 향긋한 에스프레소를 섞어 만든 힐링 프라페.', '플레인요거트스무디': '더 시원하게 요거트의 새콤달콤한 맛을 오롯이 만끽할 수 있는 스무디.', '슈크림허니퐁크러쉬': '바닐라빈 향을 머금은 부드러운 슈크림과 리얼 벌꿀이 들어간 퍼프허니 시리얼을 시원하게 즐기는 프라페.', '플레인퐁크러쉬': '우유에 죠리퐁 씨리얼이 믹싱 된 얼음을 갈아 만든 시원한 프라페음료', '라임모히또': '상큼한 라임과 달콤한 향기의 애플민트가 어우러져 상쾌함을 한잔에 가득 채운 모히또 음료.', '레몬에이드': '시트러스향 가득한 레몬의 상큼함과 톡쏘는 탄산의 상쾌함이 만난 청량 에이드.', '블루레몬에이드': '레몬에이드의 상큼한 청량감에 블루큐라소의 진한 향미를 더한 에이드.', '자몽에이드': '자몽의 달콤쌉싸름한 맛과 탄산의 톡쏘는 목넘김이 어우러진 트로피컬 에이드.', '청포도에이드': '산뜻한 청포도와 상쾌한 탄산의 달달한 조화가 인상적인 에이드.', '유니콘매직에이드 (핑크)': '섞으면 마법처럼 색이 변하는 재미에 레몬의 상큼함으로 입까지 즐거운 이색 에이드.', '유니콘매직에이드 (블루)': '섞으면 마법처럼 색이 변하는 재미에 라임의 청량함으로 입까지 즐거운 이색 에이드.', '체리콕': '체리의 새콤함과 청량감을 동시에 즐길 수 있는 환상적인 에이드.', '메가에이드': '상큼한 레몬, 상쾌한 라임, 달콤쌉싸름한 자몽의 3색 맛을 한데 어우른 메가MGC커피 시그니처 에이드.', '녹차': '고소한 감칠맛과 부드러운 목넘김으로 산뜻하게 마음을 위로하는 국내산 녹차.', '사과유자차': '애플티의 향긋함과 유자청의 상큼달콤함을 한컵에 담아낸 과일티.', '얼그레이': '홍차 특유의 풍부한 플레이버를 만끽할 수 있는 허브티.', '캐모마일': '마음을 진정 시켜주는 산뜻한 풀내음을 느낄 수 있는 허브티.', '페퍼민트': '멘톨향의 묵직한 청량감, 상쾌한 맛과 향이 인상적인 허브티.', '복숭아아이스티': '깊은 맛의 홍차와 달콤한 복숭아의 은은한 향이 어우러진 시원한 여름철 인기 음료.', '유자차': '비타민이 가득 든 상큼달콤한 유자를 듬뿍 넣어 향긋한 즐거움을 전하는 과일티.', '레몬차': '상큼한 레몬의 맛과 향을 오롯이 살린 비타민C 가득한 과일티.', '자몽차': '달콤쌉싸름한 자몽의 조화로운 맛을 한 잔 가득 느낄 수 있는 과일티.', '허니자몽블랙티': '달콤한 꿀청에 재운 자몽에 홍차의 부드러움을 어우른 상큼한 과일티.'}
menu_food = {'추카포카 미니언즈 파티 홀케이크': '[한정판매] 떠들썩한 파티타임엔 꾸덕하고 진한 초코가나슈, 달콤한 초코크림, 부드러운 우유크림이 레이어링된 미니언즈 케이크', '따끈따끈 간식꾸러미': '겨울 대표 간식 팥&슈크림 붕어빵과 앙버터호두과자, 꿀을 가득 머금은 미니호떡으로 구성된 돌아온 따끈따끈 간식꾸러미', '초코스모어쿠키': '초코칩이 콕콕 박힌 촉촉한 초코 쿠키에 달콤하게 구운 마시멜로우가 만나 더 진한 초코 맛 쿠키.', '와앙 피자 보름달빵': '한끼로도 든든한 중독적인 추억의 와앙 큰 소시지 피자빵', '와앙 콘마요 보름달빵': '톡톡 터지는 옥수수콘이 매력적인 와앙 큰 콘치즈마요 보름달빵', '뚱크림치즈약과쿠키': '쿠키 안에 바닐라맛 크림치즈  가득!\n달달하고 꾸덕한 약과가 통째로 올라간 쫀득한 쿠키', '오트밀 팬케이크': '건강한 오트밀가루로 만든 팬케이크에 달콤한 메이플 시럽과 프레지덩 버터, 쥬에그 과일잼이 더해진 팬케이크', '티라미수 팬케이크': '에스프레소의 향이 느껴지는 달콤한 팬케이크에 크리미한 크림이 가득 올라간 부드러운 티라미수 팬케이크', '그래놀라 스모어 쿠키': '그래놀라가 콕콕 박힌 통곡물 쿠키에 \n달콤하게 구운 마시멜로우가 만나 더욱 건강한 쿠키', '버터버터소금빵': '고소한 프랑스산 프레지덩 버터를 듬뿍넣어 더 부드럽고 짭쪼롬하게 즐길 수 있는 베이커리 메뉴', '크루아상': '바삭하고 부드러운 식감에 고소한 버터향을 가득 담은 베이커리 메뉴.', '말차스모어쿠키': '화이트 초코칩이 가득 박힌 말차 쿠키에 달콤하게 구운 마시멜로우를 얹어 달콤쌉싸름한 매력을 간직한 쿠키.', '마카다미아 쿠키': '고소한 마카다미아를 넣어 만든 메가MGC커피 시그니처 쿠키.', '초콜릿칩 쿠키': '진한 초콜릿칩을 넣어 만든 메가MGC커피 시그니처 쿠키.', '플레인크로플': '버터풍미가 가득한 크루와상의 바삭함과 와플의 부드러움을 합친 겉바속촉 베이커리 메뉴.', '아이스크림크로플': '따뜻하고 바삭한 크로플 위에 차갑고 달콤한 바닐라 아이스크림을 올려 만든 매력적인 베이커리 메뉴.', '아이스허니와앙슈': '꿀을 섞은 크림을 바삭한 쿠키슈 안에 넣어, 건강하고 맛있게 완성한 디저트.', '크로크무슈': '고소한 식빵 사이에 햄과 치즈를 샌드하고, 빵 윗면에 멜팅치즈를 토핑해 든든한 한끼를 선물하는 샌드위치.', '몽쉘케이크': '진하고 폭신한 초콜릿 스펀지 사이에 부드러운 생크림이 듬뿍 들어간 몽쉘 케이크.', '햄앤치즈샌드': '햄과 치즈의 조화로운 한끼를 만끽할 수 있는 메가커피 샌드위치.'}
menu_product = {'미니언즈 틴토이': '[한정판매] 미니언즈 콜렉터라면 수집욕구 뿜뿜! 틴케이스로 활용 가능한 랜덤 틴토이!', '미니언즈 콜드컵': '[한정판매] 메가MGC커피와 함께라면 미니언즈 콜드컵도 640ml 대용량', '미니언즈 머들러': '[한정수량] 스테인리스로 만들어 내구성이 강한 미니언즈 머들러로 귀여운 홈카페 완성!', '엠지씨 머그(옐로우)': '귀여운 디테일로 소장가치를 더한 대용량 머그', 'MGC 텀블러(웜그레이)': '뛰어난 보온보냉력으로 하루종일 그대로, MGC 데일리 텀블러', 'MGC 텀블러(옐로우)': '뛰어난 보온보냉력으로 하루종일 그대로, MGC 데일리 텀블러', 'MGC 텀블러(스카이)': '뛰어난 보온보냉력으로 하루종일 그대로, MGC 데일리 텀블러', '메가 엠지씨 스틱 오리지날 아메리카노': '예가체프 원두의 레드와인을 연상케 하는 깊은 풍미, 화이트 초콜릿의 고급스런 단 맛에 풍부한 바디감을 더해 밸런스 잡힌 맛을 느낄 수 있는 아메리카노', '메가 엠지씨 스틱 디카페인 아메리카노': '물의 삼투압을 이용한 독일 워터 프로세스 방식으로 카페인을 줄이고,브라질 원두 특유의 산미와 달콤함, 바디감은 고스란히 담아 조화로운 맛을 느낄 수 있는 아메리카노', '메가 엠지씨 스틱 스테비아 믹스커피': '무지방 우유가 함유된 프리마로 커피 본연의 맛은 배가시키고대체 감미료 스테비아로 당과 칼로리를 낮춰 부담 없이 달콤한 라떼의 맛을 즐길 수 있는 믹스커피', '메가 엠지씨 스틱 스테비아 디카페인 믹스커피': '무지방 우유가 함유된 프리마로 커피 본연의 맛은 배가시키고\n대체 감미료 스테비아로 당과 칼로리는 낮춘 \n디카페인임에도 밸런스 잡힌 스테비아 디카페인 믹스커피', '메가 엠지씨 티플레저 블루밍 캐모마일': '마음의 안정과 여유를 주는 은은하고 향긋한 캐모마일의 꽃향과 \n싱그러운 레몬그라스, 비타민C가 풍부한 사과를 블렌딩한 \n디카페인 캐모마일 블렌딩 티', '메가 엠지씨 티플레저 프루티 루이보스': '무게감 있으면서도 개운하고 깔끔한 전세계 4% 클래식 등급 루이보스와\n비타민C가 풍부한 제주도산 귤피, 전남 고흥산 유자를 블렌딩한\n디카페인 루이보스 블렌딩 티', '메가 엠지씨 티플레저 스위트 히비스커스': '상큼한 히비스커스에 비타민C, 비타민E가 풍부한 레몬머틀과\n달콤한 패션후르츠향, 천연 감미료 스테비아를 더해 새콤달콤하게 블렌딩한\n디카페인 히비스커스 블렌딩 티', '스테비아 케이스': '천연 감미료 스테비아 1gx40개입 케이스.', '콜드브루 원액': '집에서도 간편하게 콜드브루 커피의 맛을 느낄 수 있는 상품.', '텀블러(화이트)': '기능성과 비주얼을 다잡은 메가MGC커피 텀블러.', '텀블러(실버)': '기능성과 비주얼을 다잡은 메가MGC커피 텀블러.', '텀블러(브론즈)': '기능성과 비주얼을 다잡은 메가MGC커피 텀블러.', '머그(옐로우)': '일상 어디서든 활용하기 좋은 메가MGC커피 대용량 머그컵.'}
menu_str_1 = """ 
스모어 블랙쿠키 프라페	4,400원
스모어 카라멜쿠키 프라페	4,400원
코코넛커피 스무디	4,800원
플레인퐁 크러쉬	3,900원
초코허니퐁 크러쉬	3,900원
슈크림허니 퐁크러쉬	3,900원
딸기퐁 크러쉬	3,900원
바나나퐁 크러쉬	3,900원
쿠키프라페	3,900원
딸기쿠키 프라페	3,900원
민트프라페	3,900원
커피프라페	3,900원
리얼초코프라페	3,900원
녹차프라페	3,900원
스트로베리 치즈홀릭	4,500원
플레인요거트 스무디	3,900원
딸기요거트 스무디	3,900원
망고요거트 스무디	3,900원
스노우 샹그리아 에이드	3,900원
레드오렌지 자몽주스	4,000원
샤인머스캣 그린주스	4,000원
딸기주스	4,000원
딸기바나나 주스	4,000원
메가에이드	3,900원
레몬에이드	3,500원
블루레몬 에이드	3,500원
자몽에이드	3,500원
청포도에이드	3,500원
유니콘매직에이드 (핑크)	3,800원
유니콘매직에이드 (블루)	3,800원
체리콕	3,300원
라임모히또	3,800원
따끈따끈 간식꾸러미	3,900원
초코스모어 쿠키	2,900원
뚱크림치즈약과쿠키	3,300원
와앙 피자 보름달빵	3,900원
와앙 콘마요 보름달빵	3,900원
오트밀 팬케이크	4,400원
티라미수 팬케이크	4,400원
그래놀라 스모어쿠키	2,900원
크로크무슈	3,800원
버터버터소금빵	3,200원
햄앤치즈샌드	2,000원
아이스허니 와앙슈	2,400원
몽쉘케이크	5,300원
말차스모어 쿠키	2,900원
플레인크로플	2,500원
아이스크림 크로플	3,500원
머그(옐로우)	9,000원
메가엠지씨스틱 오리지날 아메리카노	4,100원
메가엠지씨스틱 디카페인 아메리카노	4,900원
메가엠지씨스틱 스테비아 믹스커피	4,800원
메가 엠지씨 스틱 스테비아 디카페인 믹스커피	5,400원
스테비아 케이스	5,900원
메가 엠지씨 티플레저 블루밍 캐모마일	9,500원
메가 엠지씨 티플레저 프루티 루이보스	9,500원
메가 엠지씨 티플레저 스위트 히비스커스	9,500원
MGC 텀블러(웜그레이)	19,800원
MGC 텀블러(옐로우)	19,800원
MGC 텀블러(스카이)	19,800원
텀블러(실버)	15,000원
텀블러(브론즈)	15,000원
텀블러(화이트)	15,000원
"""
def get_description(menu_name, menu):
    # 공백을 제거한 menu_name
    normalized_menu_name = menu_name.replace(" ", "")

    # menu_beverage 딕셔너리를 순회
    for key, value in menu.items():
        # 키에서 공백 제거
        originkey = key
        normalized_key = key.replace(" ", "")
        # 공백이 제거된 menu_name과 key가 일치하면 해당 value 반환
        if normalized_menu_name == normalized_key:
            value = value.replace("\n"," ")
            return value, originkey

    # 일치하는 항목이 없을 경우 None 반환
    return None, None


two_menu = menu_str_2.split("\n")
two_menu = [i.strip() for i in two_menu]
one_menu = menu_str_1.split("\n")
one_menu = [i.strip() for i in one_menu]
menudicttwo = dict()
menutwolist = []
menudictone = dict()
menuonelist = []
menu = []
def merge_dictionaries(*dicts):
    merged_dict = {}
    for dictionary in dicts:
        merged_dict.update(dictionary)
    return merged_dict
def price_indicate(list):
    answer = ""
    if (list[0]!="0원") and (list[1]!="0원"):
        answer = "both"
    elif (list[0]=="0원") and (list[1]!="0원"):
        answer = "onlyice"
    elif (list[0]!="0원") and (list[1]=="0원"):
        answer = "onlyhot"
    elif (list[0]=="0원") and (list[1]=="0원"):
        answer = "no_temperature"
    return answer
for t in two_menu:
    a = re.findall(pattern,t)
    b = re.search(pattern,t)
    category = ""
    if b is not None:
        a.append('0원')
        menu_name = t[:b.start()-1].replace('\t','')
        menu_type = price_indicate(a)
        if menu_name in category2.keys():
            category = category2[menu_name]
            previous_category = category
        else:
            category = previous_category
        new_description = merge_dictionaries(menu_beverage,menu_food,menu_product)
        description, key = get_description(menu_name, new_description)
        img_file = key + ".jpg"
            
        this_menu_info = {"menu_name":menu_name, 
                          "menu_category":category, 
                          "menu_price":a,
                          "menu_type":menu_type,
                          "description":description,
                          "img_path":img_file
                          }

        menu.append(this_menu_info)
for t in one_menu:
    a = re.findall(pattern,t)
    b = re.search(pattern,t)
    category = ""
    if b is not None:
        a.insert(0, '0원')
        a.insert(0, '0원')
        menu_name = t[:b.start()-1].replace('\t','')
        menu_type = price_indicate(a)
        if menu_name in category1.keys():
            category = category1[menu_name]
            previous_category = category
        else:
            category = previous_category
        new_description = merge_dictionaries(menu_beverage,menu_food,menu_product)
        description, key = get_description(menu_name, new_description)
        img_file = key + ".jpg"
        this_menu_info = {"menu_name":menu_name, 
                          "menu_category":category, 
                          "menu_price":a,
                          "menu_type":menu_type,
                          "description":description,
                          "img_path":img_file
                          }

        menu.append(this_menu_info)
        
print(menu)