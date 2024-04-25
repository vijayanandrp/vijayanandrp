
Update to the latest provider version where the primary and foreign keys are supported. In my case I have choosen `5.17.0`

```terraform
# Initialise the terraform environment
terraform {
  required_providers {
    google = {
      source  = "google"
      version = "~> 5.17.0"
    }
  }
```

Upgrade the providers in local version.

```bash
terraform init -upgrade    
```

Example Script how to add the concept of primary/foreign keys.

```terraform


resource "google_bigquery_table" "dimension_table_1" {
  deletion_protection = false
  provider    = google.impersonated
  dataset_id  = google_bigquery_dataset.raw_ds.dataset_id
  table_id    = "xxx_dim_table_1"
  description = "Dimension table 1"
  friendly_name  = "Dimension table 1"


  time_partitioning {
    type = "DAY"
  }


  # PRIMARY KEY ONLY
  table_constraints {
    primary_key { 
      columns = ["id"] 
    }
  }


  schema = <<EOF
  [
    {
      "name": "id",
      "type": "INTEGER",
      "mode": "REQUIRED",
      "description": "Identity column"
    },
    {
      "name": "name",
      "type": "STRING",
      "mode": "NULLABLE",
      "description": "Name"
    },
    {
      "name": "state",
      "type": "STRING",
      "mode": "NULLABLE",
      "description": "State where the head office is located"
    }
  ]
  EOF


  clustering  = [
    "state"
  ]


  labels = {
    env = "dev"
  }


}


resource "google_bigquery_table" "dimension_table_2" {
  deletion_protection = false
  provider    = google.impersonated
  dataset_id  = google_bigquery_dataset.raw_ds.dataset_id
  table_id    = "xxx_dim_table_2"
  description = "Dimension table 2"
  friendly_name  = "Dimension table 2"


  time_partitioning {
    type = "DAY"
  }


  # PRIMARY KEY ONLY
  table_constraints {
    primary_key { 
      columns = ["id"] 
    }
  }


  schema = <<EOF
  [
    {
      "name": "id",
      "type": "INTEGER",
      "mode": "REQUIRED",
      "description": "Identity column"
    },
    {
      "name": "name",
      "type": "STRING",
      "mode": "NULLABLE",
      "description": "Name"
    },
    {
      "name": "state",
      "type": "STRING",
      "mode": "NULLABLE",
      "description": "State where the head office is located"
    }
  ]
  EOF


  clustering  = [
    "state"
  ]


  labels = {
    env = "dev"
  }


}




resource "google_bigquery_table" "metric_table" {
  deletion_protection = false
  provider    = google.impersonated
  dataset_id  = google_bigquery_dataset.raw_ds.dataset_id
  table_id    = "xxx_metric_table"
  description = "Metric table"
  friendly_name  = "Metric table"


  time_partitioning {
    type = "DAY"
  }


  # PRIMARY KEY AND 2 FOREIGN KEYS
  table_constraints {


    primary_key { 
      columns = ["id"] 
    }
    
    foreign_keys { 


      name = "dim_fk_key_1"


      referenced_table {
        project_id  = google_bigquery_dataset.raw_ds.project
        dataset_id  = google_bigquery_dataset.raw_ds.dataset_id
        table_id    = "xxx_dim_table_1"
      }


      column_references {
        referencing_column = "dim_id_1"
        referenced_column = "id"
      }
   }


    foreign_keys { 


      name = "dim_fk_key_2"


      referenced_table {
        project_id  = google_bigquery_dataset.raw_ds.project
        dataset_id  = google_bigquery_dataset.raw_ds.dataset_id
        table_id    = "xxx_dim_table_2"
      }


      column_references {
        referencing_column = "dim_id_2"
        referenced_column = "id"
      }
    }
  
    
  }
  


  schema = <<EOF
  [
    {
      "name": "id",
      "type": "INTEGER",
      "mode": "REQUIRED",
      "description": "Identity column"
    },
    {
      "name": "dim_id_1",
      "type": "INTEGER",
      "mode": "REQUIRED",
      "description": "Dimension table 1 - Identity column"
    },
    {
      "name": "dim_id_2",
      "type": "INTEGER",
      "mode": "REQUIRED",
      "description": "Dimension table 2 - Identity column"
    },
    {
      "name": "value",
      "type": "STRING",
      "mode": "NULLABLE",
      "description": "value"
    },
    {
      "name": "time",
      "type": "TIMESTAMP",
      "mode": "NULLABLE",
      "description": "time"
    }
  ]
  EOF


  labels = {
    env = "dev"
  }


}


```

# References
1. [Github Post](https://github.com/GoogleCloudPlatform/cloud-solutions/blob/1957e6e9865006e6a53d4db9059e18cc5a6b4e25/projects/dataflow-bigquery-change-data-capture/terraform/bigquery.tf#L21)
2. [Terraform BigQuery Table constraints](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table#table_constraints)
