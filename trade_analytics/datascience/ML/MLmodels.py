from __future__ import division

import numpy as np
import pandas as pd
import collections
import pdb
from scipy import interp
import scipy
import pickle
import os
import json
from scipy.sparse import coo_matrix, hstack ,vstack
import copy
import datascience.models as dtscmd

np.random.seed(1337)  # for reproducibility


###################################################################
####################   KERAS  #####################################
###################################################################
from keras.models import load_model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D,Convolution1D,ZeroPadding1D
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
from keras import __version__ as keras_version
from keras import regularizers
from keras.layers import Dense, Dropout, Activation
from keras.layers.advanced_activations import LeakyReLU,PReLU
from keras.layers.pooling import AveragePooling1D
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from keras import applications
# deep models
from keras.layers import Input
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.inception_v3 import InceptionV3




###################################################################
####################   SKLEARN  #####################################
###################################################################
from sklearn.cross_validation import KFold
from sklearn.metrics import log_loss
from sklearn.externals import joblib
from sklearn.metrics import average_precision_score,accuracy_score,recall_score,precision_score
from sklearn.metrics import log_loss,accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder,LabelEncoder
from sklearn import linear_model,decomposition
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.svm import SVC 
from sklearn.svm import LinearSVC
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold
from itertools import cycle
from sklearn.metrics import roc_curve, auc

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression,SGDClassifier
from sklearn.linear_model import RidgeCV
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score, ShuffleSplit

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC


###################################################################
####################   XGBOOST  #####################################
###################################################################
import xgboost as xgb


###################################################################
####################   Exporting  #####################################
###################################################################




###################################################################
####################   BASE MODELS  #####################################
###################################################################


class BaseClassificationModel(object):
	name=None
	savetype='joblib'
	classification_type='binary'

	def __init__(self):
		pass

	def loadmodel(self,model):
		self.model=model
		path=self.model.modelpath()
		if self.saveformat=='joblib':
			with open(path,'r') as F:
				self.clf=joblib.load(F)
		elif self.saveformat=='keras':
			self.clf = load_model(path)


		if 'validation_metrics' not in self.model.Info:
			self.model.Info['validation_metrics']={}

		return self.clf


	@classmethod
	def GenModels(cls,Project,data):
		pass

	def loaddata(self):
		if self.model.Data.Datatype!='Train':
			raise Exception("Need Training Data For model")
		ParentData=self.model.Data.ParentData
		self.validation_datasets=dtscmd.Data.objects.filter(ParentData=ParentData,Datatype='Validation')
		self.train_data=dtscmd.Data.objects.get( id=self.model.Data.id) 

	def pre_processing_train(self,X,Y):
		return (X,Y)

	def pre_processing_validation(self,X,Y):
		return (X,Y)

	def load_training_data(self):
		X,Y,Meta=self.train_data.getdata()
		return (X,Y)
				
	def validation_shard_iter(self,validation_data):
		shards=dtscmd.DataShard.objects.filter(Data=validation_data)
		for shard in shards:
			X,Y,Meta=shard.getdata()
			yield (X,Y)

	def post_process_model(self):
		pass

	def getfit_args_kwargs(self):
		return ((),{})

	def train(self):
		if self.model.Status=='Trained' or self.model.Status=='Validated':
			print "Model is already trained/validated, so skipping training"
			self.post_process_model()
			return

		try:
			self.model.Status='Running'
			self.model.save()

			X,Y=self.load_training_data()
			X,Y=self.pre_processing_train(X,Y)

			args,kwargs=self.getfit_args_kwargs()

			self.clf.fit(X,Y,*args,**kwargs)

			self.post_process_model()

			self.savemodel()

			self.model.Status='Trained'
			self.model.save()
			print "Training done for ",self.model.id
		except:
			self.model.Status='UnTrained'
			self.model.save()

	def predict(self,X):
		return self.clf.predict(X)

	def Run_validation(self,validation_data):
		Ypred=None
		Yvalid=None
		for X,Y in self.validation_shard_iter(validation_data):
			X,Y=self.pre_processing_validation(X,Y)

			Y1=np.reshape(self.clf.predict(X),Y.shape)
			if Ypred is None:
				Ypred=Y1 
				Yvalid=Y
			else:
				Ypred=np.vstack((Ypred, Y1 ))
				Yvalid=np.vstack((Yvalid, Y ))



		model_metrics=self.getmetrics(Ypred,Yvalid)
		obj, created = dtscmd.ModelMetrics.objects.get_or_create(Data=validation_data,MLmodel=self.model)
		obj.Metrics=model_metrics
		obj.save()
		print "Done with validation id = ",validation_data.id," for model = ",self.model.id



	def Run_validation_all(self):
		for validation_data in self.validation_datasets:
			self.Run_validation(validation_data)

		self.model.Status='Validated'
		self.model.save()

	def Run_validation_id(self,validationid):
		validation_data = self.validation_datasets.get(id=validationid)
		self.Run_validation(validation_data)



	def getmetrics(self,Ypred,Yvalid):

		logloss=log_loss(Yvalid ,Ypred, eps=1e-15, normalize=True)
		avgprec= average_precision_score(Yvalid, Ypred)
		acc= accuracy_score(Yvalid, Ypred )
		recallscore= recall_score(Yvalid, Ypred,average='micro' )
		precisionscore= precision_score(Yvalid, Ypred ,average='micro' )

		model_metrics={'logloss':logloss, 'avgprec':avgprec, 'acc':acc, 'recallscore':recallscore , 'precisionscore':precisionscore }
		return model_metrics


	def savemodel(self):
		if self.model.saveformat=='joblib':
			joblib.dump(self.clf, self.model.modelpath())
		elif self.model.saveformat=='keras':
			self.clf.save(self.model.modelpath())

		self.model.save()


		


