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



<br>
<br>
<details>
<summary>🚀 API 호출 테스트 결과</summary>
<div markdown="1">

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
#### ➡️ [기본 URL](https://13.124.49.137/) <br>

<br>

## ✔️ Test Case 

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

