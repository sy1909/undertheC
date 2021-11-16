from django.shortcuts import render
import datetime
import tensorflow
import tensorflow.compat.v1 as tf
import numpy as np
tf.compat.v1.disable_eager_execution()
#exec(open("final_project_ESG/model_load_py.py" , encoding ="UTF8").read())
print('여기는 views 실행이 됐나요')
X = tf.placeholder(tf.float32, shape=[None, 4])
Y = tf.placeholder(tf.float32, shape=[None, 1])
W = tf.Variable(tf.random_normal([4, 1]), name="weight")
b = tf.Variable(tf.random_normal([1]), name="blas")

# 가설을 설정합니다.
hypothesis = tf.matmul(X, W) + b

# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.train.Saver()
model = tf.global_variables_initializer()

# 세션 객체 생성
sess = tf.Session()
sess.run(model)

# 저장된 학습 모델을 파일로부터 불러옵니다.
# 배출권 시세예측 체크포인트 모델
save_path = "./final_project_ESG/model/saved1.cpkt"
saver.restore(sess, save_path)

def index(request):
    print('index 화면 진입')
    return render(request , 'index.html')
    
    
def model_load(request):
    print('예측버튼이 눌렸습니다.')

    #,'석탄가격', '코스피', '원유가격', '전력수요'
    #   203.01     3015.06    82.28      1444840
    # 4가지 변수를 입력 받습니다.
    if request.method == 'POST': 
        avg_temp = request.POST['avg_temp'] #석탄
        min_temp = request.POST['min_temp'] #코스피
        max_temp = request.POST['max_temp'] #원유
        rain_fall = request.POST['rain_fall'] #전력

        price =0        
        # 사용자의 입력 값을 이용해 배열을 만듭니다.
        data = ((avg_temp, min_temp, max_temp, rain_fall), )
        arr = np.array(data, dtype=np.float32)

        # 예측을 수행한 뒤에 그 결과를 출력합니다.
        x_data = arr[0:4]
        dict = sess.run(hypothesis, feed_dict={X: x_data})
        print(dict[0])
        context = {'price' : str(dict[0])}
        
        return render(request , 'index.html' , context)
    

    #,'석탄가격', '코스피', '원유가격', '전력수요'
    #   203.01     3015.06    82.28      1444840    
    
    
    # if request.method == 'POST':   
    # id = request.POST['id']
    # title = request.POST['title']
    # content = request.POST['content'] 
    # writer = request.POST['writer']
    # # 실제 서버에 save에서 생성하는 create 함수
    # bbs = Bbs.objects.get(id = id)
    # bbs.title = title 
    # bbs.content = content
    # bbs.writer = writer
    # bbs.save()
    # return redirect('list')
    #return render(request , 'index.html')