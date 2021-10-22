# [위코드 x 원티드] 백엔드 프리온보딩 선발 과제

## 사용한 기술 스택
- python, django

## 구현 내용
- 사용자 인증, 인가(회원가입 및 로그인)
- 게시판 CRUD API 

## 구현 방법
#### 회원가입
- 사용자로부터 이름, 아이디로 쓸 이메일, 비밀번호를 받습니다. 
이메일은 고유하기 때문에 id로 사용하기에 적합하다 판단하여 설정하였습니다.
이름, 이메일, 비밀번호 모두 정규식을 통해 부합하지 않는 데이터에 대한 예외처리를 수행하였습니다.
- 비밀번호는 bcrypt를 통해 hashing하여 저장합니다.

#### 로그인
- 사용자는 이메일, 비밀번호를 통해 로그인합니다.
- 사용자의 원활한 이용을 위해 jwt 토큰을 발행하여 제공합니다.

#### 게시판
- 게시판은 최근 생성된 순으로 보여줍니다.
- 게시글을 작성하기 위해서는 로그인을 해야하고 jwt를 통해 확인합니다. 마찬가지로 게시글의 수정, 삭제도 동일하게 적용됩니다.
- 단순 게시판이나 특정 게시물을 열람하는 것은 로그인을 필요로 하지 않습니다.

## ENDPOINT 
| **METHOD** | **ENDPOINT**   | **body**   | **수행 목적** |
|:------|:-------------|:-----------------------:|:------------|
| POST   | /users/register | email, name, password | 회원가입    |
| POST   | /users/login  | email, password       | 로그인        |
| POST    | /posts/newpost | title, content      | 게시글 작성 |
| GET   | /posts/main        |                   | 게시글 리스트   |
| GET    | /posts/post/<post_id>|                        | 게시글 보기 |
| PATCH  | /posts/post/manage/<post_id> | title, content | 게시글 수정     |
| DELETE | /posts/post/manage/<post_id> |               | 게시글 삭제 |

## API 명세
**1. 회원가입**

| **이름**       | **data type**  | **body input**                          | **처리**|
|:----------|--------|----------------------------|------------------------|
| name     | string | "name" : "peter"            | 영문/한글 2-30글자 사이의 값 입력 |
| email    | string | "email" : "dissgogo@gmail.com" | "@"와 "."을 기준으로 그 사이 2-3글자 포함|
| password | string | "password" : "dlangus123!"   | 영문/한글, 숫자, 특수문자를 각각 하나 이상 포함한 10-20글자 |

<br>

**SUCCESS EXAMPLE**
```
{
'MESSAGE':'SUCCESSFULLY REGISTERED'
}
```
**ERROR EXAMPLE**
```
# body의 일부 미입력 시
{
  'MESSAGE':'KEY_ERROR'
}
```
```
# body 자체가 없을 시
{
  'MESSAGE':'VALUE_ERROR'
}
``` 

---

**2. 로그인**

| **이름**       | **data type**  | **body input**                          | **처리**|
|:----------|--------|----------------------------|------------------------|
| email    | string | "email" : "dissgogo@gmail.com" | "@"와 "."을 기준으로 그 사이 2-3글자 포함|
| password | string | "password" : "dlangus123!"   | 영문/한글, 숫자, 특수문자를 각각 하나 이상 포함한 10-20글자 |

**SUCCESS EXAMPLE**
```
# 로그인 성공(200)
{
  "MESSAGE"   : "SUCCESS",
  "user_name" : "peter", // 로그인한 유저명 반환
  "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.OsMsy8bfdW_gIJetsU2-FjfeeBd5uaiIG2V92ThJiWA", // jwt 토큰
}
```

**ERROR EXAMPLE**
```
# body 일부 미입력 시(400)
{
  "MESSAGE": "KEY_ERROR"
}
```
```
# body 없을 시(400)
{
  "MESSAGE": "VALUE_ERROR"
}
```
```
# 가입된 이메일 존재하지 않을 시(403)
{
  "message": "EMAIL_DOES_NOT_EXISTS"
}
```
```
# 비밀번호가 일치하지 않을 시(403)
{
  "message": "INVALID_PASSWORD"
}
```
---
**3. 게시글 작성**
| **이름**       | **data type**  | **body input**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| title    | string | "title" : "post1's title is here" | 글자를 하나 이상 포함해야 한다(공백 불가) |
| content | string | "content" : "content of the post1"   | 글자를 하나 이상 포함해야 하며, 공백 제외 11글자 이상 작성|