###################################################################
####################   XGBOOST  #####################################
###################################################################

class XGBOOSTmodels(BaseClassificationModel):
	name='XGBOOST'
	saveformat='xgboost'

	def savemodel(self):
		filename=self.model.modelpath()
		self.clf.save_model(filename)
		
		self.model.save()

	def loadmodel(self):
		path=self.model.modelpath()
		clf = xgb.Booster() #init model
		clf.load_model(path) # load data

		return clf

	def predict(self,X):
		dtest = xgb.DMatrix(X)
		return self.clf.predict(dtest)

	def train(self):
		X,Y=self.pre_processing_train()

		dtrain = xgb.DMatrix( X, label=Y)
		
		evallist  = [(dtrain,'train')]
		plst=self.model.Misc['modelparas']['plst']
		num_round=self.model.Misc['modelparas']['num_round']
		self.clf.train( plst, dtrain, num_round, evallist )

		self.post_process_model()

	@classmethod
	def GenModels(cls,Project,Data):

		D=Data.gen_one_shard()
		X=D['X']
		Y=D['Y']
		
		N=0
		num_round = 300
		early_stopping_rounds=10
		param = {
					 'silent':1, 'objective':'multi:softmax','num_class':8, 
					'nthread' :6, 'eval_metric':'mlogloss', 'subsample': 0.7, 'colsample_bytree': 0.7,
					'min_child_weight':0, 'booster':"gbtree",
				}

		
		for max_depth in [50,100,250,500]:
			for eta in np.arange(0.1,0.9,0.2):
				for lmda in [0,10,50,100]:

					if Data.ouput_type=='binary:':
						for obj in ['reg:linear','reg:logistic','binary:logistic']:
							param['max_depth']=max_depth
							param['eta']=eta
							param['lambda']=lmda
							param['objective']=obj
							param['max_delta_step']=1
							param['scale_pos_weight'] = Data.Misc['#0']/Data.Misc['#1'] #sum_wneg/sum_wpos

							plst = list(param.items())+[('eval_metric', 'ams@0.15'),('eval_metric', 'auc'),('eval_metric','rmse'),('eval_metric','mae'),('eval_metric','logloss'),('eval_metric','logloss')]
							plst=plst+[('eval_metric','error@%s'%t) for t in np.arange(0,1,0.1) ]
							
							num_round=eta*1000

							dtrain = xgb.DMatrix( X, label=Y)
							evallist  = [(dtrain,'train')]
							plst = param.items()
							bst = xgb.train( plst, dtrain, num_round, evallist )

							modelparas={'param':param,'plst':plst,'num_round':num_round,'early_stopping_rounds':early_stopping_rounds}
							info={'createdbyclass':cls.__name__,'doc':cls.__doc__}

							model=dtscmd.MLmodels(Project=Project,Data=Data,Name=cls.name,Userfilename=cls.filename,Info=info,Misc={'modelparas':modelparas} ,Status='UnTrained' ,saveformat=cls.saveformat)
							model.save()
							model.initialize()
							filename=model.modelpath()
							bst.save_model(filename)
							
							
							N=N+1

					elif Data.ouput_type=='multiclass':
						for obj in ['reg:linear','reg:logistic','multi:softprob']:
							param['max_depth']=max_depth
							param['eta']=eta
							param['lambda']=lmda
							param['objective']=obj
							param['max_delta_step']=1		

							plst = list(param.items())+[('eval_metric', 'ams@0.15'),('eval_metric', 'auc'),('eval_metric','rmse'),('eval_metric','mae'),('eval_metric','logloss'),('eval_metric','logloss')]
							plst=plst+[('eval_metric','error@%s'%t) for t in np.arange(0,1,0.1) ]
							
							num_round=eta*1000

							dtrain = xgb.DMatrix( X, label=Y)
							evallist  = [(dtrain,'train')]
							plst = param.items()
							bst = xgb.train( plst, dtrain, num_round, evallist )

							modelparas={'param':param,'plst':plst,'num_round':num_round,'early_stopping_rounds':early_stopping_rounds}

							model=dtscmd.MLmodels(Project=Project,Data=Data,Name=cls.name,Misc={'modelparas':modelparas} ,Status='UnTrained' ,saveformat=cls.saveformat)
							model.save()
							model.initialize()
							filename=model.modelpath()
							bst.save_model(filename)
							
							N=N+1
		



