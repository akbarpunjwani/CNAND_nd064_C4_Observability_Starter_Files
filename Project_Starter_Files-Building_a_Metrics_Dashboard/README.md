**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*DONE:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

## Setup the Jaeger and Prometheus source
*DONE:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

## Create a Basic Dashboard
*DONE:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

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

## Tracing our Flask App
*DONE:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.

## Jaeger in Dashboards
*DONE:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

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


