## KT-SquidGame Read Me

<p align="center">
    <img src="pics/logo-com.svg"/>
</p>
<h4 align="center">드라마 '오징어 게임' 속 컨텐츠를 직접 체험할 수 있는 AI 플랫폼</h4>
<p align="center">
  <a href="#tutorial">Tutorial</a></a> • 
  <a href="#features">Features</a> •  
  <a href="#system-structure">System Structures</a> • 
  <a href="#files">Files</a> • 
  <a href="#contributor">Contributors</a> • 
  <a href="#license">License</a>
</p>
<p align="center">
    이 프로젝트는 2022 KT 하반기 인턴교육 과정 중 진해되었습니다. <br/>
    이 프로젝트는 상업적인 목적이 포함되어 있지 않습니다. 
    이 프로젝트는 팀 '우린깐부잖어'에 의해 개발되었습니다.<br/>
    해당 레포는 'AI 오징어 게임'의 웹 페이지 코드를 저장하고 있습니다.      
</p>




## Tutorial

<h5>해당 코드는 AI 오징어게임의 ◯△☐ 디비디비딥 코드입니다.</h5>
<h5>Teachable Machine을 통해 학습한 AI model을 통해 도형 카드를 인식하여 디비디비딥 게임을 구현했습니다.</h5>
<h5>만약, 컴퓨터가 ◯ 카드를 뽑았을 때, 사용자가 △ 혹은 ☐ 카드를 제시한다면 성공입니다.</h5>
<h5>만약, 컴퓨터가 ◯ 카드를 뽑았을 때, 사용자가 ◯ 카드 제시 혹은 아무도 카드 제시하지 않았다면 실패입니다.</h5>



## Features

<p align="center">
    <h5>1. '무궁화 꽃이 피었습니다' 게임</h5>
	<h5>2. '달고나 깨기' 게임 </h5>
	<h5>3. '◯△☐ 디비디비딥'</h5>
	<h5>4. 랭킹 보기</h5>
</p>


## System Structure
<h5>1. Teachable Machine AI 모델 학습</h5>
<h5>2. 이미지 촬영 및 저장</h5>
<h5>3. 도형 카드 인식</h5>
<h5>4. 도형 카드 class 분류</h5>
<h5>5. 도형 카드 일치여부 확인</h5>
<h5>6. 게임 결과 출력</h5>

## Files
- image : 게임에 필요한 이미지 촬영 후 저장한 이미지가 들어있는 폴더
- templates :  서버 테스트를 위한 index.html 파일이 들어있는 폴더
- keras_model.h5 : Teachable Machine을 통해 학습한 모델 파일
- label : 학습 모델의 label 정보가 들어있는 파일
- main.py : ◯△☐ 디비디비딥 게임을 수행하는 서버
  - timer(): 사진 촬영을 위한 타이머 함수
  - gen_frames(): 동영상을 읽어와서 AI모델을 적용하여 결과를 출력

## Contributor

Maintainer : 윤혜정, 전민준

Contributor : 김남협, 김수연, 김서정, 김주환, 박수정, 유동헌, 윤혜정, 조민호, 전민준, 허나연


## License

MIT License
