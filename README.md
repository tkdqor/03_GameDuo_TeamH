# 03_GameDuo_TeamH

## ✅ 프로젝트 개요
- 게임의 구조를 알아보는 프로젝트입니다. 기본적인 로그인 로그아웃 기능을 제공하며 특정 게임공간을 여러명의 유저들이 함께 사용할때 충돌이 일어나지 않게 설계하였습니다. <br>
- 기능으로는 레이드의 시작, 종료, 레이드 상태조회, 랭킹조회등을 제공합니다. <br>

<br>

## 📌 과제 분석
<div>
<details>
<summary>과제소개</summary> 
<div markdown="1">
🗣보스레이드 PVE 컨텐츠 관련 아래 6가지 라우터를 REST API 명세서 규칙을 준수하여 구현해주세요. <br>

1. 유저 생성
 
2. 유저 조회
 
3. 보스레이드 상태 조회
 
4. 보스레이드 시작
 
5. 보스레이드 종료
 
6. 랭킹 조회

</div>
</details>

<details>
<summary>요구사항</summary> 
<div markdown="1">

- 유저 생성
  - 중복되지 않는 userId를 생성
  - 생성된 userId를 응답
  
- 유저 조회
  - 해당 유저의 보스레이드 총 점수와 참여기록 응답
  
- 보스레이드 상태 조회
  - 보스레이드 현재 상태 응답
    - canEnter : 입장 가능한지
    - enteredUserId : 현재 진행중인 유저가 있다면, 해당 유저의 id
  - 입장 가능 조건 : 한번에 한 명의 유저만 보스레이드를 진행할 수 있습니다.
    - 아무도 보스레이드를 시작한 기록이 없다면 시작 가능합니다.
    - 시작한 기록이 있다면 마지막으로 시작한 유저가 보스레이드를 종료했거나, 시작한 시간으로부터 레이드 제한시간만큼 경과되었어야 합니다.

- 보스레이드 시작
  - 레이드 시작 가능하다면 중복되지 않는 raidRecordId를 생성하여 isEntered:true와 함께 응답
  - 레이드 시작이 불가하다면 isEntered : false

- 보스레이드 종료
  - raidRecordId 종료 처리
    - 레이드 level에 따른 score 반영
  - 유효성 검사
    - 저장된 userId와 raidRecoridId 일치하지 않다면 예외 처리
    - 시작한 시간으로부터 레이드 제한시간이 지났다면 예외 처리

- 보스레이드 랭킹 조회
  - 보스레이드 totalScore 내림차순으로 랭킹을 조회합니다.

</div>
</details>
</div>

#### ➡️ 분석결과
보스레이드 관련 api는 고려해야 할 예외상황이 많기 때문에, 아래와 같이 api 별로 예외처리를 했습니다.
<details>
<summary>보스레이드 상태조회 api 예외처리</summary> 
<div markdown="1">

1. 레이드 기록들 중, end_time 필드의 값이 없는 기록을 플레이 중이라고 볼 수 있습니다.

2. 비정상적으로 종료된 기록(유저의 컴퓨터가 다운되거나, 꺼지는 등)은 end_time 필드의 값이 없을 수 있습니다.

3. end_time 필드의 값이 없는 기록들 중, enter_time이 현재시각과 비교했을 때 게임 제한 시간보다 이전이라면 비정상 종료된 기록입니다.

<b>결론</b>: 예외 처리 후에도 남은 기록이 있다면, 누군가가 플레이 중이므로, 입장 불가능 응답을 보냅니다.
</div>
</details>

<details>
<summary>보스레이드 시작 api 예외처리</summary> 
<div markdown="1">

1. 보스레이드 상태조회 api와 동일하게, 플레이 중인 유저가 있는지 확인합니다.

2. 플레이 중인 유저가 없다면 게임을 시작하고, 플레이 중인 유저가 있다면 게임 시작 불가능으로 응답합니다. 

3. 동시에 시작을 하려는 유저들이 있는 경우, Redis로 구현한 queue로 문제를 핸들링 합니다.
- 여러 유저가 동시에 게임을 시작하려 해도, queue에 가장 먼저 자신의 정보를 넣은 유저만 게임을 시작할 수 있습니다.
</div>
</details>

<details>
<summary>보스레이드 종료 api 예외처리</summary> 
<div markdown="1">

1. 존재하지 않는 레이드를 종료하려는 경우 400/bad request로 예외 처리 합니다.

