# Healthare High Relevance Clinical Terms (HRCT)
The goal with Healthcare HRCT is to find the clinically relevant terms in documents to help identify the patients that are likely to end up with a particular diagnosis. The hope is that by identifying the patient's primary issue, treatment can be carried out earlier resulting in more positive outcomes, especially where a patient only has a small timeframe to get treatment to result in a positive outcome such as a severe sepsis diagnosis. 

The package within will allow you to build a model using labelled datasets (one with the diagnosis and one without) which are required and additionally you may choose to include a third dataset consisting of notes of the same type that will be used to designate a background distribution, but this third dataset is not required to build the model.

To import the model you can use the following import statement:

                **from** hrct_model **import** HRCTmodel
                

Required python packages:
