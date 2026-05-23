# HTTP 내용정리

## 전체 흐름
브라우저 -> HTTP요청 -> 서버 처리 -> HTTP 응답 -> 브라우저 화면 출력 

## URL
```txt
https:// -> 프로토콜(Scheme)
example.com -> 도메인
/post/1/admin -> 리소스 경로(path)
?search=hotnews -> 쿼리 파라미터

```

## HTTP Message
-> 실제 데이터 묶음
- 실제로 어떻게 오는가 (message)
```python
b'POST /posts HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\n{"title":"hello"}'
```

- 이걸 파이썬으로 파싱
```python
def parsing_http(raw_data):
    # bytes -> str 변환
    message = raw_data.decode()
    result = {} # dict 

    # Header / Body 분리
    header_part, body = message.split("\r\n\r\n", 1)
    # 줄 단위 분리
    lines = header_part.split("\r\n")
    # Start Line
    method, path, version = lines[0].split(" ")
    result["method"] = method
    result["path"] = path
    result["version"] = version

    # Headers
    headers = {}
    for line in lines[1:]:
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    result["headers"] = headers

    # Body
    result["body"] = body
    return result
```
- 결과 
```python
{
    'method': 'POST',
    'path': '/posts',
    'version': 'HTTP/1.1',
    'headers': {
        'Host': 'example.com',
        'Content-Type': 'application/json'
    },
    'body': '{"title":"hello"}'
}
```



## HTTP Request Method
| Method | role | exam |
|---|---|---|
| GET | 조회(데이터 위치 URL) | 게시글 조회 |
| Post | 생성(데이터 위치 Body) | 회원 가입 |
| PUT | 전체 수정 | 토큰 초기화 |
| PATCH | 부분 수정 | 비밀번호 변경 |
| DELETE | 삭제 | 게시글 삭제 |

## HTTP Status Code 


| 번호대 | 의미 |
|---|---|
| 1xx | 정보 |
| 2xx | 성공 |
| 3xx | 리다이렉트 |
| 4xx | 클라이언트 오류 |
| 5xx | 서버 오류 |

## 자주 쓰는 코드

| 코드 | 의미 |
|---|---|
| 200 | 성공 |
| 201 | 생성 성공 |
| 204 | 성공했지만 반환 데이터 없음 |
| 400 | 잘못된 요청 |
| 401 | 인증 필요 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 429 | 요청 너무 많음 |
| 500 | 서버 오류 |