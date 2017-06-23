from __future__ import division
from celery import shared_task
import stockapp.models as stkmd
import dataapp.models as dtamd
import featureapp.models as ftmd
import datascience.models as dtscmd
import datascience.ML.MLmodels as MLmd
import datascience.ML.MLlibs as MLlibs

import itertools as itt
import numpy as np
import multiprocessing as mp
from Queue import Empty
import time
import pandas as pd
from django import db

import logging
logger = logging.getLogger('debug')


## Update Data Meta ########################

@shared_task
def Compute_ShardMisc(Dataid,shardname):
	return MLlibs.GetShardInfo(Dataid,shardname)

@shared_task
def Compute_DataMisc(Dataid):
	Data=dtscmd.Data.objects.get(id=Dataid)
	shard_info={}
	for shardname in Data.get_shardnames():
		shard_info[shardname]=Compute_ShardMisc(Dataid,shardname)

	for shardname in Data.get_shardnames():
		Data.ShardInfo[shardname]=shard_info[shardname]

	Data.save()



### Do ML #######################

@shared_task
def TrainModel(modelid):
	"""
	Train a specific model with model id as modelid
	"""
	model=dtscmd.MLmodels.objects.filter(id=modelid)
	ModelCLass=MLmd.ModelFactory(model)

	MCL=ModelCLass(model)
	MCL.loadmodel()
	MCL.loaddata()
	MCL.train()
	MCL.Run_validation_all()
	MCL.savemodel()


@shared_task
def TrainProject(Projectid):
	"""
	Train all models of a Project with id as Projectid
	"""
	MLmodels_ids=dtscmd.MLmodels.objects.filter(Project__id=Projectid,Status='UnTrained').values_list('id',flat=True)
	for modelid in MLmodels_ids:
		TrainModel(modelid)


#	Model Validation
@shared_task
def ValidateModeldata(modelid,validationdataid):
	"""
	Run Validation on validationdata with id validationdataid using modelid
	"""
	model=dtscmd.MLmodels.objects.filter(id=modelid)
	ModelCLass=MLmd.ModelFactory(model)

	MCL=ModelCLass(model)
	MCL.loadmodel()
	MCL.loaddata()
	MCL.Run_validation_id(validationdataid)
	MCL.savemodel()

# TODO: Write help
@shared_task
def ValidateModel(modelid):
	"""
	Run Validation for modelid on all validation data.
	"""
	model=dtscmd.MLmodels.objects.filter(id=modelid)
	ModelCLass=MLmd.ModelFactory(model)

	MCL=ModelCLass(model)
	MCL.loadmodel()
	MCL.loaddata()

	for validationdataid in MCL.validation_datasets.values_list('id',flat=True):
		ValidateModeldata(modelid,validationdataid)



@shared_task
def ValidateProject(Projectid):
	"""
	Run validation for the whole project
	"""
	MLmodels_ids=dtscmd.MLmodels.objects.filter(Project__id=Projectid,Status='Trained').values_list('id',flat=True)
	for modelid in MLmodels_ids:
		ValidateModel(modelid)
