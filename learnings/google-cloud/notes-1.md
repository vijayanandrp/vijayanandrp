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


# Google Cloud database/storage decision tree

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/444d2d6a-7774-4fce-8f2a-ac8a683b43be)


# Google Cloud data transformation tools decision tree (Dataproc or Dataflow)

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/17c2bb28-44ff-4ff6-99ba-785212e3b237)
