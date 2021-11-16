**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*DONE:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation
![Kubectl Monitoring](./answer-img/monitoringinstallation_kubectl.jpg?raw=true "Kubectl Monitoring")

## Setup the Jaeger and Prometheus source
*DONE:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.
![Grafana Homepage after Admin Login](./answer-img/grafanahomepage_adminlogin.jpg?raw=true "Grafana Homepage after Adminlogin")

## Create a Basic Dashboard
*DONE:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.
![Basic Dashboard Prometheus](./answer-img/BasicDashboard_Prometheus.jpg?raw=true "Basic Dashboard Prometheus")

## Describe SLO/SLI
*DONE:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.
SLI is an indicator of how much we were able to achieve the SLO defined. For monthly uptime SLO, we can have SLI in terms of the duration for which the service remain unavailable, which we could then reduce as much as possible. For request response time SLO, we could average out the request response time, which would then give us the current SLI.

## Creating SLI metrics.
*DONE:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 
Latency: To understand how much time it takes to process customer request
Traffic: To understand the trend of requests that inflows at all time
Errors: To know the count of requests that receives error 500 response
Saturation: To understand the utilization of CPUs, Memory & other resources. The more saturated the system is the more improved load balancing and more urgent arrangements of new resources are required. For how many duration the resources remained in 100% utilization
Utilization: To understand for how many duration the resources are utilized to serve requests

## Create a Dashboard to measure our SLIs
*DONE:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.
![Uptime Dashboard Last6hours](./answer-img/UptimeDashboard_Last6hours.jpg?raw=true "Uptime Dashboard")
![Uptime Dashboard Last24hours](./answer-img/UptimeDashboard_Last6hours.jpg?raw=true "UptimeDashboard Last24hours")

## Tracing our Flask App
*DONE:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.
![TracingFlask BackendAPIendpoint](./answer-img/TracingFlask_BackendAPIendpoint.jpg?raw=true "Tracing Flask BackendAPIendpoint")

## Jaeger in Dashboards
*DONE:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.
![Jaeger Explore In Grafana BackendAPI](./answer-img/JaegerExploreInGrafana_BackendAPI.jpg?raw=true "JaegerExploreInGrafana BackendAPI")

## Report Error
*OUTOFSCOPE:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue.

TROUBLE TICKET (https://knowledge.udacity.com/questions/741672)

Name:

Date:

Subject:

Affected Area:

Severity:

Description:


## Creating SLIs and SLOs
*DONE:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name three SLIs that you would use to measure the success of this SLO.
For each month, we have service minutes of 30 days x 24 hrs x 60 mins = 43,200 mins. To achieve 99.95% uptime means 43,179mins of uptime and 21mins of downtime. Below SLIs would be used to measure it:
1) Monitor the Start Timings of the Pod along with the number of replicas. If the container is down it should not exceed 21mins of error budget
2) Monitor the Traffic flow of the frontend and more specific to the Backend and Trial API serving the frontend. This is related in case there is downtime, as the downtime during no traffic or low traffic may give support in covering error budget.
3) Percentage of Success hits to Frontend, Backend & Trial (which is currently giving more 500) should always be above 99.95% during the monthly duration

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create KPIs to accurately measure these metrics. We will make a dashboard for this, but first write them down here.
1) "Percentage of Success Hits" to Backend should be 99.95% or above
2) "Latency of Backend API" should be under 100 milliseconds
3) CPU Utilization should be under 70%
4) Memory Utilization should be under 70%
5) Throughput of Read+Write of default namespace should be 1.5MB/s (subject to this disk in use)
6) Current Network Bandwidth of Receive / Trasmit should be 1Mb/s

## Final Dashboard
*DONE*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  
![FinalDashboard](./answer-img/FinalDashboardWithMetrics.jpg?raw=true "FinalDashboard")

### Description of HEAT MAPs used:
In our dashboard the Heat Maps are used to monitor the Traffic Inflow at each of the services using the below PromQL:
```sum(flask_http_request_duration_seconds_bucket{method="GET",container="backend"}) by (container)```

### Description of METRICS showing Request Status wise Counts:
The counts indicates the overall counts of the GET request for each category of response type i-e success, error 4x and error 5x. Below PromQL is used:
```sum(flask_http_request_total{method="GET",container=~"backend"}) by(container, status)```

### Description of Uptime Monitoring graph for each Container
This shows the heartbeat of our services for every minute as to when the services were down and for how long. Below PromQL is used:
```sum(up{container=~"backend"}) by (pod)```

### Description of Latency Metrics in millisecond for each microservice
This metrics shows the average response time in millisecond disregard of the response category whether it was success or error. Below PromQL is used:
``` sum(flask_http_request_duration_seconds_sum{method="GET",status="200",container="backend"}) by(container) / (sum(flask_http_request_duration_seconds_count{method="GET",status="200",container="backend"}) by (container)) * 1000 ```

### Description of Success Percentage
This metric indicates the overall ratio of success that our web user experienced out of all the request attempts made. Below PromQL is used:
``` ((sum(flask_http_request_duration_seconds_count{method="GET", status="200", container="backend"}) by(container))/(sum(flask_http_request_duration_seconds_count{method="GET", container="backend"}) by(container)))*100 ```

### Description of Timeseries graph of 4x Errors
This graph illustrates the occurances of the Errors with 401, 404 and 410 status. It shows time and points of total requests that got the error response. Below PromQL is used:
```sum(flask_http_request_total{container=~"backend",status=~"403|404|410"}) by (status,container)```

### Description of Timeseries graph of 5x Errors
This graph illustrates the occurances of the Errors with Internal Server Error status. It shows time and points of total requests that got the error response. Below PromQL is used:
```sum(flask_http_request_total{container=~"backend",status=~"500|503"}) by (status,container)```


For Saturation, the builtin out of the box dashboard shall be used, named as ```General / Kubernetes / Compute Resources / Cluster```
![Compute Resources](./answer-img/FinalDashboardWithMetrics_BuiltIn.jpg?raw=true "FinalDashboard_BuiltIn")

### Description of CPU Utilization and Memory Utilization
These metric indicates the overall computing and memory resources been consumed by the kubernetes cluster. As an example the 93.6% utilization is red alert showing that compute power is almost fully utilized and action is required. Similarly, utilization of 74.5% indicates we are still left with 25% of memory and hence the status is not that alarming.

### Description of CPU Usage & Memoru Usage graph
This graph indicates that which resources of which NAMESPACE is consuming how much of computing power. As an example we can observe that monitoring namespace which is running Prometheus and Grafana is consuming most of the computing power. Also, the timeline is shown to help us know the timeseries based status.

![Compute Resources](./answer-img/FinalDashboardWithMetrics_BuiltIn2.jpg?raw=true "FinalDashboard_BuiltIn")
### Description of Current Network Usage
This graph shows the bandwidth of network been consumed. In case this matches with the KPI we set than it is OK else red alert in order to avoid any saturation at network level which may cause SLI to be difficult to achieve

### Description of Disk Read+Write Throughput
This graphical representation along with Tabular dashboard panel indicates the current throughput and utilization of the storage. The figures should be within the Error Budget so that we do not loose out the KPI or the Service Level Indicator.