**SUCCESS EXAMPLE**
```
# 생성 성공 시(201)
{
  "MESSAGE": "SUCCESS"
}
```
**ERROR EXAMPLE**
```
# body 일부 미입력 시(400)
{
  'MESSAGE':'KEY_ERROR'
}
```
```
# body 미입력 시(400)
{
  "message": "INVALID DATA FORMAT"
}
```
```
# title 공백만 있고 글자 없을 시(404)
{
  "MESSAGE": "TITLE MUST CONTAIN WORDS"
}
```
```
# content(본문) 공백만 있고 글자 없을 시(404)
{
  {"MESSAGE": "MUST CONTAIN WORDS"}
}
```
```
# content의 길이가 공백 제외 10글자 이하일 시(404)
{
  "MESSAGE": "NEED_MORE_THAN_10_WORDS"
}
```
---
**4. 게시글 리스트 조회**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| page    | string |  posts/main?page=1 | page 위치를 int형으로 입력받는다. 미입력 시 자동으로 1, 0 이하의 숫자 받으면 에러처리 |
  
- page를 query parameter로 전달 받으면 LIMIT을 통해 한 페이지 당 20개의 게시물을 보여줄 수 있게끔 구현

**SUCCESS EXAMPLE**
```
{
    "RESULT": {
        "data": [
            {
                "title": "testtitle2dasd",
                "author": "jack",
                "written": "2021.10.21 11:34",
                "post_id": 3,
                "user_id": 2
            },
            {
                "title": "타이틀만 수정해보는중입니다1",
                "author": "peter",
                "written": "2021.10.20 18:27",
                "post_id": 1,
                "user_id": 1
            }
        ],
        "post_count": 2 // 포스트 개수 카운트하여 전달 
    }
}
```
**ERROR EXAMPLE**
```
# query parameter가 0 또는 음수가 전달되었을 시(404)
{
  "MESSAGE": "MUST START WITH GREATER THAN 0"
}
```
---

**5. 게시글 상세 조회**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id    | string |  posts/post/1 | path parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 반환 |
  
**SUCCESS EXAMPLE**
```
{
    "RESULT": {
        "title": "타이틀만 수정해보는중입니다1", // 게시글 제목
        "author": "peter", // 작성자
        "user_id": 1, // 작성자 id
        "content": "dasdasdasdasd", // 게시글 내용
        "written": "2021.10.20 18:27" // 작성 시간
    }
}
```
**ERROR EXAMPLE**
```
# 게시글이 존재하지 않을 시(404)
{
  "MESSAGE": "POST DOES NOT EXIST"
}
```
---

**6. 게시글 수정**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id   | string |  posts/post/manage/1 | path parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면  |
| title | string | "title": "hi this is updated post"| 타이틀을 수정할 경우 공백을 제외한 글자가 존재하여야 한다 |
| content | string |"content": "hi this is new post content"| 본문을 수정할 경우 공백을 제외한 글자가 11글자 이상 존재하여야 한다|

- PATCH METHOD 사용
- title, content 둘 중 하나만 body에 실어보내도 된다. (title, content 중 하나 선택하여 수정하거나 모두 수정 가능)

**SUCCESS EXAMPLE**
```
# 성공적으로 수정 시(201)
{
  "MESSAGE": "SUCCESSFULLY UPDATED"
}
```

**ERROR EXAMPLE**
```
# body 없을 시(400)
{
  "message": "INVALID DATA FORMAT"
}
```
```
# 해당 게시글이 존재하지 않을 시(404)
{
  "MESSAGE": "POST DOES NOT EXIST"
}
```
```
# 권한이 없는 사용자가 수정하려 할 시(404)
{
  "MESSAGE": "INVALID USER"
}
```
```
# title이 공백만 있고 글자가 없을 시(404)
{
  "MESSAGE": "TITLE MUST CONTAIN WORDS"
}
```
```
# content가 공백만 있고 글자가 없을 시(404)
{
  "MESSAGE": "MUST CONTAIN WORDS"
}
```
```
# content가 공백 제외 10글자 이하일 시(404)
{
  "MESSAGE": "NEED_MORE_THAN_10_WORDS"
}
```

---
 
**7. 게시글 삭제**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id    | string |  posts/post/manage/1 | path parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 삭제 |

- delete METHOD 사용

**SUCCESS EXAMPLE**
```
# 성공 시(204)
{
  "MESSAGE": "SUCCESSFULLY DELETED"
}
```
**ERROR EXAMPLE**
```
# 해당 게시글이 없을 시(404)
{
  "MESSAGE": "POST DOES NOT EXIST"
}
```
```
# 권한없는 사용자가 삭제하려 할 시(404)
{
  "MESSAGE": "INVALID USER"
}
```
  
  
  