2. 관리자와 레이드를 시작한 본인만 보스레이드를 종료 할 수 있습니다.
</div>
</details>

<br>

## 🛠 사용 기술
- API<br>
![python badge](https://img.shields.io/badge/Python-3.9-%233776AB?&logo=python&logoColor=white)
![django badge](https://img.shields.io/badge/Django-4.0.6-%23092E20?&logo=Django&logoColor=white)

- DB<br>
![mysql badge](https://img.shields.io/badge/MySQL-5.7.38-%234479A1?&logo=MySQL&logoColor=white)
![redis badge](https://img.shields.io/badge/redis-7.0-red?logo=redis&logoColor=white)
- 배포<br>
![aws badge](https://img.shields.io/badge/AWS-EC2-%23FF9900?&logo=Amazon%20EC2&logoColor=white)
![docker badge](https://img.shields.io/badge/Docker-20.10.17-%232496ED?&logo=Docker&logoColor=white)
![nginx badge](https://img.shields.io/badge/Nginx-1.23.0-%23009639?logo=NGINX&locoColor=white)
![uwsgi badge](https://img.shields.io/badge/uWSGI-2.0-brightgreen)

- ETC<br>
  <img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=Git&logoColor=white"/>

<br>

## :black_nib: 이슈 관리
![image](https://user-images.githubusercontent.com/96563183/179135162-a8fa2e3d-3ab7-4fe1-8997-90019f8b25db.png)
깃허브 이슈와 간단차트를 통해 태스크 및 일정관리를 했습니다. <br>


<br>

## ✨🍰✨ 코드 컨벤션
<img width="655" alt="pre-commit 완료" src="https://user-images.githubusercontent.com/83942213/178410269-6ab7bfa9-89a0-4a0c-ba9f-038f1e13de1f.png">

Formatter
- isort
- black

Lint
- flake8

로컬에선 pre-commit 라이브러리 사용으로 커밋 전 세가지 라이브러리를 한번에 실행하고 통과되지않을시 커밋이 불가능합니다.
레포지토리에는 github action으로 다시 한번 체크 후, 통과되지 않으면 merge가 block됩니다.

<br>

## 🌟 API 명세서
<img width="1176" alt="스크린샷 2022-07-15 오후 4 35 39" src="https://user-images.githubusercontent.com/76423946/179175389-367d73d6-b0dc-4131-9bec-20cf4f73fad8.png">

- 회원 생성은 두개의 키값인 nickname과 password를 받아서 수행합니다. 예외처리로는 각각의 키값이 6자리를 넘지 못하면 동작되지 않습니다.  
- 회원 로그인은 기본적인 로그인 기능과 로그인이 되는 상황에서 jwt토큰을 함께 요청하고 해당 토큰 값을 response에 같이 반환 합니다.
- 회원 로그아웃은 두가지로 구현하였습니다. 기본적인 장고의 logout()을 사용하되 한가지 경우는 토큰을 반납하면서 blacklist에 등록하고 다른 방법은 토큰 반납이 없이 로그아웃 됩니다.
- 회원조회는 전체조회와 단건조회로 나뉘어집니다. 그냥 문자상으로는 전체 회원의 내용과 특정 회원의 데이터를 보여주는 방식으로 다를 것이라고 생각되지만 전체 조회는 회원 전체의 리스트가 맞지만 단건조회는 회원 개인의 레이드레코드를 같이 서빙해준다는 점이 다릅니다.
- 보스레이드 상태조회는 보스레이드 상태를 조회합니다. 레이드 레코드의 endtime이 현재 시점에서 입력이 안되어있는 필드가 있는지 또 그 필드의 진행시간을 얼마나 지났는지를 판별하여 입장 가능 여부를 판별하게 됩니다.
- 보스레이드 시작은 API호출시 레이드 레코드의 starttime에 지금 시간을 등록하면서 시작하게 됩니다.
- 보스레이드 종료는 PATCH 메소드를 이용해서 보스레이드 시작에서 만든 레이드 레코드의 필드의 내용에서 endtime부분을 변경하게 됩니다.
- 랭킹 확인은 Redis에서 업데이트한 플레이어의 스코어 기록을 재가공하여 플레이어들의 스코어 배열을 정렬하여 받아서 이것을 원하는 랭킹 순위만큼 슬라이싱하여 유저에게 서빙합니다. 동일한 데이터에서 사용자의 닉네임을 이용하여 랭킹을 확인하여 같이 서빙합니다.


<br>
<br>
<details>
<summary>🚀 API 호출 테스트 결과</summary>
<div markdown="1">

- 회원 생성
<img width="994" alt="image" src="https://user-images.githubusercontent.com/89897944/179219478-9dfc392f-33b2-4ab1-b5c9-1cf079ee362d.png">

- 회원 로그인
<img width="1149" alt="image" src="https://user-images.githubusercontent.com/89897944/179219524-86991749-5838-4780-86cf-7a1dc88fc11f.png">

- 회원 로그아웃
<img width="977" alt="image" src="https://user-images.githubusercontent.com/89897944/179219994-549bd82a-d54d-4e0e-8277-36c4a972d9a4.png">

- 회원 로그아웃( 토큰 유지 )
<img width="891" alt="image" src="https://user-images.githubusercontent.com/89897944/179220054-cc50ccae-20da-4616-b40d-af7248da9198.png">

- 전체 회원 조회 : admin 유저만 가능
<img width="910" alt="image" src="https://user-images.githubusercontent.com/89897944/179220138-67f24c97-4b3a-433b-b9f9-f003041c8fec.png">
<img width="987" alt="image" src="https://user-images.githubusercontent.com/89897944/179220324-65764b7d-f03e-4c8c-8f3e-b751a285a730.png">

- 회원 단건 조회 : 회원정보와 해당 회원의 레이드 레코드가 같이 출력
<img width="1082" alt="image" src="https://user-images.githubusercontent.com/89897944/179220461-15805b45-65ee-4eeb-b6ae-c29c13f2887d.png">

- 보스레이드 상태 조회
<img width="932" alt="image" src="https://user-images.githubusercontent.com/89897944/179220513-e4a4734c-5710-4d2f-8448-fbf11393c641.png">

- 보스레이드 시작
<img width="889" alt="image" src="https://user-images.githubusercontent.com/89897944/179220550-ca4c9498-d0aa-4440-8b93-d936cf01ee74.png">

- 보스레이드 종료

- 랭킹 확인
<img width="1053" alt="image" src="https://user-images.githubusercontent.com/89897944/179220633-fa53af23-38b1-48ac-9eef-93664112f734.png">


</div>
</details>

<br>

## 📋 ERD
<img width="399" alt="image" src="https://user-images.githubusercontent.com/89897944/179209834-9b62c161-a7d3-4d9f-947d-dd1265ca6554.png">
최종 모델링입니다. 초기 모델에서는 테이블을 3개로 구성하는 것으로 진행하였으나 redis를 사용하면서 정적파일을 변경사항이 있을때 
가져오는 방식으로 동작 방식을 수정하면서 간소화 되었습니다.

<br>

## 🌎 배포
Docker, NginX, uWSGI를 사용하여 AWS EC2 서버에 배포하였습니다. <br>
➡️ [서비스 주소](http://3.34.126.200/) <br>

### 🖼 서비스 아키텍처
![image](https://user-images.githubusercontent.com/96563183/179229678-0eeca455-3776-4d8a-a6af-2f2a3c7f53a1.png)

<br>

### 📂 디렉토리 구조
![image](https://user-images.githubusercontent.com/96563183/179320826-e175f4cf-3b70-4074-a77f-e253548379e8.png)

<br>

## ✔️ Test Case 
유저 생성 및 로그인, 로그아웃, 유저 조회 API와 보스레이드 상태 조회, 시작, 종료 API TESTCASE 수행
<img width="1088" alt="스크린샷 2022-07-15 오후 6 04 36" src="https://user-images.githubusercontent.com/95380638/179210977-0c61620a-f97b-4600-815a-8c0b428a8ac1.png">



<br>

## 👋 TeamH Members
|Name|Task|Github|
|-----|----|-------|
|고희석|배포, 서버관리|https://github.com/GoHeeSeok00| 
|김민지|보스레이드 관련 API|https://github.com/my970524|
|김상백|테스트 케이스|https://github.com/tkdqor|
|김훈희|유저관련, 랭킹조회 API|https://github.com/nmdkims| 
|이정석|Redis 캐싱|https://github.com/sxxk2|

➡️ [GameDuo 과제 노션 페이지](https://www.notion.so/8940341de3ca468898d177ad08b683aa)

