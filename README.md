# ✏Team 노각코

## ✅ 프로젝트 소개

![logo_yw (1)](README.assets/logo_yw (1)-16691708076806.png)

- 프로젝트 개요: 노각코 팀의 스터디 및 다양한 모임 플랫폼
- 프로젝트 명 : CodeBee ( 코드비 )
- 벌집으로 날아드는 벌처럼 모여서 공부하고 꿈을 이루자
- 프로젝트 기간:  2022.11.09 ~ 2022.11.22
- http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com/reviews/

<br>

## 🎯 기획 목표

- 스터디 모임 플랫폼

- 온라인, 오프라인 분류

- 각 스터디 주제, 태그별 카테고리

- 다양한 활동을 위한 모임 플랫폼


<br>

## 🎯 프로젝트 목표

### Frontend

- Django-Template 사용을 통한 템플릿 관리
- **내장 라이브러리 사용 경험** 쌓기
- REST API 활용 능력 향상
- **AWS** 사용을 통한 **동적 사이트** 배포

<br>

### Backend

- Django 사용을 통한 DB 관리
- AWS 사용을 통한 사이트 배포
- Social Login 기능 구현
- 카카오 메시지 기능 추가

<br>

### 📣공통

- 백엔드-프론트엔드 커뮤니케이션 및 통신으로 **협업 경험 쌓기**

<br>

## 👥 팀원 구성

- **Frontend**

  - 안예지
  - 윤효근

  **Backend**

  - 김현중(팀장)
  - 문현동
  - 문상희
  
    <br>

## 🎥 시연 영상

Main

![image-20221123113933436](README.assets/image-20221123113933436.png)

- Login ( 일반가입, 소셜가입 구분 - 구글, 깃헙, 카카오)

![login](README.assets/login.gif)

- Signup ( postcode, 인증을위한 휴대폰, 이메일 )

![signup](README.assets/signup.gif)

![signup2](README.assets/signup2.gif)

- index ( 카테고리별 분류, 카드디자인 )
  ![index](README.assets/index.gif)
- study_detail
  - Select option - 직접입력, select
  - 온라인의 경우 온라인주소
  - 오프라인의 경우 지도에 마커 표시 혹은 주소입력으로 좌표저장
  - 태그 기능 구현 ( 자동완성기능, DB에서 사용자가 사용한 태그들을 불러옴 )

![study_create](README.assets/study_create.gif)

- 스터디 참여신청 > 호스트의 승인 > 활동 종료 > 리뷰 작성 활성화 > 작성 > 수정, 삭제 (비동기)

![study_review](README.assets/study_review.gif)

![study_detail](README.assets/study_detail.gif)

- Accounts_detail ( follow, 활동내역 )

![account_detail](README.assets/account_detail.gif)

- 회원탈퇴 ( 소셜탈퇴, 탈퇴 )

![quit2](README.assets/quit2.gif)

<br>

## 👨‍💻 적용 기술

- Frontend: JavaScript, CSS, Bootstrap, Kakao Map api, Social Login API

- Backend: Python, Django,

- 협업 tool: Git & Github, Notion, Discord, Kanbanboard


<div align="left">
       <img src="https://img.shields.io/badge/Django-green?style=flat&logo=Django&logoColor=092E20"/>
       <img src="https://img.shields.io/badge/Python-blue?style=flat&logo=Django&logoColor=3776AB"/>
       <img src="https://img.shields.io/badge/CSS-pink?style=flat&logo=Django&logoColor=1572B6"/>
       <img src="https://img.shields.io/badge/JavaScript-yellow?style=flat&logo=Django&logoColor=F7DF1E"/>
       <img src="https://img.shields.io/badge/HTML-orange?style=flat&logo=Django&logoColor=E34F26"/>
       <img src="https://img.shields.io/badge/VSCODE-Full%20Stack-purple"/>
       <img src="https://img.shields.io/badge/GITHUB-black?style=flat&logo=Django&logoColor=181717"/>
     </div>
<br>

## 🖊 주 구현 기능

