5주차 회고

- ImageNet으로 사전 학습된 ResNet18, VGG16을 불러와 CIFAR-10 분류에 쓰는 전이 학습 흐름을 익혔다. 기존 가중치는 고정하고 마지막 분류층만 바꿔 학습하는 방식이었다.
- 같은 데이터·같은 학습 코드로 ResNet18과 VGG16을 비교해보니, 이번 설정에서는 VGG16이 더 높은 정확도를 보였다. 모델 구조 차이가 성능과 학습 시간에 바로 영향을 준다는 걸 숫자로 확인했다.
- train / val / test를 나누고, epoch마다 val accuracy를 보며 best checkpoint를 저장하는 학습 루프를 직접 짜봤다.
- make_classification으로 만든 가상 데이터에 RandomForest를 적용하고, GridSearch와 RandomSearch로 하이퍼파라미터를 찾아봤다. GridSearch는 후보를 전부 탐색하고, RandomSearch는 일부만 샘플링해서 더 빠르게 좋은 조합을 찾을 수 있다는 차이를 알게 됐다.

- 사전 합성한 데이터에서 system / user / assistant 역할별 대화 형식을 읽고, 학습용 입력으로 바꾸는 방법을 배웠다.
- assistant가 말한 부분만 loss를 계산하도록 label을 -100으로 가리는 방식을 추천받아서 사용해봤다. 
- Embedding, positional embedding, causal mask, MultiheadAttention, FFN으로 작은 Transformer를 직접 구성해봤다. LLM이 다음 토큰을 예측하는 기본 구조를 코드로 한번 더 따라가 보았다.
- 입력을 한 칸 밀어서 다음 토큰을 맞추는 학습 방식과, inference 때는 마지막 토큰 logits에서 argmax로 한 단어씩 이어 붙이는 autoregressive 생성 방식의 연결을 배웠다.
- 이전에 만들어둔 데이터셋을 바탕으로 모델을 직접 학습시켜봤다. 데이터는 1000개만 써서 품질은 아직 별로지만, val loss 기준 early stopping과 checkpoint 저장까지 돌려보며 학습 전체 흐름을 경험했다.
- system 프롬프트에 페르소나를 넣으면 같은 모델도 답변 톤이 달라진다는 걸 확인했다. 프롬프트 설계도 모델 성능만큼 중요하다는 느낌을 받았다.


- 이번주는 학교 프로젝트 마무리와 발표라서 더 보완하지 못하였다. 
- 다음주가 지나면 완전히 KTB에 집중할수있어서 최대한으로 과제를 보완하여 최고의 품질로 만들어보겠다. 


- 추가로 올리기 전에 jsonl 파일을 깃이그노어에 설정을 안해서 커밋이 꼬이는 문제가 발생하였다. 
- 아직 그것을 해결하는법을 몰라서 cursor에 부탁해서 해결했다..
- 이미 커밋된 히스토리를 지워야하는데, soft reset 을 해야한다는것을 알았다. 