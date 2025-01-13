# Data Engineering Project - Ready D25 &nbsp; &nbsp; &nbsp;<img align="center" width="50" alt="image" src="https://github.com/Ready-Talent/data-engineering-project-template/assets/70844012/4c10ad15-6b48-4ce3-9829-9e823191b410">

As a Data Engineer in a major consultancy firm, i have been tasked to lead a new project.

## Project Description 
The Brazilian e-commerce company “Olist” has hired our consulting firm to produce some insights using its data. 
<br>
<br>
## Project Architecture 
<img src="Untitled design.png" alt="Alt text" width="100%"/>

<br>
<br>

### 1- Transfers:
The data that you will work with is stored in multiple sources. First, some of the tables are stored in a postgres database and some will be retrieved via an API. we will move this data from the different sources to BigQuery.<br>
<br>

### 2- Modeling:
We will apply the necessary modeling techniques to transform the raw data in the landing tables to multiple dimension and fact tables and store them in BigQuery. 
<br>
<br>
## Database ER diagram

<img src="Database ER diagram.png" alt="Alt text" width="100%"/>


<br><br>
### 3- Reporting:
We will build views in BigQuery from the dimension and fact tables and use them to build a dashboard on Looker Studio.
<br><br>
Those view are answers the following questitions :

- Who are the top customers by total order value?  
- What is the average number of orders per customer?  
- What are the top-selling products by quantity?  
- Which product categories generate the most revenue?  
- What is the total number of orders placed each month (trend over time)?  
- What is the distribution of payment methods used by customers?  

<br><br>
### Report Link : https://lookerstudio.google.com/s/sAGZyC6ljc8
