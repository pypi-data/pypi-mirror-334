CREATE OR REPLACE FUNCTION schema_inference(data string,name string) RETURNS string LANGUAGE PYTHON AS 
$$
import traceback
import json
from neutrino.onboard.agent import DataOnboardingAgent


def schema_inference(data, name):
    results = []
    for (data, name) in zip(data, name):
        try:
            agent = DataOnboardingAgent()
            inference_ddl, inference_json = agent.inference(data, name)
            
            result = {}
            result["ddl"] = inference_ddl
            result["json"] = inference_json

            results.append(json.dumps(result))
        except Exception as e:
            trace = traceback.format_exc()
            results.append(trace)

    return results

$$;


CREATE OR REPLACE FUNCTION field_summary(data string, columns string) RETURNS string LANGUAGE PYTHON AS 
$$
import traceback
from neutrino.onboard.agent import DataOnboardingAgent


def field_summary(data, columns):
    results = []
    for (data, columns) in zip(data, columns):
        try:
            agent = DataOnboardingAgent()
            summary_result = agent.summary(data, columns)
            results.append(summary_result)
        except Exception as e:
            trace = traceback.format_exc()
            results.append(trace)

    return results

$$;

CREATE OR REPLACE FUNCTION analysis_recommendation(data string, columns string, name string) RETURNS string LANGUAGE PYTHON AS 
$$
import traceback
from neutrino.onboard.agent import DataOnboardingAgent


def analysis_recommendation(data, columns, name):
    results = []
    for (data, columns, name) in zip(data, columns, name):
        try:
            agent = DataOnboardingAgent()
            recommendation_result = agent.recommendations(data, columns, name)
            results.append(recommendation_result)
        except Exception as e:
            trace = traceback.format_exc()
            results.append(trace)

    return results

$$;