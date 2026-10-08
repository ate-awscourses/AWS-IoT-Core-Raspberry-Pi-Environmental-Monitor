# AWS IoT Raspberry Pi Monitoring Platform

## Overview

This project is an end-to-end AWS IoT monitoring solution built using a Raspberry Pi 5, AWS IoT Core, DynamoDB, Lambda, CloudWatch, and SNS.

The Raspberry Pi collects system metrics including CPU, memory, and disk utilization and securely publishes telemetry data to AWS IoT Core using MQTT over TLS with X.509 certificate authentication.

AWS services process, store, visualize, and generate alerts based on incoming telemetry data.

---

## Architecture

```text
+-------------------+
| Raspberry Pi 5    |
|-------------------|
| CPU Usage         |
| Memory Usage      |
| Disk Usage        |
+---------+---------+
          |
          | MQTT + TLS
          |
          v
+-------------------+
| AWS IoT Core      |
+---------+---------+
          |
          |
    +-----+-----+
    |           |
    v           v

+---------+   +---------+
|DynamoDB |   | Lambda  |
+---------+   +----+----+
                  |
                  v

            +-----------+
            |CloudWatch |
            +-----+-----+
                  |
                  v

            +-----------+
            |SNS Alerts |
            +-----------+
