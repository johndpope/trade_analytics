
import pandas as pd
import numpy as np
import featureapp.models as ftmd
import featureapp.featuremodel as dtaftmd
import featureapp.FeatureCodes.AnonymousUser as FCan

import dataapp.datamanager as dtamng
import stockapp.models as stkmd

import datascience.models as dtscmd 




# @mnt.logperf('datascience',printit=True)
def CreateStockData_mondays_directfrom_DM(SymbolId,dataId):
	"""
	T0TFSymbol_dict= [{'T0':,'Tf':,'Symbol':},{}]
	"""
	data=dtscmd.Data.objects.get(id=dataId)	

	col2write=['Close',u'Open', u'High',u'Low','Volume',u'SectorId',
            u'IndustryId',             u'CCI5',
                 u'CCI50',            u'EMA8',         u'EMAstd8',
                 u'SMA10',          u'SMA100',           u'SMA20',
                u'SMA200',           u'SMA50',        u'SMAstd20',
              u'VolSMA10',u'VolSMA20']

	TFs=dtalibs.getdatearrays(ondays='EveryMonday')

	DM=dtamng.DataManager(SymbolIds=[SymbolId],Append2ReqCols=['Sector','Industry','CCI5','CCI50','CCI100','VolSMA10','VolSMA20'])

	DM.AddStockData()
	DM.AddStockMetacols()
	DM.AddIndicatorCols()
	TFs=dtalibs.getdatearrays(ondays='EveryMonday')
	for (X,Y,Xflat,Yflat,Meta,Metaflat) in DM.CreateTrainingDataSet(col2write,TFs,width_back=360,width_front=180):
		shard=dtscmd.DataShard(Data=data)
		shard.save()
		shard.savedata(X=X,Y=Y,Meta=Meta)

