

**Cloud SQL** provides managed MySQL, PostgreSQL, and SQL Server databases, which will reduce administrative effort. Twenty-five TB can be accommodated efficiently on Cloud SQL.

**Cloud SQL** options are regional and have less scalability compared to **Cloud Spanner**.

 > You want to migrate the database to Google Cloud. You need a solution that will provide global scale and availability and require minimal maintenance. What should you do?

Migrate to **Cloud Spanner.**

> Your **Cloud Spanner** database stores customer address information that is frequently accessed by the marketing team. When a customer enters the country and the state where they live, this information is stored in different tables connected by a foreign key. The current architecture has performance issues. You want to follow Google-recommended practices to improve performance. What should you do?

A. Create interleaved tables, and store states under the countries.

Feedback
A: Option A is correct because **Cloud Spanner** supports interleaving that guarantees data being stored in the same split, which is performant when you need a strong data locality relationship.

B: Option B is not correct because denormalizing is not a preferred approach in relational databases. It leads to multiple rows with repeated data.

C: Option C is not correct because reducing the size of the fields to short names will have lower impact because the data access and joins will be a bigger performance issue.

D: Option D is not correct because packing multiple types of data into the same cell is not recommended for relational databases.


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



  **BigQuery** doesn’t support global scale. BigQuery also isn’t the best option for migrating a transactional database like PostgreSQL because it is more analytics-focused.

 **Dataflow** to recreate the jobs in a serverless approach. Move the data to Cloud Storage.
 . Use hopping windows in Dataflow. for moving averages

Your scooter-sharing company collects information about their scooters, such as location, battery level, and speed. The company visualizes this data in real time. To guard against intermittent connectivity, each scooter sends repeats of certain messages within a short interval. Occasional data errors have been noticed. The messages are received in Pub/Sub and stored in BigQuery. You need to ensure that the data does not contain duplicates and that erroneous data with empty fields is rejected. What should you do?

 . Use **Dataflow** to subscribe to Pub/Sub, process the data, and store the data in BigQuery.


 graceful decommissioning will finish work in progress on a worker node before it is removed from the **Dataproc** cluster.


 Use a **Transfer Appliance** to move the existing data to Google Cloud. Set up a Dedicated or Partner Interconnect for daily transfers.
