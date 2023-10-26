GET_DATA_SCHEMA_CODE_TEMPLATE_CSV = """
import pandas as pd
import json
df = pd.read_csv('{file_path}')
schema = {{}}
for column in df.columns:
    dtype = str(df[column].dtype)
    if dtype == "object":
        dtype_detail = "string"
    elif "int" in dtype or "float" in dtype:
        dtype_detail = {{
            "type": dtype,
            "min": df[column].min(),
            "max": df[column].max()
        }}
    else:
        dtype_detail = dtype

    schema[column] = dtype_detail
schema_str = str(schema)
print("The schema dictionary uses DataFrame column names as keys. For numeric columns, the value is another dictionary detailing its type, min, and max values; for string columns, the value is simply string; and for others, it's the datatype as a string.")
print(schema_str)
print("The sample of the data:")
print(df.head(3))"""

GET_DATA_SCHEMA_CODE_TEMPLATE_EXCEL = """import pandas as pd
import json

df = pd.read_excel('{file_path}')

schema = {{}}
for column in df.columns:
    dtype = str(df[column].dtype)
    if dtype == "object":
        dtype_detail = "string"
    elif "int" in dtype or "float" in dtype:
        dtype_detail = {{
            "type": dtype,
            "min": df[column].min(),
            "max": df[column].max()
        }}
    else:
        dtype_detail = dtype

    schema[column] = dtype_detail

schema_str = str(schema)

print("The schema dictionary uses DataFrame column names as keys. For numeric columns, the value is another dictionary detailing its type, min, and max values; for string columns, the value is simply string; and for others, it's the datatype as a string.")
print(schema_str)
print("The sample of the data:")
print(df.head(3))"""

CODE_INTERPRETER_PREFIX = """
You are an AI code interpreter.
Your goal is to help users do a variety of jobs by executing Python code.

You should:
1. Comprehend the user's requirements carefully & to the letter.
2. call the `run_code` function.
3. Use `function_call` as role and don't use `assistant` in the generated message
4. Only provide 1 python code chunk

Note: If the user uploads a file, you will receive a system message "Add a filename at file_path". Use the file_path in the `run_code`.

The question is as follow:

---

"""

DATA_CLEANING_PROMPT_TEMPLATE = """
Here is the data schema of the file: {data_schema}
Now you need to clean and process the data in the following steps:

1. Basic Inspection: Provide a basic summary and statistics of the dataset to identify potential issues.
2. Handling Missing Values: Check for missing values in the dataset and suggest appropriate methods to handle them.
3. Outliers Detection: Detect outliers in numeric columns and recommend strategies to address them.
4. Data Type Consistency: Verify the data types of each column and suggest corrections if there are inconsistencies.
5. String Cleaning (if textual data is present): Identify inconsistencies in textual data, such as varying case, extra spaces, or common typos, and suggest corrections.
6. Category Consistency (for categorical data): Inspect categorical columns for consistency in category values and suggest standardizations if needed.

And then use print function to output the result of the cleaning and process.

"""




#Planner prompt

PROJECT_TYPE_SELECTOR_PROMPT = """Here is my project requirement: {project_requirement}

Please tell me what type of project it is, and only output the project type.

If the type is other, please output "other: xxx" where xxx is the type.

You can choose from the following options:

Regression, Classification, ANOVA, Clustering, Time Series, Association Rules, NLP, Recommender System, Dimension Reduction, Survival Analysis, Longitudinal Analysis, Other
"""

PLANNER_PROMPT = {}

PLANNER_PROMPT["ANOVA"] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several parts:

1. Summary of data

2. Diagnostics

3. ANOVA model fitting

4. Post Hoc analysis

5. Conclusion

You need to help me plan what's the specific plan of each part of the project. Your output should be this format:

---

# Step i

plan for step i

---
"""

PLANNER_PROMPT["Time Series"] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a time series analysis.

Here is the sample project plan if we want to use SARIMA model to model the a sample data:

---

# Step 1: Exploratory Analysis

- Plot the train data.
- Note observations like increasing trend, seasonality, and variance.
- Use Box-Cox transformation to stabilize variance.

---

# Step 2: Model Preparation

- Analysis the seasonal effect and trend effect.
- Ensure time series is stationary by making lag 1 and lag 12 differences.
- Confirm stationarity with Augmented Dickey-Fuller Test.

---

# Step 3: Model Selection

- Examine sample ACF and PACF plots to determine model parameters.
- Use the determined parameters to select a range of candidate models.
- Calculate AICc for each candidate model. 
- Choose the model with the smallest AICc as the best model.

---

# Step 4: Model Diagnostic:

- Check residuals of the model to ensure they resemble white noise.
- Validate normality using histogram, qqplot, and Shapiro-Wilks test.
- Confirm model residuals' independence using Box-Pierce, Ljung-Box, and McLeod-Li tests.
- Verify model is stationary and invertible by checking characteristic roots.

---

# Step 5: Forecasting

- Forecast electricity production for the years 1991 to 1995 using the selected SARIMA model.
- Plot the forecasts along with a 95 percentage confidence interval.
- Compare forecasted values with actual test data.

---

Now you need to help me plan what's the specific plan of each part of the project. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT["Regression"] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a regression analysis.

Now you need to help me plan what's the specific plan of each part of the project. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""


REVISE_PLAN_PROMPT = """Here is my project context: {project_requirement}

We are at step {step_number}. Here is the previous step report result: {previous_result}

Now please revise the plan of following steps. Here is the plan:

{step_plans}

If no need to revise, please output "no need to revise" only.

"""





# Step filler prompt

STEP_FILLER_BODY_STEP1 = """Here is my project context: {project_requirement}

Here is my project data: {file_info}

Here is the data schema: {data_schema}

Here is the preprocess result: {data_preproces_result}

Now we start step 1. Here is the step 1 plan:

{step_plan}

"""

STEP_FILLER_BODY_STEP_NOT1 = """Here is my project context: {project_requirement}

Here is my project data: {file_info}

Here is the data schema: {data_schema}

Here is the previous code for step {step_name}: {step_code}

Here is the step {step_name} result: {step_result}

Now we start step {step_number}. Here is the step {step_number} plan:

{step_plan}

"""

STEP_FILLER_BODY_STEP_CONCLUSION = """Here is my project context: {project_requirement}

Here is the previous step report result: {previous_result}

Now we start step Conclusion. Here is the plan:

{step_plan}

You need to provide the report of the conclusion part. Please give suggestions of the previous steps report if needed. 

"""



STEP_PARAGRAPH_PROMPT = """Here is my project context: {project_requirement}

Here is the step {step_number} plan:

{step_plan}

Here is the step {step_number} code:

{step_code}

Here is the step {step_number} result: 

{step_result}

Now please convert the result into the {part_name} part of the report. The plot indicated in result with [plot_name] will be inserted in the report with [plot_name].

""" # TODO, need to craft the prompt of result generating!!!!