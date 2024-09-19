![Python](https://img.shields.io/badge/Python-333333?style=flat&logo=python)
![Apache Spark](https://img.shields.io/badge/-Apache%20Spark-333333?style=flat&logo=apache-spark)
![PySpark](https://img.shields.io/badge/-PySpark-333333?style=flat&logo=apache-spark)
![Jupyter](https://img.shields.io/badge/-Jupyter_Notebook-333333?style=flat&logo=jupyter)
![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![MySQL](https://img.shields.io/badge/-MySQL-333333?style=flat&logo=mysql)
![Azure](https://img.shields.io/badge/-Microsoft%20Azure-333333?style=flat&logo=microsoft-azure)
![Powerbi](https://img.shields.io/badge/-PowerBI-333333?style=flat&logo=powerbi)
![VSC](https://img.shields.io/badge/Visual_Studio_Code-333333?style=flat&logo=visual%20studio%20code&logoColor=white)


# Data Synergi Solutions

<p align="center">
  <img src="Images/Portada.gif">
</p>

Group 62 Data BI Repository: Data Analysis Project with Microsoft Fabric (Azure Data Stack)

Overview 📝
This project aims to develop a comprehensive framework addressing key aspects of data engineering, data analysis, visualization, and machine learning model development within the Steam Community, using Microsoft Fabric (Azure Data Stack). The framework is designed to optimize the collection, processing, and analysis of data related to user behavior, gaming trends, and interactions within the Steam community. Additionally, it includes a comparative analysis of gaming data across other popular platforms such as Nintendo and PlayStation. The insights derived from this analysis will provide valuable support for strategic decision-making, including new game development, marketing strategy optimization, and enhancing user experience on the platform.

## Project Structure

| Folder/File              | Description                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| **/data**                | Folder that stores datasets and files used by the Analysis,  Dashboard and ML models.                              |
| **/Notebooks**           | Folder containing Jupyter notebooks used for ETL, EDA and feature engineering processes |
| **/Images**              | Folder containing relevant and illustrative images for the analysis project. |
| **requirements.txt**     | File listing dependencies and libraries required to run the project.                           |
| **gitignore**            | File specifying folders and files to be ignored by version control (git).                      |
| **LICENSE**              | MIT LICENSE - File specifying the terms under which the source code is shared.                 |
| **functions.py**         | Python file with functions to deploy in the main file 'app-py' |
| **app.py**              | Main Python file serving as an entry point for the application, defining Model configuration and execution|
| **README.md**            | Main project documentation in English.                                                         |
| **README_ESP.md**        | Main project documentation in Spanish.                                                         |


## Authors

<p align="center">
  <img src="Images/Team.png">
</p>


| Name                     | Rol                                       | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)|![LinkedIn](https://img.shields.io/badge/linkedin-%231DA1F2.svg?style=for-the-badge&logo=linkedin&logoColor=white)                |
| ------------------------ | ----------------------------------------- | -------------------------------- |--------------------------------|
| **Leonardo Cortés**      | Project Manager (PM), Data Engineer, Data Analyst   |[leocortes85](https://github.com/leocortes85/)  |[Leonardo Cortés Zambrano](https://www.linkedin.com/in/leonardo-cort%C3%A9s-zambrano/)
| **Beverly Gonzalez**      | ML Engineer and Data Scientist           |[licette32](https://github.com/licette32/) |[Beberly Gonzalez](https://www.linkedin.com/in/beverly-j-l-gonzalez-c/)|

## Key Features

1. **Technology Stack:**
   - Utilized **Microsoft Fabric**, which encompasses the full **Azure Data Stack**, to develop a complete end-to-end data solution.

2. **Data Architecture:**
   - Implemented a **Medallion Architecture** to optimize data access and maintain a continuous workflow, ensuring the data remains accessible, manageable, and ready for downstream processes.

      <p align="center">
  <img src="Images/Medallion.png">
   </p>
   <p align="center">
  <img src="Images/Medallion_flow.png">
   </p>

3. **Data Transformations:**
   - Performed **Extract, Transform, and Load (ETL)** operations using the **Pandas** library, automating data loading from client-provided folders.
   - Applied strategies to handle nested data structures and eliminated irrelevant or highly null columns to optimize the data for further use.
   - Conducted an **incremental load** of information, using external APIs, web scraping, and custom functions to complement the dataset.

4. **Feature Engineering:**
   - Conducted extensive **feature engineering** to ensure the data was fully consumable, cleaned, and prepped for machine learning processes and data analysis.

5. **Dimensional Structure and Semantic Model:**
   - Built a **dimensional structure** stored in a **semantic model** to enable insightful analysis.
   - Developed a **Power BI dashboard** that provides visual analytics and insights into the video game market.
 <p align="center">
  <img src="Images/Dashboard.png">
   </p>


6. **Recommendation Models:**
   - Developed **recommendation models** using **machine learning** techniques, specifically leveraging **cosine similarity** for user and item recommendations.

7. **Model Testing and Deployment:**
   - Conducted tests of the machine learning models using **Azure ML** tools.
   - Created a `functions.py` file that stores all the functions to be executed during the deployment phase.

8. **Streamlit Deployment:**
   - Deployed the entire project via **Streamlit** through the `app.py` file, allowing users to:
     - View the interactive **dashboard**.
     - Interact with the **machine learning models**, including item and user recommendations, showcasing the project's full capabilities.
