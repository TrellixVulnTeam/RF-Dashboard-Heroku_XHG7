import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import seaborn as sns
import subprocess

def draw_meshgrid():
    a = np.arange(start=X[:, 0].min() - 1, stop=X[:, 0].max() + 1, step=0.01)
    b = np.arange(start=y.min() - 1, stop=y.max() + 1, step=0.01)
    # b = np.arange(start=X[:, 1].min() - 1, stop=X[:, 1].max() + 1, step=0.01)

    XX, YY = np.meshgrid(a, b)

    input_array = np.array([XX.ravel(), YY.ravel()]).T
    # input_array = np.array([XX.ravel(), YY.ravel()]).T

    return XX, YY, input_array

X,y=load_diabetes(return_X_y=True)
df=pd.DataFrame(X)
df['target']=y
X=df[9].values.reshape(442,1)
y=df['target'].values
# (n_samples=300,noise=0.2,random_state=20)
X_train,X_test,y_train,y_test=train_test_split(X,y)


st.sidebar.markdown("# Support Vector Regression Dashboard")

# dataset=st.sidebar.selectbox(
#     'Dataset',
#     ('DS1','DS2')
# )

tuning=st.sidebar.radio(
    'Hyper Parameter',
    ('Default Value','Tuning')
)
if tuning=='Tuning':
    st.sidebar.info('Initially, all parameter values are set to default. Change them according to your need.:smiley:')
    kernel=st.sidebar.selectbox(
        'Kernel Type',
        ('rbf','linear','poly','sigmoid','precomputed')
    )

    # if kernel=='poly':
    #     degree=st.sidebar.slider('Degree of the polynomial kernel function (Have to realise)',value=3)
    # else:
    #     degree=0
    #
    # gamma = st.sidebar.selectbox(
    #     'Gamma',
    #     ('scale', 'auto', 'float')
    # )
    #
    # if gamma=='float':
    #     gamma=st.sidebar.number_input('Gamma Value (Have to think about range)')
    #
    # if kernel=='poly' or kernel=='sigmoid':
    #     coef0=st.sidebar.number_input('Coefficient 0 (Have to think about name, range)')
    # else:
    #     coef0=0.0
    #
    # tol=st.sidebar.number_input('Tolerance (Have to think about range)',value=0.001)
    #
    # C=st.sidebar.number_input('C (Regularization Parameter) (Have to think about range <=1)',min_value=0.01,value=1.0)
    #
    # epsilon=st.sidebar.number_input('Epsilon Value',min_value=0.01,value=0.1)
    #
    # shrinking=st.sidebar.selectbox(
    #     'Shrinking',
    #     ('True','False')
    # )
    # if shrinking=='True':
    #     shrinking=True
    # else:
    #     shrinking=False
    #
    # cache_size=st.sidebar.slider('Cache Size (In MB) (Not Working!!)',value=200,max_value=500)
    #
    # verbose=st.sidebar.selectbox(
    #     'Verbose',
    #     ('True','False')
    # )
    # if verbose=='True':
    #     verbose=True
    # else:
    #     verbose=False
    #
    # max_iter=st.sidebar.slider('Maximum Iteration',value=-1,max_value=500,min_value=-1)

    clf=SVR(kernel)
    #,degree,gamma,coef0,C,epsilon,shrinking,cache_size,verbose, max_iter)
else:
    clf=SVR()


fig,ax=plt.subplots()

# sns.scatterplot(X,y)
ax.scatter(X,y)
# ax.scatter(X.T[0],X.T[1],cmap='viridis')
orig=st.pyplot(fig)


if st.sidebar.button('Run Algorithm'):
    with st.spinner('Your model is getting trained..:muscle:'):
        orig.empty()
        clf.fit(X_train,y_train)
        y_pred=clf.predict(X_test)

        XX,YY,input_array=draw_meshgrid()
        # labels=clf.predict(input_array)
        # labels = clf.predict(input_array)

        # ax.plot(y_pred,labels.reshape(XX.shape))
        x=np.linspace(X.min(),X.max(),X.shape[0]).reshape(X.shape)
        # print(x.shape)
        # x.reshape(X_test.shape)
        ax.plot(x,clf.predict(x),color='red')
        # ax.contourf(XX,YY,labels.reshape(XX.shape),alpha=0.3,cmap='rainbow')

        plt.xlabel('Col1')
        plt.ylabel('Col2')
        orig=st.pyplot(fig)
        st.sidebar.subheader("Mean absolute error of the model: "+str(round(mean_squared_error(y_test,y_pred),2)))
    st.success("Done!")
# subprocess = subprocess.Popen(clf,shell=True, stdout=subprocess.PIPE)
# subprocess_return = subprocess.stdout.read()
# print(subprocess_return)