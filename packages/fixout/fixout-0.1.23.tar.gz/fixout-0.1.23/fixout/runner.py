import numpy as np
import pickle
import datetime
import copy

from sklearn.preprocessing import LabelEncoder

from fixout import fairness, interface
from fixout.helper import ReverseFairness, UnfairModel, clazzes
from fixout.interface.ttypes import SensitiveFeature, FairMetricEnum

import warnings
warnings.filterwarnings('ignore')


import fixout.web.webapp as interface

class FixOutRunner:
    """
    A class to process and evaluate fairness in machine learning models, given a FixOut artifact.

    See Also
    --------
    fixout.artifact.FixOutArtifact : A FixOut artifact.
    """
    
    def __init__(self,report_name=""):
        """
        Initializes the FixOutRunner with a report name.
        
        Parameters:
        -----------
        report_name : str, optional
            Name of the report. Defaults to an empty string.
        """
        self.input = {}
        self.input["report_details"] = {}
        self.input["report_details"]["report_name"] = report_name
        self.input["report_details"]["generated"] = datetime.datetime.now().date()

        self.output = {}

    def __common(self, fxa):
         
        self.input["model"] = fxa.model
        self.input["X"] = fxa.X
        self.input["y"] = fxa.y
        self.input["f_names"] = fxa.features_name
        self.input["nonnumeric_features"] = fxa.nonnumeric_features

        self.input["testing_data"] = fxa.test_data
        
        self.input["dictionary"] = fxa.dictionary 

        if self.input["model"] is None and fxa.y_pred is None:
            raise

        if fxa.y_pred is None:
            self.output["y_pred"] = self.input["model"].predict(self.input["X"])
        else:
            self.output["y_pred"] = fxa.y_pred
        self.prob_y_pred = fxa.prob_y_pred

        sens_f_indexes = [u for u,_,_ in fxa.sensfeatList]
        sens_f_unprivPops = [v for _,v,_ in fxa.sensfeatList]
        sens_f_unprivPops_discretes = []
        self.input["sens_f_names"] = [w for _,_,w in fxa.sensfeatList]

        encoders = []

        transformed_data = copy.deepcopy(self.input["X"])
        
        for i in range(len(self.input["f_names"])):
            
            le = None
            
            if i in self.input["nonnumeric_features"]:
                le = LabelEncoder( )
                le.fit(self.input["X"][:,i])
                transformed_data[:,i] = le.transform(self.input["X"][:,i]).astype(float)

            encoders.append(le)

        self.input["sens_f_index"] = sens_f_indexes
        
        ######
        # for each column
        for i in range(len(self.input["sens_f_index"])):
            
            sens_f_index = self.input["sens_f_index"][i]

            if sens_f_index in self.input["nonnumeric_features"]: 

                le = encoders[sens_f_index]
                sens_f_unprivPops_discreted = int(le.transform([sens_f_unprivPops[i]])[0])
                
                new_array = [1 if x == str(float(sens_f_unprivPops_discreted)) else 0 for x in transformed_data[:,sens_f_index]]
                transformed_data[:,sens_f_index] = np.array(new_array)
            
            else:
                sens_f_unprivPops_discreted = int(sens_f_unprivPops[i])
                    
            sens_f_unprivPops_discretes.append(sens_f_unprivPops_discreted)
        
        
        self.sensitivefeatureslist = []
        
        # for each sensitive feature
        for i in range(len(self.input["sens_f_index"])):

            aSensitiveFeature = SensitiveFeature()
            aSensitiveFeature.featureIndex = self.input["sens_f_index"][i] 
            aSensitiveFeature.unprivPop = sens_f_unprivPops_discretes[i]
            aSensitiveFeature.unprivPop_original = sens_f_unprivPops[i]
            aSensitiveFeature.name = self.input["sens_f_names"][i]
            aSensitiveFeature.description = ""
            aSensitiveFeature.type = 1 if self.input["sens_f_index"][i] in self.input["nonnumeric_features"] else 0
            self.sensitivefeatureslist.append(aSensitiveFeature)
        
        ######

        transformed_data = transformed_data.astype(float)
        self.input["X"] = transformed_data
        
        self.input["model_availability"] = self.input["model"] is not None
        self.input["sens_f_unpriv"] = [x.unprivPop for x in self.sensitivefeatureslist],
        self.input["sens_f_unpriv_original"] = [x.unprivPop_original for x in self.sensitivefeatureslist],
        self.input["sens_f_type"] = [1 if x in self.input["nonnumeric_features"] else 0 for x in self.sensitivefeatureslist],
        self.input["sens_f_pair"] = [(x.featureIndex, x.name) for x in self.sensitivefeatureslist]
        
        self.output["prob_y_pred"] = None, # Fix it
        
        rev_fairness = ReverseFairness()
        self.input["reversed_models"] = []
        rev_train = rev_fairness.build_reversed_models(self.input["X"], self.input["y"], self.sensitivefeatureslist)
        self.input["reversed_models"].append(rev_train)
        for X_test,y_test,_ in self.input["testing_data"]:
            rev_test = rev_fairness.build_reversed_models(self.input["X"], self.input["y"], self.sensitivefeatureslist, X_test, y_test)
            self.input["reversed_models"].append(rev_test)
    
        unfair_model = UnfairModel()
        self.input["unfair_model"] = []
        unfair_train =  unfair_model.build_unfair_model(self.input["X"], self.input["y"], self.sensitivefeatureslist)
        self.input["unfair_model"].append(unfair_train)
        for X_test,y_test,_ in self.input["testing_data"]:
            runfair_test = unfair_model.build_unfair_model(self.input["X"], self.input["y"], self.sensitivefeatureslist, X_test, y_test)
            self.input["unfair_model"].append(runfair_test)


        self.__assess_fairness()


    def __assess_fairness(self):

        self.output["metrics_list"] = [FairMetricEnum.DP, FairMetricEnum.EO, FairMetricEnum.PE, FairMetricEnum.EOD]
        self.output["nonStandardMetricsToBeCalculated"] = [FairMetricEnum.PP, FairMetricEnum.CEA]

        self.output["result"] = self.__eval_fairness(self.output["metrics_list"],
                                                   self.sensitivefeatureslist,
                                                   self.input["X"].tolist(),
                                                   self.input["y"].tolist(),
                                                   self.output["y_pred"],
                                                   "original")
        
        self.output["nonstandardResults"] = self.__eval_fairness(self.output["nonStandardMetricsToBeCalculated"],
                                                               self.sensitivefeatureslist,
                                                               self.input["X"].tolist(),
                                                               self.input["y"].tolist(),
                                                               self.output["y_pred"],
                                                               "original")
        self.__baselines()

    def __eval_fairness(self,metrics,sensFeatures,X,y,y_pred,txtIndicator):
        
        results = []
        for sensitiveFeature in sensFeatures:
            r = fairness.computeFairnessMetrics(metrics,
                                       sensitiveFeature, 
                                       X, 
                                       y,
                                       y_pred)
            results.append((sensitiveFeature,r,txtIndicator))
        
        return results

    
    def run(self, fxa, show=True):
        """
        Runs FixOut with a given artifact.

        Parameters:
        -----------
        fxa : FixOutArtifact
            Original model, training and/or testing data to process.
        show : bool, optional
            If True (default), the output will be shown using a web interface, 
            otherwise only the evaluation will be executed and the results returned.

        Returns:
        --------
        tuple or None
            If `show` is True, returns None and actives a web interface.
            Otherwise, returns the computed evaluation results.

        """

        self.__common(fxa)
                
        if show:
            pickle.dump((self.input, self.output),open(str("repport_output.fixout"),"wb"))
            interface.app.run()
            return None
        
        return self.output
    
    '''
    def data_distribution(self):
        return None
    def get_correlation(self):
        return None
    def get_reverse(self):
        return None
    def get_discriminatory(self):
        return None
    '''

    def get_fairness(self,
                     model="original",
                     sensitivefeature=None):
        """
        Retrieves calculated fairness metrics for a given model and sensitive feature.

        Parameters:
        -----------
        model : str, optional
            The model label to filter results (default: "original").
        sensitivefeature : str, optional
            The specific sensitive feature to filter results (default: None).

        Returns:
        --------
        dict
            A dictionary where keys are model labels and values are the calculated fairness metrics.
        """
        
        result = {}

        for sensf, calculated_metrics, model_label in self.output["result"]:#, self.output["nonstandardResults"]]:
            if sensitivefeature is not None and sensitivefeature == sensf.name:
                result[model_label] = calculated_metrics
            elif sensitivefeature is None:
                result[model_label] = calculated_metrics

        return result        

    def __baselines(self):

        predictions_list=[]

        for clazz,clazz_name in clazzes:
            self.__build_model(clazz,clazz_name,predictions_list)

        for name_method, preditions in predictions_list:
            for sensitiveFeature in self.sensitivefeatureslist:
                r = fairness.computeFairnessMetrics(self.output["metrics_list"],
                                        sensitiveFeature, 
                                        self.input["X"].tolist(), 
                                        self.input["y"].tolist(),
                                        preditions)
                self.output["result"].append((sensitiveFeature,r,name_method))

                nonStandardR = fairness.computeFairnessMetrics(self.output["nonStandardMetricsToBeCalculated"],
                                       sensitiveFeature, 
                                       self.input["X"].tolist(), 
                                       self.input["y"].tolist(),
                                       preditions)
                self.output["nonstandardResults"].append((sensitiveFeature,nonStandardR,name_method))

    def __build_model(self, clazz, name_method, predictions_list):

        clf = clazz()
        clf.fit(self.input["X"], self.input["y"])
        y_pred = clf.predict(self.input["X"])
        predictions_list.append((name_method, y_pred))

