from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import datetime
import tensorflow
import tensorflow.compat.v1 as tf
import numpy as np
tf.compat.v1.disable_eager_execution()
#exec(open("final_project_ESG/model_load_py.py" , encoding ="UTF8").read())
print('여기는 views2 실행이 됐나요')
X = tf.placeholder(tf.float32, shape=[None, 7])
Y = tf.placeholder(tf.float32, shape=[None, 1])
W = tf.Variable(tf.random_normal([7, 1]), name="weight")
b = tf.Variable(tf.random_normal([1]), name="blas")

# 가설을 설정합니다.
hypothesis = tf.matmul(X, W) + b
# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.train.Saver()
model = tf.global_variables_initializer()

# 세션 객체 생성
sess = tf.Session()
sess.run(model)

save_path = "./final_project_ESG/model2/saved_emission.cpkt"
saver.restore(sess, save_path)

def model_load_emission(request):
    if request.method == 'POST': 
        var1 = request.POST['var1'] #석탄
        var2 = request.POST['var2'] #코스피
        var3 = request.POST['var3'] #원유
        var4 = request.POST['var4'] #전력
        var5 = request.POST['var5']
        var6 = request.POST['var6']
        var7 = request.POST['var7']

    price =0        
    # 사용자의 입력 값을 이용해 배열을 만듭니다.
    data = ((var1, var2, var3, var4,var5,var6,var7), )
    arr = np.array(data, dtype=np.float32)

    # 예측을 수행한 뒤에 그 결과를 출력합니다.
    x_data = arr[0:7]
    dict = sess.run(hypothesis, feed_dict={X: x_data})
    print(dict[0])
    context = {'price' : str(dict[0][0])}
    
    return JsonResponse(context,safe = False)