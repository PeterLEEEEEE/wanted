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
**회원가입**

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

**로그인**

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
**게시글 작성**
| **이름**       | **data type**  | **body input**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| title    | string | "title" : "post1's title is here" | 글자를 하나 이상 포함해야 한다(공백 불가) |
| content | string | "content" : "content of the post1"   | 글자를 하나 이상 포함해야 하며, 공백 제외 11글자 이상 작성|

