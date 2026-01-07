from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import boto3
from datetime import datetime, timedelta, timezone
import os


load_dotenv()
DEFAULT_IP = os.getenv("DEFAULT_IP", "")
app = Flask(__name__)
ec2 = boto3.client("ec2")
cloudwatch = boto3.client("cloudwatch")




#Cloudwatch cant get instance by IP, so we need to get instance ID first
def get_instance_id_by_ip(ip_address):
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance.get("PrivateIpAddress") == ip_address:
                return instance["InstanceId"]
    return None



#To get the metrics from CloudWatch
def get_cpu_metrics(instance_id, hours, period_seconds):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    
        
    metrics = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=period_seconds,
        Statistics=["Average"],
        Unit="Percent"
    )
    return metrics


@app.route("/")
def home():
    return send_file("index.html")

@app.route("/api/cpu")
def get_cpu():
    ip_address = request.args.get("ip", DEFAULT_IP)
    hours = int(request.args.get("hours", 3))
    interval = int(request.args.get("interval", 600))
    
    instance_id = get_instance_id_by_ip(ip_address)
    
    if not instance_id:
        return jsonify({"error": "Instance not found"}), 404
    
    metrics = get_cpu_metrics(instance_id, hours, interval) 
    #Sorting is by Timestamps
    datapoints = sorted(metrics["Datapoints"], key=lambda x: x["Timestamp"])
    timestamps = []
    cpu_values = []
    
    for point in datapoints:
        #Convert the timestamp to a readable format
        timestamps.append(point["Timestamp"].strftime("%H:%M"))
        cpu_values.append(round(point["Average"], 2))
    
    return jsonify({
        "instance_id": instance_id,
        "ip_address": ip_address,
        "timestamps": timestamps,
        "cpu_values": cpu_values
    })


if __name__ == "__main__":
    app.run(debug=True)