###################################################################
####################   RandomForrest  #####################################
###################################################################
class RandomForrestmodels(BaseClassificationModel):
	name='RandomForrest'
	saveformat='joblib'

	@classmethod
	def GenModels(cls,Project,Data):
		if Data.Datatype!='Train':
			raise Exception("Need Training Data For model")

		N=0
		for n_estimators in [10,100,250,300]:
			for max_features in ['log2','auto']+[0.25,0.5,0.75,1]:
				for max_depth in [50,100,150,250,400]:
					for class_weight in ['balanced','balanced_subsample',None]:
						clf=RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth,min_samples_leaf=200, n_jobs=5,max_features=max_features,class_weight=class_weight)
						modelparas={'n_estimators':n_estimators, 'n_jobs':5,'max_features':max_features,'class_weight':class_weight,max_depth:max_depth}
						model=dtscmd.MLmodels(Project=Project,Data=Data,Userfilename=cls.filename,Name=cls.__name__,Info={'modelparas':modelparas,'description':cls.__doc__} ,Status='UnTrained' ,saveformat=cls.saveformat)
						model.save()
						model.initialize()
						filename=model.modelpath()
						joblib.dump(clf, filename)
						N=N+1

	

###################################################################
####################   LinearSVC  #####################################
###################################################################
class LinearSVCmodels(BaseClassificationModel):
	name='LinearSVC'
	saveformat='joblib'

	@classmethod
	def GenModels(cls,Project,Data):
		if Data.Datatype!='Train':
			raise Exception("Need Training Data For model")

		N=0
		for C in [1, 10, 100, 1000,10000]:
			clf=LinearSVC(C=C)
			modelparas={'C':C}
			model=dtscmd.MLmodels(Project=Project,Data=Data,Userfilename=cls.filename,Name=cls.__name__,Info={'modelparas':modelparas,'description':cls.__doc__} ,Status='UnTrained' ,saveformat=cls.saveformat)
			model.save()
			model.initialize()
			filename=model.modelpath()
			joblib.dump(clf, filename)
			N=N+1

###################################################################
####################   QuadraticDiscriminantAnalysis  ###############
###################################################################
class QDAmodels(BaseClassificationModel):
	name='QDA'
	saveformat='joblib'

	@classmethod
	def GenModels(cls,Project,Data):
		if Data.Datatype!='Train':
			raise Exception("Need Training Data For model")

		N=0
		for reg_param in [1, 10, 100, 1000,10000]:
			clf=QuadraticDiscriminantAnalysis(reg_param=reg_param)
			modelparas={'reg_param':reg_param}
			model=dtscmd.MLmodels(Project=Project,Data=Data,Userfilename=cls.filename,Name=cls.__name__,Info={'modelparas':modelparas,'description':cls.__doc__} ,Status='UnTrained' ,saveformat=cls.saveformat)
			model.save()
			model.initialize()
			filename=model.modelpath()
			joblib.dump(clf, filename)
			N=N+1

