import statsmodels.api as sm
from statsmodels.formula.api import ols
from bindata import *
from alldata import *
import pickle as pkl

alldata = pkl.load(open("alldata.pkl", "rb"))
bindata = pkl.load(open("bindata.pkl", "rb"))
bindata_vehicle = pkl.load(open("bindata_vehicle.pkl", "rb"))

def get_anova():
    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    doses = ['vehicle', 'lowdose', 'highdose']

    anova = {}

    eventrate =

    model = ols('height ~ C(Fertilizer) + C(Watering) +\
    C(Fertilizer):C(Watering)',
                data=dataframe).fit()
    result = sm.stats.anova_lm(model, type=2)