- 회원인증
  - 인증된 회원만 스터디 모집 게시글 작성이 가능
  - 실참여자만 작성 가능한 후기 시스템으로 정보의 정확도를 향상

- 모각코 진행 장소 정보 제공 기능

  - 원하는 지역 주변 정보를 제공

    ex) 강남 스터디,

  - 키워드 검색

- 카카오 메시지 알림 기능

  - 카카오 메시지 알림 기능으로 스터디 활동 편의성 제공
  - 직접 작성 간으한 기능으로 원활한 스터디 진행에 도움

- 유저간 정보 제공

  - Github 등 회원 정보 제공으로 유저간 상호 작용을 활성화

- 스터디 승인 · 거부 · 강퇴 기능

  - 유저 기반의 스터디 자정 작용

  ![image-20221123170954941](README.assets/image-20221123170954941.png)

- 카테고리의 세분화

  - 유저가 필요로 하는 스터디 탐색 기능

  ![image-20221123170933690](README.assets/image-20221123170933690.png)

- <br>

## 💻 팀원별 상세 구현 기능

**김현중**

- Home 작성
  - Home 페이지 대문 구현
  - 스터디 만들기, 참여하기 버튼
  - 스터디 만들기, 참여하기 시 주의사항 안내
  
- Index 온,오프라인 분류
  - 그리드 적용
- Study 만들기
  - 그리드 적용
  - 광고배너, 지도 검색 결과 리스트, 지도 분리
  - Select input, 직접입력 선택시 input 구현
  - 온라인, 오프라인 선택시 타입에 맞는 입력창 제공
    - Label, Placeholder, map display
    - JS 작성
  - Kakao Map api 구현
    - 초기 지도에서 주소 혹은 키워드 검색 기능 구현
    - 검색시 관련 리스트 출력
    - 지도에 마커를 선택하거나 새로운 마커를 찍을 경우 해당 좌표, 도로명 주소 반환
    - 반환된 주소를 자동입력, 마커의 상호명 입력, 위도, 경도 DB에 전송
    - Text Area initial 적용, (스터디 소개 양식 제공)
    - 스터디 시작일 종료일, Study의 외래키로 관리, ( 여러번 스터디 모임 가능 )
    - 해시태그 기능 구현, (Tagify)
      - 자동완성, 기본값 + DB에 있는 이전 사용자들이 사용한 Tag 제공

- Study Detail
  - 모집중인 스터디와 모집이 마감된 스터디 템플릿 분리
  - Detail Front 구현 
    - 스터디 소개 줄바꿈 구현
    - 리뷰 작성탭과 모달로 작성폼 제공
    - DB에 저장된 X,Y (위도,경도)값으로 지도를 띄워줌
  - 카카오 메시지전송 기능 구현
    - 카카오톡 인증 유저 한정
    - 스터디에 가입신청을 했을 경우 스터디장에게 알림메시지 전송
    - 스터디장은 카카오톡 인증된 유저들에게 메시지를 담아 보낼 수 있음
    - 기타 알림등은 추가 예정
- Study Review
  - 리뷰 작성 모달폼 구현
  - 리뷰 수정 및 삭제 비동기 구현
  - 리뷰의 경우 참여자는 한 개의 종료된 스터디에 한 개의 후기만을 작성할 수 있음
  - Front : 버튼숨김, 리뷰는 볼 수 있음
  - Back: 스터디에 참여했고, 한 번만 작성 가능함.


<br>

**안예지**

- 인덱스 페이지(`/reveiws/`)
  - 게시글 카드 디자인
    - 언어 타입 별로 다른 이모지 출력
    - 현재 가입 신청 인원/제한 인원 출력
    - 카드 title 잘리지 않게 ellipse 처리
- 유저 정보 페이지(`/accounts/<int:pk>`)
  - 헤더 이미지
  - 유저가 참여 중인 현재 진행 중 스터디 출력
  - 유저의 활동 내역 출력
    - github, BOJ
    - 스터디 참여 내역 출력, 스터디 언어별 다른 음영 주기
    - 최근 리뷰 활동 카드 디자인
  - 단지 시스템 구현
    - 점수에 따라 단지 이미지 채워지게

<br>