###################################################################
################(####   NN  #####################################
###################################################################
class NNmodels_1layer(BaseClassificationModel):
	name='NN1layer'
	saveformat='keras'

	def getfit_args_kwargs(self):
		args=()
		kwargs=self.model.modelparas['fit_kwargs']
		return (args,kwargs)

	def getclassweights(self,Y):
		n=Y.shape[1]
		ss=0
		class_weights={}
		for i in range(n):
			N=Y[Y[:,i]==1,:].shape[0]
			ss=ss+N
			class_weights[i]=N

		for key in class_weights.keys():
			class_weights[key]=class_weights[key]/ss
		
		return class_weights

	@classmethod
	def GenModels(cls,Project,Data):
		N=1
		X,Y,Meta=dtscmd.DataShard.objects.filter(Data=Data).first().getdata()
		input_dim=X.shape[1]
		output_dim=len(np.unique(Y))
		meandim=int((input_dim+output_dim)/2)
		for batch_size in [50,100,5000]: 
			for nb_epoch in [100,250,500,750]:
				for l2 in [0.02,0.2]:
					for dropout in [0,0.2]:
						for act in ["sigmoid",'relu']:
							for Nneurons in [2*input_dim,meandim]:
								# random_state = 50+N
								N=N+1
						
								model = Sequential()
								model.add(Dense(output_dim=Nneurons, input_dim=input_dim,kernel_regularizer=regularizers.l2(l2),))
								model.add(Activation(act))
								model.add(Dropout(dropout))

								model.add(Dense(output_dim=output_dim))
								model.add(Activation("softmax"))

								sgd = SGD(lr=1e-3, decay=1e-4, momentum=0.3, nesterov=True)
								model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
								
								modelparas={'batch_size':batch_size, 'nb_epoch':nb_epoch,'l2':l2,'dropout':dropout,'act':act,'Nneurons':Nneurons}
								modelparas['fit_args']=()
								modelparas['fit_kwargs']={'batch_size':batch_size, 'epochs':nb_epoch, 'verbose':1, 'validation_split':0.1,  'class_weight':None}

								model=dtscmd.MLmodels(Project=Project,Data=Data,Userfilename=cls.filename,Name=cls.__name__,Info={'modelparas':modelparas,'description':cls.__doc__} ,Status='UnTrained' ,saveformat=cls.saveformat)
								model.save()
								model.initialize()
								filename=model.modelpath()
								
								model.save(filename)




###################################################################n
####################   CNN1D  #####################################
###################################################################
class CNN1Dmodels(BaseClassificationModel):
	name='CNN1D'
	saveformat='keras'

	@classmethod
	def GenModels(cls,Project,Data):
		N=0
		batch_size = 16
		nb_epoch = 20
		random_state = 51



		model = Sequential()
		model.add(ZeroPadding2D((1, 1), input_shape=(3, 224, 224)))
		model.add(Convolution2D(4, 3, 3, activation='relu'))
		model.add(ZeroPadding2D((1, 1)))
		model.add(Convolution2D(4, 3, 3, activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		model.add(ZeroPadding2D((1, 1)))
		model.add(Convolution2D(8, 3, 3, activation='relu'))
		model.add(ZeroPadding2D((1, 1)))
		model.add(Convolution2D(8, 3, 3, activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		model.add(Flatten())
		model.add(Dense(32, activation='relu'))
		model.add(Dropout(0.5))
		model.add(Dense(32, activation='relu'))
		model.add(Dropout(0.5))
		model.add(Dense(8, activation='softmax'))

		sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
		model.compile(optimizer=sgd, loss='categorical_crossentropy')

		modelparas={}
		model=dtscmd.MLmodels(Project=Project,Data=Data,Userfilename=cls.filename,Name=cls.__name__,Info={'modelparas':modelparas,'description':cls.__doc__} ,Status='UnTrained' ,saveformat=cls.saveformat)
		dbmodel.save()
		model.initialize()
		filename=model.modelpath()
		
		model.save(filename)


		N=N+1

		
