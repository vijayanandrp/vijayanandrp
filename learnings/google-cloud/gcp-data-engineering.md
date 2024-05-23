# Main Points
============

1. https://medium.com/@manojkumar.vadivel/2024-new-google-professional-data-engineer-certification-exam-guide-0cf63622a4d1
2. https://www.googlecloudcommunity.com/gc/Community-Blogs/Your-guide-to-preparing-for-the-Google-Cloud-Professional-Data/ba-p/543105
3. https://cloud.google.com/blog/products/data-analytics/decision-tree-for-data-analytics-workloads-on-google-cloud
4. Zero to Hero GCP pdf
5. Dan Sulavian GCP DE pdf
6. Linux Academy book pdf
7. Mock Questions - Practice
   

2024 New Google Professional Data Engineer Certification Exam Guide
===================================================================

![Professional Data Engineer Certification Logo](https://miro.medium.com/v2/resize:fit:468/0*em3c24RMMNqAzf-8.png)

I have successfully re-certified Google’s new version of Professional Data Engineer exam, I realized that there are no online courses out there that prepare people for the new version of the exam, so sharing my experience.

Google Cloud updated the exam guide for the Professional data engineering certification exam, Starting from **November 13th 2023,** If you planning to take the exam refer to the new updated guide.

I have been certified for the third consecutive time, Compared to previous version of PDE exam, This time got very realistic practical questions with stronger focus on Data Engineering topics.

Previously Google included many Data science and Machine learning related questions which may not relevant to data engineering related tasks. For that Google introduced new “Machine Learning Engineer” Certification.

The Professional Data Engineer exam assesses your skills in following area:

> Designing Data Processing system  
> Data Ingestion and Preparation  
> Data Storage  
> Data Analysis  
> Automating Workloads  
> Monitoring & Alerting Data System  
> Cost Optimisation  
> Access Management

In the new version, Google incorporated their recent big data products such as **BQ Omni, Analytics Hub, VertexAI, DataPlex, DataLake and Redis MemoryStore** into the syllabus

Top Priority Topics:
====================

I Encountered more questions from the following topics, So I suggest deep dive into following mentioned services

1.  BigQuery
2.  Cloud storage
3.  Dataflow
4.  BigTable
5.  Dataproc
6.  CloudSQL
7.  Spanner
8.  Pub/sub

Understanding the features and uses of these services is crucial for data engineering in Google cloud. It will boost your confidence in answering related questions during the exam. you can expect **more then 50% questions** from these sections

Secondary Importance:
=====================

1.  Cloud Composer
2.  DataFusion
3.  DLP API
4.  DataPrep
5.  Analytics Hub
6.  DataStore
7.  Transfer Service
8.  BQ Administration (Slot Management).

Expect **1 to 3 questions** from these sections. so allocating sufficient study time to grasp the nuances of these topics is highly recommended

Considerable Priority:
======================

Be ready for **1 to 2 questions** about the following Google Cloud services. These services are new additions specifically related to Data Engineering, so make sure to overlook them in your preparation.

*   BQ Omni
*   DataLake
*   Redis Memory Store
*   Dataform
*   DataStream
*   VertexAI
*   DataPlex
*   Org Policies
*   ML Engineering.

Additionally, you may receive questions from other fundamental topics like Networking, Monitoring, Logging and Alerting services.

Study Materials:
----------------

1.  CloudGuru: [https://www.pluralsight.com/cloud-guru/courses/google-certified-professional-data-engineer](https://www.pluralsight.com/cloud-guru/courses/google-certified-professional-data-engineer)
2.  Product Documentations: [https://cloud.google.com/learn/certification/guides/data-engineer](https://cloud.google.com/learn/certification/guides/data-engineer)
3.  Practice Google’s Sample Questions: [https://docs.google.com/forms/d/e/1FAIpQLSfkWEzBCP0wQ09ZuFm7G2\_4qtkYbfmk\_0getojdnPdCYmq37Q/viewform](https://docs.google.com/forms/d/e/1FAIpQLSfkWEzBCP0wQ09ZuFm7G2_4qtkYbfmk_0getojdnPdCYmq37Q/viewform)
4.  Practice passnexam.com sample questions: [https://www.passnexam.com/google/professional-data-engineer](https://www.passnexam.com/google/professional-data-engineer)

Solving a significant number of practice questions can boost your confidence and provide insight into question patterns. However, it’s important to note that Google has updated the exam questions, and you can expect a maximum of **3 to 5 questions** only from the practice dumps. Therefore, your hands-on experience with Google Cloud Platform (GCP) plays vital role clear the certification.

I hope this information proves helpful. Best of luck if you are planning to take the new PDE certification exam.

[

Professional Data Engineer \* Manojkumar Vadivel \* Google Cloud
----------------------------------------------------------------

### I got Google Cloud Certified! I have what it takes to leverage Google Cloud technology https://goo.gl/qpCWAE

google.accredible.com



](https://google.accredible.com/e703433a-e720-45d3-99bd-03927968011f?record_view=true&source=post_page-----0cf63622a4d1--------------------------------)

PS if you have any questions, or would like something clarified, you can find me on [LinkedIn.](https://www.linkedin.com/in/manojkumar-vadivel-206220a6/)

https://medium.com/@manojkumar.vadivel/2024-new-google-professional-data-engineer-certification-exam-guide-0cf63622a4d1


https://docs.google.com/forms/d/e/1FAIpQLSfkWEzBCP0wQ09ZuFm7G2_4qtkYbfmk_0getojdnPdCYmq37Q/viewscore?viewscore=AE0zAgAS7Gv-f0w-ehgVJ3W6h3Ws3Zo7Cp_efU4fvQfQdZo4RkPTVNfxDvQPigAI0zExTZw

-------------------------------------------------

**Cloud SQL** provides managed MySQL, PostgreSQL, and SQL Server databases, which will reduce administrative effort. Twenty-five TB can be accommodated efficiently on Cloud SQL.

**Cloud SQL** options are regional and have less scalability compared to **Cloud Spanner**.

-------------------------------------------------
You want to migrate the database to Google Cloud. You need a solution that will provide global scale and availability and require minimal maintenance. What should you do?

Migrate to **Cloud Spanner.**

Your **Cloud Spanner** database stores customer address information that is frequently accessed by the marketing team. When a customer enters the country and the state where they live, this information is stored in different tables connected by a foreign key. The current architecture has performance issues. You want to follow Google-recommended practices to improve performance. What should you do?

A. Create interleaved tables, and store states under the countries.

Feedback
A: Option A is correct because **Cloud Spanner** supports interleaving that guarantees data being stored in the same split, which is performant when you need a strong data locality relationship.

B: Option B is not correct because denormalizing is not a preferred approach in relational databases. It leads to multiple rows with repeated data.

C: Option C is not correct because reducing the size of the fields to short names will have lower impact because the data access and joins will be a bigger performance issue.

D: Option D is not correct because packing multiple types of data into the same cell is not recommended for relational databases.

-------------------------------------------------

**Bigtable** is the recommended database for time series data that requires high throughput reads and writes.

Example:
You are building the trading platform for a stock exchange with millions of traders. 
Trading data is written rapidly. You need to retrieve data quickly to show visualizations to the traders,
such as the changing price of a particular stock over time. 
You need to choose a storage solution in Google Cloud. What should you do?

Key Visualizer for **Bigtable** generates visual reports for your tables that detail your usage based on the row keys that you access, show you how Bigtable operates, and can help you troubleshoot performance issues.

Example:
> Your company collects data about customers to regularly check their health vitals. You have millions of customers around the world. Data is ingested at an average rate of two events per 10 seconds per user. You need to be able to visualize data in Bigtable on a per user basis. You need to construct the **Bigtable key** so that the operations are performant. What should you do?

 Construct the key as user-id#device-id#activity-id#timestamp.
 the design does not monotonically increase, thus avoiding hotspots.

-------------------------------------------------

  **BigQuery** doesn’t support global scale. BigQuery also isn’t the best option for migrating a transactional database like PostgreSQL because it is more analytics-focused.

  
You are working on optimizing **BigQuery** for a query that is run repeatedly on a single table. The data queried is about 1 GB, and some rows are expected to change about 10 times every hour. You have optimized the SQL statements as much as possible. You want to further optimize the query's performance. What should you do?

A. Create a **materialized view** based on the table, and query that view.
A: Option A is correct because materialized views periodically cache the results of a query for increased performance. Materialized views are suited to small datasets that are frequently queried. When underlying table data changes, the materialized view invalidates the affected portions and re-reads them.

-------------------------------------------------

 **Dataflow** to recreate the jobs in a serverless approach. Move the data to Cloud Storage.
 . Use hopping windows in Dataflow. for moving averages

Your scooter-sharing company collects information about their scooters, such as location, battery level, and speed. The company visualizes this data in real time. To guard against intermittent connectivity, each scooter sends repeats of certain messages within a short interval. Occasional data errors have been noticed. The messages are received in Pub/Sub and stored in BigQuery. You need to ensure that the data does not contain duplicates and that erroneous data with empty fields is rejected. What should you do?

 . Use **Dataflow** to subscribe to Pub/Sub, process the data, and store the data in BigQuery.

-------------------------------------------------

 graceful decommissioning will finish work in progress on a worker node before it is removed from the **Dataproc** cluster.


-------------------------------------------------

 Use a **Transfer Appliance** to move the existing data to Google Cloud. Set up a Dedicated or Partner Interconnect for daily transfers.


---------------------------------------------


https://www.googlecloudcommunity.com/gc/Community-Blogs/Your-guide-to-preparing-for-the-Google-Cloud-Professional-Data/ba-p/543105


|||
|--- |--- |
|Open source|Google Cloud managed service|
|Hadoop, Spark, Hive|Dataproc|
|Beam|Dataflow|
|Airflow|Cloud Composer|
|Kafka, RabbitMQ|Pub/Sub|
|Cassandra|Cloud Bigtable|


# Study the Google Cloud Resource Hierarchy 
Make sure you’re familiar with the Google Cloud Resource hierarchy, including how and when permissions are assigned. Google Cloud offers IAM, which lets you assign granular access to specific Google Cloud resources and prevents unwanted access to other resources. IAM lets you control who (users) has what access (roles) to which resources by setting IAM policies on the resources.

You can set an IAM policy at the organization level, the folder level, the project level, or (in some cases) the resource level. Resources inherit the policies of the parent resource. If you set a policy at the organization level, it is inherited by all its child folder and project resources, and if you set a policy at the project level, it is inherited by all its child resources.

The effective policy for a resource is the union of the policy set on the resource and the policy inherited from its ancestors. This inheritance is transitive. In other words, resources inherit policies from the project, which inherit policies from the organization resource. Therefore, the organization-level policies also apply at the resource level. Learn more here. 



![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/c4a3cb3c-aea4-4739-8f29-2529d71c208b)


![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/72bc5d5f-0e86-4ee5-bb4c-49386a11ce4d)


