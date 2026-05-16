import sys
import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path 
from dotenv import load_dotenv

# 비동기
import asyncio
import aiohttp

GRID_FILE = Path(__file__).parent / "grid.json"

def load_env():
    load_dotenv()
    keys = {
        "KMA_SERVICE_KEY": os.getenv("KMA_SERVICE_KEY"),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
    }
    missing = [k for k , v in keys.items() if not v]
    if missing:
        print(f"환경변수 누락 : {', '.join(missing)}")
        print(".env 파일을 확인하시오")
        sys.exit(1)
    return keys

# grid.json 읽기
def load_grid():
  with open(GRID_FILE, "r", encoding="utf-8") as f:
    return json.load(f)

# ai model load
def load_model():
    from llama_cpp import Llama
    return Llama(model_path=os.getenv("MODEL_PATH"), n_ctx=1024, verbose=False, chat_format="chatml")

# 지역 검색 (where, where 지역 -> 하위 지역 출력 )
def where(grid, keyword):
        if keyword in grid:
            regions = [k for k in grid[keyword] if k != "_default"]
            print(f"{keyword}: {', '.join(regions)}")
        else:
            found = []
            for sido, subs in grid.items():
                for name in subs:
                    if name != "_default" and keyword in name:
                        found.append(f"{sido} {name}")
            if found:
                print('\n'.join(found))
            else:
                print(f"검색 결과 없음: {keyword}")

# 브리핑 생성 (2단계)
def generate_briefing(llm, region, weather):
    if weather["pty"] != "없음":
        status = weather["pty"]
    else:
        status = weather["sky"]

    # 1단계: 생활 조언 추출
    step1 = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 날씨 브리핑 도우미야. 날씨 데이터를 보고 생활 조언을 해줘. 해당되는 것만 말하고 필요 없는 건 생략해."},
            {"role": "user", "content": (
                f"{region} 오늘 날씨: 기온 {weather['tmp']}도(최저 {weather['tmn']}/최고 {weather['tmx']}), "
                f"{status}, 강수확률 {weather['pop']}%, 습도 {weather['reh']}%, 풍속 {weather['wsd']}m/s. "
                f"옷차림, 우산, 가습기, 열사병 주의, 난방 중 해당되는 것만 조언해줘."
            )}
        ],
        max_tokens=250,
        repeat_penalty=1.3,
        stop=["<|im_end|>", "<|im_start|>", "<||im_end|>"], # 경량모델 특성상 시그널 토큰을 처리하지 못함
    )["choices"][0]["message"]["content"].strip()

    # 2단계: 말투 보정
    step2 = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 문장을 부드럽고 친근하게 다듬는 도우미야. 내용은 바꾸지 말고 말투만 다듬어줘."},
            {"role": "user", "content": step1}
        ],
        max_tokens=250,
        repeat_penalty=1.3,
        stop=["<|im_end|>", "<|im_start|>", "<||im_end|>"],
    )["choices"][0]["message"]["content"].strip()

    return step2


# 격자좌표 찾기 
def find_grid(grid, region):
    if region in grid:
        return grid[region]["_default"]
    for sido, subs in grid.items():
        if region in subs:
            return subs[region]
    return None 

# 기상청 api 호출
def fetch_weather(service_key, nx, ny):
    now = datetime.now()
    # 기상청 발표 시각이 따로 있음. 
    base_times = ["0200", "0500", "0800", "1100", "1400", "1700", "2000", "2300"]
    
    # 기상청 발표 이후에 40분 간격 뒀음 
    ref = now - timedelta(minutes=40)
    base_date = ref.strftime("%Y%m%d") # 20260516 년/월/일 포멧
    hour = ref.strftime("%H00") # 시각 + 00 붙임 
    
    base_time = "2300"
    for t in base_times:
        if t <= hour:
            base_time = t

    if base_time == "2300" and hour < "2300":
        base_date = (ref - timedelta(days=1)).strftime("%Y%m%d")

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": service_key,
        "numOfRows": "300",
        "pageNo": "1",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    items = data["response"]["body"]["items"]["item"]
    today = now.strftime("%Y%m%d")
    now_hour = now.strftime("%H00")

    result = {}
    for item in items:
        cat = item["category"]
        # 최저/최고 기온
        if cat in ("TMN","TMX") and item["fcstDate"] == today:
            result[cat] = item["fcstValue"]
        # 나머지 항목들
        elif cat in ("TMP","SKY","PTY","POP","REH","WSD"):
            if item["fcstDate"] == today and item["fcstTime"] >= now_hour:
                result.setdefault(cat,item["fcstValue"])
    
    sky = {"1": "맑음", "3": "구름많음", "4": "흐림"}
    pty = {"0": "없음", "1": "비", "2": "비/눈", "3": "눈", "4": "소나기"}

    return {
        "tmp": result.get("TMP", "?"),
        "tmn": result.get("TMN", "?"),
        "tmx": result.get("TMX", "?"),
        "sky": sky.get(result.get("SKY", ""), "?"),
        "pty": pty.get(result.get("PTY", ""), "?"),
        "pop": result.get("POP", "?"),
        "reh": result.get("REH", "?"),
        "wsd": result.get("WSD", "?"),
    }

# 봇파더로 텔레그램 전송및 받아보기 
async def send_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = { "chat_id":chat_id, "text":message}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return resp.status == 200


# 메인
async def main():
    args = sys.argv[1:]

    if not args:
        print("사용법: todayW <지역명> / todayW where <키워드>")
        return

    grid = load_grid()

    # where 모드
    if args[0] == "where":
        if len(args) < 2:
            print("사용법: todayW where <키워드>")
            return
        where(grid, args[1])
        return

    # 날씨 조회
    region = args[0]
    coord = find_grid(grid, region)
    if coord is None:
        print(f"'{region}' 지역을 찾을 수 없음. todayW where <키워드>로 검색해보세요.")
        return

    env = load_env()
    weather = fetch_weather(env["KMA_SERVICE_KEY"], coord[0], coord[1])

    # 메시지 1: 날씨 데이터
    if weather["pty"] != "없음":
        status = weather["pty"]
    else:
        status = weather["sky"]

    msg_weather = (
        f"[{region} 오늘 날씨]\n"
        f"하늘: {status}\n"
        f"기온: {weather['tmp']}도 (최저 {weather['tmn']} / 최고 {weather['tmx']})\n"
        f"강수확률: {weather['pop']}%\n"
        f"습도: {weather['reh']}% | 풍속: {weather['wsd']}m/s"
    )

    # 메시지 2: 브리핑 생성
    llm = load_model()
    msg_briefing = generate_briefing(llm, region, weather)

    print(msg_weather)
    print()
    print(msg_briefing)

    # 텔레그램 전송 (2건)
    token = env["TELEGRAM_BOT_TOKEN"]
    chat_id = env["TELEGRAM_CHAT_ID"]
    ok1 = await send_telegram(token, chat_id, msg_weather)
    ok2 = await send_telegram(token, chat_id, msg_briefing)

    if ok1 and ok2:
        print("\n전송 완료")
    else:
        print("\n전송 실패")


if __name__ == "__main__":
    asyncio.run(main())